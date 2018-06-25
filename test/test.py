from dial_client import util
import time
clients = util.CaptureDevices()
for client in clients:
    client.Launch('YouTube')
    time.sleep(10)
    client.Close('YouTube')
    client.Launch('Netflix')
    time.sleep(10)
    client.Close('Netflix')