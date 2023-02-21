# Data saving
def data_saving(self, file_name: str, data: str) -> None:
    with open(".\data\\retrieved\{}".format(file_name), "w") as file:
        for line in data:
            file.write(line)
            
# Write MD
def to_markdown(self, src: str, dst: str, template_path: str) -> None:
    file = []
    with open(template_path, "r") as template:
        for line in template:
            if r"{}" in line:
                s = line.replace(r"{}","1")
            file.append(line)
    doc = open(dst, "w")
    doc.writelines(file)
    doc.close()