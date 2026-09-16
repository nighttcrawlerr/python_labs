s = input()

for i in range(len(s)):
    if s[i].isupper():
        start = i
        break

for i in range(start, len(s)):
    if s[i].isdigit():
        step = i + 1 - start
        break

slovo = ""
for i in range(start, len(s), step):
    slovo += s[i]
    if s[i] == ".":
        break

print(slovo)