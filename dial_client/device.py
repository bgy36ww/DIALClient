import requests
from requests.exceptions import HTTPError
from dial_client import app
from dial_client import parser


class Device(requests.Session):
  """Device container for accessing device information.

  Attributes:
    M-Search response info:
      location: url for UPnP description
      st: Search Target
      usn: Device UUID (Required by UPnP protocol)
      wakeup: Mac address and Timeout(Can be empty)
    Device Description info(Device Manufacturer can have any of this empty):
      friendly_name: A easy to understand name for this device, should use manufacturer + model_name if not available.
      model_name: Model name
      model_number: Model number
      manufacturer: Manufacturer name
      model_description: Short description of the model
  """

  def __init__(self, response):
    super(Device, self).__init__()
    self.location = response['location']
    self.st = response['st']
    self.usn = response['usn']
    self.wakeup = response.get('wakeup', '')
    # HTTP Header names are case-insensitive
    # headers dictionary take care of that
    info = self.get(self.location)
    self.app_url = _AppUrlHandling(info.headers.get('application-url'))
    device_tree = parser.ParseDeviceTree(info.content)
    self.friendly_name = device_tree['friendlyName']
    self.model_name = device_tree['modelName']
    self.model_number = device_tree['modelNumber']
    self.manufacturer = device_tree['manufacturer']
    self.model_description = device_tree['modelDescription']
    self.headers['Content-Type'] = 'text/plain;charset=UTF-8'

  def GetApp(self, application_name='', dial_version=''):
    """Returns the Application information response on the device.

    Args:
      application_name: The application name in string you want to check, it's different for each app.
          The registry of DIAL Application Names can be found here:
          http://www.dial-multiscreen.org/dial-registry/namespace-database
          If this is empty, GetApp on some Devices can find the current or the latest running app on TV.
      dial_version: New in Protocol 2.1, can be use in the future to specify which DIAL version you want.

    Return:
      A App class with the app information on the Device. If not available, this will raise an HTTPError.

    """
    if dial_version:
      dial_version = '?clientDialVer=' + dial_version
    info = self.get(self.app_url + '/' + application_name + dial_version)
    info.raise_for_status()
    return app.App(info.content)

  def Launch(self, application_name, args=''):
    """Launches a installed device app

    Args:
      application_name: The application name you want to launch, in string.
      args: what args you want to put after the app id. Can pass customized url or args to app.

    Returns:
      The http response from the device.
    """
    self.Close(application_name)
    if len(args) == 0:
      self.headers['Content-Length'] = '0'
    return self.post(self.app_url + '/' + application_name, args)

  def Close(self, application_name=''):
    """Closes the app if it's currently running, it needs to support DIAL version 1.7.1 protocol 6.4.2
    it sends a delete request to Application Resource URL + "/run" address.

    Args:
      application_name: The application name you want to close

    Returns:
      The http response from the device.
    """
    try:
      application = self.GetApp(application_name)
    except HTTPError:
      print('No Active App')
      raise
    if not application_name:
      application_name = application.name
    if application.state == 'stopped':
      print('Application is not running. Nothing to do.')
      return None
    return self.delete(self.app_url + '/' + application_name + '/' + _HandleHref(application.link['href']));

# TODO add more cases in the future
def _AppUrlHandling(url):
  """Handles special case in the url"""
  url = url.rstrip('/')
  return url

def _HandleHref(url):
  """The reason this is here is because in spec 1.7.1, it puts the entire url in href. However, in spec 2.1,
  it's corrected and only shows the last portion. Since we are not sure which spec user is using,
  we use a universal way to parse them
  """
  return url.rstrip('/').split('/')[-1]
