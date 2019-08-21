with open('SQL.txt', 'r') as f:
    write_to_file = open('output_changes.txt','w')
    line_number = 0
    exception = ['DW_UPDATE_LOG']
    for line in f:
        flag = False
        line_number += 1
        word_counter = 0
        for word in line.split():
            word_counter += 1
            if word_counter == 1 and word[:2] == "--": #check the last two characters. if commented, move to next line
                break
            if word.upper() in ['UPDATE','INSERT','DELETE','TRUNCATE', 'DROP']: # check for change keyword
                flag = True
            if word.upper() in exception: #if exceptio found do not include
                flag = False
        if flag:
            write_to_file.write("Line number {}: {}".format(line_number,line))
    write_to_file.close()
