from dial_client import parser
from dial_client import ssdp
from dial_client import device

"""Client module for managing device property and connection control"""


# TODO make integration here in the future

def CaptureDevices(timeout=5, binding_address=''):
  """This provides a basic usage of this library.
   It Starts the Discovery service and finds available devices.
   Returns a list of device module defined by device.py
  """
  discover_service = ssdp.Discover(binding_address)
  res = discover_service.GetDeviceResponse(timeout)
  parsed_data = parser.ParseResponse(res)
  sample_devices = []
  location_map = {}
  for data in parsed_data:
    try:
      sample_device = device.Device(data)
      if sample_device.location in location_map.keys():
        continue
      location_map[sample_device.location] = sample_device
      sample_devices.append(sample_device)
    except Exception as e:
      print("Encountered error while finding devices: {}".format(e))
  return sample_devices
