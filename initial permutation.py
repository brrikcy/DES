import random
plain_text=input("Enter the plain text")
plain_text_lst=[]
split_64_binary=[]
permuted_table=[]
for i in plain_text:
    plain_text_lst.append(i)
for j in range(8):
    temp=plain_text_lst.pop(0)
    ASCII=ord(temp)
    Binary=bin(ASCII)[2:].zfill(8)
    for k in Binary:
        split_64_binary.append(k)

def gen_permutation_table():
    permutation_table=[]
    for i in range(1,65):
        permutation_table.append(i)
    random.shuffle(permutation_table)
    return permutation_table

p_table=gen_permutation_table()
for i in p_table:
    permuted_table.append(split_64_binary[i-1])
print(permuted_table)
