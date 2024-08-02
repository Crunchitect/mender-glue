import logging
import subprocess
import requests
import json
from websocket_server import WebsocketServer

slug = requests.get("https://api.github.com/repos/ultimaker/cura/contents/resources/definitions")
printers = json.dumps([printer['name'].replace('.def.json', '') for printer in slug.json()])

def new_client(client, server):
    print("New STL Slicer Called")

def message_received(client, server, message):
    opcode, content = str(message).split('%', 1)
    printer_name = 'anet3d_et4'
    print("RECIEVED:", content)
    match opcode:
        case 'stl':
            with open("in.stl", "w") as f:
                f.write(content)
            subprocess.call(['./cura/CuraEngine.exe',
                            'slice',
                            *['-j', f'./cura/definitions/{printer_name}.def.json'],
                            *['-l', './in.stl'],
                            *['-o', './out.gcode'],
                            *['-s', 'roofing_layer_count=1']])
            output = ''
            with open("out.gcode", "r") as f:
                output = f.read()
            print("SEND: ", output)
            server.send_message(client, output)
            logging.info("STL sliced.")
        case 'printer':
            printer_name = content
            server.send_message(client, 'ok')
        case 'printerlist':
            server.send_message(client, printers)
    

server = WebsocketServer(host='127.0.0.1', port=1533, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.run_forever()
