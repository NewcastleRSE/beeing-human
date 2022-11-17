import re
CLEANR = re.compile('<.*?>') 
CLEAN_EMPTY = re.compile('<p></p>') 

def remove_tags(text):
    cleantext = re.sub(CLEANR, '', text)
    return cleantext

def remove_empty_tags(text):
    cleantext = re.sub(CLEAN_EMPTY, '', text)
    print(cleantext)
    return cleantext
