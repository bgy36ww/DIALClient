"""XMl parser used for parsing device response and transform them to objects"""
from lxml import etree


def ParseResponse(responses):
  """extract M-Search info from HTTP responses"""
  maps = []
  for response in responses:
    lines = response.split('\r\n')
    fields = {}
    for line in lines:
      line = CleanText(line)
      try:
          key, value = line.split(': ', 1)
      except ValueError:
          continue
      # not a pair
      if not key or not value:
        continue
      if key in fields:
        continue
      # DIAL spec indicate this is case insensitive.
      fields[key.lower()] = value
    CheckPresence(fields)
    maps.append(fields)
  return maps

def CheckPresence(fields):
  """This function checks for the integrity of the search response

  Args:
    fields: fields of the response

  Returns: None

  Raises: ValueError
  """
  if "location" not in fields:
    raise ValueError("location not found in the targeted device's M-Search response")
  if "st" not in fields:
    raise ValueError("Search Target not found in the targeted device's M-Search response")

def CleanText(text):
  text = text.replace('\r','')
  text = text.replace('\n','')
  return text

"""Extract information according to UPnP spec:
http://upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.0.pdf
http://upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.1.pdf
"""
def ParseDeviceTree(content):
  """extract Device info from the xml"""
  root_tree = etree.fromstring(content)
  nsmap = root_tree.nsmap
  # nsmap will put default namespace into None key, we want to take it out.
  nsmap['default'] = nsmap[None]
  device_tree = root_tree.find('default:device', nsmap)
  dic = {'friendlyName': ParseTreeNode(device_tree, nsmap, 'friendlyName'),
         'modelName': ParseTreeNode(device_tree, nsmap, 'modelName'),
         'modelNumber': ParseTreeNode(device_tree, nsmap, 'modelNumber'),
         'manufacturer': ParseTreeNode(device_tree, nsmap, 'manufacturer'),
         'modelDescription': ParseTreeNode(device_tree, nsmap, 'modelDescription')}
  return dic

def ParseTreeNode(node, nsmap, name):
  """helper function to find children text of the Node"""
  ele = node.find('default:' + name, nsmap)
  if ele is None:
    return 'Unknown'
  else:
    return ele.text

def ParseForAttrib(node, nsmap, name):
  """helper function to find attrib of the Node"""
  ele = node.find('default:' + name, nsmap)
  if ele is None:
    return {}
  else:
    return ele.attrib

def GetKey(node, nsmap, ns='default'):
  return node.tag.replace('{' + nsmap[ns] + '}', '')

def ParseAppTree(content):
  """extract App info from the xml"""
  root_tree = etree.fromstring(content)
  nsmap = root_tree.nsmap
  nsmap['default'] = nsmap[None]
  dic = {'name': ParseTreeNode(root_tree, nsmap, 'name'),
         'options': ParseForAttrib(root_tree, nsmap, 'options'),
         'state': ParseTreeNode(root_tree, nsmap, 'state'), }
  link_dic = ParseForAttrib(root_tree, nsmap, 'link')
  # if href data is not available on device
  if 'href' not in link_dic:
      link_dic['href'] = 'run'
  additional_data = root_tree.find('default:additionalData', nsmap)
  additional_data_dic = {}
  if additional_data is not None:
    for data in additional_data.getchildren():
      key = GetKey(data, nsmap)
      additional_data_dic[key] = data.text
  dic['link'] = link_dic
  dic['additional_data'] = additional_data_dic
  return dic
