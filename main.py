from txt2tei.file_operations import load_txt_file_to_lines
from txt2tei.file_operations import load_txt_file_to_string
from txt2tei.parser import parser

lines = load_txt_file_to_lines("data/test_Butler1609_Nov.txt")
string = load_txt_file_to_string("data/test_single_open_close_parser.txt")

parser(string)