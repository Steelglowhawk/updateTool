import time
import xml.etree.ElementTree as Et
from zipfile import ZipFile
import random
import os
import shutil
from datetime import datetime


def name_for_ik():
    """
    :return: выдает имена формата ###-###-###-###-### в шестнадцатиричной системе для интеграционных конвертов
    """
    first_part = str(hex(random.randint(1000000000, 9999999999)))
    second_part = str(hex(random.randint(10000, 99999)))
    third_part = str(hex(random.randint(10000, 99999)))
    fourth_part = str(hex(random.randint(10000, 99999)))
    fifth_part = str(hex(random.randint(100000000000000, 999999999999999)))
    return f'{first_part[2:10]}-{second_part[2:6]}-{third_part[2:6]}-{fourth_part[2:6]}-{fifth_part[2:14]}'


def atribute_generator(char_value):  # 17 символов для имени файла ED, 9 символов для номера договора
    """
    :param char_value: количество знаков в срезе
    :return: случайное число, которое зависит от системной даты и времени
    """
    a = str(int(time.time()*10000000))
    return a[len(a)-char_value::]


def envelope_change_attrib(namespaceprefix, namespaceuri, xml_source_file_path, tags, paramreplace, path_to_save_xml):
    """
    Изменение аттрибутов в файле Envelope
    :param namespaceprefix: префикс пространства имен в файле envelope (igr)
    :param namespaceuri: ссылка пространства имен в envelope
    :param xml_source_file_path: путь к файлу envelope
    :param tags: теги, по которым идет поиск
    :param paramreplace: словарь из параметров тегов и их новых значений
    :param path_to_save_xml: путь и имя для готового файла
    :return: запись в файл в том же каталоге
    """
    Et.register_namespace(namespaceprefix, namespaceuri)  # для записи в файле необходимо передать prefix и uri
    tree = Et.parse(xml_source_file_path)  # открываем xml файл и парсим
    root = tree.getroot()
    for i in tags:
        for element in root.findall('.//*[@{' + namespaceuri + '}' + i + ']'):  #
            for key, value in paramreplace.items():
                if element.attrib['{' + namespaceuri + '}' + i] in key:
                    if len(str(element.text).strip()) > 0:  # как сделать проверку на None
                        if element.text is None:
                            element.attrib['{' + namespaceuri + '}fileIdentity'] = value
                        else:
                            element.text = value
                    else:
                        element.attrib['{' + namespaceuri + '}fileIdentity'] = value
    tree.write(path_to_save_xml)


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


def routeinfo_change_attrib(namespaceprefix, namespaceuri, xml_source_file_path, path_to_save_xml, new_text):
    """
    Редактирование RouteInfo
    :param namespaceprefix: префикс пространства имен в файле ED421 (igr)
    :param namespaceuri: ссылка пространства имен в файле ED421
    :param xml_source_file_path: путь к файлу
    :param path_to_save_xml: путь и имя для готового файла
    :param new_text: текст, который будет записан между тегами
    :return: запись в xml-файл
    """
    Et.register_namespace(namespaceprefix, namespaceuri)

    tree = Et.parse(xml_source_file_path)
    root = tree.getroot()
    root.find('{' + namespaceuri + '}DocumentPackID').text = new_text
    tree.write(path_to_save_xml)  # сохранение xml файла


def create_new_directory(path_to_new_directory, directory_name):
    """
    :param path_to_new_directory: путь, где будет создан каталог path
    :param directory_name: имя для нового каталога
    :return: создает каталог temp по указанному пути, если его не существует
    """
    if os.path.exists(path_to_new_directory + '/' + directory_name):
        pass
    else:
        os.mkdir(path_to_new_directory + '/' + directory_name)
    return path_to_new_directory + '/' + directory_name + '/'


def get_arhive(path, *files):
    """
    :param path: путь, где будет создать архив
    :param files: файлы, которые будут помещаться в архив
    :return:
    """
    with ZipFile(path, 'w') as new_zip:  # добавить после path функцию вызова нового имени
        for arg in files:
            filename = arg[str(arg).rfind('/') + 1:]
            new_zip.write(arg, arcname=str(filename))
            os.remove(arg)


