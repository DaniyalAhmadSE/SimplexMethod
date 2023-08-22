from typing import List
from models.equation import Equation
from models.expression import Expression
from models.term import Term
from services.get_subbed_vars import get_subbed_vars
from services.quit_or_back import quit_or_back

prob_var = 'z'
n_dvs: int = 0
n_cons: int = 0
dcsn_vars: List[str] = []
prob_eq: Equation
obj_terms: List[Term] = []
cons_eqs: List[Equation] = []


def menu_det_cons(i_con=0, i_cdv_init=0):
    qb_d_cons = None
    while qb_d_cons is None:
        while i_con < n_cons:
            con_terms: List[Term] = [0]*n_dvs

            print(
                f"Enter details of Constraint {str(i_con + 1)}\n\n"
                "Enter the coefficients of variables: "
            )
            qb_cv_cons = None
            while qb_cv_cons is None:
                i_cdv = i_cdv_init
                while i_cdv < n_dvs:
                    con_term_str = input(
                        dcsn_vars[i_cdv] + ': '
                    )

                    qb_cv_cons = quit_or_back(con_term_str)

                    if qb_cv_cons:
                        print('Quitting...')
                        raise SystemExit
                    elif qb_cv_cons is False:
                        print('Going Back...')
                        if i_cdv == 0:
                            menu_cv_of(i_ofdv=n_dvs)
                            break
                        i_cdv -= 1
                        i_con -= 2
                        continue
                    else:
                        try:
                            con_term = int(con_term_str)
                        except ValueError:
                            print('Invalid Input')
                            qb_cv_cons = None
                            continue

                        con_terms[i_cdv] = Term(
                            con_term, [dcsn_vars[i_cdv]]
                        )
                    i_cdv += 1
                if i_cdv == 0:
                    continue


def menu_cv_of(i_ofdv=0):
    qb_cv_of = None
    s_p = 's' if i_ofdv == 0 else ''
    while qb_cv_of is None:
        print(
            "\nEnter the coefficient" + s_p + " of variable"
            + s_p + "in the objective function: "
        )
        while i_ofdv < n_dvs:
            term_i_str = input(dcsn_vars[i_ofdv] + ': ')
            qb_cv_of = quit_or_back(term_i_str)

            if qb_cv_of is True:
                print('Quitting...')
                raise SystemExit
            elif qb_cv_of is False:
                print('Going Back...')
                if i_ofdv == 0:
                    menu_n_cons()
                    return
                i_ofdv -= 1
                continue
            else:
                try:
                    term_i = int(term_i_str)
                except ValueError:
                    print('Invalid Input')
                    qb_cv_of = None
                    continue
                obj_terms[i_ofdv] = Term(
                    term_i, [dcsn_vars[i_ofdv]]
                )
            i_ofdv += 1

    prob_eq = Equation(
        Expression([Term(1, [prob_var])]),
        Expression(obj_terms),
        has_z=True
    )
    menu_det_cons()


def menu_n_cons():
    qb_n_con = None
    while qb_n_con is None:

        n_cons_str = input('Enter Number of Constraints: ')
        qb_n_con = quit_or_back(n_cons_str)

        if qb_n_con is True:
            print('Quitting...')
            raise SystemExit
        elif qb_n_con is False:
            menu_n_dvs()
            return
        else:
            try:
                n_cons = int(n_cons_str)
            except ValueError:
                print('Invalid Input')
                continue
            cons_eqs: List[Equation] = [0]*n_cons
            menu_cv_of()


def menu_n_dvs():
    qb_dv = None
    while qb_dv is None:
        n_dvs_str = input('Enter Number of Decision Variables: ')
        qb_dv = quit_or_back(n_dvs_str)

        if qb_dv is True:
            print('Quitting...')
            raise SystemExit
        elif qb_dv is False:
            menu_init()
            return
        else:
            try:
                n_dvs = int(n_dvs_str)
            except ValueError:
                print('Invalid Input')
                continue
            dcsn_vars: List[str] = get_subbed_vars(n_dvs)
            obj_terms: List[Term] = [0]*n_dvs
            menu_n_cons()


def menu_init():
    qb_init = None
    while qb_init is None:
        print(
            "Welcome to SOLVEX v1.0\n\n"
            "Tip: Enter q at any point to quit\n"
            "Tip: Enter b at any point to go 1 step back\n"
            "Tip: Enter r at any point to restart\n"
        )
        init_input = input('Enter any other to start calculation: ')

        if init_input is True:
            print('Quitting...')
            return
        elif init_input is False:
            print('Restarting...\n')
            qb_init = None
            continue
        else:
            menu_n_dvs()


menu_init()
