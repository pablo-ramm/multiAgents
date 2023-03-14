# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python server to interact with Unity
# Sergio. Julio 2021

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json


import numpy as np

# Size of the board:
width = 30
height = 30
num_boids = 20

# Set the number of agents here:





def update_positions():
    f = open('in.txt', 'r')
    data = f.readline()
    print("json info: ")
    
    data = data.replace("\'", "\"")
    print(data)
    print(type(json.loads(data)))
    return json.loads(data)

""" [Vector(26.91, 24.82, 0.00), Vector(18.07, 10.18, 0.00), Vector(22.06, 22.61, 0.00), Vector(5.24, 8.27, 0.00), Vector(20.05, 12.29, 0.00), Vector(16.00, 10.57, 0.00), Vector(22.16, 21.43, 0.00), Vector(22.56, 23.67, 0.00), Vector(20.74, 15.04, 0.00), Vector(16.09, 25.46, 0.00), Vector(18.70, 12.44, 0.00), Vector(10.55, 12.78, 0.00), Vector(23.33, 6.92, 0.00), Vector(16.61, 26.39, 0.00), Vector(16.87, 24.05, 0.00), Vector(12.93, 20.16, 0.00), Vector(13.45, 26.35, 0.00), Vector(5.03, 13.77, 0.00), Vector(7.63, 30.00, 0.00), Vector(8.57, 9.93, 0.00)]
127.0.0.1 - - [13/Mar/2023 13:40:39]
 """


def positions_to_json(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x": p["x"],
            "y": p["y"],
            "id": p["id"]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)

#[{"x": 24.963197629269995, "z": 20.340207755463897, "y": 0.0}, {"x": 7.516105267114175, "z": 7.982949724518204, "y": 0.0}, {"x": 4.138083767593665, "z": 17.111744761616038, "y": 0.0}, {"x": 18.657826767783533, "z": 11.548527718125104, "y": 0.0}, {"x": 20.27837472734353, "z": 24.763777697754765, "y": 0.0}, {"x": 16.954181624333927, "z": 20.956988781566626, "y": 0.0}, {"x": 8.913423774505887, "z": 23.90824437317171, "y": 0.0}, {"x": 2.9591965016314847, "z": 20.579019417949304, "y": 0.0}, {"x": 29.465814937996367, "z": 13.53149166922771, "y": 0.0}, {"x": 18.085131902996284, "z": 19.10318411265041, "y": 0.0}, {"x": 20.943305604241417, "z": 18.1199627243289, "y": 0.0}, {"x": 6.607844972710783, "z": 10.655109141126749, "y": 0.0}, {"x": 17.005479557865275, "z": 14.223102760402174, "y": 0.0}, {"x": 2.4956597118122046, "z": 1.764441722656209, "y": 0.0}, {"x": 1.752094485132849, "z": 1.6683146600788472, "y": 0.0}, {"x": 10.434192845594485, "z": 10.208928027942802, "y": 0.0}, {"x": 20.302211630017897, "z": 21.413806535525822, "y": 0.0}, {"x": 26.47951425540373, "z": 13.558576705793843, "y": 0.0}, {"x": 23.217567655341036, "z": 16.52308542236839, "y": 0.0}, {"x": 19.02742266671335, "z": 9.196407763497696, "y": 0.0}]


class Server(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        
        # post_data = self.rfile.read(content_length)
        post_data = json.loads(self.rfile.read(content_length))
        
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        # str(self.path), str(self.headers), post_data.decode('utf-8'))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), json.dumps(post_data))

        '''
        x = post_data['x'] * 2
        y = post_data['y'] * 2
        z = post_data['z'] * 2
        
        position = {
            "x" : x,
            "y" : y,
            "z" : z
        }

        self._set_response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        self.wfile.write(str(position).encode('utf-8'))
        '''

        positions = update_positions()

        print("positions: ")
        print(positions)
        print(type(positions))
        # print(positions)
        self._set_response()
        resp = "{\"data\":" + json.dumps(positions) + "}"
        # print(resp)
        self.wfile.write(resp.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")  # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:  # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
