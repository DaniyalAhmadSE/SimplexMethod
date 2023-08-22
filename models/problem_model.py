from typing import List
from models.equation import Equation
from models.term import Term
from services.convert_to_sub import get_substr


class ProblemModel:
    def __init__(
        self,
        prob_eq: Equation,
        cons_eqs: List[Equation],
        dcsn_vars: List[str],
        is_max: bool,
        has_def_con: bool = True,
    ) -> None:
        self._is_max = is_max
        self._prob_eq = prob_eq
        self._cons_eqs = cons_eqs
        self._dcsn_var_names = dcsn_vars
        self._has_def_con = has_def_con
        self._slack_count = 0
        self._r_count = 0

    def get_is_max(self) -> bool:
        return self._is_max

    def set_is_max(self, is_max: bool) -> None:
        self._is_max = is_max

    def get_prob_eq(self) -> Equation:
        return self._prob_eq

    def set_prob_eq(self, prob_eq: Equation) -> None:
        self._prob_eq = prob_eq

    def get_cons_eqs(self) -> List[Equation]:
        return self._cons_eqs

    def set_cons_eqs(self, cons_eqs: List[Equation]) -> None:
        self._cons_eqs = cons_eqs

    def get_dcsn_var_names(self) -> List[str]:
        return self._dcsn_var_names

    def get_has_def_con(self) -> bool:
        return self._has_def_con

    def set_has_def_con(self, has_def_con: bool) -> None:
        self._has_def_con = has_def_con

    def get_slack_count(self) -> int:
        return self._slack_count

    def set_slack_count(self, s_count: int) -> None:
        self._slack_count = s_count

    def get_r_count(self) -> int:
        return self._r_count

    def set_r_count(self, r_count: int) -> None:
        self._r_count = r_count

    def get_dcsn_count(self) -> None:
        return len(self.dcsn_var_names)

    def add_term_to_all(self, term: Term, except_i: int, add_to_prob: bool = True) -> None:
        if add_to_prob:
            self.prob_eq.l_exp.terms.append(term)

        for i, each_ceq in enumerate(self.cons_eqs):
            if i != except_i:
                each_ceq.l_exp.terms.append(term)

    def convert_to_std(self):

        self.prob_eq.move_terms_lhs()
        all_coeffs = self.prob_eq.l_exp.coeffs + self.prob_eq.r_exp.coeffs
        for each_ceq in self.cons_eqs:
            all_coeffs = all_coeffs + each_ceq.l_exp.coeffs + \
                each_ceq.r_exp.coeffs + [each_ceq.r_exp.constant]

        all_digits = all_coeffs + (
            [self.prob_eq.l_exp.constant, self.prob_eq.r_exp.constant]
        )

        big_m = 10**(len(str(max(all_digits))) + 1)
        if not self.is_max:
            big_m *= -1

        n_cons = len(self.cons_eqs)
        for i in range(n_cons):
            self.cons_eqs[i].has_s = self.cons_eqs[i].is_ineq_gt or self.cons_eqs[i].is_ineq_lt
            self.cons_eqs[i].slack_if_valid(self.slack_count + 1)
            if self.cons_eqs[i].has_s:
                self.slack_count += 1
                self.add_term_to_all(
                    Term(0, ['S' + get_substr(self.slack_count)]), i
                )

        for i in range(n_cons):
            self.cons_eqs[i].has_r = self.cons_eqs[i].is_ineq_gt or self.cons_eqs[i].is_equal
            self.cons_eqs[i].r_if_valid(self.r_count + 1)
            if self.cons_eqs[i].has_r:
                self.r_count += 1
                self.prob_eq.l_exp.terms.append(
                    Term(big_m, ['R' + get_substr(self.r_count)])
                )
                self.add_term_to_all(
                    Term(0, ['R' + get_substr(self.r_count)]), i, False
                )
            if self.cons_eqs[i].has_s:
                self.cons_eqs[i].is_ineq_gt = False
                self.cons_eqs[i].is_ineq_lt = False

    def get_all_v_names(self):
        all_v_names = [None] * \
            (self.dcsn_count + self.slack_count + self.r_count)

        for i in range(self.dcsn_count):
            all_v_names[i] = self.dcsn_var_names[i]

        for i in range(self.slack_count):
            all_v_names[i + self.dcsn_count] = 'S' + get_substr(i + 1)

        for i in range(self.r_count):
            all_v_names[i + self.dcsn_count +
                        self.slack_count] = 'R' + get_substr(i + 1)

        return all_v_names

    def display(self, end='\n') -> None:
        if self.is_max:
            print('Max: ', end='')
        else:
            print('Min: ', end='')

        self.prob_eq.display('\n\n')
        print('Constraints:')
        for each_ceq in self.cons_eqs:
            each_ceq.display()

        if self.has_def_con:
            print()
            for i, each_dv in enumerate(self.dcsn_var_names):
                if i != 0:
                    print(', ', end='')
                print(each_dv, end='')

            print(' ≥ 0', end='')
        print(end=end)

    is_max: bool = property(get_is_max, set_is_max)
    prob_eq: Equation = property(get_prob_eq, set_prob_eq)
    cons_eqs: List[Equation] = property(get_cons_eqs, set_cons_eqs)
    dcsn_var_names: List[str] = property(get_dcsn_var_names)
    has_def_con: bool = property(
        get_has_def_con, set_has_def_con,
    )
    dcsn_count: int = property(get_dcsn_count)
    slack_count: int = property(get_slack_count, set_slack_count)
    r_count: int = property(get_r_count, set_r_count)
    all_v_names: List[str] = property(get_all_v_names)
