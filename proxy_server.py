#!/usr/bin/env python3
import socket

HOST = ""
PORT = 8081
BUFFER_SIZE = 1024

addr_info = socket.getaddrinfo("www.google.com", 80, proto=socket.SOL_TCP)
(family, socktype, proto, canonname, sockaddr) = addr_info[0]

def main():
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST,PORT))
		s.listen(1)
		
		while True:
			conn, addr = s.accept()
			with conn:
				print("Connected by:", addr)
				with socket.socket(family, socktype) as proxy_end:
					#Connect to google
					proxy_end.connect(sockaddr)

					# Send incoming conn data to google
					send_full_data = b""
					while True:
						data = conn.recv(BUFFER_SIZE)
						if not data:
							break
						send_full_data += data
					proxy_end.sendall(send_full_data)

				full_data = b""
				while True:
					data = proxy_end.recv(BUFFER_SIZE)
					if not data:
						break
					full_data += data
				#print(full_data)
				conn.sendall(full_data)


if __name__ == "__main__":
	main()
