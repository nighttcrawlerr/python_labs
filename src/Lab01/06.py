n = int(input("in_1: "))

full_time = 0
part_time = 0

for i in range(n):
    surname, name, age, form = input(f"in_{i + 2}: ").split()
    if form == "True":
        full_time += 1
    else:
        part_time += 1

print(f"out: {full_time} {part_time}")
