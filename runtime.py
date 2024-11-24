import xml.etree.ElementTree as ET
import socket
import time

class FunctionBlock:
    def __init__(self, name, inc, count):
        self.name = name
        self.inc = inc
        self.count = count

    def execute(self):
        if self.inc:
            self.count += 1
        return self.count

def load_program(xml_data):
    root = ET.fromstring(xml_data)
    fb_name = root.find(".//FunctionBlock").get("name")
    inc = bool(root.find(".//Data[@name='INC']").text)
    count = int(root.find(".//Var[@name='count']").get("initial"))
    return FunctionBlock(fb_name, inc, count)

def receive_program(host='localhost', port=61499):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Исполнительная среда ожидает соединения на {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Соединение установлено с {addr}")
            data = conn.recv(4096)
            return data

def main():
    program_data = receive_program()
    fb = load_program(program_data)

    while True:
        fb.inc = True
        current_count = fb.execute()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Время: {current_time}, Счет: {current_count}")
        fb.inc = False
        time.sleep(1)  # Такт выполнения

if __name__ == "__main__":
    main()
