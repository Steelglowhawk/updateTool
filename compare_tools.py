import time
import xml.parsers.expat as xmle
import xml.etree.ElementTree as ET


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


def change_attrib_element(xml_source_file_path, element, new_value, path_to_save_xml):
    """
    Изменение элемента атрибута тега
    :param xml_source_file_path: путь к xml-файлу
    :param element: строка с именем элемента атрибута тега
    :param new_value: строка с новым значением элемента атрибута
    :param path_to_save_xml: путь и имя для готового файла
    :return:
    """
    tree = ET.parse(xml_source_file_path)
    root = tree.getroot()
    # поиск элемента (в root или в потомке)
    if root.get(element) is not None:
        print('The element is found in root with value is', root.get(element))
        root.attrib[element] = new_value
        print(f'New value for element {element} is {new_value}')
        tree.write(path_to_save_xml)  # сохранение xml файла
    else:  # если не найдено в root искать в дочерних элементах (работает только для потомков первого порядка)
        print(f'Element {element} is not found in root')
        for child in root:
            if child.get(element) is not None:
                print(f'The element {element} is found in {child} with value is', child.get(element))

                # print(child.tag, child.attrib)
                # print(f'attrib = {attrib}')

                child.attrib[element] = new_value
                print(f'New value for element {element} is {new_value}')

                # print(attrib.keys())
                # print(attrib.values())
                # print(child.get(element))
                # print(child.tag,)
                # print(child.find('{urn:cbr-ru:elk:v2021.1.0}CreditOpTerms').attrib)
                # root.find('{urn:cbr-ru:elk:v2021.1.0}CreditOpTerms').attrib = {'Keys':'Value'}
                tree.write(path_to_save_xml)  # сохранение xml файла


# Блок с вызовом функций
path = '../files/xml/ED421452554500003102022115928091.xml'

# change_attrib_element(path, 'ReqNum', atribute_generator(19), '../files/xml/test_2.xml')
# change_attrib_element(path, 'EDNo', atribute_generator(9), '../files/xml/test_3.xml')

# проверка функции
change_attrib_element(path, 'ReqNum', attribute_generator(9), '../files/xml/test_2.xml')


# TODO: в тегах какие-то посторонние символы. Проверить парсер в импорте
# TODO: пропадает при сохранении тег <?xml ...>
# TODO: генерируемое значение для элементов атрибутов тегов может иметь в начале 0. Надо выяснить принимается ли такой
