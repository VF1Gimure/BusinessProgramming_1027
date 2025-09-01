# Python Language and File I/O Cheatsheet

---

## ✅ PYTHON LANGUAGE CHEATSHEET

### Basics

```python
print("Hello, world!")
x = 5 + 3
```

### Variables

```python
x = 10
y = 3.14
name = "Luis"
flag = True
```

### Input and Output

```python
name = input("Your name: ")
age = float(input("Your age: "))
print("Hello", name)
```

### Conditionals

```python
if age > 18:
    print("Adult")
elif age == 18:
    print("Just turned 18")
else:
    print("Minor")
```

### Loops

```python
for i in range(5):
    print(i)

i = 0
while i < 5:
    print(i)
    i += 1
```

### Functions

```python
def greet(name):
    return "Hello " + name
```

### Lists

```python
items = [1, 2, 3]
items.append(4)
items[0] = 10
```

### Tuples

```python
pos = (10, 20)
x, y = pos
```

### Dictionaries

```python
person = {"name": "Luis", "age": 30}
print(person["name"])
```

### Sets

```python
s = {1, 2, 3}
s.add(4)
```

### List Comprehensions

```python
squares = [x*x for x in range(10)]
```

### Lambda Functions

```python
square = lambda x: x**2
```

### Classes

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(self.name, "says hello")
```

### Importing Modules

```python
import math
print(math.sqrt(25))
```

### Printing with Formatting

#### ✅ Using f-strings (Python 3.6+)

```python
name = "Luis"
score = 95
print(f"{name} scored {score} points.")

pi = 3.14159
print(f"Pi is approximately {pi:.2f}")
```

#### ❗ Compatible alternative (Python < 3.6)

```python
print("{} scored {} points.".format(name, score))
print("Pi is approximately {:.2f}".format(pi))
```

---

## ✅ FILE I/O

### `open()` Modes (Text)

#### `'w'` — Write-only

- **Use when:** Create or overwrite file
- **Clears file: Yes**

```python
with open("dummy.txt", "w") as f:
    f.write("Line A\nLine B\nLine C\n")
```

#### `'r'` — Read-only

```python
with open("dummy.txt", "r") as f:
    print(f.read())
```

#### `'a'` — Append

```python
with open("dummy.txt", "a") as f:
    f.write("Appended line\n")
```

#### `'r+'` — Read and write

```python
with open("dummy.txt", "r+") as f:
    f.readline()
    f.write(" ← inserted here\n")
```

#### `'w+'` — Write and read

- **Clears file: Yes**

```python
with open("dummy.txt", "w+") as f:
    f.write("Overwritten!\n")
    f.seek(0)
    print(f.read())
```

#### `'a+'` — Append and read

```python
with open("dummy.txt", "a+") as f:
    f.write("New log entry\n")
    f.seek(0)
    print(f.read())
```

### Binary Modes

| Text Mode | Binary Mode |
| --------- | ----------- |
| `'r'`     | `'rb'`      |
| `'w'`     | `'wb'`      |
| `'a'`     | `'ab'`      |
| `'r+'`    | `'rb+'`     |
| `'w+'`    | `'wb+'`     |
| `'a+'`    | `'ab+'`     |

Use binary modes for:

- Images
- Audio
- Raw byte files

---

## ✅ JSON FILE I/O

### Using `json` (Standard)

```python
import json

with open("data.json", "r") as f:
    data = json.load(f)

for item in data:
    print(item["name"])
```

### Using `pandas.read_json()`

```python
import pandas as pd

df = pd.read_json("data.json")
print(df["name"])
```

### Manual `loads()` + filtering

```python
import json

with open("data.json", "r") as f:
    raw = f.read()
    data = json.loads(raw)

filtered = [d for d in data if d["score"] > 80]
for d in filtered:
    print(d["name"])
```

---

## ✅ CSV FILE I/O

### `csv.reader`

```python
import csv

with open("scores.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

### `csv.DictReader`

```python
import csv

with open("scores.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["score"])
```

### `pandas.read_csv()`

```python
import pandas as pd

df = pd.read_csv("scores.csv")
print(df["score"])
```

### Manual Filtering from Raw Text

```python
with open("scores.csv", "r") as f:
    lines = f.readlines()[1:]  # skip header
    passed = [line.strip() for line in lines if int(line.strip().split(",")[1]) > 80]

for line in passed:
    print(line)
```

