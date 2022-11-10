from txt2tei.file_operations import load_txt_file_to_lines
from txt2tei.file_operations import load_txt_file_to_string
from txt2tei.parser import parser
from txt2tei.md_finders import find_tags_in_text

# lines = load_txt_file_to_lines("data/test_Butler1609_Nov.txt")
string = load_txt_file_to_string("data/test_combined_no_singles.txt")

valid_tags, tokenized_text = parser(string)
find_tags_in_text(valid_tags, tokenized_text, string)