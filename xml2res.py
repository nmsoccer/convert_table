#coding = "gbk"
import xml.etree.ElementTree as ET

def load_xml(xml_file):
    tree = ET.parse(xml_file)
    if tree:
        print "load " , xml_file , "success"
    else:
        print "load " , xml_file , "failed"
    return tree


def macro_dict_append(macro_dict , macros_node):
    '''------append each macro node to
    macro dict------'''
    i = 1
    for macro_node in macros_node:
        #check name
        if 'name' not in macro_node.attrib:
            print "!ERROR: MACRO NO." , i , "HAS NO NAME"
            return
        #check id
        if 'id' not in macro_node.attrib:
            print "!ERROR: MACRO NO." , i , " " , macro_node.attrib['name'] , "NO ID"
            return
        macro_dict[macro_node.attrib['name']] = macro_node.attrib['id']
        #check if desc
        if 'desc' in macro_node.attrib:
            macro_dict[macro_node.attrib['name']] = macro_dict[macro_node.attrib['name']] + "&" + macro_node.attrib['desc']
        i = i + 1



def build_macro_dict(root , macro_dict):
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
    for macros_node in macros_set:
        ret = macro_dict_append(macro_dict , macros_node)
    return ret


def type_dict_append(type_dict , types_set , macro_dict):
    i = 0

    for type_node in types_set:
        if 'name' not in type_node.attrib:
            print "!ERROR: TYPE NO." , i , "HAS NO NAME"
            return -1

        i = i+1
 #       print "READY TO CONVERT NEW TYPE>>>>>>>>>>>>"
        #------handle each item------
        type_dict[type_node.attrib['name']] = ""
        j = 1
        for item_node in type_node.findall('item'):
 #           print item_node.attrib

            if 'name' not in item_node.attrib:
                print "!ERROR: TYPE NO." , i , "ITEM NO." , j , " HAS NO NAME"
                return -1
            if 'type' not in item_node.attrib:
                print "!ERROR: TYPE NO." , i , "ITEM NO." , j , " HAS NO TYPE"
                return -1

            #------set value------
            item_type = item_node.attrib['type']
            flag = 0    #0:type is normal; 1: type is struct or other self defined type
            if item_type == "char":
                value = 's'
            elif item_type == "uchar":
                value = 'B'
            elif item_type == "short":
                value = 'h'
            elif item_type == "ushort":
                value = 'H'
            elif item_type == "int":
                value = 'i'
            elif item_type == "uint":
                value = 'I'
            elif item_type == "long":
                value = 'l'
            elif item_type == "ulong":
                value = 'L'
   #         elif item_type == "string":   #string as char[]
   #             value = 'b'
            elif item_type == "long long":
                value = 'Q'
            elif item_type == "float":
                value = 'f'
            elif item_type == "double":
                value = 'd'
  #          elif '*' in item_type:   #pointer uses type of long
  #              value = 'l'
            else:   #special type
                flag = 1

#            print "value is" , value
            #---set value according to falg----
            real_str = " "
            if flag == 1:   #special type
                if item_type not in type_dict:  #not define type before
                    print "!ERROR: TYPE NO." , i , "ITEM NO." , j , "special type " , item_tye , "not defined"
                    return -1

                if 'count' in item_node.attrib: #repeat count
                    count = item_node.attrib['count']

                    if count in macro_dict: #number often uses macro
                        count = macro_dict[count]
                    elif count[0] < '0' or count[0] > '9': # not imediate number unknown count
                        print "!ERROR: TYPE NO." , i , "ITEM NO." , j , "count " , count , "not defined"
                        return -1

   #                 print "count is " , item_node.attrib['count'] , "real number is: " , count
                    k = 0
                    while k<int(count):
                        real_str =  real_str + type_dict[item_type]
                        k = k +1
                else:
                    real_str = real_str + type_dict[item_type]

            else:   #normal type
                if 'count' in item_node.attrib:
                    count = item_node.attrib['count']

                    if count in macro_dict: #number often uses macro
                        count = macro_dict[count]
                    elif count[0] < '0' or count[0] > '9': # not imediate number unknown count
                        print "!ERROR: TYPE NO." , i , "ITEM NO." , j , "count " , count , "not defined"
                        return -1

                    print "count is " , item_node.attrib['count'] , "real number is: " , count
                    real_str = real_str + count + value
                else:
                    real_str = real_str + value

#            print "real_str is: " , real_str
            j = j + 1

            #get item string
            type_dict[type_node.attrib['name']] = type_dict[type_node.attrib['name']] + real_str[1:]
   #         print "type value is: " , type_dict[type_node.attrib['name']]

    return 0



def build_type_dict(root , type_dict , macro_dict):
    '''......parse type into type dict
    type_dict. key is name of type,and value is a string that symbals type of member......'''

    #types_set concludes all type nodes
    types_set = root.findall("type")
    if types_set:
        print "get TAG TYPE success"
    else:
        print "get TAG TYPE failed"
        return -1
    #handle  types node
    ret = type_dict_append(type_dict , types_set , macro_dict)
    return ret


def xml2h(root , macro_dict):
    '''......parse xml into xx_res.h
    macro and struct......'''

    #open file
    header_file = file("xx_res.h" , "w")

    #write macro
    for macro_name in macro_dict:
        print " " , macro_name , ": " , macro_dict[macro_name]
        value_array = macro_dict[macro_name].split('&')
        print value_array



    header_file.close()


def main():
    '''------Conver specific xml to resource file and header file

    parse MACRO AND TYPE INTO DICT------'''
    tree = load_xml("test.xml")
    root = tree.getroot()
    if root:
        print "root tag: " , root.tag

    #BUILD MACRO DICT
    print build_macro_dict.__doc__
    macro_dict = {}
    build_macro_dict(root , macro_dict)
    print macro_dict

    #BUILD TYPE DICT
    print build_type_dict.__doc__
    type_dict = {}
    ret = build_type_dict(root , type_dict , macro_dict)

    if ret == -1: #failed
        return -1

    print type_dict
    #write to xx_res.bin
    f = file("xx_res.bin" , "w")


    for each_type in type_dict.items():
  #      print "type is: " , each_type , " ; value is: " , each_type_value
  #      writing_str = "&" , each_type , ":" , each_type_value , "\n"
        fstr =  ":".join(each_type)
        fstr = fstr + ":end\n"
        print fstr
        f.write(fstr)

    f.close()
    print "xml to xx_res.bin success!"

    print "ready to generate xx_res.h......."
    xml2h(root , macro_dict)





    return 0


#=====================================================================================#
print main.__doc__
main()



