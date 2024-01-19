import random
import math

"""
key_generation() function is used for key expansion in which
the functions with operations to be performed on key of 8 characters are called
in sequential order. 
This function takes no argument and it returns a list containing 16 keys each of which
are a list of 48 bit binary.
"""


def key_generation():
    key_list = []
    entered_key = read_key()
    pc1_binary_table = conv_to_binary(entered_key)
    pc1_output = permuted_choice_1(pc1_binary_table)
    pc1_output_split1 = pc1_output[0]  # accessing outputs of permuted_choice_1() which returns
    pc1_output_split2 = pc1_output[1]  # two values into a tuple using indices.

    # giving 1 as parameter for shifts so that 1 bit shift is performed in the first round
    cls_output = circular_left_shift(pc1_output_split1, pc1_output_split2, 1)

    cls_output_split1 = cls_output[0]  # inputs for 1st permuted choice-2
    cls_output_split2 = cls_output[1]

    for rounds in range(1, 17):

        # for rounds 1,2,9 and 16 1 bit lcs is done.
        if rounds + 1 == 2 or rounds + 1 == 9 or rounds + 1 == 16:
            no_of_shift = 1
        else:
            # for all other rounds, 2 bit lcs is done.
            no_of_shift = 2

        generated_key = permuted_choice_2(cls_output_split1, cls_output_split2)

        # appending generated key into key list
        key_list.append(generated_key)

        # updating variables inorder to give input to the next round
        cls_recursive_output = circular_left_shift(cls_output_split1, cls_output_split2, no_of_shift)
        cls_output_split1 = cls_recursive_output[0]
        cls_output_split2 = cls_recursive_output[1]
    return key_list


"""
encryption() function is used for encrypting the plain text in which
the functions with operations to be performed on each 8 bit block
of plain text are called in sequential order. 
This function takes no argument and prints the cipher text as output. 
"""


def encryption():
    plain_text_lst = read_plain_text()
    global iterations_required, keys, cipher_text  # globalizing to use in the decryption function
    iterations_required = int(len(plain_text_lst) / 8)  # no of 8 bit blocks of plain text
    keys = key_generation()  # list of 16 keys
    cipher_text = ''
    for i in range(iterations_required):
        plain_text_binary_table = conv_to_binary(plain_text_lst)
        initial_permutation_result = mapping(initial_permutation_ptable, plain_text_binary_table)

        # splitting initial permutation result into left and right half
        Li = initial_permutation_result[:32]
        Ri = initial_permutation_result[32:64]

        for round in range(16):
            expansion_table_result = mapping(expansion_box_ptable, Ri)
            round_subkey = keys[round]
            """performing x-or operation on values of two lists by using zip function
            which will return tuple of corresponding values of each lists which is accessed
            using for loop and two variables a and b"""
            exp_res_xor_subkey = [a ^ b for a, b in zip(expansion_table_result, round_subkey)]
            s_box_result = substitution_box(exp_res_xor_subkey)
            permutation_box_result = mapping(permutation_box_ptable, s_box_result)

            # swapping Ri and Li using temp
            # updating variables inorder to give input to the next round
            temp_for_swapping = Ri
            Ri = [a ^ b for a, b in zip(permutation_box_result, Li)]
            Li = temp_for_swapping

        _32_bit_swap_result = Ri + Li
        inv_initial_permutation_result = inv_initial_permutation(_32_bit_swap_result)

        # adding result of each iteration into cipher_text
        cipher_text += inv_initial_permutation_result

    # printing cipher text
    print("")
    print("ENCRYPTION")
    print("*" * 10)
    print(f"Cipher text: {cipher_text}")


"""
decryption() function is used for decrypting the plain text in which
the functions with operations to be performed on each 8 bit block
of cipher text are called in sequential order. 
This function takes no argument and prints the plai text as output. 
"""


def decryption():
    # accessing variables declared in encryption() function
    global cipher_text, iterations_required, keys, plain_text_length

    plain_text = ''
    cipher_text_list = list(cipher_text)

    # performing operations performed during encryption with keys in reverse order
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


"""
read_plain_text() function prompts the user to enter the plain text,
perform padding on the plain text if required, and put the plain text into a list
This function takes no argument and return a list of padded plain text entered
by the user as output.
"""


def read_plain_text():
    global plain_text_length  # to be accessed in encryption and decryption functions
    plain_text = input("Enter the plain text: ")
    plain_text_length = len(plain_text)
    plain_text_lst = []

    padding_required = len(plain_text) % 8  # checking if entered plain text is a multiple of 8 or not
    # if not multiple of 8, padding is required else, no padding is required.

    if padding_required != 0:
        """using ljust to fill zeros at the end of plain text in the required amount if 
        padding is required. The amount of zeros to be added is found by multiplying 8 with ciel
        value of length of plain text when divided by 8.
        For example, if len(plain_text) = 19, 8*ciel(19/8) = 8*ciel(2.37) = 8*3=24 so 24-19=5
        0's will be added to the end by ljust function"""
        plain_text = plain_text.ljust(8 * math.ceil(len(plain_text) / 8), '0')
    plain_text_lst = list(plain_text)
    return plain_text_lst


