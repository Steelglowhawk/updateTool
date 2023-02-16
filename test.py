import xml.etree.ElementTree as Et
import pathlib


def ed421_change_attrib(namespaceprefix, namespaceuri, xml_source_file_path, path_to_save_xml, **kwargs):
    """
    Изменение аттрибутов в файле ED421
    :param namespaceprefix: префикс пространства имен в файле ED421 (пусто)
    :param namespaceuri: ссылка пространства имен в файле ED421
    :param xml_source_file_path: путь к файлу ED421
    :param path_to_save_xml: путь и имя для готового файла
    :param kwargs: аттрибуты тега и их новые значения
    :return:
    """
    Et.register_namespace(namespaceprefix, namespaceuri)
    tree = Et.parse(xml_source_file_path)
    root = tree.getroot()
    for key, value in kwargs.items():
        if root.findall(f'.[@{key}]'):  # поиск атрибута в корневом элементе
            root.attrib[key] = value
        elif root.findall(f'.//*[@{key}]'):  # поиск атрибута в дочерних элементах
            root.find(f'.//*[@{key}]').set(key, value)
    tree.write(path_to_save_xml)  # сохранение xml файла


# переменные
start_path = pathlib.Path.cwd().parent  # путь для MacOS
envelope_path = start_path.joinpath('sample/envelope.xml')
routeinfo_path = start_path.joinpath('sample/RouteInfo.xml')
ed421_path = start_path.joinpath('sample/ED421.xml')
prefix_ed421 = ''
uri_for_ed421 = 'urn:cbr-ru:elk:v2021.1.0'
new_name_ED421 = start_path.joinpath('ED421_001.xml')
# new_name_ED421 = start_path + 'ED421' + atribute_generator(17) + '.xml'

# словарь для аргумента функции
attributes_and_values = dict(EDNo='testNo',
                             EDDate='13-01-2023',
                             ReqNum='testReq',
                             ApplicationSum='testSum')


# изменение значений в ED421 и сохранение в другом каталоге
ed421_change_attrib(prefix_ed421,
                    uri_for_ed421,
                    ed421_path,
                    new_name_ED421,
                    **attributes_and_values)
