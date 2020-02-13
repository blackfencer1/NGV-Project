from socket import *
import socket
import cv2
import numpy as np
import time
import sys
import os


class Telecommunication(self):
    def __init__(self):
        # Input server IP
        self.host = "192.168.255.21"
        self.port = 5003
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.host, self.port))

    def sendframe(self):
        while True:
            try:
                f = open("./data/*.jpg", 'rb')
                frame_data = f.read()
                if frame_data:
                    self.server_socket.sendall(frame_data)
                    answer = self.server_socket.recv(4096)
                    print('amswer = %s' % answer)

                    if answer == 'GOT IMAGE':
                        print('Send image successfully!')

            except:
                print('No Image')
                break
