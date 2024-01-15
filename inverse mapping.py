import random
def mapping(permutation_table, binary_table):
    permuted_table = []
    for i in permutation_table:
        permuted_table.append(binary_table[i - 1])
    return permuted_table


def generate_random_table(start, end):
    permutation_table = []
    for i in range(start, end + 1):
        permutation_table.append(i)
    random.shuffle(permutation_table)
    return permutation_table

def inverse_mapping(permutation_table,binary_table):
    inv_permuted_table=[]
    for i in range(1,len(permutation_table)+1):
        for j in range(len(permutation_table)):
            if i==permutation_table[j]:
                inv_permuted_table.append(binary_table[j])
    return inv_permuted_table
b1=[0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
p=generate_random_table(1,64)
print(p)
b2=mapping(p,b1)
print(b2)
print(inverse_mapping(p,b2))