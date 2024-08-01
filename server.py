import logging
import subprocess
from websocket_server import WebsocketServer

def new_client(client, server):
    logging.info("New STL Slicer Called")

def message_received(client, server, message):
    stl = str(message)
    with open("in.stl", "w") as f:
        f.write(stl)
    subprocess.Popen(['./cura/CuraEngine.exe',
                      'slice',
                      *['-j', './definintions/def.json'],
                      *['-l', '../in.stl'],
                      *['-o', '../out.gcode'],
                      *['-s', 'roofing_layer_count=1']])
    output = ''
    with open("out.gcode", "r") as f:
        output = f.read()
    server.send_message(client, output)
    logging.info("STL sliced.")
    

server = WebsocketServer(host='127.0.0.1', port=1533, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.run_forever()
