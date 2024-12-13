import xml.etree.ElementTree as ET
import subprocess
import os

def create_sys_file(filename):
    # Создание корневого элемента
    system = ET.Element("System", Name="demo1", Comment="")

    # Добавление VersionInfo
    version_info = ET.SubElement(system, "VersionInfo", Version="1.0", Author="test", Date="2024-12-13")

    # Добавление Application
    application = ET.SubElement(system, "Application", Name="demo1App", Comment="")
    sub_app_network = ET.SubElement(application, "SubAppNetwork")

    # Добавление FB STRING2STRING
    fb_string2string = ET.SubElement(sub_app_network, "FB", Name="STRING2STRING", Type="STRING2STRING", Comment="", x="1500", y="400")
    ET.SubElement(fb_string2string, "Parameter", Name="IN", Value="'hello'", Comment="")

    # Добавление FB OUT_ANY_CONSOLE
    fb_out_any_console = ET.SubElement(sub_app_network, "FB", Name="OUT_ANY_CONSOLE", Type="OUT_ANY_CONSOLE", Comment="", x="3360", y="310")
    ET.SubElement(fb_out_any_console, "Parameter", Name="QI", Value="true", Comment="")

    # Добавление EventConnections
    event_connections = ET.SubElement(sub_app_network, "EventConnections")
    ET.SubElement(event_connections, "Connection", Source="STRING2STRING.CNF", Destination="OUT_ANY_CONSOLE.REQ", Comment="", dx1="530")
    ET.SubElement(event_connections, "Connection", Source="OUT_ANY_CONSOLE.CNF", Destination="STRING2STRING.REQ", Comment="", dx1="60", dx2="60", dy="45")

    # Добавление DataConnections
    data_connections = ET.SubElement(sub_app_network, "DataConnections")
    ET.SubElement(data_connections, "Connection", Source="STRING2STRING.OUT", Destination="OUT_ANY_CONSOLE.IN", Comment="", dx1="530")

    # Добавление Device
    device = ET.SubElement(system, "Device", Name="FORTE_PC", Type="FORTE_PC", Comment="", x="1950", y="720")
    ET.SubElement(device, "Parameter", Name="MGR_ID", Value='"localhost:61499"', Comment="Device manager socket ID")
    ET.SubElement(device, "Attribute", Name="Profile", Type="STRING", Value="HOLOBLOC")
    ET.SubElement(device, "Attribute", Name="Color", Type="STRING", Value="255,190,111")

    # Добавление Resource
    resource = ET.SubElement(device, "Resource", Name="EMB_RES", Type="EMB_RES", Comment="", x="0", y="0")
    fb_network = ET.SubElement(resource, "FBNetwork")

    # Добавление FB в Resource
    fb_string2string_res = ET.SubElement(fb_network, "FB", Name="demo1App.STRING2STRING", Type="STRING2STRING", Comment="", x="1500", y="400")
    ET.SubElement(fb_string2string_res, "Parameter", Name="IN", Value="'hello'", Comment="")

    fb_out_any_console_res = ET.SubElement(fb_network, "FB", Name="demo1App.OUT_ANY_CONSOLE", Type="OUT_ANY_CONSOLE", Comment="", x="3360", y="310")
    ET.SubElement(fb_out_any_console_res, "Parameter", Name="QI", Value="true", Comment="")

    # Добавление EventConnections в Resource
    event_connections_res = ET.SubElement(fb_network, "EventConnections")
    ET.SubElement(event_connections_res, "Connection", Source="demo1App.STRING2STRING.CNF", Destination="demo1App.OUT_ANY_CONSOLE.REQ", Comment="", dx1="530")
    ET.SubElement(event_connections_res, "Connection", Source="demo1App.OUT_ANY_CONSOLE.CNF", Destination="demo1App.STRING2STRING.REQ", Comment="", dx1="60", dx2="60", dy="45")
    ET.SubElement(event_connections_res, "Connection", Source="START.COLD", Destination="demo1App.STRING2STRING.REQ", Comment="", dx1="390")
    ET.SubElement(event_connections_res, "Connection", Source="START.WARM", Destination="demo1App.STRING2STRING.REQ", Comment="", dx1="390")

    # Добавление DataConnections в Resource
    data_connections_res = ET.SubElement(fb_network, "DataConnections")
    ET.SubElement(data_connections_res, "Connection", Source="demo1App.STRING2STRING.OUT", Destination="demo1App.OUT_ANY_CONSOLE.IN", Comment="", dx1="530")

    # Добавление Segment
    segment = ET.SubElement(system, "Segment", Name="Ethernet", Type="Ethernet", Comment="", x="2095", y="1700", dx1="1500")
    ET.SubElement(segment, "Attribute", Name="Color", Type="STRING", Value="70,153,214")

    # Добавление Mapping
    ET.SubElement(system, "Mapping", From="demo1App.STRING2STRING", To="FORTE_PC.EMB_RES")
    ET.SubElement(system, "Mapping", From="demo1App.OUT_ANY_CONSOLE", To="FORTE_PC.EMB_RES")

    # Добавление Link
    link = ET.SubElement(system, "Link", SegmentName="Ethernet", CommResource="FORTE_PC", Comment="")

    # Сохранение XML в файл
    tree = ET.ElementTree(system)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

def create_fboot_file(sys_filename, fboot_filename):
    # Парсинг .sys файла
    tree = ET.parse(sys_filename)
    root = tree.getroot()

    fboot_content = []

    # Создание ресурса
    fboot_content.append(";<Request ID=\"2\" Action=\"CREATE\"><FB Name=\"EMB_RES\" Type=\"EMB_RES\" /></Request> EMB_RES;")

    # Создание функциональных блоков
    for fb in root.findall(".//FB"):
        fb_name = fb.get("Name")
        fb_type = fb.get("Type")
        fboot_content.append(f"<Request ID=\"{len(fboot_content)+1}\" Action=\"CREATE\"><FB Name=\"{fb_name}\" Type=\"{fb_type}\" /></Request> EMB_RES;")

    # Создание соединений
    connection_id = len(fboot_content) + 1
    for connection in root.findall(".//Connection"):
        source = connection.get("Source")
        destination = connection.get("Destination")
        fboot_content.append(f"<Request ID=\"{connection_id}\" Action=\"CREATE\"><Connection Source=\"{source}\" Destination=\"{destination}\" /></Request> EMB_RES;")
        connection_id += 1

    # Запуск приложения
    fboot_content.append("<Request ID=\"START\" Action=\"START\"/>")

    # Запись в .fboot файл
    with open(fboot_filename, 'w') as file:
        file.write("\n".join(fboot_content))

def run_forte_with_fboot(fboot_filename):
    # Полный путь к исполняемому файлу forte
    forte_path = r"C:\Users\kirar\Desktop\forte.exe"

    # Запуск программы forte с использованием командной строки
    command = [forte_path, "-f", fboot_filename]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")

def main():
    sys_filename = "demo1.sys"
    fboot_filename = "demo1.fboot"

    create_sys_file(sys_filename)
    print(f"SYS file created: {sys_filename}")

    create_fboot_file(sys_filename, fboot_filename)
    print(f"FBOOT file created: {fboot_filename}")

    run_forte_with_fboot(fboot_filename)

if __name__ == "__main__":
    main()
