# listwalker
A tool for traversing multi-dimensional lists in Python.

### Installation
```bash
pip install --upgrade listwalker
```

### Examples
```py
from listwalker import ListWalker2D

walker2D = ListWalker2D[int]([
	[1, 2, 3, 4, 5],
	[6, 7, 8, 9, 10],
	[11, 12, 13, 14, 15],
	[16, 17, 18, 19, 20],
	[21, 22, 23, 24, 25],
	[26, 27, 28, 29, 30]
])  # The cursor is at 1

walker2D.walk_down()  # The cursor is at 6
walker2D.walk_down()  # The cursor is at 11
walker2D.walk_down()  # The cursor is at 16
walker2D.walk_right()  # The cursor is at 17

print(walker2D.cursor_element.value)  # -> 17
print(walker2D.get_neighbors())
# {
# 	'up': ListWalkerElement(12),
# 	'right': ListWalkerElement(18),
# 	'down': ListWalkerElement(22),
# 	'left': ListWalkerElement(16)
# }

walker2D.print()
# +---+----+--------+----+----+----+
# |   | 0  |   1    | 2  | 3  | 4  |
# +---+----+--------+----+----+----+
# | 0 | 1  |   2    | 3  | 4  | 5  |
# | 1 | 6  |   7    | 8  | 9  | 10 |
# | 2 | 11 |   12   | 13 | 14 | 15 |
# | 3 | 16 | > 17 < | 18 | 19 | 20 |
# | 4 | 21 |   22   | 23 | 24 | 25 |
# | 5 | 26 |   27   | 28 | 29 | 30 |
# +---+----+--------+----+----+----+
```
