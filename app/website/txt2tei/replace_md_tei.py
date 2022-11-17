def replace_tags(valid_tags, tokenized_text):
    tag_to_html = {
        '#': '<h1>',
        '/#': '</h1>',
        '##': '<h2>',
        '/##': '</h2>',
        '###': '<h3>',
        '/###': '</h3>',
        '*': '<em>',
        '/*': '</em>',
        '{': '<span class="drop-capital">',
        '}': '</span>',
        '[cw:': '<p class="catch-word">',
        '[': '<p class="sig">',
        ']': '</p>',
        '\\': '<span class="side-note">',
        '/': '</span>'
    }
    for tag in valid_tags:
        tokenized_text[tag[0]] = tag_to_html[tokenized_text[tag[0]]]
        tokenized_text[tag[1]-1] = tag_to_html[tokenized_text[tag[1]-1]]
    return tokenized_text

def add_outer_tags(converted_text):
    outer_tags = {
        '\r\n': '</p><p>',
        '===': '<br/>',
        '~~~': '<br/>[Ornament]<br/>'
    }
    converted_text = [outer_tags[tag] if tag in outer_tags.keys() else tag for tag in converted_text]
    # changes the first to just an open tag
    for i, token in enumerate(converted_text):
        if token == '</p><p>':
            converted_text[i] = '<p>'
            break
    return converted_text