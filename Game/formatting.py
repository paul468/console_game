def form(string,symbol,table,stats):
    f = []
    final = ""
    for i in string:
        f.append(i)
    for i in range(len(f)):
        if f[i] == symbol or f[i] == "":
            final += str(stats[table[f[i+1]]])
        else:
            if f[i] not in table.keys() or f[i-1] != symbol:
                final += f[i]
            elif f[i] != symbol:
                final += " "
    return final
