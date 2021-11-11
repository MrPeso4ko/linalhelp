# Простой инструмент для проведения элементарных преобразований

---

### Использование:
#### Ввод чисел
Вводим колличество строк и столбцов, затем саму матрицу:
```pycon
MxN->
>>>3 4
1 4/5 3 4
5 6 1.25 8
9 10 11 12/6
```
Доступный способ ввода чисел:
* как int: `1`
* как float: `1.5`
* как обыкновенную дробь: `8/4`

После ввода матрицы, и после каждого элементарного преобразования,
матрица выводится на экран, все числа выводятся как целые
(если возможно), или как несократимые дроби.

```pycon
1   4/5 3   4
5   6   5/4 8
9   10  11  2
```

#### Элементарные преобразования

Доступно три команды: 
1. Поменять строки местами: `s i j`
    
    Эта команда меняет строки `i` и `j` местами (здесь и далее строки
нумеруются с единицы)
```pycon
1   4/5 3   4
5   6   5/4 8
9   10  11  2
>>>s 1 2
5   6   5/4 8
1   4/5 3   4
9   10  11  2
```
2. Домножить строку на число: `m i x` 
    
    Команда домножает строку `i` на число `x`
```pycon
1   4/5 3   4
5   6   5/4 8
9   10  11  2
>>>m 1 3
3   12/5    9   12
5   6   5/4 8
9   10  11  2
>>>m 2 1/2
3   12/5    9   12
5/2 3   5/8     4
9   10  11      2
```
3. Добавить к одной строке другую с коэффициентом: `a i j x`
    
    Команда добавляет к строке `i` строку `j`, домноженную на `x`
```pycon
5   1   7   10
3   1   7   10
2   3   7   8
6   9   21  24
>>>a 1 2 -1
2   0   0   0
3   1   7   10
2   3   7   8
6   9   21  24
>>>a 3 4 -1/3
2   0   0   0
3   1   7   10
0   0   0   0
6   9   21  24
```

### TODO:
* Команду `tex` для вывода истории преобразований в LaTeX
* Команду `frac` для изменения способа вывода - обыкновенные дроби/десятичные
* Команду `undo` для отката преобразований
* Попробовать добавить поддержку символов `sympy`
