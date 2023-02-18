
# Cole Thompson / Nathan Yang
# cwthomps@uci.edu / npyang@uci.edu
# 36762668 / 63942782
import ds_client, socket, ds_protocol, time


server = "168.235.86.101"
port = 3021
username = "hellocookiedough"
password = 'thisisapassword'

def message(client:socket, token:str):
  """This function posts a message to the server given a token and message."""
  stamp = time.time() # Create a timestamp
  post_msg = {"token": token, "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": stamp}}

  resp = ds_client._connect(post_msg, client)
  x = ds_protocol._response(resp)
  return x

def request(client, message, token):
  post_msg = {"token": token, "directmessage": message}
  resp = ds_client._connect(post_msg, client)
  x = ds_protocol._response(resp)
  return x

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    try:
        # Connect to the server
        c.settimeout(3)
        c.connect((server, port))
        print(f"client connected to {server} on {port}")
    except:
        print("Was not able to connect to server/port.")
    
    token = ds_client.join(c, username, password)
    resp = message(c, token)
    assert resp == "Direct message sent"
    resp = request(c, "new", token)
    assert type(resp) == list
    resp = request(c, "all", token)
    assert type(resp) == list

