fio = input("ФИО: ")

parts = fio.split()
cleaned = " ".join(parts)
initials = "".join(x[0].upper() for x in parts)

print(f"Инициалы: {initials}.")
print(f"Длина (символов): {len(cleaned)}")


