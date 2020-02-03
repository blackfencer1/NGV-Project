''''''''''''''''''''''
코드 내용
# 라즈베리파이에서 ubuntu로 pi-camera 스트리밍
# ubuntu에서 라즈베리파이로 html파일 데이터 전송
[수정 - 2020.02.02.] - ununtu에서 html파일 scraping 코드 추가(확인 안함)
''''''''''''''''''''''
import socket
import cv2
import numpy as np
import requests
 
#socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
 
HOST = '192.168.0.116'
PORT = 5001
 
#TCP 사용
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')
 
#서버의 아이피와 포트번호 지정
s.bind((HOST,PORT))
print('Socket bind complete')
# 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
s.listen(10)
print('Socket now listening')
 
#연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
conn,addr=s.accept()
 
while True:
    # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype = 'uint8')
    
    #data를 디코딩한다.
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    print(np.shape(frame))
    cv2.imshow('ImageWindow',frame)
    cv2.waitKey(1)
    
    #yolo_mark bounding box 좌표값 전송(확인 안함)
    resp = requests.get('http://home/heejunhghong/BlackfencerWeb/index.html')
    conn.send(resp.txt)
    
