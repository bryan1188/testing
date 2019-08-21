'''
    Get all the columns in where clause and write to output_columns_in_where.txt file

'''
from Utilities import unpack_select_from_elements


def util_trim_comma(input_string):
    '''
        this utility will check if it has comma at the end, then trim comma
    '''
    # strip string for trailing spaces
    input_string = input_string.strip()

    if input_string[-1] == ',':
        # comma found
        input_string = input_string[:-1] #remove last character which is comma
        input_string = input_string.strip() # do another stripping
    return input_string

def process_word(**kwargs):
    '''
        function to process the word read from input stream and add to the list (based on the input)
        accepted paramaters:
            object_list - either it is select_columns, where_columns, from_tables, etc.
            word - word to be processed
            flag_dict - check if a separator was found
    '''
    object_list = kwargs.get('object_list', None)
    word = kwargs.get('word', None)
    flag_dict = kwargs.get('flag_dict', None)
    if object_list:
        #list not empty
        if not flag_dict['separator_found_flag']:
            if ',' not in word:
                # for aliased column
                # append the word to the last element
                object_list[-1] = "{} {}".format(object_list[-1],word)
            else:
                # comma found
                object_list[-1] = "{} {}".format(object_list[-1],word)
                flag_dict['separator_found_flag'] = True
        else:
            object_list.append(word)
            if ',' not in word:
                flag_dict['separator_found_flag'] = False
    else:
        object_list.append(word)

def process_collection(**kwargs):
    '''
        do some processing on the collection lists
        this will be executed after statement terminator is found
        expected arguments:
            select_columns - list of the columns in select
            from_tables - list of tables in from clause
            where_columns - list of columns used in where clause
        return value:

    '''
    select_columns = kwargs.get('select_columns', None)
    where_columns = kwargs.get('where_columns', None)
    from_tables = kwargs.get('from_tables', None)

    #process from_tables
    from_tables_dict_list = list()
    '''
        dictionary format:
            {
                'table_name': <name of table>,
                'table_alias': <alias(if any, else None)>
            }
    '''
    for table in from_tables:
        pass

    #process select_columns
    select_columns_dict_list = list()
    '''
        dictionary format:
            {
                'column_full_name': <column_full_name_as_specfied>,
                'column_name': <name of column>,
                'alias': <alias(empty if alias not use)>,
                'table': <from_what_table(empty if not provided in sql)
            }
    '''
    for column in select_columns:
        select_columns_dict = dict()
        if len(column.split()) == 3:
            # column has alias
            select_columns_dict['column_name'] = column.split()[0]
            select_columns_dict['alias'] = util_trim_comma(column.split()[-1])
        else:
            select_columns_dict['column_name'] = util_trim_comma(column.split()[0])
            select_columns_dict['alias'] = None

        #check for table
        #add logic for aliased table
        if len(select_columns_dict['column_name'].split('.')) > 1:
            # table is specified in column name

            select_columns_dict['column_full_name'] = select_columns_dict['column_name']
            select_columns_dict['column_name'] = select_columns_dict['column_name'].split('.')[-1]

            #remove the column name to get table name
            select_columns_dict['table'] = select_columns_dict['column_full_name'][:(
                    len(select_columns_dict['column_full_name']) - len(select_columns_dict['column_name']) - 1
                    )]

            #logic for alias tabled will be added here....
        else:
            select_columns_dict['table'] = None

        select_columns_dict_list.append(select_columns_dict)

    print('''
        select_columns_orig: {}
        select_columns: {}
        tables: {}
    '''.format(select_columns,select_columns_dict_list,from_tables)
    )
    # empty collections
    select_columns.clear()
    where_columns.clear()
    from_tables.clear()

def process_collection_(**kwargs):
    '''
        temporary function
    '''
    select_clause = kwargs.get('select_clause',None)
    select_columns = unpack_select_from_elements(clause_string=select_clause)
    from_clause = kwargs.get('from_clause', None)
    from_tables = unpack_select_from_elements(clause_string=from_clause)
    print('''
        select clause: {}
        from clause: {}
        '''.format(select_columns,from_tables))

with open('input_columns_in_where.txt', 'r') as f:
    # write_to_file = open('output_columns_in_where.txt')
    select_columns = list()
    where_columns = list()
    from_tables = list()
    select_clause = ''
    from_clause = ''
    current_sql_clause = None
    flag_dict = dict()
    flag_dict['separator_found_flag'] = False
    flag_dict['statement_terminator_found_flag'] = False
    flag_dict['beginning_flag'] = True
    flag_dict['last_word_is_keyword'] = False
    SQL_CLAUSE_KEYWORDS = ('SELECT','FROM','WHERE','GROUP','ORDER') #get only the first word
    for line in f: # check every line from input file
        for word in line.split(): #check every word in line
            if word[:2] == '--':
                # comment found, move to next line
                break

            #check for keyword
            if word.upper() in SQL_CLAUSE_KEYWORDS:
                # keword found
                flag_dict['separator_found_flag'] = False
                flag_dict['last_word_is_keyword'] = True
                current_sql_clause = word.upper()
                if word.upper() == 'SELECT' and not flag_dict['beginning_flag']:
                    process_collection(
                        select_columns = unpack_select_from_elements(clause_string=select_clause),
                        from_tables = unpack_select_from_elements(clause_string=from_clause),
                        where_columns=where_columns
                    )
                    # process_collection(select_clause=select_clause,from_clause=from_clause)
                continue
            else:
                flag_dict['last_word_is_keyword'] = False

            if current_sql_clause:
                if current_sql_clause == 'SELECT':
                    select_clause = ' '.join([select_clause, word])
                if current_sql_clause == 'FROM':
                    from_clause = ' '.join([from_clause, word])
                if current_sql_clause == 'WHERE':
                    where_columns.append(word)
                if flag_dict['statement_terminator_found_flag'] \
                    and not flag_dict['beginning_flag']:
                    #end of statement. do some processing
                    flag_dict['statement_terminator_found_flag'] = False
            flag_dict['beginning_flag'] = False

    process_collection(
        select_columns=select_columns,
        from_tables=from_tables,
        where_columns=where_columns
    )
    # print('''
    #     Select columns: {}
    # '''.format(select_columns))
