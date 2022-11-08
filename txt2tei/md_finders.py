# finds all level one headers
def find_headers_1(text):
    # DRAFT REGEX
    # (?<=#{1})([\s\S]*)(?=#{1})