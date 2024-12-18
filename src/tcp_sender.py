import socket
import struct

class TcpSender:
    def __init__(self, file_path):
        """
        Initialize the TCP sender with a file path and send the file content to the server.
        """
        self.file_path = file_path
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.set_connection()
            self.send_fboot()
            self.disconnect()
        except:
            print('Error during connection with forte')

    def set_connection(self):
        """
        Set up the connection to the server.
        """
        server_address = ('localhost', 61499)
        self.client_socket.connect(server_address)

    def disconnect(self):
        """
        Disconnect from the server.
        """
        self.client_socket.close()

    def send_fboot(self):
        """
        Send the content of the fboot file to the server.
        """
        print("File path:", self.file_path)
        file = open(self.file_path, 'r')

        while True:
            message = file.readline()[:-1]
            if not message:
                break

            separator = message.find(';')
            res_name = message[:separator]
            xml_com = message[separator + 1:]
            res_name_length = struct.pack('h', separator)[::-1]
            xml_com_length = struct.pack('h', len(xml_com))[::-1]
            message = '\x50' + res_name_length.decode() + res_name + '\x50' + xml_com_length.decode() + xml_com

            self.client_socket.sendall(message.encode())

            try:
                self.client_socket.settimeout(10.0)
                response = self.client_socket.recv(1024)
                print(f'Received: {response.decode()}\n')

            except socket.timeout:
                print("Timeout: waiting for data...")
                continue
