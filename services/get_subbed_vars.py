from services.convert_to_sub import get_substr


def get_subbed_vars(n_dcsn_vars, prefix='x'):
    dcsn_vars = [prefix] * n_dcsn_vars
    for i in range(n_dcsn_vars):
        if (i + 1) < 10:
            dcsn_vars[i] += get_substr(i + 1)
        else:
            str_i = str(i + 1)
            for each in str_i:
                dcsn_vars[i] += get_substr(int(each))

    return dcsn_vars
