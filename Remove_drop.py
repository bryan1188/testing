import sys

def write_to_file_switcher(file_writer, line_number, string_to_write, debug_switch=False):
    if debug_switch:
        file_writer.write("Line #{}: {}".format(line_number,string_to_write))
    else:
        file_writer.write(string_to_write)

with open('SQL.txt', 'r') as f:
    write_to_file = open('output.txt','w')
    if len(sys.argv) > 1:
        debug_mode = True
    else:
        debug_mode = False
    flag = False
    line_number = 0
    for line in f:
        line_number += 1
        for word in line.split():
            if word[:2] == "--": #check the last two characters. if commented(-- is sql comment), skip line
                break
            if flag:
                if word[:2] == "--": #check the last two characters. if commented, move to next line
                    break
                if word.lower() in ['order','where']:
                    flag = False
                    write_to_file.write("\n")
                else:
                    if word[-1] == ',':
                         write_to_file_switcher(write_to_file,line_number,word[:-1] + "\n",debug_mode)
                         # write_to_file.write("Line #{}: {}".format(line_number,word[:-1] + "\n"))
                         # write_to_file.write(word[:-1] + "\n") #exclude  comma
                    elif word[-1] == ';': #(;) statement terminator
                        write_to_file_switcher(write_to_file,line_number,word[:-1] + "\n",debug_mode)
                        # write_to_file.write("Line #{}: {}".format(line_number,word[:-1] + "\n"))
                        # write_to_file.write(word[:-1] + "\n")
                        flag = False
                    else:
                        write_to_file_switcher(write_to_file,line_number,word + " ",debug_mode)
                        # write_to_file.write("Line #{}: {}".format(line_number,word + " "))
                        # write_to_file.write(word + " ")

            if word.lower() == "from":
                flag = True
            if word.lower() in ['order','where',';','for']:
                flag = False
    write_to_file.close()
