import csv
import random
import string


minimum = int(input("Введите минимальное значение"))
maximum = int(input("Введите максимальное значение"))
num_columns = int(input("Введите число столбцов"))
num_lines = int(input("Введите число строк"))
monicker = input("Введите имя файла")

##for _ in num_columns:

for _ in range(num_lines):
        line = [random.randint(minimum, maximum)
                for _ in range(num_columns)]




with open("testfile.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(...)