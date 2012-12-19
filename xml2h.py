#coding = "gbk"
import xml.etree.ElementTree as ET

def load_xml(xml_file):
    tree = ET.parse(xml_file)
    if tree:
        print "load " , xml_file , "success"
    else:
        print "load " , xml_file , "failed"
    return tree


def parse_macro(root , macro_dict , header_file):
    '''------parse macro into macro dict
    macro_dict------'''
 #  GET TAG MACROS
    macros_set = root.findall('macros')
    if macros_set:
        print "get TAG MACROS success"
    else:
        print "get TAG MACROS failed"
        return -1

 #  GET EACH MACROS TAG IN MACROS_SET
    macros_node = macros_set[0]

#   parse each macro node
    i = 1
    for macro_node in macros_node:
        #check name
        if 'name' not in macro_node.attrib:
            print "!ERROR: MACRO NO." , i , "HAS NO NAME"
            return -1
        #check id
        if 'id' not in macro_node.attrib:
            print "!ERROR: MACRO NO." , i , " " , macro_node.attrib['name'] , "NO ID"
            return -1
#        macro_dict[macro_node.attrib['name']] = macro_node.attrib['id']
        write_str = "#define " + macro_node.attrib['name'] + " " + macro_node.attrib['id']

        #check if desc
        if 'desc' in macro_node.attrib:
 #           macro_dict[macro_node.attrib['name']] = macro_dict[macro_node.attrib['name']] + "&" + macro_node.attrib['desc']
            write_str = write_str + " /* " + macro_node.attrib['desc'] + "*/"

        write_str = write_str.encode('UTF-8')
        write_str = write_str + "\n"
#        print "it is " , write_str
        header_file.write(write_str)
        i = i + 1


def parse_type(root , type_dict , header_file):
    #type_node set
    type_set = root.findall('type')

    #parse each type_node
    i = 0
    #---------------type node-----------------
    for type_node in type_set:
        if 'name' not in type_node.attrib:
            print "!ERROR: TYPE NO." , i , "HAS NO NAME"
            return -1
#        print "it is: " + type_node.attrib['name']

        write_str = "struct " + type_node.attrib['name'] + "{\n"

        #-----------item_set--------------------
        item_set = type_node.findall('item')
        j = 0
        for item_node in item_set:
            if 'name' not in item_node.attrib:
                print "!ERROR: TYPE NO." , i , "ITEM NO." , j , " HAS NO NAME"
                return -1
            if 'type' not in item_node.attrib:
                print "!ERROR: TYPE NO." , i , "ITEM NO." , j , " HAS NO TYPE"
                return -1
 #           print ">>" + item_node.attrib['name']

            #------item type-----
            is_struct = 0   #not struct
            type_str = "    "   #four space before
            item_type = item_node.attrib['type']
            if item_type == 'char':
                type_str = type_str + "char "
            elif item_type == "uchar":
                type_str = type_str + "unsigned char "
            elif item_type == "short":
                type_str = type_str + "short "
            elif item_type == "ushort":
                type_str = type_str + "unsigned short "
            elif item_type == "int":
                type_str = type_str + "int "
            elif item_type == "uint":
                type_str = type_str + "unsigned int "
            elif item_type == "long":
                type_str = type_str + "long "
            elif item_type == "ulong":
                type_str = type_str + "unsigned long "
   #         elif item_type == "string":   #string as char[]
   #             value = 'b'
            elif item_type == "long long":
                type_str = type_str + "long long "
            elif item_type == "float":
                type_str = type_str + "float "
            elif item_type == "double":
                type_str = type_str + "double "
  #          elif '*' in item_type:   #pointer uses type of long
  #              value = 'l'
            else:   #special type
                type_str = type_str + "struct "

            #----item name------
            type_str = type_str + item_node.attrib['name']

            #----count----
            if 'count' in item_node.attrib:
                type_str = type_str + "[" + item_node.attrib['count'] + "]"

            type_str = type_str + ";"

            #----desc-----
            if 'desc' in item_node.attrib:
                type_str = type_str + " /*" + item_node.attrib['desc'] + " */"
                type_str = type_str.encode('UTF-8')

            type_str = type_str + "\n"
            write_str = write_str + type_str
            j = j + 1
        #end for item_node in item_set
        write_str = write_str + "};\n"
        write_str = write_str + "typedef struct " + type_node.attrib['name'] + "  " + type_node.attrib['name'].upper() + ";\n"
        write_str = write_str + "typedef struct " + type_node.attrib['name'] + " * pst" + type_node.attrib['name'].upper() + ";\n"
        write_str = write_str + "\n\n"
#        print "it is: " , write_str
        header_file.write(write_str)
    #end for type_node in type_set

    return 0



def main():
    '''------Conver specific xml to header file

    parse MACRO INTO MACRODEFINE; TYPE INTO STRUCT------'''
    tree = load_xml("test.xml")
    root = tree.getroot()
    if root:
        print "root tag: " , root.tag

    #open file
    header_file = file("xx_res.h" , "w")

    #parse macro
    print "Ready to parse macro..."
    macro_dict = {}
    ret = parse_macro(root , macro_dict , header_file)
#    print macro_dict
    if ret == -1:
        return -1


    #parse type
    print "Ready to parse type..."
    type_dict = {}
    ret = parse_type(root , type_dict , header_file)
    if ret == -1:
        return -1


    header_file.close()

#=====================================================================================#
print main.__doc__
main()
