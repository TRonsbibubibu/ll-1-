def is_final_char(c):
    return not c.isupper()


def get_last_uti(char, str):
    for i in range(len(str)-1, -1, -1):
        if str[i] == char:
            return (True, str[i+1:i+2])
    return (False, str)