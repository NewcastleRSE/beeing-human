def replace_tags(valid_tags, tokenized_text):
    for tag in valid_tags:
        if tokenized_text[tag[0]] == '*':
            tokenized_text[tag[0]] = '<em>'
            tokenized_text[tag[1]-1] = '</em>'
    print("".join(tokenized_text[:]))