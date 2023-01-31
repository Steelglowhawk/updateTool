import time
import xml.parsers.expat as xmle
import xml.etree.ElementTree as ET

ET.register_namespace('', 'urn:cbr-ru:elk:v2021.1.0')

# Создание и сохранение xml
# p = ET.Element('parent')
# c = ET.SubElement(p, 'child1')

# ET.dump(p) # вывод в консоль
# tree = ET.ElementTree(p)
# tree.write('../files/test.xml')
# сохранение xml файла


def attribute_generator(slice):
    """
    Создание значения для элемента атрибута
    :param slice: количество знаков в срезе
    :return: случайное число, которое зависит от системной даты и времени
    """
    a = str(int(time.time()*10000000))
    return a[-slice:-1]


def ed421_change_attrib(xml_source_file_path, path_to_save_xml, **kwargs):
    """
    Изменение атрибутов в ED421
    :param xml_source_file_path: путь к xml-файлу
    :param path_to_save_xml: путь и имя для готового файла
    :param kwargs: аттрибуты тега и их новые значения
    :return:
    """
    ET.register_namespace('', 'urn:cbr-ru:elk:v2021.1.0')

    tree = ET.parse(xml_source_file_path)
    root = tree.getroot()

    for key, value in kwargs.items():
        if root.findall(f'.[@{key}]'):  # поиск атрибута в рутовом элементе
            root.attrib[key] = value
        elif root.findall(f'.//*[@{key}]'):  # поиск атрибута в дочерних элементах
            root.find(f'.//*[@{key}]').set(key, value)
    tree.write(path_to_save_xml)  # сохранение xml файла


def route_info(xml_source_file_path, path_to_save_xml):
    """
    Редактирование RouteInfo
    :param xml_source_file_path: путь к xml-файлу
    :param path_to_save_xml: путь и имя для готового файла
    :return:
    """
    namespace = 'http://www.cbr.ru/igr/'
    ET.register_namespace('igr', namespace)

    tree = ET.parse(xml_source_file_path)
    root = tree.getroot()
    root.find('{' + namespace + '}DocumentPackID').text = 'testText'
    tree.write(path_to_save_xml)  # сохранение xml файла

    # print(xml)
    
# Блок с вызовом функций
# path = '../files/xml/ED421452554500003102022115928091.xml' #  путь для Mac
path = './files/xml/ED421452554500003102022115928091.xml'  # путь для Windows
attributes_and_values = {'EDNo': 'test1', 'ReqNum': 'test2'}
# path = './files/xml/envelope.xml' #  путь для Windows
# change_attrib_element(path, 'ReqNum', atribute_generator(19), '../files/xml/test_2.xml')
# change_attrib_element(path, 'EDNo', atribute_generator(9), '../files/xml/test_3.xml')
path_routeInfo = './files/xml/5bbf2a8b-fa43-4234-b222-66810ea28e5f/5a9eab65-00df-424f-89f0-e4424407d2c2'  # путь для Windows
# проверка функции
# change_attrib_element(path, 'ReqNum', attribute_generator(9), '../files/xml/test_2.xml')
ed421_change_attrib(path, './files/xml/test_2.xml', **attributes_and_values)
route_info(path_routeInfo, './files/xml/routeInfo_2.xml')
