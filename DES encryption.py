import random
import math

def key_generation():
    key_list = []
    pc1_output = permuted_choice_1()
    pc1_output_split1 = pc1_output[0]
    pc1_output_split2 = pc1_output[1]
    cls_output = circular_left_shift(pc1_output_split1, pc1_output_split2, 1)
    cls_output_split1 = cls_output[0]
    cls_output_split2 = cls_output[1]
    pc2_permutation_table = gen_permutation_table(48)
    for rounds in range(1,17):
        if rounds+1 == 2 or rounds+1 == 9 or rounds+1 == 16:
            no_of_shift = 1
        else:
            no_of_shift = 2
        generated_key = permuted_choice_2(cls_output_split1, cls_output_split2,pc2_permutation_table)
        key_list.append(generated_key)
        cls_recursive_output = circular_left_shift(cls_output_split1, cls_output_split2, no_of_shift)
        cls_output_split1 = cls_recursive_output[0]
        cls_output_split2 = cls_recursive_output[1]
    return key_list
def plaintext_operations():
    plain_text_lst=read_plain_text()
    initial_permutation_table = gen_permutation_table(64)
    iterations_required = int(len(plain_text_lst) / 8)
    for i in range(iterations_required):
        initial_permutation_binary_table = conv_to_binary(plain_text_lst)
        initial_permutation_result=mapping(initial_permutation_table,initial_permutation_binary_table)
        """The following operations have to be added to this loop. 
        1. 16 round operations
        2. 32 bit swap
        3. Inverse initial permutation  """










def read_plain_text():
    plain_text = input("Enter the plain text: ")
    plain_text_lst = []
    padding_required = len(plain_text) % 8
    if padding_required != 0:
        plain_text = plain_text.ljust(8 * math.ceil(len(plain_text) / 8), '0')
    for i in plain_text:
        plain_text_lst.append(i)
    return plain_text_lst


def conv_to_binary(user_input_list):
    split_binary_list = []
    for j in range(8):
        temp = user_input_list.pop(0)
        ASCII = ord(temp)
        Binary = bin(ASCII)[2:].zfill(8)
        for k in Binary:
            split_binary_list.append(k)
    return split_binary_list


def gen_permutation_table(n):
    permutation_table = []
    for i in range(1, n + 1):
        permutation_table.append(i)
    random.shuffle(permutation_table)
    return permutation_table


def mapping(permutation_table, binary_table):
    permuted_table = []
    for i in permutation_table:
        permuted_table.append(binary_table[i - 1])
    return permuted_table


def read_key():
    while True:
        key = input("Enter the key (8 charecters) :")
        if len(key) == 8:
            break
    key_list = []
    for i in key:
        key_list.append(i)
    return key_list


def permuted_choice_1():
    key_list = read_key()
    pc1_binary_table = conv_to_binary(key_list)
    for i in range(1, 9):
        j = (8 * i) - (i * 1)
        pc1_binary_table.pop(j)
    pc1_permutation_table = gen_permutation_table(56)
    pc1_permutation_result = mapping(pc1_permutation_table, pc1_binary_table)
    pc1_result_1 = pc1_permutation_result[:28]
    pc1_result_2 = pc1_permutation_result[28:]
    return pc1_result_1, pc1_result_2


def circular_left_shift(cls_inp1, cls_inp2, shifts):
    for i in range(shifts):
        shift_val = cls_inp1.pop(0)
        cls_inp1.append(shift_val)
        shift_val = cls_inp2.pop(0)
        cls_inp2.append(shift_val)
    cls_output1 = cls_inp1
    cls_output2 = cls_inp2
    return cls_output1, cls_output2



def permuted_choice_2(pc2_input1, pc2_input2,pc2_permutation_table):
    pc2_binary_table = pc2_input1 + pc2_input2
    indices_to_be_removed = [9, 18, 22, 25, 35, 38, 43, 54]
    i = 0
    for index in indices_to_be_removed:
        pc2_binary_table.pop(index - (i + 1))
        i += 1
    pc2_output = mapping(pc2_permutation_table, pc2_binary_table)
    return pc2_output



plaintext_operations()