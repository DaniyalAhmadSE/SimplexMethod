from typing import List
from models.problem_model import ProblemModel
from services.convert_to_sub import get_substr


class SimplexAPI:
    def __init__(self, prob: ProblemModel) -> None:
        self._prob: ProblemModel = prob
        self._mat: List[List[float]] = [[]]

    def get_prob(self) -> ProblemModel:
        return self._prob

    def get_mat(self):
        return self._mat

    def set_mat(self, mat: List[List[float]]) -> None:
        self._mat = mat

    def get_basic_vns(self):
        cons_count = len(self.prob.cons_eqs)
        cons_last_v_names = [None] * cons_count
        for i in range(cons_count):
            cons_last_v_names[i] = self.prob.cons_eqs[i].l_exp.last_non_zero_term.var_name

        return cons_last_v_names

    def init_matrix(self) -> ProblemModel:

        n_cols_nc = self.prob.dcsn_count + self.prob.slack_count + self.prob.r_count
        n_cols = n_cols_nc + 1

        basic_count = len(self.prob.cons_eqs)

        self.mat = [
            [0 for _ in range(n_cols)]
            for _ in range(basic_count + 1)
        ]

        basic_vns = self.basic_vns
        non_basic_vns = [
            x for x in self.prob.all_v_names if x not in basic_vns
        ]

        col_names = non_basic_vns + basic_vns

        for i in range(n_cols_nc):
            self.mat[0][i] = self.prob.prob_eq.l_exp.get_coeff_of(
                col_names[i]
            )
        self.mat[0][-1] = self.prob.prob_eq.r_exp.constant

        for i, each_ceq in enumerate(self.prob.cons_eqs, 1):
            for j in range(n_cols_nc):
                self.mat[i][j] = each_ceq.l_exp.get_coeff_of(
                    col_names[j]
                )
            self.mat[i][-1] = each_ceq.r_exp.constant

        basic_cs = n_cols_nc - (basic_count)
        for i in range(basic_cs, n_cols_nc):
            if self.mat[0][i] != 0:
                new_z_r = [0]*n_cols
                tar_row = self.mat[i - basic_cs + 1]
                for j, each in enumerate(tar_row):
                    new_z_r[j] = self.mat[0][j] - (self.mat[0][i] * each)
                self.mat[0] = new_z_r

    def display_mat(self):
        for row in self.mat:
            for each in row:
                sym_spc = ''
                if each >= 0:
                    sym_spc = ' '
                print(sym_spc + str(round(each, 1)), end=' ')
            print()
            # if i == 0:
            #     print('____________________________________')
        print()

    def get_is_optimal(self):
        for each in self.mat[0][:-1]:
            if self.prob.is_max:
                if each < 0:
                    return False
            else:
                if each > 0:
                    return False
        return True

    def get_entering_ci(self) -> int:
        if self.is_optimal:
            raise Exception("Optimal solution has been found already")

        entering = self.mat[0][0]
        index = 0

        for i, each in enumerate(self.mat[0][:-1]):
            if self.prob.is_max:
                if each < entering and each < 0:
                    entering = each
                    index = i
            else:
                if each > entering and each > 0:
                    entering = each
                    index = i

        return index

    def get_leaving_ri(self, e_ci: int):
        ratios = [None]*(len(self.mat) - 1)

        for i, row in enumerate(self.mat[1:], 1):
            divisor = self.mat[i][e_ci]

            if divisor != 0:
                ratios[i - 1] = row[-1] / divisor
            else:
                ratios[i - 1] = -1

        min_r = None
        index = 0

        for i, each_r in enumerate(ratios, 1):
            if each_r >= 0:
                if min_r is None or each_r < min_r:
                    min_r = each_r
                    index = i

        # print('Min R  : ' + str(min_r))
        return index

    def iter_till_opt(self, display: bool = True):
        e_cis = []
        l_ris = []
        while not self.is_optimal:
            n_items = len(self.mat[0])

            e_ci = self.entering_ci
            e_cis.append(e_ci)
            print('E_CI   : ' + str(e_ci))

            l_ri = self.get_leaving_ri(e_ci)
            l_ris.append(l_ri)
            print('L_RI   : ' + str(l_ri), end='\n\n')

            pr_rep = [None] * n_items

            for i, each in enumerate(self.mat[l_ri]):
                pr_rep[i] = each / self.mat[l_ri][e_ci]

            self.mat[l_ri] = pr_rep

            for i, row in enumerate(self.mat):
                new_row = [None] * n_items
                pcc = row[e_ci]
                if i != l_ri:
                    for j, each in enumerate(row):
                        new_row[j] = each - (pcc * pr_rep[j])
                    self.mat[i] = new_row

            if display:
                self.display_mat()
                # input('Press Enter to continue...')

        return [e_cis, l_ris]

    def solve(self):

        self.prob.display()

        self.prob.convert_to_std()

        self.prob.display()

        self.init_matrix()

        self.display_mat()

        [e_cis, l_ris] = self.iter_till_opt()

        self.print_solution(e_cis, l_ris)

    def print_solution(self, e_cis: List[int], l_ris: List[int]):
        sol_c = [None] * len(self.mat)

        for i, row in enumerate(self.mat):
            sol_c[i] = row[-1]

        z = sol_c[0]
        dcsns = [[None, 0] for _ in range(len(self.prob.dcsn_var_names))]
        for i, dcsn_v in enumerate(self.prob.dcsn_var_names):
            dcsns[i][0] = dcsn_v

        for i, eci in enumerate(e_cis):
            dcsns[eci][1] = sol_c[l_ris[i]]

        s_count = self.prob.slack_count
        slacks = [[None, 0] for _ in range(s_count)]

        for each in range(1, s_count + 1):
            if each != 0 and each not in l_ris:
                slacks[each - 1][0] = 'S' + get_substr(each)
                slacks[each - 1][1] = sol_c[each]

        print("Optimal Solution:\n")
        if self.prob.is_max:
            print(f"    Max: Z = {str(z)}")
        else:
            print(f"    Min: Z = {str(z)}")
        print("\nfor:\n")

        for i, each in enumerate(dcsns):
            com = '    '
            if i != 0:
                com = ', '

            print(com + each[0] + ' = ' + str(round(each[1], 1)), end='')

        print('\n')

        i = 0
        for each in slacks:
            if each[0] is not None:
                com = '    '
                if i != 0:
                    com = ', '
                print(com + each[0] + ' = ' + str(round(each[1], 1)), end='')
                i += 1
        print('\n')

    prob: ProblemModel = property(get_prob)
    mat: List[List[float]] = property(get_mat, set_mat)
    is_optimal: bool = property(get_is_optimal)
    entering_ci: int = property(get_entering_ci)
    basic_vns: List[str] = property(get_basic_vns)
