import xml.etree.ElementTree as ET
import socket

def load_program(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return ET.tostring(root, encoding='utf-8')

def send_program_to_runtime(program, host='localhost', port=61499):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(program)
        s.close()

def main():
    file_path = input("Введите путь к файлу программы: ")
    program = load_program(file_path)
    send_program_to_runtime(program)
    print("Программа отправлена в исполнительную среду.")

if __name__ == "__main__":
    main()
