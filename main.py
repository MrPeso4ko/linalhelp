from math import gcd
from copy import deepcopy


def lcm(a, b):
    return (a * b) // gcd(a, b)


def to_roman(data):
    ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    hunds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    thous = ["", "M", "MM", "MMM", "MMMM"]

    t = thous[data // 1000]
    h = hunds[data // 100 % 10]
    te = tens[data // 10 % 10]
    o = ones[data % 10]

    return t + h + te + o


class Fraction:
    FRAC = 0
    FLOAT = 1
    TEX = 2
    OUTPUT_MODE = FRAC
    PRECISION = 2

    def is_int(self):
        return self.q == 1

    def __init__(self, s=None):
        self.p = 0
        self.q = 1
        if s is None:
            pass
        elif type(s) == int:
            self.p = s
            self.q = 1
        elif type(s) == str:
            if '/' in s:
                self.p, self.q = map(int, s.split('/'))
            else:
                tmp = Fraction(float(s))
                self.p = tmp.p
                self.q = tmp.q
        elif type(s) == float:
            if int(s) == s:
                self.p = int(s)
                self.q = 1
            else:
                s = str(s)
                p = len(s) - s.find('.') - 1
                s = s.replace('.', '')
                self.p = int(s)
                self.q = 10 ** p
        elif type(s) == Fraction:
            self.p = s.p
            self.q = s.q
        else:
            assert False
        self.normalize()

    def normalize(self):
        d = gcd(self.p, self.q)
        self.p //= d
        self.q //= d
        assert self.q != 0

    def __str__(self):
        if self.q == 1:
            return str(self.p)
        else:
            if Fraction.OUTPUT_MODE == Fraction.FRAC:
                return "{}/{}".format(self.p, self.q)
            elif Fraction.OUTPUT_MODE == Fraction.FLOAT:
                return str(round(self.p / self.q, Fraction.PRECISION))
            elif Fraction.OUTPUT_MODE == Fraction.TEX:
                return r"\frac{" + str(self.p) + "}{" + str(self.q) + "}"
            else:
                assert False

    def __mul__(self, other):
        res = Fraction()
        other_f = Fraction(other)
        res.p = self.p * other_f.p
        res.q = self.q * other_f.q
        res.normalize()
        return res

    def __rmul__(self, other):
        return self * other

    def __add__(self, other):
        other_f = Fraction(other)
        res = Fraction()
        res.q = self.q * other_f.q
        res.p = self.p * other_f.q + self.q * other_f.p
        res.normalize()
        return res

    def __radd__(self, other):
        return self + other

    def __int__(self):
        return int(self.p / self.q)

    def __float__(self):
        return self.p / self.q

    def __lt__(self, other):
        if type(other) in (int, float):
            return float(self) < other
        elif type(other) == Fraction:
            return self.p * other.q < other.p * self.q
        else:
            assert False

    def __gt__(self, other):
        if type(other) in (int, float):
            return float(self) > other
        elif type(other) == Fraction:
            return self.p * other.q > other.p * self.q
        else:
            assert False

    def __le__(self, other):
        if type(other) in (int, float):
            return float(self) <= other
        elif type(other) == Fraction:
            return self.p * other.q <= other.p * self.q
        else:
            assert False

    def __ge__(self, other):
        if type(other) in (int, float):
            return float(self) >= other
        elif type(other) == Fraction:
            return self.p * other.q >= other.p * self.q
        else:
            assert False

    def __neg__(self):
        return -1 * self


commands = ['m',
            'q',
            's',
            'a',
            't',
            'gcd',
            'dlcm',
            'undo',
            'frac',
            'float',
            'tex']
m, n = 0, 0
matrix = []
m_history = []
op_history = []


def is_const(command):
    assert command in commands
    return command not in ['a', 'm', 's', 't']


def swap(i, j):
    global m, n, matrix
    tmp1 = list(matrix[i - 1])
    tmp2 = list(matrix[j - 1])
    for ind in range(n):
        matrix[i - 1][ind] = tmp2[ind]
        matrix[j - 1][ind] = tmp1[ind]


def mult(i, x):
    global m, n, matrix
    for ind in range(n):
        matrix[i - 1][ind] *= x


def out():
    global m, n, matrix
    for ind in range(m):
        print(ind + 1, ') ', sep='', end='\t')
        print(*matrix[ind], sep='\t')


def add(i, j, x):
    global m, n, matrix
    for ind in range(n):
        matrix[i - 1][ind] += matrix[j - 1][ind] * x


def line_gcd(i):
    global matrix, m, n
    res = 0
    for ind in range(n):
        if matrix[i - 1][ind].is_int():
            res = gcd(res, int(matrix[i - 1][ind]))
        else:
            return -1
    return res


def line_denominator_lcm(i):
    global n, m, matrix
    res = 1
    for ind in range(n):
        res = lcm(res, matrix[i - 1][ind].q)
    return res


def transp():
    global m, n, matrix
    tmp = [[] for _ in range(n)]
    for ind_x in range(m):
        for ind_y in range(n):
            tmp[ind_y].append(deepcopy(matrix[ind_x][ind_y]))
    m, n = n, m
    matrix = deepcopy(tmp)


def out_tex(filename):
    global m, n, m_history, op_history
    prev_output_mode = Fraction.OUTPUT_MODE
    Fraction.OUTPUT_MODE = Fraction.TEX
    with open(filename, 'w') as fout:
        for m_ind in range(len(m_history)):
            mat = m_history[m_ind]
            print(r"\begin{pmatrix}", file=fout)
            for ind in range(len(mat)):
                line = mat[ind]
                if ind < len(mat) - 1:
                    print(*line, sep=' & ', end=r' \\ ', file=fout)
                else:
                    print(*line, sep=' & ', file=fout)
            print(r"\end{pmatrix}", file=fout)
            if m_ind < len(op_history):
                op = op_history[m_ind]
                if op[0] == 'a':
                    _, i, j, x = op
                    i = int(i)
                    j = int(j)
                    x = Fraction(x)
                    if x > 0:
                        print(r" {} = {} + {} \cdot {} ".format(to_roman(i), to_roman(i), x, to_roman(j)), file=fout)
                    else:
                        print(r" {} = {} - {} \cdot {} ".format(to_roman(i), to_roman(i), -x, to_roman(j)), file=fout)
                elif op[0] == 'm':
                    _, i, x = op
                    i = int(i)
                    x = Fraction(x)
                    print(r" {} = {} \cdot {} ".format(to_roman(i), x, to_roman(i)), file=fout)
                elif op[0] == 't':
                    _, = op
                    print(r" \ T \  ", file=fout)
                elif op[0] == 's':
                    _, i, j = op
                    i = int(i)
                    j = int(j)
                    print(r" {} \leftrightarrow {} ".format(to_roman(i), to_roman(j)), file=fout)
                print(r" \longrightarrow ", file=fout)
    Fraction.OUTPUT_MODE = prev_output_mode


def main():
    global m, n, matrix, m_history, op_history
    m, n = map(int, input("MxN->").split())
    matrix = [list(map(Fraction, input().replace('−', '-').split())) for _ in range(m)]
    m_history.append(deepcopy(matrix))
    out()
    while True:
        cmd = input("->")
        cmd = cmd.split()
        if cmd[0] in commands:
            try:
                if cmd[0] == 's':
                    _, i, j = cmd
                    i = int(i)
                    j = int(j)
                    swap(i, j)
                elif cmd[0] == 'q':
                    _, = cmd
                    break
                elif cmd[0] == 'm':
                    _, i, x = cmd
                    i = int(i)
                    x = Fraction(x)
                    mult(i, x)
                elif cmd[0] == 'a':
                    _, i, j, x = cmd
                    i = int(i)
                    j = int(j)
                    x = Fraction(x)
                    add(i, j, x)
                elif cmd[0] == 't':
                    _, = cmd
                    transp()
                elif cmd[0] == 'gcd':
                    _, i = cmd
                    i = int(i)
                    res = line_gcd(i)
                    if res != -1:
                        print("gcd of line {}: {}".format(i, line_gcd(i)))
                    else:
                        print("Невозможно посчитать gcd")
                elif cmd[0] == 'dlcm':
                    _, i = cmd
                    i = int(i)
                    print("denominator lcm of line {}: {}".format(i, line_denominator_lcm(i)))
                elif cmd[0] == 'undo':
                    _, = cmd
                    if len(op_history) > 0:
                        op_history.pop()
                        m_history.pop()
                        matrix = deepcopy(m_history[-1])
                    else:
                        print("Нет операций для отката")
                elif cmd[0] == 'frac':
                    _, = cmd
                    Fraction.OUTPUT_MODE = Fraction.FRAC
                elif cmd[0] == 'float':
                    _, p = cmd
                    p = int(p)
                    Fraction.OUTPUT_MODE = Fraction.FLOAT
                    Fraction.PRECISION = p
                elif cmd[0] == 'tex':
                    _, filename = cmd
                    out_tex(filename)
            except ValueError:
                print("Неверно введены аргументы")
            except IndexError:
                print("Неверно введены индексы")
            else:
                if not is_const(cmd[0]):
                    m_history.append(deepcopy(matrix))
                    op_history.append(deepcopy(cmd))
        else:
            print("Некорректная команда")
        out()


if __name__ == '__main__':
    main()
