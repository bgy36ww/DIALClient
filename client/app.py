from client import parser


class App(object):
  """ App object containing the app descriptions

  Attributes:
    name: the name of the App
    options: allowStop's value, indicate if DIAL version 1.7.1 protocol 6.4.2 is supported or not. {allowStop: true/false}
    link: contains rel and href in dictionary format{string:string}
    state: current state of the app, is it running or not.
    additional_data: contains additional data as a dictionary of {string:string}
  """
  def __init__(self, info):
    parsed_info = parser.ParseAppTree(info)
    self.name = parsed_info['name']
    self.options = parsed_info['options']
    self.state = parsed_info['state']
    self.link = parsed_info['link']
    self.additional_data = parsed_info['additional_data']
