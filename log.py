
colors = { 
"END":  '\33[0m',
"BOLD":  '\33[1m',
"ITALIC":  '\33[3m',
"URL":  '\33[4m',
"BLINK":  '\33[5m',
"BLINK2":  '\33[6m',
"SELECTED":  '\33[7m',
"BLACK":  '\33[30m',
"RED":  '\33[31m',
"GREEN":  '\33[32m',
"YELLOW":  '\33[33m',
"BLUE":  '\33[34m',
"VIOLET":  '\33[35m',
"BEIGE":  '\33[36m',
"WHITE":  '\33[37m',
"BLACKBG":  '\33[40m',
"REDBG":  '\33[41m',
"GREENBG":  '\33[42m',
"YELLOWBG":  '\33[43m',
"BLUEBG":  '\33[44m',
"VIOLETBG":  '\33[45m',
"BEIGEBG":  '\33[46m',
"WHITEBG":  '\33[47m',
"GREY":  '\33[90m',
"RED2":  '\33[91m',
"GREEN2":  '\33[92m',
"YELLOW2":  '\33[93m',
"BLUE2":  '\33[94m',
"VIOLET2":  '\33[95m',
"BEIGE2":  '\33[96m',
"WHITE2":  '\33[97m'}

def p(*args):
    command = [];
    for name in args:
        if '~' in str(name):
            command.append(colors[name[1:].upper()])
        else : command.append(name)
    print(*command, colors['END'])


# P("~red", "rr", "~green", "this is blue")


