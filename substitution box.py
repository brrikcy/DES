import random
def gen_random_table(start,end):
    permutation_table = []
    for i in range(start,end+1):
        permutation_table.append(i)
    random.shuffle(permutation_table)
    return permutation_table
def substitution_box(xor_result):


    s_box_list = []
    for boxes in range(8):
        s_box = [gen_random_table(0,15),
                gen_random_table(0,15),
                gen_random_table(0,15),
                gen_random_table(0,15)]
        s_box_list.append(s_box)


    s_box_1 = s_box_list[0]
    s_box_2 = s_box_list[1]
    s_box_3 = s_box_list[2]
    s_box_4 = s_box_list[3]
    s_box_5 = s_box_list[4]
    s_box_6 = s_box_list[5]
    s_box_7 = s_box_list[6]
    s_box_8 = s_box_list[7]
    print(f"sb-1 {s_box_1}")
    print(f"sb-2 {s_box_2}")
    print(f"sb-3 {s_box_3}")
    print(f"sb-4 {s_box_4}")
    print(f"sb-5 {s_box_5}")
    print(f"sb-6 {s_box_6}")
    print(f"sb-7 {s_box_7}")
    print(f"sb-8 {s_box_8}")

    substitution_result = []
    def substitute(s_box, split_6_binary):
        print("*"*10)
        print(f"Split 6 binary {split_6_binary}")
        row_index = str(split_6_binary[0]) + str(split_6_binary[5])
        row_index = int(row_index, 2)
        print(f"row index:{row_index}")
        column_index = ''
        for i in range(1, 5):
            column_index += str(split_6_binary[i])
        column_index = int(column_index, 2)
        print(f"column index:{column_index}")
        sub_value = s_box[row_index][column_index]
        sub_value_binary = bin(sub_value)[2:].zfill(4)
        print(f"sub value binary :{sub_value_binary}")
        for bit in sub_value_binary:
            substitution_result.append(int(bit))


    substitute(s_box_1, xor_result[:6])
    substitute(s_box_2, xor_result[6:12])
    substitute(s_box_3, xor_result[12:18])
    substitute(s_box_4, xor_result[18:24])
    substitute(s_box_5, xor_result[24:30])
    substitute(s_box_6, xor_result[30:36])
    substitute(s_box_7, xor_result[36:42])
    substitute(s_box_8, xor_result[42:48])
    print(f"substitution result {substitution_result}")
    print(f"result length {len(substitution_result)}")
substitution_box([0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1])