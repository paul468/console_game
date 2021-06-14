import os, json, random, colors.colors, time, formatting





to_str = json.dumps
f=object()
newbie = False
commands = []
situations = {}
generation = {}
dead = False
statistics={}
items = {}
table = {
"d":"days",
"x":"money",
"i":"items",
"p":"people",
"n":"name",
"e":"enemies"
}
def generate_newspaper(sentences, whitespace,stats):
    final = []
    for i in sentences:
        final.append(("¬| "+formatting.form(i, "$", table, stats)+" |¬").replace("  ", " "))
    final.append("\n")
    return final
def register_item(item:dict, alias):
    table[alias] = item["name"]
    with open("items.json", "r+") as f:
        pass
with open("situations.json") as l:
    situations = json.load(l)
with open("generation.json") as l:
    generation = json.load(l)
with open("items.json") as l:
    items = json.load(l)
def game_command(func):
    commands.append(func)
    return func
@game_command
def reset(*args):
    args[1]["money"] = 10
@game_command
def save_stats(*args):
    f= open(args[1]["name"] + ".json", "w+")
    f.write(to_str(args[1]))
    f.close()
    f=open(args[1]["name"]+".json", "r+")
@game_command
def leave(*args):
    save_stats(args[0], args[1])
    quit()
@game_command
def statistics(*args):
    print(args[1])

@game_command
def help(*args):
    global commands
    print("Commands are: ")
    for i in commands:
        print(i.__name__)

@game_command
def buy(*args):
    print("The shop is closed at the moment.")


@game_command
def debug(*args):
    args[1]["money"] -= 1

def render_news(news):
    for i in news:
        print(color({"before":["\033[91m"], "string":i, "after":["\033[0m"]}))
        time.sleep(0.3)
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
                else:
                    if l["operand"] == "+":
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
            for j in commands:
                if j.__name__ == i["func"]:
                    j(args[0], args[1])
            n = generate_newspaper(i["sentences"], "", args[1])
            render_news(n)
    args[1]["days"]+=1
@game_command
def clear(*args):
    os.system('clear')
            

color = colors.colors.color
console = input(color({"after":["\033[0m"],"before":["\033[92m"],"string":"Hello! How are you today! Enter a Command ([Load] for loading a Save File, [Create] for creating a new game)"})).lower()

if console == "create":
    print("Note that you can't name two characters the same or your save files will be corrupted.")
    newbie = True
    name = input("Please Enter the Name of your Character: ")
    statistics = {"name":name, "money":10, "items":[], "people":0}
    f=open(name+".json", "w+")
elif console == "load":
    name = input("Please Enter the Name of your Character: ")
    f=open(name+".json")
    statistics = json.load(f)


news = generate_newspaper(["Welcome!", "We have loaded up the game."], " ", statistics)
render_news(news)
def main():
    global statistics, name, f
    exited = False
    while not exited:
        command = input("Please Enter a Command: ").lower()
        for i in commands:
            if i.__name__ == command:
                i(f, statistics)
main()
