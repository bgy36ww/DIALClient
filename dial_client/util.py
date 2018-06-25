from dial_client import parser
from dial_client import ssdp
from dial_client import device

"""Client module for managing device property and connection control"""


# TODO make integration here in the future

def CaptureDevices():
  """This provides a basic usage of this library.
   It Starts the Discovery service and finds available devices.
   Returns a list of device module defined by device.py
  """
  discover_service = ssdp.Discover()
  res = discover_service.GetDeviceResponse()
  parsed_data = parser.ParseResponse(res)
  sample_devices = []
  for data in parsed_data:
    sample_device = device.Device(data)
    sample_devices.append(sample_device)
  return sample_devices
