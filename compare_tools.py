import xml.parsers.expat as xmle
import xml.etree.ElementTree as ET


path = '/Users/steelhawk/PycharmProjects/UpdateTool/files/xml/ED421452554500003102022115928091.xml'

# Создание и сохранение xml
p = ET.Element('parent')
c = ET.SubElement(p, 'child1')
ET.dump(p)
tree = ET.ElementTree(p)
tree.write('../files/test.xml')  # сохранение xml файла

# Открытие и разбор файла
tree1 = ET.parse(path)
root = tree1.getroot()

for child in root:
    print(child.tag, child.attrib)
    print(child.tag,)

print(tree1.findall('CreditConsDate'))
print(root.findall('CreditConsDate'))


# print(root)
