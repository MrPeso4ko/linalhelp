from math import gcd


class Fraction:
    def __init__(self, s=None):
        self.x = 0
        self.y = 1
        if s is None:
            pass
        elif type(s) == int:
            self.x = s
            self.y = 1
        elif type(s) == str:
            if '/' in s:
                self.x, self.y = map(int, s.split('/'))
            else:
                tmp = Fraction(float(s))
                self.x = tmp.x
                self.y = tmp.y
        elif type(s) == float:
            if int(s) == s:
                self.x = int(s)
                self.y = 1
            else:
                s = str(s)
                p = len(s) - s.find('.') - 1
                s = s.replace('.', '')
                self.x = int(s)
                self.y = 10 ** p
        elif type(s) == Fraction:
            self.x = s.x
            self.y = s.y
        else:
            assert False
        self.normalize()

    def normalize(self):
        d = gcd(self.x, self.y)
        self.x //= d
        self.y //= d
        assert self.y != 0

    def __str__(self):
        if self.y == 1:
            return str(self.x)
        else:
            return "{}/{}".format(self.x, self.y)

    def __mul__(self, other):
        res = Fraction()
        if type(other) == int or type(other) == Fraction:
            other_f = Fraction(other)
        else:
            assert False
        res.x = self.x * other_f.x
        res.y = self.y * other_f.y
        res.normalize()
        return res

    def __rmul__(self, other):
        return self * other

    def __add__(self, other):
        if type(other) == int or type(other) == Fraction:
            other_f = Fraction(other)
        else:
            assert False
        res = Fraction()
        res.y = self.y * other_f.y
        res.x = self.x * other_f.y + self.y * other_f.x
        res.normalize()
        return res

    def __radd__(self, other):
        return self + other


m, n = 0, 0
matrix = []


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
    out()
    while True:
        cmd = input("->")
        if cmd.startswith('s'):
            _, i, j = cmd.split()
            i = int(i)
            j = int(j)
            swap(i, j)
        elif cmd.startswith('q'):
            break
        elif cmd.startswith('m'):
            _, i, x = cmd.split()
            i = int(i)
            x = Fraction(x)
            mult(i, x)
        elif cmd.startswith('a'):
            _, i, j, x = cmd.split()
            i = int(i)
            j = int(j)
            x = Fraction(x)
            add(i, j, x)
        out()


if __name__ == '__main__':
    main()
