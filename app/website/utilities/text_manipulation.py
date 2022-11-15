import re
CLEANR = re.compile('<.*?>') 

def remove_tags(text):
    cleantext = re.sub(CLEANR, '', text)
    return cleantext