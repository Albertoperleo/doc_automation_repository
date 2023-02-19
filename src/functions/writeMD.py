file = []
with open(r".\data\templates\doc.txt", "r") as template:
    for line in template:
        if r"{}" in line:
            s = line.replace(r"{}","1")
        file.append(s)


doc = open(r".\prueba1.md", "w")
doc.writelines(file)
doc.close()