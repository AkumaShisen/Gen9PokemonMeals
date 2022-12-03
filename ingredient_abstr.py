#abstraction by Akumashisen #3030
#working with json file from MattMckenzy #0741

import numpy as np
import string

powers = ["Egg", "Catching","Exp","Raid","Item Drop", "Humungo", "Teensy","Encounter","Title","Sparkling"]
types = ["Normal","Fighting","Flying","Poison","Ground","Rock","Bug","Ghost","Steel","Fire","Water",
    "Grass","Electric","Psychic","Ice","Dragon","Dark","Fairy"]
tastes = ["Sweet","Salty","Sour","Bitter","Hot"]

col_names_int = powers  + types + tastes + ["Cost"]
power_start,power_end = 0, len(powers)
types_start,types_end = power_end, power_end+len(types)
tastes_start,tastes_end = types_end, types_end+len(tastes)


col_names_int_dict=dict()
for i in range(len(col_names_int)) :
    col_names_int_dict[col_names_int[i]] = i


def simplify(string) :
    return string.replace(" ", "").lower()
class Ingredient :
    def __init__(self, name, list):
        self.entries = list
        self.name = name
    def get_raw(self,column) :
        return self.entries[col_names_int_dict[column]]
    def get(self,column) : 
        if not column in col_names_int_dict :
            return 0
        return self.get_raw(column)

    def type_val(self) :
        return self.entries[types_start:types_end]
    def powers_val(self) :
        return self.entries[power_start:power_end]
    def tastes_val(self) : 
        return self.entries[tastes_start:tastes_end]

    #values,types
    def type_sort(self) :
        return zip(*sorted(zip(self.type_val(),types),key=lambda x: x[0],reverse= True ))
    def powers_sort(self) :
        return zip(*sorted(zip(self.powers_val(),powers),key=lambda x: x[0],reverse= True ))
    def tastes_sort(self) :
        return zip(*sorted(zip(self.tastes_val(),tastes),key=lambda x: x[0],reverse= True ))
    
    def print_control(self,values,control) :
        for e in control :
            print("{:^10}".format(e),end="")
        print()
        for e in values :
            print("{:^10}".format(e),end="")
        print()

    def print_types(self) :
        values,control = self.type_sort()
        self.print_control(values,control)
    def print_powers(self) :
        values,control = self.powers_sort()
        self.print_control(values,control)
    def print_tastes(self) :
        values,control = self.tastes_sort()
        self.print_control(values,control)
        

    def print_raw(self) :
        print("{:<20}".format(self.name),end="")
        for e in self.entries :
            print("{:>6}".format(e),end="")
        print()
    def print(self) :
        print(self.name)
        self.print_tastes()
        self.print_powers()
        self.print_types()

    def sum_list(v) :
        if not type(v)==list :
            return v
        res_entries = np.zeros(len(col_names_int),dtype=int)
        for e in v :
            res_entries += e.entries
        res_name = ",".join([e.name for e in v])
        return Ingredient(res_name,res_entries)

    def sum(*v) :
        return Ingredient.sum_list(v)

class Ingredient_List :
    def __len__(self):
        return len(self.index_dict)
    def __init__(self, ingr_list):
        self.index_dict = dict()
        for i in range(len(ingr_list)) :
            self.index_dict[simplify(ingr_list[i]["Name"])] = i

        self.name_list = [e["Name"]   for e in ingr_list ]
        self.int_matrix = np.zeros((len(ingr_list),len(col_names_int)),dtype=int)
        for i in range(len(ingr_list)) :
            ingredient = ingr_list[i]
            self.int_matrix[i][col_names_int_dict["Cost"]] = ingredient["Cost"] 
            for key in ingredient :
                if(type(ingredient[key]) ==list) :
                    for name_val in ingredient[key] :
                        self.int_matrix[i][col_names_int_dict[name_val["Name"]]] += name_val["Value"]
    
    def get_ingr_raw(self,ingredient) :
        index = self.index_dict[ingredient]
        return Ingredient(self.name_list[index],self.int_matrix[self.index_dict[ingredient]])

    def get_ingr(self,ingredient) :
        ingredient=simplify(ingredient)
        if not ingredient in self.index_dict :
            return None
        return self.get_ingr_raw(ingredient)

    def get_entry_raw(self,ingredient, column) :
        return self.int_matrix[self.index_dict[ingredient]][col_names_int_dict[column]]
    def get_entry(self,ingredient, column) :

        ingredient=simplify(ingredient)
        if not column in col_names_int_dict or not ingredient in self.index_dict :
            return 0
        return self.get_entry_raw(ingredient,column)
    def print(self,limit = -1) :

        for i in range(len(self.name_list)) :
            if i==limit :
                break
            print("{:<20}".format(self.name_list[i]),end="")

            for e in self.int_matrix[i] :
                print("{:>6}".format(e),end="")

            print()
def get_recipe_sum_raw(recipe_fillings, recipe_condiments, fillings,condiments) :
    return Ingredient.sum_list([fillings.get_ingr_raw(ingr) for ingr in recipe_fillings.split(",")] +
                                [condiments.get_ingr_raw(ingr) for ingr in recipe_condiments.split(",")])

def get_recipe_sum(recipe, fillings,condiments) :
    return Ingredient.sum_list([fillings.get_ingr(ingr) or condiments.get_ingr(ingr) for ingr in recipe.split(",")])