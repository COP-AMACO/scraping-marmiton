from marmiton import Marmiton, RecipeNotFound

# Search :
query_options = {
    "aqt": "Fondue savoyarde",  # Query keywords - separated by a white space
    "dt": "platprincipal",      # Plate type : "entree", "platprincipal", "accompagnement", "amusegueule", "sauce" (optional)
    "exp": 2,                   # Plate price : 1 -> Cheap, 2 -> Medium, 3 -> Kind of expensive (optional)
    "dif": 2,                   # Recipe difficulty : 1 -> Very easy, 2 -> Easy, 3 -> Medium, 4 -> Advanced (optional)
    "prt": 1,                   # Recipe particularity: 1 -> Vegetarian, 2 -> Gluten-free, 3 -> Vegan, 4 -> Lactose-free, 5 -> Balanced (optional)
    "rct": 2,                   # Cooking type: 1 -> Oven, 2 -> Stovetop, 3 -> No-cook, 4 -> Microwave, 5 -> Barbecue/Plancha (optional)
    "ttlt": 45,                 # Total time in minutes: 15, 30, or 45 (optional)
}
try:
    # Search for recipes with the given options
    query_result = Marmiton.search(query_options)
except RecipeNotFound as e:
    print(f"No recipe found for '{query_options['aqt']}'")
    print(e)
    import sys
    sys.exit(0)

# Get :
recipe = query_result[0]
main_recipe_url = recipe['url']

try:
    detailed_recipe = Marmiton.get(main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)
except RecipeNotFound as e:
    print(f"No recipe found for '{query_options['aqt']}'")
    import sys
    sys.exit(0)

# Display result :
print("## %s\n" % detailed_recipe['name'])  # Name of the recipe
print("Recette par '%s'" % (detailed_recipe['author']))
print("Noté %s/5 par %s personnes." % (detailed_recipe['rate'], detailed_recipe['nb_comments']))
print("Temps de cuisson : %s / Temps de préparation : %s / Temps total : %s." % (detailed_recipe['cook_time'] if detailed_recipe['cook_time'] else 'N/A',detailed_recipe['prep_time'], detailed_recipe['total_time']))
print("Difficulté : '%s'" % detailed_recipe['difficulty'])
print("Budget : '%s'" % detailed_recipe['budget'])

print("\nRecette pour %s :\n" % detailed_recipe['recipe_quantity'])
for ingredient in detailed_recipe['ingredients']:  # List of ingredients
    print("- %s" % ingredient)

print("")

for step in detailed_recipe['steps']:  # List of cooking steps
    print("# %s" % step)

if detailed_recipe['author_tip']:
	print("\nNote de l'auteur :\n%s" % detailed_recipe['author_tip'])
