import os, json, random, time, sys, inspector, gen





to_str = json.dumps
f=object()
newbie = False
commands = []
situations = {}
generation = {}
dead = False
statistics={}
triggers = []
items = {}
table = {
"d":"days",
"x":"money",
"i":"items",
"p":"people",
"n":"name",
"e":"enemies",
"%":"noticed"
}
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

def color(text):
    string = ""
    for l in text["before"]:
        string += l
    string += text["string"]
    for l in text["after"]:
        string += l
    return string

def generate_newspaper(sentences, whitespace,stats):
    final = []
    for i in sentences:
        final.append(("¬| "+form(i, "$", table, stats)+" |¬").replace("  ", " "))
    final.append("\n")
    return final
def render_news(news):
    for i in news:
        for l in i:
                print(color({"before":["\033[91m"], "string":l, "after":["\033[0m"]}), end="")
                time.sleep(0.07)
                sys.stdout.flush()
        print("\n")
def register_item(item:dict):
    items[item["name"]] = item


def add_prop(name, alias, default_value):

    table[name] = alias
    statistics[name] = default_value

def add_death(death:dict):
    situations["situations"].append(death)

def add_bonus(bonus:dict):
    generation["situations"].append(bonus)

def game_command(func):
    commands.append(func)
    return func

def trigger_func(func):
    triggers.append(func)
    return func


@trigger_func
def notice(*args):
    args[1]["noticed"] = True

@game_command
def reset(*args):
    args[1]["money"] = 10
@game_command
def save_stats(*args):
    f= open(args[1]["name"] + ".json", "w+")
    f.write(to_str(args[1]))
    f.close()
    f=open(args[1]["name"]+".json", "r+")


@trigger_func
def blank(*args):
    pass

@game_command
def infiltrate(*args):
    width, height = 5,5
    exited = False
    print("Legend: \n0: Gate\n=: Wall\nG: Guards")
    gena = gen.Generator(width, height, ["1","2","3"])
    gena.generate()
    print("\n")
    while not exited:
        cons = input("Enter an infiltration command ([map] for the current overview of the map , [move] to open up the moving menu.): ")
        if cons == "exit":
            exited = True
        if cons == "map":
            for i in gena.final:
                print(i)
            

@game_command
def stats(*args):
    print(args[1])

@game_command
def help(*args):
    global commands
    print("Commands are: ")
    for i in commands:
        print(i.__name__)

@game_command
@trigger_func
def leave(*args):
    save_stats(args[0], args[1])
    quit()



def trigger_sit(name):
    try:
        for i in situations["situations"]:
            if i["name"] == name:
                news = generate_newspaper(i["sentences"], " ", statistics)
                render_news(news)
                for l in triggers:
                    if l.__name__ == i["func"]:
                        l(f, statistics, generation, items, situations)
    except KeyError as e:
        print("ERROR : ", "The developer forgot a bug here when he put in the wrong dict key!! How stupid of him! leaving and saving now...\n(Don't worry your save files are safe.)")
        leave(f, statistics, generation, items, situations)

@game_command
def buy(*args):
    if random.randint(0,100) <= 80:
        print("The shop is closed at the moment.")
        return;
    else:
        print("The shop is open!")
    shop = []
    for i in args[3]:
        roll = random.randint(0,100)
        if roll <= args[3][i]["probability"]:
            shop.append(args[3][i])
    for i in shop:
        print(i["name"], i["description"], "price : " + str(i["price"]))
    item = input("please put in the name of the item you want to buy: ")
    for i in args[3]:
        if args[3][i]["name"] == item:
            print("Item found in stock!")
            args[1]["money"] -= 10
            args[1]["items"].append(args[3][i])
    del shop


@game_command
def debug(*args):
    args[1]["money"] -= 1


