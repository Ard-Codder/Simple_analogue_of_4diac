import xml.etree.ElementTree as ET
import socket
import time
import threading
import random

class FunctionBlock:
    def __init__(self, name, inc=False, count=None, message=""):
        self.name = name
        self.inc = inc
        self.count = count
        self.message = message

    def execute(self):
        if self.inc and self.count is not None:
            self.count += 1
        return self.count, self.message

def load_program(xml_data):
    root = ET.fromstring(xml_data)
    fb_name = root.find(".//FunctionBlock").get("name")
    inc = bool(root.find(".//Data[@name='INC']").text) if root.find(".//Data[@name='INC']") is not None else False
    count = int(root.find(".//Var[@name='count']").get("initial")) if root.find(".//Var[@name='count']") is not None else None
    message = root.find(".//Var[@name='message']").get("initial") if root.find(".//Var[@name='message']") is not None else ""
    return FunctionBlock(fb_name, inc, count, message)

def receive_program(host='localhost', port=61499):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Исполнительная среда ожидает соединения на {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Соединение установлено с {addr}")
                data = conn.recv(4096)
                if data:
                    return data

def run_program(fb, program_number, color):
    while True:
        fb.inc = True
        current_count, message = fb.execute()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output = f"Время: {current_time}"
        if fb.message:
            output += f", Сообщение: {message}"
        if fb.count is not None:
            output += f", Счет: {current_count}"
        print(f"\033[{color}mПрограмма: {fb.name}, Номер: {program_number}\033[0m, {output}")
        fb.inc = False
        time.sleep(1)  # Такт выполнения

def main():
    global running
    running = True
    program_number = 1
    program_colors = {}

    while running:
        try:
            program_data = receive_program()
            fb = load_program(program_data)
            if fb.name not in program_colors:
                program_colors[fb.name] = random.randint(91, 97)  # Генерация случайного цвета
            color = program_colors[fb.name]
            program_thread = threading.Thread(target=run_program, args=(fb, program_number, color))
            program_thread.start()
            program_number += 1
        except Exception as e:
            print(f"Ошибка: {e}")
            running = False

if __name__ == "__main__":
    main()
