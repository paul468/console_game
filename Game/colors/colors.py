def color(text):
    string = ""
    for l in text["before"]:
        string += l
    string += text["string"]
    for l in text["after"]:
        string += l
    return string
