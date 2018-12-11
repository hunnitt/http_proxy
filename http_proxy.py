#!/usr/bin/python3

import socket
import threading
import httplib
import sys

def usage():
    print("syntax : python3 http_proxy.py < port >")
    print("sample : python3 http_proxy.py 8080")
    sys.exit(0)

def is_http(msg):
    if "HTTP/1.1" in msg:
        return True
    else:
        return False

def server_side(proxy_socket_c, proxy_socket_s, server_socket, server_addr):
    while True:
        try:
            recv_resp = server_socket.recv(1024).decode()
            if not recv_resp:
                break
            else:
                proxy_socket_c.send(recv_resp)
        
        except:
            break

    print("s - [-] Server disconnected")
    server_socket.close()

def client_side(proxy_socket_c, proxy_socket_s, client_socket, client_addr):
    while True:
        try:
            recv_msg = client_socket.recv(1024).decode()
            if not recv_msg:
                break
            else:
                if is_http(recv_msg):
                    url_start = str(recv_msg).find("Host: ") + 6
                    url_end = str(recv_msg).index("\r\n")
                    url = str(recv_msg)[url_start:url_end]
                    proxy_socket_s.connect((url, 80))
                    proxy_socket_s.send(recv_msg)
                else:
                    continue
        except:
            break

    print("c - [-] Client disconnected!")
    client_socket.close()
            


def run_proxy_c(proxy_socket_c, proxy_socket_s):
    print("c - [+] Waiting for clients...")

    while True:
        try:
            (client_socket, client_addr) = proxy_socket_c.accept()
            print("c - [+] New client from", client_addr)

            client_service = threading.Thread(target=client_side, args=(proxy_socket_c, proxy_socket_s, client_socket, client_addr))
            client_service.start()
        except:
            print("c - [-] error occured.")
            break

def run_proxy_s(proxy_socket_s, proxy_socket_c):
    print("s - [+] Waiting for responses...")

    while True:
        try:
            (server_socket, server_addr) = proxy_socket_s.accept()
            print("s - [+] New server from", server_addr)

            server_service = threading.Thread(target=server_side, args=(proxy_socket_c, proxy_socket_s, server_socket, server_addr))
            server_service.start()

        except:
            print("s - [-] error occured.")
            break

def main():
    if len(sys.argv) != 2:
        usage()
    
    port_c = int(sys.argv[1])
    port_s = 80

    proxy_socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[+] client-side socket() Complete.")
    proxy_socket_c.bind(('127.0.0.1', port_c))
    print("[+] client-side bind() Complete.")
    proxy_socket_c.listen(20)
    print("[+] client-side listen() Complete")

    print("")

    proxy_socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[+] server-side socket() Complete.")
    proxy_socket_s.bind(('0.0.0.0', port_s))
    print("[+] server-side bind() Complete.")
    proxy_socket_s.listen(20)
    print("[+] server-side listen() Complete")

    print("[+] Running Proxy...")
    proxy_c = threading.Thread(target=run_proxy_c, args=(proxy_socket_c, proxy_socket_s))
    proxy_c.start()
    proxy_s = threading.Thread(target=run_proxy_s, args=(proxy_socket_s, proxy_socket_c))
    proxy_s.start()

if __name__ == '__main__':
	main()