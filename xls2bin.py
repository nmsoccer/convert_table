#converse XXXX.xsl file to XXXX.bin
#binary file records stat of xls file
#conversing process needs xx.res.bin as reference
import xlrd
import sys
import struct
import binascii


def convert_xls_file(xls_file):
    print "ready to convers " , xls_file , "......"

    #open xls file
    book = xlrd.open_workbook(xls_file)
    sheet = book.sheets()[0]

    #read convlist.ini to find xls_file's refer data struct type
    convlist_file = file("convlist.ini" , "r")
    if convlist_file == False:
        print "!ERROR Can not open convlist.ini"
        return -1
    while True:
        line = convlist_file.readline()
        if len(line) == 0:
            break
        if line[0] == '#':
            continue
        convlist_array = line.split('&')
 #       print convlist_array
        if xls_file == convlist_array[0]:
            data_type = convlist_array[1]
            print "data type is: " , data_type
            break
    convlist_file.close()

    #load xx_res.bin to search data_type
    res_bin_file = file("xx_res.bin" , "r")
    if res_bin_file == False:
        print "!ERROR Can not open xx_res.bin"
        return -1
    while True:
        line = res_bin_file.readline()
        if len(line) == 0:
                break
        bin_array = line.split(':')
        if bin_array[0] == data_type:
            type_value = bin_array[1]
            print "data type " , data_type , "value is: " , type_value
            break
    res_bin_file.close()


    #each row in sheet
    print "ready to generate bin/" , convlist_array[2]
    target_bin_file = file("bin/" + convlist_array[2] , "wb")
    for row_index in range(sheet.nrows):
        if row_index == 0:
            continue

        row_value = []
        for column_index in range(sheet.ncols):
             print "it is: " , sheet.row(row_index)[column_index].value
             result = sheet.row(row_index)[column_index].value
             if isinstance(result , float):
                 result = int(result)
             else:
 #                print "string"
                 #converse unicode string to utf-8
                 result = result.encode('UTF-8')
             row_value.append(result)
#        print row_value

        #converse data
        data_struct = struct.Struct(type_value)
        print "repack data :" , row_value
        data = data_struct.pack(*row_value)
        print "packed data :" , data
        hex_data = binascii.hexlify(data)
        print "hex data:" , hex_data
        target_bin_file.write(data)
 #       target_bin_file.write(10)


    target_bin_file.close()




def main():
    '''------Conver xls file into bin file

    as resource in game------'''
    #needs xls file
    if len(sys.argv) < 2:
        print "!ERROR Please input xls file"
        return -1
    #converting...
    convert_xls_file(sys.argv[1])

#    book =xlrd.open_workbook("test.xls")

#    sh=book.sheets()[0]

#    for row in range(sh.nrows):
#        if row == 0:
#            continue

#        print row
#        for i in range(len(sh.row(row))):
#		tmp = tmp + sh.row(row)[i].value
#		tmp = tmp + "\t"
#        tmp = sh.row(row)[i].value
#            print sh.row(row)[i].value

#=====================================================================================#
print main.__doc__
main()
