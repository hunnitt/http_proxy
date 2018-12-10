#!/usr/bin/python3

import socket
import threading
import httplib
import urlparse
import sys

client_sockets = []
lock = threading.Lock()

def usage():
    print("syntax : python3 http_proxy.py < port >")
    print("sample : python3 http_proxy.py 8080")
    sys.exit(0)

def is_http(msg):
    if "HTTP/1.1" in msg:
        return True
    else:
        return False

def server_side(proxy_socket):
    


def client_side(proxy_socket, client_socket, client_addr):
    while True:
        recv_msg = client_socket.recv(1024).decode()
        if not recv_msg:
            break
        else:
            if is_http(recv_msg):
                url_start = str(recv_msg).find("Host: ")
            else:
                continue

    with lock:
        print("[-] Client disconnected!")
        client_sockets.remove(client_socket)
        print("[-] ",len(client_sockets)," clients left.")
        client_socket.close()
            


def run_proxy_c(proxy_socket):
    print("[+] Waiting for clients...")

    while True:
        (client_socket, client_addr) = proxy_socket.accept()
        with lock:
            client_sockets.append(client_socket)
            
        client_service = threading.Thread(target=client_side, args=(proxy_socket, client_socket, client_addr))
        client_service.start()


def run_proxy_s(proxy_socket):
    print("[+] Waiting for responses...")

    while True:
        (server_socket, server_addr) = proxy_socket.accept()

        

def main():
    if len(sys.argv) != 2:
        usage()
    
    port = int(sys.argv[1])

    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[+] socket() Complete.")

    proxy_socket.bind(('127.0.0.1', port))
    print("[+] bind() Complete.")

    proxy_socket.listen(20)
    print("[+] listen() Complete")

    print("[+] Running Proxy for clients.")
    proxy = threading.Thread(target=run_proxy_c, args=(proxy_socket))
    proxy.daemon = True 
    proxy.start()

    print("[+] Running Proxy for servers.")
    proxy = threading.Thread(target=run_proxy_s, args=(proxy_socket))
    proxy.daemon = True 
    proxy.start()

if __name__ == '__main__':
	main()