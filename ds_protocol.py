# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Cole Thompson / Nathan Yang
# cwthomps@uci.edu / npyang@uci.edu
# 36762668 / 63942782

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type','message'])


def extract_json(json_msg:str) -> DataTuple:
  '''
  Calls the json.loads function on a json string and converts it to a DataTuple object.
  '''
  try:
    json_obj = json.loads(json_msg)
    try:
      type = json_obj['response']['type']
      message = json_obj['response']['message']
    except:
      type = json_obj['response']['type']
      message = json_obj['response']['messages']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(type, message)


def _response(resp:str) -> bool:
  """
  This function calls the extract_json function and returns False or the retrieved message.
  """
  response_tuple = extract_json(resp)

  if response_tuple.type == "error":
    print(response_tuple.message)
    return False
  elif type(response_tuple.message) == list:
    return response_tuple.message
  else:
    return response_tuple.message
