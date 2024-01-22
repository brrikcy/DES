import math


def key_generation():
    key_list = []
    pc1_output = permuted_choice_1()
    pc1_output_split1 = pc1_output[0]
    pc1_output_split2 = pc1_output[1]
    cls_output = circular_left_shift(pc1_output_split1, pc1_output_split2, 1)
    cls_output_split1 = cls_output[0]
    cls_output_split2 = cls_output[1]

    for rounds in range(1, 17):
        if rounds + 1 == 2 or rounds + 1 == 9 or rounds + 1 == 16:
            no_of_shift = 1
        else:
            no_of_shift = 2
        generated_key = permuted_choice_2(cls_output_split1, cls_output_split2, permuted_choice_2_ptable)
        key_list.append(generated_key)
        cls_recursive_output = circular_left_shift(cls_output_split1, cls_output_split2, no_of_shift)
        cls_output_split1 = cls_recursive_output[0]
        cls_output_split2 = cls_recursive_output[1]
    return key_list


def encryption():
    global cipher_text,iterations_required,keys
    plain_text_lst = read_plain_text()
    iterations_required = int(len(plain_text_lst) / 8)
    keys = key_generation()
    cipher_text = ''
    for i in range(iterations_required):
        plain_text_binary_table = conv_to_binary(plain_text_lst)
        initial_permutation_result = mapping(initial_permutation_ptable, plain_text_binary_table)
        Li = initial_permutation_result[:32]
        Ri = initial_permutation_result[32:64]
        for round in range(16):
            expansion_table_result = expansion_table(Ri)
            round_subkey = keys[round]
            exp_res_xor_subkey = [a ^ b for a, b in zip(expansion_table_result, round_subkey)]
            s_box_result = substitution_box(exp_res_xor_subkey)
            permutation_box_result = mapping(permutation_box_ptable, s_box_result)
            temp_for_swapping = Ri
            Ri = [a ^ b for a, b in zip(permutation_box_result, Li)]
            Li = temp_for_swapping

        _32_bit_swap_result = Ri + Li
        inv_initial_permutation_result = inv_initial_permutation(_32_bit_swap_result)
        cipher_text += inv_initial_permutation_result
    print("")
    print("ENCRYPTION")
    print("*" * 10)
    print(f"Cipher text: {cipher_text}")
def decryption():
    global cipher_text, iterations_required, keys, plain_text_length

    plain_text = ''
    cipher_text_list = list(cipher_text)

    for i in range(iterations_required):
        cipher_text_binary = conv_to_binary(cipher_text_list)
        cipher_txt_ini_per_res = mapping(initial_permutation_ptable, cipher_text_binary)
        Li = cipher_txt_ini_per_res[:32]
        Ri = cipher_txt_ini_per_res[32:64]
        for round in range(16):
            expansion_table_result = mapping(expansion_box_ptable, Ri)

            round_subkey = keys[-(round + 1)]  # accessing keys in reverse order

            exp_res_xor_subkey = [a ^ b for a, b in zip(expansion_table_result, round_subkey)]
            s_box_result = substitution_box(exp_res_xor_subkey)
            permutation_box_result = mapping(permutation_box_ptable, s_box_result)
            temp_for_swapping = Ri
            Ri = [a ^ b for a, b in zip(permutation_box_result, Li)]
            Li = temp_for_swapping
        _32_bit_swap_result = Ri + Li
        inv_initial_permutation_result = inv_initial_permutation(_32_bit_swap_result)
        plain_text += inv_initial_permutation_result
    plain_text = plain_text[:plain_text_length]
    print("")
    print("DECRYPTION")
    print("*" * 10)
    print(f"Decrypting {cipher_text} we get,")
    print(f"plain text: {plain_text}")

def read_plain_text():
    plain_text = input("Enter the plain text: ")
    global plain_text_length
    plain_text_length=len(plain_text)
    padding_required = plain_text_length % 8
    if padding_required != 0:
        plain_text = plain_text.ljust(8 * math.ceil(len(plain_text) / 8), '0')
    plain_text_lst=list(plain_text)
    return plain_text_lst


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
    inv_conv_to_binary = ''
    for i in range(1, 9):
        extract = binary_list[8 * (i - 1):8 * i]
        extract_binary_string = ''
        for bit in extract:
            extract_binary_string += str(bit)
        ASCII = int(extract_binary_string, 2)
        letter = chr(ASCII)
        inv_conv_to_binary += letter
    return inv_conv_to_binary


def mapping(permutation_table, binary_table):
    permuted_table = []
    for i in permutation_table:
        permuted_table.append(binary_table[i - 1])
    return permuted_table


def inverse_mapping(permutation_table, binary_table):
    inv_permuted_table = []
    for i in range(1, len(permutation_table) + 1):
        for j in range(len(permutation_table)):
            if i == permutation_table[j]:
                inv_permuted_table.append(binary_table[j])
    return inv_permuted_table


