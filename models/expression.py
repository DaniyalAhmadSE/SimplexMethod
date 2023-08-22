from typing import List

from models.term import Term


class Expression:
    def __init__(
        self,
        terms: List[Term],
        const: float = 0,
    ) -> None:
        self._terms = terms
        self._constant = const

    def get_terms(self) -> List[Term]:
        return self._terms

    def set_terms(self, terms: List[float]) -> None:
        self._terms = terms

    def get_constant(self) -> float:
        return self._constant

    def set_constant(self, const: float) -> None:
        self._constant = const

    def get_term(self, i: int) -> Term:
        return self._terms[i]

    def set_term(self, term: float, i: int) -> None:
        self._terms[i] = term

    def get_has_z(self) -> bool:
        for each_t in self.terms:
            if each_t.var_name == 'z':
                return True
        return False

    def get_has_var(self) -> bool:
        return len(self.terms) > 0

    def get_coeffs(self) -> List[float]:
        return [each_t.coeff for each_t in self.terms]

    def get_last_non_zero_term(self):
        for each_t in reversed(self.terms):
            if each_t.coeff != 0:
                return each_t

    def get_coeff_of(self, v_name: str):
        for each_t in self.terms:
            if each_t.var_name == v_name:
                return each_t.coeff
        return 0

    def display(self, end='\n') -> None:
        for i, each_t in enumerate(self.terms):
            to_print = ''
            if each_t.coeff >= 0:
                to_print = ' +'
                if i == 0:
                    to_print = ' '
            else:
                to_print = ' '
            print(to_print, end='')
            each_t.display(end='')

        if len(self.terms) > 0 and self.constant > 0:
            print(' +', end='')

        if self.constant != 0 or len(self.terms) == 0:
            print(self.constant, end='')

        print('', end=end)

    terms: List[Term] = property(get_terms, set_terms)
    constant: float = property(get_constant, set_constant)
    has_z: bool = property(get_has_z)
    has_var: bool = property(get_has_var)
    coeffs: List[float] = property(get_coeffs)
    last_non_zero_term: Term = property(get_last_non_zero_term)
