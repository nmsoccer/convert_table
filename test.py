import xml.etree.ElementTree as ET


def print_type_node(node):
    print "====TYPE" , node.tag , "===="
    print node.attrib
    if node.attrib.has_key('name'):
	print "name is: " , node.attrib['name']
    if node.attrib.has_key('type'):
	print "type is: " , node.attrib['type']
	if node.attrib['type'] == "int":
	    print "4 B"
    if node.text:
	print "text" , node.text
	
	
	
	
def print_macro_node(node):
    print "----MACRO----"
    print node.attrib
    if node.attrib.has_key('name'):
	print "name is: " , node.attrib['name']



tree = ET.parse('test.xml')
root = tree.getroot()

print "root tag" , root.tag

macros = root.find("macros")
for macro_node in macros:
    print_macro_node(macro_node)

types = root.find("type")
for type_node in types:
    print_type_node(type_node)



print "nice"