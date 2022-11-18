def find_tags_in_text(valid_tags, tokenized_text, text):
    if ''.join(tokenized_text[:]) == text:
        if valid_tags != []:
            print("\n ====== Valid tags ====== \n")
            for valid_tag in valid_tags:
                print(f"{valid_tag}: {''.join(tokenized_text[valid_tag[0]:valid_tag[1]])}")