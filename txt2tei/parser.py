def tokenizer_split(split_text):
    marks = ['[', '{', ']', '}', '*', '###', '##', '#', '~~~']
    text_tokenised = []
    for token in split_text:
        new_token = token
        for mark in marks:
            if mark in token:
                new_token = []
                broken_token = token.partition(mark)
                for b_token in broken_token:
                    if b_token != "":
                        new_token.append(b_token)
                break
        if new_token == token:
            text_tokenised.append(token)
        else:
            for n_token in new_token:
                text_tokenised.append(n_token)
    return text_tokenised

def tokenizer(text):
    # tokenizes the text, which will allow us to check for character multiples
    split_text = text.split(" ")
    text_tokenised = tokenizer_split(split_text)
    while text_tokenised != tokenizer_split(text_tokenised):
        text_tokenised = tokenizer_split(text_tokenised)
    return [x for x in text_tokenised if x != ""]
        
            

def parser_single_open_close(token, i, error_list, parser_queue):
    # checks tags that open and close with different characters
    single_marks_opening = "{["
    single_marks_closing = "}]"
    for opening, closing in zip(single_marks_opening, single_marks_closing):
            if token == opening:
                parser_queue.append((i, closing))
            elif token == closing:
                if token == parser_queue[-1][1]:
                    parser_queue.pop(-1)
                else:
                    error_list.append(f"Error: expected '{parser_queue[-1][1]}' got '{token}' instead. Position: {i}")
    return error_list, parser_queue

def parser_single_same(token, i, error_list, parser_queue, valid_tags):
    # checks tags that open and close using the same character (i.e., '*')
    single_marks = ['*']
    for mark in single_marks:
        if parser_queue != []:
            if token == mark and token != parser_queue[-1][1]:
                parser_queue.append((i, mark))
                valid_tags.append([i,0])
            elif token == mark and token == parser_queue[-1][1]:
                parser_queue.pop(-1)
                valid_tags[-1][1] = i+1
        elif parser_queue == []:
            if token == mark:
                parser_queue.append((i, mark))
                valid_tags.append([i,0])
    return error_list, parser_queue, valid_tags

def parser(text):
    
    parser_queue = []
    error_list = []
    valid_tags = []
    tokenized_text = tokenizer(text)
    for i, token in enumerate(tokenized_text):
        # error_list, parser_queue = parser_single_open_close(token, i, error_list, parser_queue)
        error_list, parser_queue, valid_tags = parser_single_same(token, i, error_list, parser_queue, valid_tags)

    if parser_queue != []:
        for orphan in parser_queue:
            error_list.append(f"Error: opening tag '{orphan[1]}' at position {orphan[0]} was never closed")
    for error in error_list:
        print(error)
    for valid_tag in valid_tags[0:10]:
        print(f"{valid_tag}: {' '.join(tokenized_text[valid_tag[0]:valid_tag[1]])}")
    print(len(valid_tags))
