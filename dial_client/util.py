from dial_client import parser
from dial_client import ssdp
from dial_client import device

"""Client module for managing device property and connection control"""


# TODO make integration here in the future

def CaptureDevices(time=5):
  """This provides a basic usage of this library.
   It Starts the Discovery service and finds available devices.
   Returns a list of device module defined by device.py
  """
  discover_service = ssdp.Discover()
  res = discover_service.GetDeviceResponse(time)
  parsed_data = parser.ParseResponse(res)
  sample_devices = []
  location_map = {}
  for data in parsed_data:
    sample_device = device.Device(data)
    if sample_device.location in location_map.keys():
      continue
    location_map[sample_device.location] = sample_device
    sample_devices.append(sample_device)
  return sample_devices
