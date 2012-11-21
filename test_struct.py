import struct
import binascii

print "Ready to test struct..."

values = ["test" , 199 , 28 , 10]
s = struct.Struct('4sihB')
data = s.pack(*values)
hex_data = binascii.hexlify(data)

print "packet data :" , data
print "hexpacket_data: " , hex_data

values.append("77")
print values

f = file("res.bin" , "w")
f.write(hex_data)
f.close()