def quit_or_back(usr_inp: str):

    result = None

    if usr_inp != '':
        if usr_inp.lower() == 'q':
            result = True
        elif usr_inp.lower() == 'b':
            result = False

    return result


print(quit_or_back(''))
