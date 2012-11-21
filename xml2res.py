#coding = "gbk"
import xml.etree.ElementTree as ET

def load_xml(xml_file):
    tree = ET.parse(xml_file)
    if tree:
        print "load " , xml_file , "success"
    else:
        print "load " , xml_file , "failed"
    return tree


def macro_dict_append(macro_dict , macros):
    print "I am here!"
    for macro in macros:
        if macro.attrib.has_key('name'):
            print "macro name is: " , macro.attrib['name']
            macro_dict[macro.attrib['name']] = macro.attrib['id']
        else:
            print "!!!ERROR macro has attrib name!"





def build_macro_dict(root , macro_dict):
    '''------parse macro into macro dict
    MACRO_DICT------'''
 #  GET TAG MACROS
    macros_set = root.findall('macros')
    print macros_set
    if macros_set:
        print "get TAG MACROS success"
    else:
        print "get TAG MACROS failed"
        return

 #  GET EACH MACRO TAG IN MACROS
    for macros in macros_set:
 #       print "??" , macros.tag
        macro_dict_append(macro_dict , macros)


def main():
    '''------Conver specific xml to resource file and header file

    parse MACRO AND TYPE INTO DICT------'''
    tree = load_xml("test.xml")
    root = tree.getroot()
    if root:
        print "root tag: " , root.tag

    print build_macro_dict.__doc__
    macro_dict = {}
    build_macro_dict(root , macro_dict)
    print macro_dict




#=====================================================================================#
print main.__doc__
main()



