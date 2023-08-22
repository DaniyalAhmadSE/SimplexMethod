def get_substr(num: int):
    sub_ecs = ['\u2080', '\u2081', '\u2082', '\u2083', '\u2084',
               '\u2085', '\u2086', '\u2087', '\u2088', '\u2089']

    sub_str = ''
    if num < len(sub_ecs):
        sub_str = sub_ecs[num]
    else:
        str_i = str(num)
        for each in str_i:
            sub_str += sub_ecs[int(each)]

    return sub_str
