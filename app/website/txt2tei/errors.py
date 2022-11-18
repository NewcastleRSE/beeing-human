def find_position_for_display(errors, tokenized_text):
    markup = ['[', '{', ']', '}', '/*', '*', '/###', '###', '/##','##', '/#', '#', '~~~']
    mark_positions = []
    for error_id, error in enumerate(errors):
        # closes with the wrong tag, or closing tag never opened
        if error[1] == 0 or error[1] == 2:
            for i, token in enumerate(tokenized_text[:error[0]]):
                if token in markup:
                    last_position = i
            mark_positions.append([last_position, error[0], str(error_id)])

        # opening tag never closed
        elif error[1] == 1:
            for i, token in enumerate(tokenized_text[error[0]+1:]):
                if token in markup:
                    last_position = i
                    break
            mark_positions.append([error[0], error[0] + last_position, str(error_id)])
    mark_positions = consolidate_positions(mark_positions)
    return mark_positions

def consolidate_positions(mark_positions):
    consolidated = []
    for position in mark_positions:
        if consolidated == []:
            consolidated = [position]
        elif position[0] < consolidated[-1][1]:
            consolidated[-1][1] = position[1]
            consolidated[-1][2] = consolidated[-1][2] + " " + position[2]
        else:
            consolidated.append(position)
    return consolidated
    

def mark_errors_for_display(errors, tokenized_text):
    mark_positions = find_position_for_display(errors, tokenized_text)
    marked_up_text = []
    for i, position in enumerate(mark_positions):
        # if it's the first error, add everything from the start until the error
        if i == 0:
            marked_up_text = tokenized_text[:position[0]]

        marked_up_text.append(f"<span class=\"error-mark\" id = \"{position[2]}\">")
        for token in tokenized_text[position[0]:position[1]]:
            marked_up_text.append(token)
        marked_up_text.append("</span>")
        

        # if it's the last errror, add everything until the end of the text
        if i == len(mark_positions)-1:
            for token in tokenized_text[position[1]:]:
                marked_up_text.append(token)
        else:
            # if it's not the last error, add everything until the start of the next error
            for token in tokenized_text[position[1]:mark_positions[i+1][0]]:
                marked_up_text.append(token)
    
    return marked_up_text