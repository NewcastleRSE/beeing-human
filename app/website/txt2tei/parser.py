def tokenizer_split(split_text):
    marks = ['[cw:', '[', '{', ']', '}', '/*', '*', '/###', '###', '/##','##', '/#', '#', '~~~', '\\', '/', '===', '\r\n']
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
    # split_text = text.split(" ")
    # preserves spaces:
    split_text = [i for j in text.split(" ") for i in (j, " ")][:-1]
    text_tokenised = tokenizer_split(split_text)
    while text_tokenised != tokenizer_split(text_tokenised):
        text_tokenised = tokenizer_split(text_tokenised)
    return [x for x in text_tokenised if x != ""]
        
            

def parser_single_open_close(token, i, error_list, parser_queue, valid_tags, single_marks_opening, single_marks_closing):
    # checks tags that open and close with different characters
    for opening, closing in zip(single_marks_opening, single_marks_closing):
            if token == opening:
                parser_queue.append((i, closing))
            elif token == closing:
                if parser_queue == []:
                    # error: closing without opening with an empty list
                    # error_list = [poosition, type, closing]
                    error_list.append([i, 2, token])
                    break
                elif token == parser_queue[-1][1] and parser_queue != []:
                    valid_tags.append([parser_queue[-1][0], i+1])
                    parser_queue.pop(-1)
                    break
                else:
                    # error_list = [position, type, expected, found]
                    error_list.append([i, 0, parser_queue[-1][1], token])
                    break
    return error_list, parser_queue, valid_tags

# def parser_single_same(token, i, error_list, parser_queue, valid_tags, single_marks):
#     # checks tags that open and close using the same character (i.e., '*')
#     for mark in single_marks:
#         if parser_queue != []:
#             if token == mark and token != parser_queue[-1][1]:
#                 parser_queue.append((i, mark))
#                 valid_tags.append([i,0])
#             elif token == mark and token == parser_queue[-1][1]:
#                 parser_queue.pop(-1)
#                 valid_tags[-1][1] = i+1
#         elif parser_queue == []:
#             if token == mark:
#                 parser_queue.append((i, mark))
#                 valid_tags.append([i,0])
#     return error_list, parser_queue, valid_tags

def parser(text):
    single_marks_opening = ['[cw:', '{', '[', '*', '###', '##', '#', '\\']
    single_marks_closing = [']', '}', ']', '/*', '/###', '/##', '/#', '/']
    parser_queue = []
    error_list = []
    valid_tags = []
    tokenized_text = tokenizer(text)
    for i, token in enumerate(tokenized_text):
        if token in single_marks_opening or token in single_marks_closing:
            error_list, parser_queue, valid_tags = parser_single_open_close(token, i, error_list, parser_queue, valid_tags, single_marks_opening, single_marks_closing)
    # report
    # 0 - Unexpected (f"Error: expected '{parser_queue[-1][1]}' got '{token}' instead. Position: {i}")
    # 1 - Opening Tag Never Closed(f"Error: opening tag '{orphan[1]}' at position {orphan[0]} was never closed")
    if parser_queue != []:
        for orphan in parser_queue:
            # error_list = [position, type, orphan]
            error_list.append([orphan[0], 1, orphan[1]])
    if error_list != []:
        # print("\n ====== Errors ====== \n")
        # order list by position
        error_list = sorted(error_list, key = lambda x: x[0])
        errors = True
        
        # this code can be used to print out errors in a readable manner

        # for error in error_list:
        #     if error[1] == 0:
        #         print(f"Error: expected '{error[2]}' got '{error[3]}' instead. Position: {error[0]}: '{' '.join(tokenized_text[error[0]:error[0]+10])}'")
        #     elif error[1] == 1:
        #         print(f"Error: opening tag '{error[2]}' at position {error[0]} was never closed: '{' '.join(tokenized_text[error[0]:error[0]+10])}'")
        #     elif error[1] == 2:
        #         print(f"Error: Closing tag '{error[2]}' at position {error[0]} was never opened: '{' '.join(tokenized_text[error[0]:error[0]+10])}'")
    else:
        errors = False
    return valid_tags, tokenized_text, error_list, errors
