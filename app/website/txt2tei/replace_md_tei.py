def replace_tags(valid_tags, tokenized_text):
    for tag in valid_tags:
        if tokenized_text[tag[0]] == '*':
            tokenized_text[tag[0]] = '<em>'
            tokenized_text[tag[1]-1] = '</em>'
        if tokenized_text[tag[0]] == '#':
            tokenized_text[tag[0]] = '<h1>'
            tokenized_text[tag[1]-1] = '</h1>'
        if tokenized_text[tag[0]] == '##':
            tokenized_text[tag[0]] = '<h2>'
            tokenized_text[tag[1]-1] = '</h2>'
    return("".join(tokenized_text[:]))