def read_key():
    while True:
        key = input("Enter the key (8 characters) :")
        if len(key) == 8:
            break
    key_list = []
    for i in key:
        key_list.append(i)
    return key_list


def permuted_choice_1():
    key_list = read_key()
    pc1_binary_table = conv_to_binary(key_list)
    # for i in range(1, 9):
    #     j = (8 * i) - (i * 1)
    #     pc1_binary_table.pop(j)

    pc1_permutation_result = mapping(permuted_choice_1_ptable, pc1_binary_table)
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


def permuted_choice_2(pc2_input1, pc2_input2, permuted_choice_2_ptable):
    pc2_binary_table = pc2_input1 + pc2_input2
    # indices_to_be_removed = [9, 18, 22, 25, 35, 38, 43, 54]
    # i = 0
    # for index in indices_to_be_removed:
    #     pc2_binary_table.pop(index - (i + 1))
    #     i += 1
    pc2_output = mapping(permuted_choice_2_ptable, pc2_binary_table)
    return pc2_output


def split_bits(list):
    half_of_list_len = int(len(list) / 2)
    split_left = list[:half_of_list_len]
    split_right = list[half_of_list_len:]
    return split_right, split_left


def expansion_table(right_split):
    expanded_table = mapping(expansion_box_ptable, right_split)
    return expanded_table


def substitution_box(xor_result):
    substitution_result = []

    def substitute(s_box, split_6_binary):

        row_index = str(split_6_binary[0]) + str(split_6_binary[5])
        row_index = int(row_index, 2)

        column_index = ''
        for i in range(1, 5):
            column_index += str(split_6_binary[i])
        column_index = int(column_index, 2)

        sub_value = s_box[row_index][column_index]
        sub_value_binary = bin(sub_value)[2:].zfill(4)

        for bit in sub_value_binary:
            substitution_result.append(int(bit))

    substitute(s_boxes_list[0], xor_result[:6])
    substitute(s_boxes_list[1], xor_result[6:12])
    substitute(s_boxes_list[2], xor_result[12:18])
    substitute(s_boxes_list[3], xor_result[18:24])
    substitute(s_boxes_list[4], xor_result[24:30])
    substitute(s_boxes_list[5], xor_result[30:36])
    substitute(s_boxes_list[6], xor_result[36:42])
    substitute(s_boxes_list[7], xor_result[42:48])
    return substitution_result


def inv_initial_permutation(_32_swap_res):
    mapping_inverse = inverse_mapping(initial_permutation_ptable, _32_swap_res)
    conv_to_binary_inverse = inv_conv_to_binary(mapping_inverse)
    return conv_to_binary_inverse





initial_permutation_ptable =[58, 50, 42, 34, 26, 18, 10, 2,
 60, 52, 44, 36, 28, 20, 12, 4,
 62, 54, 46, 38, 30, 22, 14, 6,
 64, 56, 48, 40, 32, 24, 16, 8,
 57, 49, 41, 33, 25, 17, 9, 1,
 59, 51, 43, 35, 27, 19, 11, 3,
 61, 53, 45, 37, 29, 21, 13, 5,
 63, 55, 47, 39, 31, 23, 15, 7]

permutation_box_ptable =[
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]



permuted_choice_1_ptable =[57, 49, 41, 33, 25, 17, 9,
  1, 58, 50, 42, 34, 26, 18,
 10, 2, 59, 51, 43, 35, 27,
 19, 11, 3, 60, 52, 44, 36,
 63, 55, 47, 39, 31, 23, 15,
 7, 62, 54, 46, 38, 30, 22,
 14, 6, 61, 53, 45, 37, 29,
 21, 13, 5, 28, 20, 12, 4]

permuted_choice_2_ptable =[14, 17, 11, 24, 1, 5,
 3, 28, 15, 6, 21, 10,
 23, 19, 12, 4, 26, 8,
 16, 7, 27, 20, 13, 2,
 41, 52, 31, 37, 47, 55,
 30, 40, 51, 45, 33, 48,
 44, 49, 39, 56, 34, 53,
 46, 42, 50, 36, 29, 32]


# ------------------------------------------
expansion_box_ptable =[32, 1, 2, 3, 4, 5,
 4, 5, 6, 7, 8, 9,
 8, 9, 10, 11, 12, 13,
 12, 13, 14, 15, 16, 17,
 16, 17, 18, 19, 20, 21,
 20, 21, 22, 23, 24, 25,
 24, 25, 26, 27, 28, 29,
 28, 29, 30, 31, 32, 1]

# ------------------------------------------


s_box_1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]

s_box_2 = [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
]

s_box_3 = [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
]

s_box_4 =[
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
]

s_box_5 = [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
]


s_box_6 = [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
]

s_box_7 = [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
]

s_box_8 = [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]
s_boxes_list=[s_box_1,s_box_2,s_box_3,s_box_4,s_box_5,s_box_6,s_box_7,s_box_8]


encryption()
decryption()