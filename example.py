from marmiton import Marmiton, RecipeNotFound

# Search :
query_options = {
    "aqt": "Pizza",        # Query keywords - separated by a white space
    "dt": "platprincipal", # Plate type : "accompagnement", "amusegueule", "boisson", "confiserie", "conseil", "dessert", "entree", "platprincipal", "sauce" (optional)
    "exp": 1,              # Plate price : 1 -> Cheap, 2 -> Medium, 3 -> Kind of expensive (optional)
    "dif": 1,              # Recipe difficulty : 1 -> Very easy, 2 -> Easy, 3 -> Medium, 4 -> Advanced (optional)
    "prt": 1,              # Recipe particularity: 1 -> Vegetarian, 2 -> Gluten-free, 3 -> Vegan, 4 -> Lactose-free, 5 -> Balanced (optional)
    "rct": 1,              # Cooking type: 1 -> Oven, 2 -> Stovetop, 3 -> No-cook, 4 -> Microwave, 5 -> Barbecue/Plancha (optional)
    "ttlt": 45,            # Total time in minutes: 15, 30, or 45 (optional)
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
    # Get the details of the first returned recipe
    detailed_recipe = Marmiton.get(main_recipe_url)  
except RecipeNotFound as e:
    print(f"No recipe found for '{query_options['aqt']}'")
    import sys
    sys.exit(0)

# Print the result
print(f"# {detailed_recipe['name']}\n")
print(f"Recette par '{detailed_recipe['author']}'")
print(f"Noté {detailed_recipe['rate']}/5 par {detailed_recipe['nb_comments']} personnes")
print(f"Temps de cuisson : {detailed_recipe['cook_time_min'] if detailed_recipe['cook_time_min'] else 'N/A'} min. | Temps de préparation : {detailed_recipe['prep_time_min']} min. | Temps total : {detailed_recipe['total_time_min']} min.")
print(f"Difficulté : '{detailed_recipe['difficulty']}'")
print(f"Budget : '{detailed_recipe['budget']}'")

print(f"\nIngrédient(s) pour {detailed_recipe['recipe_quantity']} :")
for ingredient in detailed_recipe['ingredients']:
    print(f"- {ingredient['name']} ({ingredient['quantity']} {ingredient['unit']})")

print(f"\nÉtapes :")
for step in detailed_recipe['steps']:
    print(f"# {step}")

if detailed_recipe['author_tip']:
    print(f"\nNote de l'auteur :\n{detailed_recipe['author_tip']}")
