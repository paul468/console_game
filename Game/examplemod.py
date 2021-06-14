import revolution

# this decorator registers this function as a command and can be called in game via calling the name of the function.
@revolution.game_command
def debug(*args):
	
	#args is a number of arguments: the 0th element is the save file of the player, the 1st element is the inventory, the 2nd is the generation (look into generation.json, these are the bonuses that can occur), 3rd are ALL items, 4th is the situations (look into situations.json), which are the deaths.
	for i in args[3]:
		print(i)

#template for an item
custom_item = {
"name":"airplane",
"price":"1",
"description":"This is a testing object.",
"properties":[
{"property":"money","operand":"+", "right":1}
]
}

#template for a death, triggered function is customisable
custom_death = {
"sentences":["This is a test", "death with two sentences.", "You have $x money."],
"conditions":[
{
"property":"money", "operand":">", "comparand":0
}],
"func":"debug"
}

#template for custom occasion that can randomly occur. The random property describes if the object is random, then describes the chance in percent.
#the $x stands for the player's current money status. the default table is as follows:
"""
$x for money
$n for the player's name
$i for his items
$p for his amount of people
$d for his amount of days 
$e for his amount of enemies
more can be added with: revolution.add_prop(name, alias, default_value), whereas alias is the character that comes AFTER the $ sign. the alias can only be one character, so choose wisely.
this formatting can be used everywhere, whereas the tag is equal to 'sentences'
"""
custom_bonus = {
	"sentences":["This is a", "testing bonus, you got 1 coin, you have now $x"],
	"effects":[{"property":"money", "operand":"+", "right":1}],
	"random":[True, 100]
}

#registering the item
revolution.register_item(custom_item)
#adding a new property
revolution.add_prop("kills", "k", 0)
#registering the death
revolution.add_death(custom_death)
#registering the occasion
revolution.add_bonus(custom_bonus)

revolution.main()
