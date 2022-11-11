def load_txt_file_to_lines(filename):
    with open(filename, 'r', encoding="utf8") as file:
        text_lines = file.readlines()
    return text_lines

def load_txt_file_to_string(filename):
    with open(filename, 'r', encoding="utf8") as file:
        text = file.read()
    return text