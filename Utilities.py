def unpack_select_from_elements(**kwargs):
    '''
        unpack the string from select clause then return a list of columns
        required paramater:
            clause_string
        return value:
            list of columns
    '''
    return_list = list()
    clause_string = kwargs.get('clause_string', None)
    if clause_string:
        return_list = [ column.strip() for column in clause_string.split(',')]
    return return_list