def compare(i, args):
        cons = []
        met = True
        for l in i["conditions"]:
            prop = args[1][l["property"]]
            
            if l["operand"] == ">=":
                if prop >= l["comparand"]:
                    cons.append(True)
                else:
                    cons.append(False)
            elif l["operand"] == "<=":
                if prop <= l["comparand"]:
                    cons.append(True)
                else:
                    cons.append(False)
            elif l["operand"] == "=":
                if prop == l["comparand"]:
                    cons.append(True)
                else:
                    cons.append(False)
        for l in cons:
            if not l:
                met = False

        return met
@game_command
def consume(*args):
    print("You have: ")
    for i in args[1]["items"]:
        print(i["name"], i["description"])
    item = input("Enter the name of the item:")
    consumed = False
    for i in args[1]["items"]:
        if i["name"] == item:
            for j in i["properties"]:
                if j["property"] != "items":
                    
                    if j["operand"] == "+":
                        args[1][j["property"]] += j["right"]
                    elif j["operand"] == "-":
                        args[1][j["property"]] -= j["right"]
                    elif j["operand"] == "/":
                        args[1][j["property"]] /= j["right"]
                    elif j["operand"] == "*":
                        args[1][j["property"]] *= j["right"]
                    elif j["operand"] == "=":
                        args[1][j["property"]] = j["right"]
                else:
                    if j["operand"] == "+":
                        for k in j["right"]:
                            args[1][j["property"]].append(items[k])                    
    for i in args[1]["items"]:
        if i["name"] == item and not consumed:
            args[1]["items"].remove(i)
            consumed = True
    print("everything went to plan!")
    
@game_command
def newday(*args):
    if args[1]["people"] > 0:
        print("Your people pay you to help you in your operations!")
        args[1]["money"] += 10 * args[1]["people"]
    print(f"You get {args[1]['people']*10}")
    for i in generation["situations"]:
        chance = i["random"][1]
        roll = random.randint(0, 100)
        if roll <= chance:
            for l in i["effects"]:
                if l["property"] != "items":
                    if l["operand"] == "+":
                        args[1][l["property"]] += l["right"]
                    elif l["operand"] == "-":
                        args[1][l["property"]] -= l["right"]
                    elif l["operand"] == "/":
                        args[1][l["property"]] /= l["right"]
                    elif l["operand"] == "*":
                        args[1][l["property"]] *= l["right"]
                else:
                    if l["operand"] == "+":
                        for k in l["right"]:
                            args[1][l["property"]].append(items[k])
                            
            n = generate_newspaper(i["sentences"], "", args[1])
            render_news(n)
            
    for i in situations["situations"]:        
        if compare(i, args):
            n = generate_newspaper(i["sentences"], "", args[1])
            render_news(n)
            for j in triggers:
                if j.__name__ == i["func"]:
                    j(*args)
            
    args[1]["days"]+=1
@game_command
def clear(*args):
    os.system('clear')
            

with open("cards.json") as l:
        items = json.load(l)
with open("situations.json") as l:
        situations = json.load(l)   
with open("generation.json") as l:
    generation = json.load(l)

def main():
    global situations, generation, items, statistics
    
    
    console = input(color({"after":["\033[0m"],"before":["\033[92m"],"string":"Hello! How are you today! Enter a Command ([Load] for loading a Save File, [Create] for creating a new game)"})).lower()

    if console == "create":
        print("Note that you can't name two characters the same or your save files will be corrupted.")
        newbie = True
        name = input("Please Enter the Name of your Character: ")
        statistics["name"] = name
        statistics["money"] = 0
        statistics["items"] = []
        statistics["people"] = 1
        statistics["enemies"] = 1000000
        statistics["days"] = 0
        statistics["noticed"] = False
        statistics["attacks"] = []
        f=open(name+".json", "w+")
    elif console == "load":
        name = input("Please Enter the Name of your Character: ")
        f=open(name+".json")
        loads = json.load(f)
        for i in loads:
            statistics[i] = loads[i]

    news = generate_newspaper(["Welcome!", "We have loaded up the game."], " ", statistics)
    render_news(news)
    exited = False
    while not exited:
        command = input("Please Enter a Command: ").lower()
        for i in commands:
            if i.__name__ == command:
                i(f, statistics, generation, items, situations)
