import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QVBoxLayout
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
import socket

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class ForteIDE(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('4DIAC IDE Prototype')
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()

        self.load_button = QPushButton('Загрузить проект', self)
        self.load_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.load_button.clicked.connect(self.load_project)
        layout.addWidget(self.load_button)

        self.generate_button = QPushButton('Сгенерировать программу', self)
        self.generate_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.generate_button.clicked.connect(self.generate_program)
        layout.addWidget(self.generate_button)

        self.run_button = QPushButton('Запустить в FORTE', self)
        self.run_button.setStyleSheet("background-color: #FF9800; color: white;")
        self.run_button.clicked.connect(self.run_in_forte)
        layout.addWidget(self.run_button)

        self.graph_button = QPushButton('Показать граф', self)
        self.graph_button.setStyleSheet("background-color: #9C27B0; color: white;")
        self.graph_button.clicked.connect(self.show_graph)
        layout.addWidget(self.graph_button)

        self.setLayout(layout)

        self.show()

    def load_project(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Project', '', 'SYS files (*.sys)')
        if file_path:
            try:
                self.tree = ET.parse(file_path)
                self.root_element = self.tree.getroot()
                logging.info('Проект загружен успешно!')
                QMessageBox.information(self, 'Успех', 'Проект загружен успешно!')
            except ET.ParseError as e:
                logging.error(f'Не удалось разобрать XML файл: {e}')
                QMessageBox.critical(self, 'Ошибка', 'Не удалось разобрать XML файл.')

    def generate_program(self):
        # Генерация простейшей последовательности функциональных блоков
        root = ET.Element("System", Name="GeneratedSystem", Comment="")
        version_info = ET.SubElement(root, "VersionInfo", Version="1.0", Author="Generated", Date="2024-10-26")
        application = ET.SubElement(root, "Application", Name="GeneratedApp", Comment="")
        sub_app_network = ET.SubElement(application, "SubAppNetwork")

        fb1 = ET.SubElement(sub_app_network, "FB", Name="FB1", Type="STRING2STRING", Comment="", x="1500", y="400")
        ET.SubElement(fb1, "Parameter", Name="IN", Value="'hello'", Comment="")

        fb2 = ET.SubElement(sub_app_network, "FB", Name="FB2", Type="OUT_ANY_CONSOLE", Comment="", x="3360", y="310")
        ET.SubElement(fb2, "Parameter", Name="QI", Value="true", Comment="")

        event_connections = ET.SubElement(sub_app_network, "EventConnections")
        ET.SubElement(event_connections, "Connection", Source="FB1.CNF", Destination="FB2.REQ", Comment="", dx1="530")
        ET.SubElement(event_connections, "Connection", Source="FB2.CNF", Destination="FB1.REQ", Comment="", dx1="60",
                      dx2="60", dy="45")

        data_connections = ET.SubElement(sub_app_network, "DataConnections")
        ET.SubElement(data_connections, "Connection", Source="FB1.OUT", Destination="FB2.IN", Comment="", dx1="530")

        device = ET.SubElement(root, "Device", Name="FORTE_PC", Type="FORTE_PC", Comment="", x="1950", y="720")
        ET.SubElement(device, "Parameter", Name="MGR_ID", Value="&quot;localhost:61499&quot;",
                      Comment="Device manager socket ID")
        ET.SubElement(device, "Attribute", Name="Profile", Type="STRING", Value="HOLOBLOC")
        ET.SubElement(device, "Attribute", Name="Color", Type="STRING", Value="255,190,111")
        resource = ET.SubElement(device, "Resource", Name="EMB_RES", Type="EMB_RES", Comment="", x="0", y="0")
        fb_network = ET.SubElement(resource, "FBNetwork")

        fb1_device = ET.SubElement(fb_network, "FB", Name="GeneratedApp.FB1", Type="STRING2STRING", Comment="",
                                   x="1500", y="400")
        ET.SubElement(fb1_device, "Parameter", Name="IN", Value="'hello'", Comment="")

        fb2_device = ET.SubElement(fb_network, "FB", Name="GeneratedApp.FB2", Type="OUT_ANY_CONSOLE", Comment="",
                                   x="3360", y="310")
        ET.SubElement(fb2_device, "Parameter", Name="QI", Value="true", Comment="")

        event_connections_device = ET.SubElement(fb_network, "EventConnections")
        ET.SubElement(event_connections_device, "Connection", Source="GeneratedApp.FB1.CNF",
                      Destination="GeneratedApp.FB2.REQ", Comment="", dx1="530")
        ET.SubElement(event_connections_device, "Connection", Source="GeneratedApp.FB2.CNF",
                      Destination="GeneratedApp.FB1.REQ", Comment="", dx1="60", dx2="60", dy="45")
        ET.SubElement(event_connections_device, "Connection", Source="START.COLD", Destination="GeneratedApp.FB1.REQ",
                      Comment="", dx1="390")
        ET.SubElement(event_connections_device, "Connection", Source="START.WARM", Destination="GeneratedApp.FB1.REQ",
                      Comment="", dx1="390")

        data_connections_device = ET.SubElement(fb_network, "DataConnections")
        ET.SubElement(data_connections_device, "Connection", Source="GeneratedApp.FB1.OUT",
                      Destination="GeneratedApp.FB2.IN", Comment="", dx1="530")

        segment = ET.SubElement(root, "Segment", Name="Ethernet", Type="Ethernet", Comment="", x="2095", y="1700",
                                dx1="1500")
        ET.SubElement(segment, "Attribute", Name="Color", Type="STRING", Value="70,153,214")

        mapping1 = ET.SubElement(root, "Mapping", From="GeneratedApp.FB1", To="FORTE_PC.EMB_RES")
        mapping2 = ET.SubElement(root, "Mapping", From="GeneratedApp.FB2", To="FORTE_PC.EMB_RES")

        link = ET.SubElement(root, "Link", SegmentName="Ethernet", CommResource="FORTE_PC", Comment="")

        tree = ET.ElementTree(root)
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Program', '', 'SYS files (*.sys)')
        if file_path:
            tree.write(file_path)
            logging.info('Программа сгенерирована успешно!')
            QMessageBox.information(self, 'Успех', 'Программа сгенерирована успешно!')

    def run_in_forte(self):
        if hasattr(self, 'root_element'):
            # Отправка команды на сервер FORTE
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(("localhost", 61499))
                    s.sendall(b"LOAD_PROJECT")  # Пример команды для загрузки проекта
                    response = s.recv(1024)
                    if response == b"OK":
                        logging.info('Проект запущен успешно в FORTE!')
                        QMessageBox.information(self, 'Успех', 'Проект запущен успешно в FORTE!')
                    else:
                        logging.error(f'Не удалось запустить проект в FORTE: {response}')
                        QMessageBox.critical(self, 'Ошибка', 'Не удалось запустить проект в FORTE.')
            except socket.error as e:
                logging.error(f'Не удалось подключиться к FORTE: {e}')
                QMessageBox.critical(self, 'Ошибка', f'Не удалось подключиться к FORTE: {e}')
        else:
            logging.error('Проект не загружен.')
            QMessageBox.critical(self, 'Ошибка', 'Проект не загружен.')

    def show_graph(self):
        if hasattr(self, 'root_element'):
            G = nx.DiGraph()
            for fb in self.root_element.findall(".//FB"):
                fb_name = fb.get("Name")
                G.add_node(fb_name)

            for conn in self.root_element.findall(".//EventConnections/Connection"):
                source = conn.get("Source").split('.')[0]
                destination = conn.get("Destination").split('.')[0]
                G.add_edge(source, destination)

            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold')
            plt.title('Граф функциональных блоков')
            plt.show()
        else:
            logging.error('Проект не загружен.')
            QMessageBox.critical(self, 'Ошибка', 'Проект не загружен.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ForteIDE()
    sys.exit(app.exec_())