"""
conv_to_binary() function takes 8 characters from the inputed list,
convert each character to it's corresponding ASCII and then the ASCII
value into 8 bit binary after which it appends each bit of each 8 bit 
binary into a list
This function takes a list of charecters as argument and returns 
the binary equivalent of ASCII value of each charecters.
"""


def conv_to_binary(user_input_list):
    split_binary_list = []
    for j in range(8):
        """popping each bits from the list for 8 times so that it process only 8 bits at a time
        to produce 64 bit binary output"""
        temp = user_input_list.pop(0)
        ASCII = ord(temp)
        """removing prefix '0b' while converting to binary and ensuring the output is 8 bit binary
        by using zfill(8) which adds zeros on the left if no. of bits is less than 8 till it is 
        equal to 8."""
        Binary = bin(ASCII)[2:].zfill(8)
        for k in Binary:
            split_binary_list.append(int(k))
    return split_binary_list


"""
inv_conv_to_binary() function performs the inverse operation of conv_to_binary().
It takes 8 bit at a time from the inputted binary list, convert it into decimal,
and then converts the decimal value into corresponding character by considering the
decimal value as it's ASCII value. This operations is performed for 8 times so that
in a single run, this function will process 64 bit binary to produce 8 characters.
This function takes a binary list as argument and returns a string containing 8 characters
as output.

"""


def inv_conv_to_binary(binary_list):
    inv_conv_to_binary = ''
    for i in range(1, 9):

        # extracting each 8 bits at a time
        extract = binary_list[8 * (i - 1):8 * i]

        extract_binary_string = ''
        for bit in extract:
            extract_binary_string += str(bit)

        # converting binary to decimal
        ASCII = int(extract_binary_string, 2)

        # converting decimal to character
        letter = chr(ASCII)

        inv_conv_to_binary += letter
    return inv_conv_to_binary


"""
mapping() function is used to permute the inputted binary table with respect to
a permutation table.
This function takes permutation list and binary list as input and returns
a list of binary after permutation as output.
"""


def mapping(permutation_table, binary_table):
    permuted_table = []
    for i in permutation_table:
        """finding the values at particular index of binary table according to the values in permutation
        table and appending them into a new list"""
        permuted_table.append(binary_table[i - 1])
    return permuted_table


"""
inverse_mapping() function performs the inverse operation of the mapping() function.
This function remaps the inputted binary list according to the permutation table to nullify
the mapping done using mapping() function.
This function takes permutation list and binary list as input and returns
a list of binary after remapping.
"""


def inverse_mapping(permutation_table, binary_table):
    inv_permuted_table = []

    # finding index of each value from 1 to 64 in the permutation table
    for i in range(1, len(permutation_table) + 1):
        for j in range(len(permutation_table)):
            if i == permutation_table[j]:

                # appending the new list with the value at the same index in the binary table in order
                inv_permuted_table.append(binary_table[j])

    return inv_permuted_table


"""
read_key() function prompts user to input key of 8 characters. It will continue
prompting for entering the key until the length of the key is 8 characters and stores 
each characters of the key in a list.
This function takes no input and returns a character list containing key of length 8. 

"""


def read_key():
    """checking if the entered key is of length 8 and prompting the user to enter the key
    intil its length is 8"""
    while True:
        key = input("Enter the key (8 characters) :")
        if len(key) == 8:
            break
    key_list = list(key)
    return key_list


"""
permuted_choice_1() function removes bits in the position which is in the multiple of
8 (8,16....) from the inputted binary list of 64 bits, Performs mapping of the binary list
of 56 bits with a permutation table of length 56 bits and puts the output in a list which is then
splitted into two parts.
This function takes a binary list as input and returns two binary lists as output.   
"""


def permuted_choice_1(key_binary_table):

    # removing bits in the position which are multiples of 8(8,16..64)
    for i in range(1, 9):
        j = (8 * i) - (i * 1)
        key_binary_table.pop(j)

    # mapping with a permutation table
    pc1_permutation_result = mapping(permuted_choice_1_ptable, key_binary_table)

    # splitting result into two 28 bit lists
    pc1_result_1 = pc1_permutation_result[:28]
    pc1_result_2 = pc1_permutation_result[28:]

    return pc1_result_1, pc1_result_2  # this returns a tuple (pc1_result_1,pc1_result_2)


"""
circular_left_shift() function performs circular left shift operations on the inputted
list(two of them) in which number of shifts to be performed is passed as a parameter while
calling the function.
This function takes two binary lists cls_inp1 and cls_inp2  and an integer 'shifts' as
argument and returns two binary lists as output
"""


def circular_left_shift(cls_inp1, cls_inp2, shifts):
    for i in range(shifts):  # initializing loop so that any number of shifts can be performed according to input

        # performing shift operation on first list
        shift_val = cls_inp1.pop(0)
        cls_inp1.append(shift_val)

        # performing shift operation on second list
        shift_val = cls_inp2.pop(0)
        cls_inp2.append(shift_val)
    cls_output1 = cls_inp1
    cls_output2 = cls_inp2

    return cls_output1, cls_output2  # this returns a tuple (cls_output1,cls_output2)


