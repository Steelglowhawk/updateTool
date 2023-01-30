import time
import xml.parsers.expat as xmle
import xml.etree.ElementTree as ET


ET.register_namespace('', "urn:cbr-ru:elk:v2021.1.0")

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
    Изменение элемента атрибута тега
    :param xml_source_file_path: путь к xml-файлу
    :param path_to_save_xml: путь и имя для готового файла
    :param kwargs: аттрибуты тега и их новые значения
    :return:
    """
    tree = ET.parse(xml_source_file_path)
    root = tree.getroot()
    print(root)
    # поиск элемента (в root или в потомке)
    for key, value in kwargs.items():
        print(key, value)

        if root.find("./[@attrib='key']") is not None:
            print('The element is found in root with value is', root.get(key))
            root.attrib[key] = value
        elif :
            print(f'Element {key} is not found in root')
            

        """
            root.attrib[i] = j
            print(f'New value for element {i} is {j}')
            tree.write(path_to_save_xml)  # сохранение xml файла
        """

        """
        else:  # если не найдено в root искать в дочерних элементах (работает только для потомков первого порядка)
            print(f'Element {keys} is not found in root')
            for child in root:
                if child.get(attrib) is not None:
                    print(f'The element {attrib} is found in {child} with value is', child.get(attrib))

                    # print(child.tag, child.attrib)
                    # print(f'attrib = {attrib}')

                    child.attrib[attrib] = new_value
                    print(f'New value for element {attrib} is {new_value}')

                    # print(attrib.keys())
                    # print(attrib.values())
                    # print(child.get(element))
                    # print(child.tag,)
                    # print(child.find('{urn:cbr-ru:elk:v2021.1.0}CreditOpTerms').attrib)
                    # root.find('{urn:cbr-ru:elk:v2021.1.0}CreditOpTerms').attrib = {'Keys':'Value'}
                    """
        tree.write(path_to_save_xml)  # сохранение xml файла



# Блок с вызовом функций
path = '../files/xml/ED421452554500003102022115928091.xml'
attributes_and_values = {'EDNo': 'test', 'ReqNum': 'test'}
# change_attrib_element(path, 'ReqNum', atribute_generator(19), '../files/xml/test_2.xml')
# change_attrib_element(path, 'EDNo', atribute_generator(9), '../files/xml/test_3.xml')

# проверка функции
# change_attrib_element(path, 'ReqNum', attribute_generator(9), '../files/xml/test_2.xml')
ed421_change_attrib(path, '../files/xml/test_2.xml', **attributes_and_values)

