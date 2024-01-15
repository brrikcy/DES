def conv_to_binary(user_input_list):
    split_binary_list = []
    for j in range(8):
        temp = user_input_list.pop(0)
        ASCII = ord(temp)
        Binary = bin(ASCII)[2:].zfill(8)
        for k in Binary:
            split_binary_list.append(int(k))
    return split_binary_list

def inv_conv_to_binary(binary_list):
    inv_conv_to_binary=''
    for i in range(1,9):
        extract=binary_list[8*(i-1):8*i]
        extract_binary_string=''
        for bit in extract:
            extract_binary_string+=str(bit)
        ASCII=int(extract_binary_string,2)
        letter=chr(ASCII)
        inv_conv_to_binary+=letter
    return inv_conv_to_binary

a=conv_to_binary(['a','b','c','d','e','f','g','h'])
print(a)
print(inv_conv_to_binary(a))