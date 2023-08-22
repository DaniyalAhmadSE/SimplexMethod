from typing import List
from models.equation import Equation
from models.expression import Expression
from models.problem_model import ProblemModel
from models.simplex_api import SimplexAPI
from models.term import Term
from services.get_subbed_vars import get_subbed_vars
from services.quit_or_back import quit_or_back


def main():

    prob_var = 'z'
    n_dvs: int = 0
    n_cons: int = 0
    dcsn_vars: List[str] = []
    prob_eq: Equation
    obj_terms: List[Term] = []
    cons_eqs: List[Equation] = []
    prob_var = 'z'
    qb_dv = None
    while qb_dv is not True:
        n_dcsn_vars_str = input('Enter Number of Decision Variables: ')
        qb_dv = quit_or_back(n_dcsn_vars_str)

        if qb_dv is True:
            print('Quitting...')
            break
        elif qb_dv is False:
            print('Restarting...')
            continue

        else:
            try:
                n_dvs = int(n_dcsn_vars_str)
            except ValueError:
                print('Invalid Input')
                qb_dv = None
                continue

            dcsn_vars = get_subbed_vars(n_dvs)
            obj_terms: List[Term] = [None]*n_dvs

            qb_n_con = None
            while qb_n_con is None:

                n_constraints_str = input('Enter Number of Constraints: ')
                qb_n_con = quit_or_back(n_constraints_str)

                if qb_n_con is True:
                    print('Quitting...')
                    raise SystemExit
                elif qb_n_con is False:
                    continue
                else:
                    try:
                        n_cons = int(n_constraints_str)
                    except ValueError:
                        print('Invalid Input')
                        qb_dv = None
                        continue

                    cons_eqs: List[Equation] = [0]*n_cons

                    qb_cv_of = None
                    i_ofdv = 0
                    while qb_cv_of is None:
                        print(
                            "\nEnter the coefficients of variables in the objective function: "
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
                                    break
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
                        if i_ofdv == 0:
                            continue

                        prob_eq = Equation(
                            Expression([Term(1, [prob_var])]),
                            Expression(obj_terms),
                            has_z=True
                        )

                        i_con = 0
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
                                    i_cdv = 0
                                    while i_cdv < n_dvs:
                                        con_term_str = input(
                                            dcsn_vars[i_cdv] + ': '
                                        )

                                        qb_cv_cons = quit_or_back(con_term_str)

                                        if qb_cv_cons is True:
                                            print('Quitting...')
                                            raise SystemExit
                                        elif qb_cv_cons is False:
                                            print('Going Back...')
                                            if i_cdv == 0:
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

                                    print(
                                        "Enter 1 for ' ≤ '\n"
                                        "Enter 2 for ' ≥ '\n"
                                        "Enter 3 for ' = '\n"
                                    )
                                    eq_input = int(
                                        input("Enter your choice: "))

                                    e_gt = False
                                    e_lt = False
                                    if eq_input == 1:
                                        e_lt = True
                                    elif eq_input == 2:
                                        e_gt = True

                                    cons_eqs[i_con] = Equation(
                                        Expression(con_terms),
                                        Expression(
                                            [], int(input('Enter constant: '))),
                                        is_ineq_gt=e_gt,
                                        is_ineq_lt=e_lt
                                    )

                            print(
                                "Enter 1 for Maximization\n"
                                "Enter 2 for Minimization\n"
                            )
                            min_max_input = int(input('Enter your choice: '))

                            problem_model = ProblemModel(
                                prob_eq, cons_eqs, dcsn_vars, is_max=(
                                    min_max_input == 1)
                            )

                            simplex_ui = SimplexAPI(problem_model)
                            simplex_ui.solve()

    return None


if __name__ == "__main__":
    main()
