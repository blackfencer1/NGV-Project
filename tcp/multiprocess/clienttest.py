import socket

if __name__ == "__main__":

	# create TCP Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# server IP, port
    s.connect(("localhost", 5000))
    recvdata = s.recv(1024)
    print (recvdata)
    s.close()
