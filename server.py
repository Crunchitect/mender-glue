import logging
import subprocess
from websocket_server import WebsocketServer

def new_client(client, server):
    print("New STL Slicer Called")

def message_received(client, server, message):
    stl = str(message)
    print("RECIEVED:", stl)
    with open("in.stl", "w") as f:
        f.write(stl)
    subprocess.call(['./cura/CuraEngine.exe',
                      'slice',
                      *['-j', './cura/definitions/def.json'],
                      *['-l', './in.stl'],
                      *['-o', './out.gcode'],
                      *['-s', 'roofing_layer_count=1']])
    output = ''
    with open("out.gcode", "r") as f:
        output = f.read()
    print("SEND: ", output)
    server.send_message(client, output)
    logging.info("STL sliced.")
    

server = WebsocketServer(host='127.0.0.1', port=1533, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.run_forever()
