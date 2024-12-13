import socket
import time
import threading

class FunctionBlock:
    def __init__(self, name, fb_type):
        self.name = name
        self.fb_type = fb_type
        self.inputs = {}
        self.outputs = {}

    def execute(self):
        # Базовая логика выполнения функционального блока
        pass

class EMB_RES(FunctionBlock):
    def __init__(self, name):
        super().__init__(name, "EMB_RES")
        self.outputs["CNF"] = False

    def execute(self):
        self.outputs["CNF"] = True
        print(f"EMB_RES {self.name} executed, CNF = {self.outputs['CNF']}")

class STRING2STRING(FunctionBlock):
    def __init__(self, name):
        super().__init__(name, "STRING2STRING")
        self.inputs["IN"] = ""
        self.outputs["OUT"] = ""
        self.outputs["CNF"] = False

    def execute(self):
        if self.inputs["IN"]:
            self.outputs["OUT"] = self.inputs["IN"]
            self.outputs["CNF"] = True
            print(f"STRING2STRING {self.name} executed, OUT = {self.outputs['OUT']}, CNF = {self.outputs['CNF']}")

class OUT_ANY_CONSOLE(FunctionBlock):
    def __init__(self, name):
        super().__init__(name, "OUT_ANY_CONSOLE")
        self.inputs["IN"] = ""
        self.inputs["REQ"] = False
        self.outputs["QI"] = False
        self.outputs["CNF"] = False

    def execute(self):
        if self.inputs["REQ"]:
            print(f"OUT_ANY_CONSOLE {self.name} executed, IN = {self.inputs['IN']}")
            self.outputs["QI"] = True
            self.outputs["CNF"] = True

def create_function_block(name, fb_type):
    if fb_type == "EMB_RES":
        return EMB_RES(name)
    elif fb_type == "STRING2STRING":
        return STRING2STRING(name)
    elif fb_type == "OUT_ANY_CONSOLE":
        return OUT_ANY_CONSOLE(name)
    else:
        return FunctionBlock(name, fb_type)

def load_program(program_data):
    fbs = {}
    connections = []
    for line in program_data.split('\n'):
        if line.startswith(';<Request'):
            request = line[1:]  # Удаление начального символа ';'
            action_start = request.find('Action="') + len('Action="')
            action_end = request.find('"', action_start)
            action = request[action_start:action_end]
            if action == "CREATE":
                if '<FB' in request:
                    fb_start = request.find('<FB Name="') + len('<FB Name="')
                    fb_end = request.find('"', fb_start)
                    name = request[fb_start:fb_end]
                    type_start = request.find('Type="') + len('Type="')
                    type_end = request.find('"', type_start)
                    fb_type = request[type_start:type_end]
                    fbs[name] = create_function_block(name, fb_type)
                elif '<Connection' in request:
                    src_start = request.find('Source="') + len('Source="')
                    src_end = request.find('"', src_start)
                    source = request[src_start:src_end]
                    dest_start = request.find('Destination="') + len('Destination="')
                    dest_end = request.find('"', dest_start)
                    destination = request[dest_start:dest_end]
                    connections.append((source, destination))
            elif action == "WRITE":
                src_start = request.find('Source="') + len('Source="')
                src_end = request.find('"', src_start)
                source = request[src_start:src_end]
                dest_start = request.find('Destination="') + len('Destination="')
                dest_end = request.find('"', dest_start)
                destination = request[dest_start:dest_end]
                connections.append((source, destination))
    return fbs, connections

def receive_program(host='localhost', port=61499):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Исполнительная среда ожидает соединения на {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Соединение установлено с {addr}")
                program_data = ""
                while True:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        break
                    program_data += data
                    conn.sendall(b"OK\n")
                return program_data

def run_program(fbs, connections):
    while True:
        for fb in fbs.values():
            fb.execute()
        for src, dest in connections:
            if '.' in src:
                src_fb, src_port = src.split('.')
                if src_fb in fbs and src_port in fbs[src_fb].outputs:
                    value = fbs[src_fb].outputs[src_port]
                    if '.' in dest:
                        dest_fb, dest_port = dest.split('.')
                        if dest_fb in fbs and dest_port in fbs[dest_fb].inputs:
                            fbs[dest_fb].inputs[dest_port] = value
        time.sleep(1)  # Такт выполнения

def main():
    global running
    running = True

    while running:
        try:
            program_data = receive_program()
            fbs, connections = load_program(program_data)
            program_thread = threading.Thread(target=run_program, args=(fbs, connections))
            program_thread.start()
        except Exception as e:
            print(f"Ошибка: {e}")
            running = False

if __name__ == "__main__":
    main()
