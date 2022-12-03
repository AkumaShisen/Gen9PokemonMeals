#json from MattMckenzy #0741

from ingredient_abstr import *
import json
import numpy as np

# Opening JSON file
f = open('ingredients.json')
data = json.load(f)
fillings = Ingredient_List(data["Fillings"])
condiment = Ingredient_List(data["Condiments"])
input = "Banana, CherryTomatoes, Chorizo, Salt, Yogurt"
ing_res = get_recipe_sum(input,fillings,condiment)
ing_res.print()