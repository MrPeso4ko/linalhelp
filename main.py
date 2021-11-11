from math import gcd
from copy import deepcopy


class Fraction:
    FRAC = 0
    FLOAT = 1
    OUTPUT_MODE = FRAC
    PRECISION = 2

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
            else:
                return str(round(self.p / self.q, Fraction.PRECISION))

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


commands = ['m',
            'q',
            's',
            'a',
            'undo',
            'frac',
            'float']
m, n = 0, 0
matrix = []
m_history = []
op_history = []


def is_const(command):
    assert command in commands
    return command not in ['a', 'm', 's']


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
        print(*matrix[ind], sep='\t')


def add(i, j, x):
    global m, n, matrix
    for ind in range(n):
        matrix[i - 1][ind] += matrix[j - 1][ind] * x


def main():
    global m, n, matrix
    m, n = map(int, input("MxN->").split())
    matrix = [list(map(Fraction, input().split())) for _ in range(m)]
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
