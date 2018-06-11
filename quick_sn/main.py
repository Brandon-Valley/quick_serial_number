

import logger

EXAMPLE_SN = '0243 8405 0296 3935 9212 2008'
BOX_NAME_IDENTIFIER = 'BOXNAME'
SN2_IDENTIFIER = 'SN2'






def read_text_file(file_path):
    with open(file_path) as text_file:  # can throw FileNotFoundError
        result = tuple(l.rstrip() for l in text_file.readlines())
        return result


#makes broken up list of strings into one big string
def format_data(data):
    formatted_data = ''
    
    try:
        for data_line in data:
            if data_line != '':
                if data_line[0] == ' ' or formatted_data == '':
                    formatted_data += data_line
                else:
                    formatted_data += ' ' + data_line
        return formatted_data
    except:
        raise Exception('ERROR  You probably have some extra lines of spaces in your data text file')




def valid_sn(pot_sn):
    if len(pot_sn) != len(EXAMPLE_SN):
        return False

    for char_num in range(len(pot_sn)):
        cur_char = pot_sn[char_num]

        if cur_char.isdigit() == False and cur_char != ' ':
            return False

        if cur_char.isdigit() != EXAMPLE_SN[char_num].isdigit():
            return False
    return True





#old-------------------------------------------------------------------
def build_sn_list(in_str):
    sn_list = []
    for char_num in range(len(in_str)):
        char = in_str[char_num]
        if char.isdigit() and ( len(in_str) - char_num ) >= len(EXAMPLE_SN):
            potential_sn = in_str[char_num : char_num + len(EXAMPLE_SN)]
            if valid_sn(potential_sn):
                sn_list.append(potential_sn)
    return sn_list
#old------------------------------------------------------------------


#old
def box_name_id_found(first_char_pos, input_str):
    if first_char_pos + len(BOX_NAME_IDENTIFIER) <= len(input_str):
        possable_box_name_id = input_str[first_char_pos: first_char_pos + len(BOX_NAME_IDENTIFIER)]
        if possable_box_name_id == BOX_NAME_IDENTIFIER:
            return True
    return False


def identifier_found(first_char_pos, input_str, identifier):
    if first_char_pos + len(BOX_NAME_IDENTIFIER) <= len(input_str):
        possable_box_name_id = input_str[first_char_pos: first_char_pos + len(identifier)]
        if possable_box_name_id == identifier:
            return True
    return False



def between_prnths(first_prnth_pos, in_string):
    b_str = ''
    cur_char_num = first_prnth_pos + 1
    while(in_string[cur_char_num] != ')'):
        b_str += in_string[cur_char_num]
        cur_char_num += 1

    #if b_str[0:2] == 'ox':#if len(b_str) != 0:
        #return b_str[3:] #bad code, im lazy
    return b_str



#txt file must start with box name
def build_sn_ll(in_str):
    #print('in ll !!!!!!!!!!!!!!!!!!')#``````````````````````````````````````````````````````````````````
    sn_ll = []

    for char_num in range(len(in_str)):
        char = in_str[char_num]

        if char == BOX_NAME_IDENTIFIER[0]:
            if identifier_found(char_num, in_str, BOX_NAME_IDENTIFIER) == True: #            if box_name_id_found(char_num, in_str) == True:
                #print('box_name id found!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')#`````````````````````````````````````````````
                prnth_start_char_num = char_num + len(BOX_NAME_IDENTIFIER)
                box_name = between_prnths(prnth_start_char_num, in_str)
                #print('box_name:', box_name)#``````````````````````````````````````````````````````````````````````````````````````````````````
                sn_ll.append([box_name])
                '''
        elif char == SN2_IDENTIFIER[0]:
            if identifier_found(char_num, in_str, SN2_IDENTIFIER) == True:
                prnth_start_char_num = char_num + len(SN2_IDENTIFIER)
                sn2 = between_prnths(prnth_start_char_num, in_str)
                sn_ll[len(sn_ll) - 1].append(sn2)
                '''
        elif char.isdigit() and ( len(in_str) - char_num ) >= len(EXAMPLE_SN):
            potential_sn = in_str[char_num : char_num + len(EXAMPLE_SN)]
            if valid_sn(potential_sn):
                #print('  sn_ll: ', sn_ll)#`````````````````````````````````````````````````````````````
                #print('     len(sn_ll): ', len(sn_ll))#``````````````````````````````````````````````````````````
                #print('        sn_ll[len(sn_ll)]: ', sn_ll[len(sn_ll) - 1])#```````````````````````````````````
                #print('          sn_ll[0]: ', sn_ll[0])#`````````````````````````````````````````````````````````````
                sn_ll[len(sn_ll) - 1].append(potential_sn)
    return sn_ll




def make_log_dict_list(serial_number_ll):
    log_dl = []
    something_added = True
    pos = 1

    while(something_added == True):
        print('top of loop,   pos: ', pos)#``````````````````````````````````````````````````````````
        something_added = False
        log_dict = {}
        for box_list in serial_number_ll:
            if pos < len(box_list):
                log_dict[box_list[0]] = box_list[pos]
                something_added = True
        log_dl.append(log_dict)
        pos += 1
    return log_dl






CSV_FILENAME = 'output.csv'
INPUT_FILE_NAME = 'input.txt'
NEW_BOX_STR = 'NEWBOX'
#need to split up by newbox
#need to get name of box
#need to make csv

input_tup = read_text_file(INPUT_FILE_NAME)
print(input_tup)

input_str = format_data(input_tup)
print(input_str)

print('')


serial_num_ll = build_sn_ll(input_str)
print(serial_num_ll)
print('')

log_dict_list = make_log_dict_list(serial_num_ll)
print(log_dict_list)
print('')

logger.logList(log_dict_list, CSV_FILENAME)

print('done')