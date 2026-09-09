n = int(input())

full_time = 0
part_time = 0

for i in range(n):
    surname, name, age, form = input().split()
    if form == "True":
        full_time += 1
    else:
        part_time += 1

print(full_time, part_time)