def move_files(copy_from, copy_to):
    """
    :param copy_from: полный путь к файлу, который будет перемещен
    :param copy_to: каталог, в который будет перемещен файл
    :return: перемещает файл, переданный из copy_from в каталог copy_to
    """
    shutil.move(copy_from, copy_to)


# -----------------------------------------------------------
# создать функцию, которая делает всю процедуру. Поместить то, что ниже в неё
# start_path = 'C:/install/test' # путь для Windows
start_path = '/Users/steelhawk/PycharmProjects/generator' # путь для MacOS
envelope_path = start_path + '/sample/envelope.xml'
routeinfo_path = start_path + '/sample/RouteInfo.xml'
ed421_path = start_path + '/sample/ED421.xml'
iteration_count = 1000  # количество конвертов
# -----------------------------------------------------------
# создать каталоги temp, converts внутри каталога
temp_path = create_new_directory(start_path, 'temp')
convert_path = create_new_directory(start_path, 'converts')
# -----------------------------------------------------------
# переменные
prefix_for_routeinfo_envelope = 'igr'
prefix_ed421 = ''
uri_for_routeinfo_envelope = 'http://www.cbr.ru/igr/'
uri_for_ed421 = 'urn:cbr-ru:elk:v2021.1.0'
text_for_sign_file = 'test signature file'
tags_attrib = ['name', 'fileType']  # теги для функции generate_xml_envelope
# -----------------------------------------------------------
# сгенерировать имена для файлов
for i in range(1, iteration_count + 1):
    print(i)
    arhive_name = name_for_ik()  # имя для архива, в который будут упакованы все файлы
    ed421_name_for_arh = name_for_ik()  # имя для архива, в котором лежит ed421
    routeinfo_name = name_for_ik()  # имя для routeinfo
    sign_name = name_for_ik()  # имя для файла с ЭП
# -----------------------------------------------------------
    new_name_ED421 = temp_path + 'ED421' + atribute_generator(17) + '.xml'
    new_name_routeinfo = temp_path + routeinfo_name
    new_name_envelope = temp_path + 'envelope.xml'
# -----------------------------------------------------------
# создать файл с подписью
    with open(temp_path + sign_name, 'w') as sign_file:
        sign_file.write(text_for_sign_file)
# заполнение словаря значениями
    tags_dictionary = dict(RouteInfo=routeinfo_name,
                           Document=ed421_name_for_arh,
                           Sign=sign_name,
                           AssociatedFileIdentity=ed421_name_for_arh)
    attributes_and_values = dict(EDNo=atribute_generator(9),
                                 ReqNum=atribute_generator(17),
                                 ApplicationSum=atribute_generator(17))
# изменение значений в ED421 и сохранение в другом каталоге
    ed421_change_attrib(prefix_ed421,
                        uri_for_ed421,
                        ed421_path,
                        new_name_ED421,
                        **attributes_and_values)
# изменение значений в RouteInfo и сохранение в другом каталоге
    routeinfo_change_attrib(prefix_for_routeinfo_envelope,
                            uri_for_routeinfo_envelope,
                            routeinfo_path,
                            new_name_routeinfo,
                            arhive_name)
# изменение значений в RouteInfo и сохранение в другом каталоге
    envelope_change_attrib(prefix_for_routeinfo_envelope,
                           uri_for_routeinfo_envelope,
                           envelope_path,
                           tags_attrib,
                           tags_dictionary,
                           new_name_envelope)
# добавление ED421 в архив
    get_arhive(temp_path + ed421_name_for_arh,
               new_name_ED421)
# формирование целого конверта
    get_arhive(temp_path + arhive_name + '.zip',
               temp_path + ed421_name_for_arh,
               new_name_routeinfo,
               new_name_envelope,
               temp_path + sign_name)
# переместить конверт
    move_files(temp_path + arhive_name + '.zip', convert_path)
# после того как все операции выполнены удалить каталог temp
os.rmdir(temp_path)
# 3 сек - 1 000 конвертов
# 0:05:15.761248 - 100 000 конвертов
