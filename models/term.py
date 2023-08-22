from typing import List


class Term:
    def __init__(self, cof: float, v_names: List[str]) -> None:
        self._coeff: float = cof
        self._var_names: List[str] = v_names

    def get_coeff(self) -> float:
        return self._coeff

    def set_coeff(self, cof: float) -> None:
        self._coeff = cof

    def get_var_names(self) -> List[str]:
        return self._var_names

    def set_var_names(self, v_names: List[str]) -> None:
        self._var_names = v_names

    def set_var_name(self, v_name=str, i: int = 0) -> None:
        self._var_names[i] = v_name

    def get_var_name(self, i: int = 0) -> str:
        return self._var_names[i]

    def get_str(self) -> str:
        return str(self._coeff) + self._var_names

    def display(self, end: str = '\n'):
        print(str(self.coeff), end='')
        for each_vn in self.var_names:
            print('.' + each_vn, end='')
        print('', end=end)

    coeff: float = property(get_coeff, set_coeff)
    var_names: List[str] = property(get_var_names, set_var_names)
    var_name: str = property(get_var_name, set_var_name)