"""
permuted_choice_2() function concatenates two lists which are given as input,removes indices 
9,18,22,25,35,38,43 and 54 from the concatenated list and perform mapping on the resultting list
with a permutation table
This function takes 2 binary lists as input and returns a binary list as output.

"""


def permuted_choice_2(pc2_input1, pc2_input2):

    # concatenating inputted list
    pc2_binary_table = pc2_input1 + pc2_input2

    indices_to_be_removed = [9, 18, 22, 25, 35, 38, 43, 54]
    i = 0

    # removing bits at the indices in the above mentioned list
    for index in indices_to_be_removed:
        pc2_binary_table.pop(index - (i + 1))
        i += 1

    # mapping using permutation table
    pc2_output = mapping(permuted_choice_2_ptable, pc2_binary_table)

    return pc2_output


"""
substitution_box() function substitutes each 6 bit blocks of inserted 48 bit binary list 
with 4 bit binary so that the output will be 32 bit binary list.
This function takes a binary list of 48 bits as argument and returns another 
binary list of 32 bits as output after performing 8 substitution operations. 
"""


def substitution_box(xor_result):
    substitution_result = []

    """
    substitute function finds the value to be substituted using the row and column index
    of s-box which has 4 rows(0,1,2,3) and 16 columns(0,1,2....16) and converts it into 4 bit binary.
    This function takes 4 by 16 s-box and 6 bit binary list as argument and substitute each 6 bits of
    the binary list. 
    """

    def substitute(s_box, split_6_binary):

        # taking 1st and 6th bits for calculating row index
        row_index = str(split_6_binary[0]) + str(split_6_binary[5])
        row_index = int(row_index, 2)  # convering into decimal

        column_index = ''
        # taking bits from 1 to 5 for calculating column index
        for i in range(1, 5):
            column_index += str(split_6_binary[i])

        # convering into decimal
        column_index = int(column_index, 2)

        # finding substitution value using row and column index and converting it to 4 bit binary
        sub_value = s_box[row_index][column_index]
        sub_value_binary = bin(sub_value)[2:].zfill(4)

        for bit in sub_value_binary:
            substitution_result.append(int(bit))

    # performing substitution for 8 six block binary of 48 bit binary with 8 different s-boxes
    substitute(s_boxes_list[0], xor_result[:6])
    substitute(s_boxes_list[1], xor_result[6:12])
    substitute(s_boxes_list[2], xor_result[12:18])
    substitute(s_boxes_list[3], xor_result[18:24])
    substitute(s_boxes_list[4], xor_result[24:30])
    substitute(s_boxes_list[5], xor_result[30:36])
    substitute(s_boxes_list[6], xor_result[36:42])
    substitute(s_boxes_list[7], xor_result[42:48])
    return substitution_result


"""
inverse_initial_permutation function remapps the inputted binary list(using inverse_mapping())
and convert each 8 bit binary into characters(using inv_conv_to_binary)
This function takes 64 bit binary list as argument and returns 8 charecters as output
"""


def inv_initial_permutation(_32_swap_res):
    mapping_inverse = inverse_mapping(initial_permutation_ptable, _32_swap_res)
    conv_to_binary_inverse = inv_conv_to_binary(mapping_inverse)
    return conv_to_binary_inverse


"""
generate_random_table() generates a list containing numbers in a specified limit
shuffled in a random order
This function takes two values, the start and end of the values of list as argument
and returns a list as output
"""


def generate_random_table(start, end):
    permutation_table = []

    # appending values into the table ranging from start to end
    for i in range(start, end + 1):
        permutation_table.append(i)

    # shuffling the values randomly
    random.shuffle(permutation_table)
    return permutation_table


# generating permutation tables for each operations.

initial_permutation_ptable = generate_random_table(1, 64)
permutation_box_ptable = generate_random_table(1, 32)
permuted_choice_1_ptable = generate_random_table(1, 56)
permuted_choice_2_ptable = generate_random_table(1, 48)

# ------------------------------------------
"""
generating permutation table for expansion box which has numbers from 1 to 32 
with 16 of them repeated.
"""
expansion_box_ptable = generate_random_table(1, 32)
repeat_bit_list = []
while (len(repeat_bit_list) < 16):
    repeat_bit_list.append(random.randint(1, 32))
    repeat_bit_list = list(set(repeat_bit_list))
expansion_box_ptable = expansion_box_ptable + repeat_bit_list

# ------------------------------------------
""""
generating 8 s-boxes each having 4 rows and 16 columns implemented using lists with each row having 
numbers from 0 to 15 arranged in a random order. Each s-boxes are appended into a list in each 
iteration which finally produces a list of 8 s-boxes.
"""
s_boxes_list = []
for boxes in range(8):
    s_box = [generate_random_table(0, 15),
             generate_random_table(0, 15),
             generate_random_table(0, 15),
             generate_random_table(0, 15)]
    s_boxes_list.append(s_box)

encryption()
decryption()
