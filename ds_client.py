# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Cole Thompson / Nathan Yang
# cwthomps@uci.edu / npyang@uci.edu
# 36762668 / 63942782
import socket
import ds_protocol
import json, time

def send(server:str, port:int, username:str, password:str, message:str=None, recipient:str=None, choices:int=None, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    try:
      # Connect to the server
      c.settimeout(3)
      c.connect((server, port))
      print(f"client connected to {server} on {port}")
    except:
      print("Was not able to connect to server/port.")
      return False

    try:
      # Get the token and join the server
      token = join(c, username, password)
      if not token:
        return False
    except:
      print()
      return False

    if choices == 1:
      check = _message(c, message, token, recipient)
      if check == False:
        return False
      else:
        return True  
    elif choices == 2:
      return request(c, "new", token)
    elif choices == 3:
      return request(c, "all", token)
      
    return True

def join(client:socket, username:str, password:str) -> bool:
  """This is used to either join as an existing user or create a new user."""
  join_msg = {"join": {"username": username,"password": password, "token":"ok"}}
  resp = _connect(join_msg, client)
  msg = json.loads(resp)
  x = ds_protocol._response(resp)

  if not x:
    return False
  return msg["response"]["token"]


def _message(client:socket, message:str, token:str, recipient:str) -> str:
  """This function posts a message to the server given a token and message."""
  stamp = time.time() # Create a timestamp
  post_msg = {"token": token, "directmessage": {"entry": message, "recipient": recipient, "timestamp": stamp}}
  resp = _connect(post_msg, client)
  check = ds_protocol._response(resp)
  return check


def request(client:socket, message:str, token:str) -> str:
  """
  This function sends a message to the server given a token and a specific message. 
  The message paramater can either be "all" or "new".
  """
  post_msg = {"token": token, "directmessage": message}
  resp = _connect(post_msg, client)
  obj = ds_protocol._response(resp)
  return obj

def _connect(msg:str, client:socket) -> str:
  """This function sends a message to the server and returns the json response."""
  m = json.dumps(msg)
  send = client.makefile('w')
  recv = client.makefile('r')

  send.write(m + '\r\n')
  send.flush()

  resp = recv.readline()
  return resp
