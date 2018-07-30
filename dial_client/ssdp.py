"""SSDP module for search and discovery"""

import socket
import time
import select

SSDP_PORT = 1900
SSDP_ADDR = '239.255.255.250'
SSDP_ST = 'ST: urn:dial-multiscreen-org:service:dial:1'
SSDP_MX = '10'
# socket timeout as 0 second
SO_TIMEOUT = 0.0


class Discover(object):
  """Simple Search and Discovery class"""
  def __init__(self):
    msearch = 'M-SEARCH * HTTP/1.1'
    host = 'HOST: ' + SSDP_ADDR + ':' + str(SSDP_PORT)
    man = 'MAN: "ssdp:discover"'
    mx = 'MX: ' + SSDP_MX
    st = SSDP_ST
    rn = '\r\n'

    self._request_string = msearch + rn + host + rn + man + \
                           rn + mx + rn + st + rn + rn
    # using ipv4 address and datagram-based protocol
    self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self._socket.settimeout(SO_TIMEOUT)

  def GetDeviceResponse(self, timeout=5):
    """Discovery function, which starts the discovery process.
    timeout after timeout is met

    Args:
      timeout: timeout in seconds

    Returns:
      list of Response from all devices responded during the time timeout time frame.
    """
    responses = []
    overtime = time.time() + timeout
    # sends requests here from a random port
    self._socket.sendto(self._request_string.encode(), (SSDP_ADDR, SSDP_PORT))
    while time.time() < overtime:
      # 0 second timeout for non-blocking reading
      read, _, _ = select.select([self._socket], [], [], 0)
      # data is ready to read
      if read:
        response = self._socket.recv(4096)
        responses.append(response.decode())
    return responses
