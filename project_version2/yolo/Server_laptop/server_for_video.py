'''
2020.02.12.
raspberry pi to Yolo server: RECEIVE FRAMES to MAKE A VIDEO
'''
from socket import *
import socket
import cv2
import numpy as np
import time
import sys
import os

# sys.path.append(os.path.join(os.getcwd(), 'python/'))
# sys.path.append(os.getcwd().replace('darknet', ''))
# sys.path.append(os.getcwd().replace('darknet', 'camData/'))
# sys.path.append(os.getcwd().replace('darknet', 'img1/'))


# Streaming_return buffer
def recvall(sock, count):
    print("ok")
    buf = b''
    while count:
        newbuf = sock.recv(count)
        print("newbuf: ", newbuf)
        print("count: ", count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def fileName():
    # 이미지 파일 저장경로
    src = "../temp/"

    dte = time.localtime()
    Year = dte.tm_year
    Mon = dte.tm_mon
    Day = dte.tm_mday
    WDay = dte.tm_wday
    Hour = dte.tm_hour
    Min = dte.tm_min
    Sec = dte.tm_sec
    imgFileName = src + str(Year) + '-' + str(Mon) + '-' + str(Day) + '_' + str(Hour) + ':' + str(Min) + ':' + str(Sec)
    return imgFileName


class Telecommunication(self):
    def __init__(self):
        # server socket
        self.host = "192.168.255.21"
        self.port = 5003
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        # waiting client
        server_socket.listen(5)
        print('Server Socket is listening')
        # establish connection with client (conn: client socket, addr: binded address)
        self.conn, self.addr = server_socket.accept()
        print('Connected to :', addr[0], ':', addr[1])

    def streaming(self):
        # IMG & VIDEO FILE NAME COUNT
        frame_cnt = 0
        img_filename_cnt = 1
        file_receive_cnt = 0

        for _ in range(1):
            data = None
            # RECEIVE CAM FRAMES
            while True:
                print("############## receive cam frames ###############")
                # delete the used frames
                rev_path = './camData/'
                rev_frame_list = os.listdir(rev_path)
                if ".USED" in rev_frame_list:
                    rev_frame_list.remove(".USED")

                # if len(rev_flist) >= 2:
                #     for fname in rev_flist:
                #         os.system('rm ' + 'temp/' + fname)
                #         # subprocess.call('rm ' + 'temp/'+fname, shell=True)
                #     file_recive_cnt = 0

                frame_data = self.conn.recv(1000000)
                data = frame_data

                if frame_data:
                    while frame_data:
                        print("receiving frames...")
                        frame_data = conn.recv(1000000)
                        data += frame_data
                        print(len(data))
                        time.sleep(1)
                    else:
                        break

            # STORE CAM FRAMES
            # cv2.imwrite('/img{}/cam{}.jpg'.format(img_filename_cnt, frame_cnt), data)
            img_fileName = fileName()
            print(img_fileName)

            if file_receive_cnt == 0:
                img_fileName = img_fileName + ".mp4"
            elif file_receive_cnt == 1:
                img_fileName = img_fileName + '.txt'

            img_file = open("./camData/" + img_fileName, "wb")
            print("Open file")
            img_file.write(data)
            img_file.close()
            print("Store frames successfully!")

            data = None
            file_receive_cnt += 1

            '''
            # FRAME TO VIDEO
            # get img file
            img_path = src + '/img' + img_filename_cnt
            '''

    # Send_open/read file
    def sendcoordinates(self):
        while True:
            # read yolo_mark bounding box
            f = open("/home/heejunghong/BlackfencerWeb/index.html", 'r')
            data = f.read()
            self.conn.send(str(data))
            f.close()

    def shutdown(self):

        self.conn.close()