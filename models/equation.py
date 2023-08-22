from models.expression import Expression
from models.term import Term
from services.convert_to_sub import get_substr


class Equation:
    def __init__(
        self,
        l_exp: Expression,
        r_exp: Expression,
        is_ineq_gt: bool = False,
        is_ineq_lt: bool = False,
        has_z: bool = False,
    ) -> None:
        self._l_exp = l_exp
        self._r_exp = r_exp
        self._is_ineq_gt = is_ineq_gt
        self._is_ineq_lt = is_ineq_lt
        self._has_z = has_z
        self._has_r = False
        self._has_s = False

    def get_l_exp(self) -> Expression:
        return self._l_exp

    def set_l_exp(self, l_exp: Expression) -> None:
        self._l_exp = l_exp

    def get_r_exp(self) -> Expression:
        return self._r_exp

    def set_r_exp(self, r_exp: Expression) -> None:
        self._r_exp = r_exp

    def get_is_ineq_gt(self):
        return self._is_ineq_gt

    def set_is_ineq_gt(self, is_ineq_gt: bool) -> None:
        self._is_ineq_gt = is_ineq_gt

    def get_is_ineq_lt(self):
        return self._is_ineq_lt

    def set_is_ineq_lt(self, is_ineq_lt: bool) -> None:
        self._is_ineq_lt = is_ineq_lt

    def get_has_z(self) -> bool:
        return (self.l_exp.has_z or self.r_exp.has_z)

    def get_has_r(self) -> bool:
        return self._has_r

    def set_has_r(self, has_r: bool) -> None:
        self._has_r = has_r

    def get_has_s(self) -> bool:
        return self._has_s

    def set_has_s(self, has_s: bool) -> None:
        self._has_s = has_s

    def get_is_equal(self) -> bool:
        return not (self.is_ineq_gt or self.is_ineq_lt)

    def move_terms_lhs(self):
        n_terms = len(self.r_exp.terms)

        if n_terms > 0:
            shifted_terms = [None] * n_terms

            for i, each_t in enumerate(self.r_exp.terms):
                shifted_terms[i] = Term(each_t.coeff * -1, each_t.var_names)

            self.l_exp.terms.extend(shifted_terms)
            self.r_exp.terms = []

            return True

        return False

    def slack_if_valid(self, slack_num: int):
        if self.is_ineq_lt:
            self.l_exp.terms.append(
                Term(1, ['S' + get_substr(slack_num)])
            )
        elif self.is_ineq_gt:
            self.l_exp.terms.append(
                Term(-1, ['S' + get_substr(slack_num)])
            )

    def r_if_valid(self, r_num: int):
        if self.is_equal:
            self.l_exp.terms.append(
                Term(1, ['R' + get_substr(r_num)])
            )
        elif self.is_ineq_gt:
            self.l_exp.terms.append(
                Term(1, ['R' + get_substr(r_num)])
            )

    def display(self, end='\n') -> None:
        self.l_exp.display(end='')

        if self.is_ineq_gt:
            print(' ≥ ', end='')
        elif self.is_ineq_lt:
            print(' ≤ ', end='')
        else:
            print(' = ', end='')

        self.r_exp.display(end='')

        print('', end=end)

    l_exp: Expression = property(get_l_exp, set_l_exp)
    r_exp: Expression = property(get_r_exp, set_r_exp)

    is_ineq_gt: bool = property(get_is_ineq_gt, set_is_ineq_gt)
    is_ineq_lt: bool = property(get_is_ineq_lt, set_is_ineq_lt)

    has_z: bool = property(get_has_z)
    has_r: bool = property(get_has_r, set_has_r)
    has_s: bool = property(get_has_s, set_has_s)

    is_equal: bool = property(get_is_equal)
