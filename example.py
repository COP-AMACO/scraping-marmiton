import sys

from marmiton import Marmiton, RecipeNotFound

# Search :
query_options = {
    # Query keywords - separated by a white space
    "aqt": "Pizza",
    # Plate type: (optional)
    # "accompagnement", "amusegueule", "boisson", "confiserie", "conseil",
    # "dessert", "entree", "platprincipal", "sauce"
    "dt": "platprincipal",
    # Plate price: (optional)
    # 1 -> Cheap, 2 -> Medium, 3 -> Kind of expensive
    "exp": 1,
    # Recipe difficulty: (optional)
    # 1 -> Very easy, 2 -> Easy, 3 -> Medium, 4 -> Advanced
    "dif": 1,
    # Recipe particularity: (optional)
    # 1 -> Vegetarian, 2 -> Gluten-free, 3 -> Vegan,
    # 4 -> Lactose-free, 5 -> Balanced
    "prt": 1,
    # Cooking type: (optional)
    # 1 -> Oven, 2 -> Stovetop, 3 -> No-cook, 4 -> Microwave,
    # 5 -> Barbecue/Plancha
    "rct": 1,
    # Total time in minutes: (optional)
    # 15, 30, or 45
    "ttlt": 45,
}

try:
    # Search for recipes with the given options
    query_result = Marmiton.search(query_options)
except RecipeNotFound as e:
    print(f"No recipe found for '{query_options['aqt']}'")
    print(e)
    sys.exit(0)

# Get :
recipe = query_result[0]
main_recipe_url = recipe["url"]
try:
    # Get the details of the first returned recipe
    detailed_recipe = Marmiton.get(main_recipe_url)
except RecipeNotFound:
    print(f"No recipe found for '{query_options['aqt']}'")
    sys.exit(0)

# Print the result
print(f"# {detailed_recipe['name']}\n")
print(f"Recette par '{detailed_recipe['author']}'")
print(
    f"Noté {detailed_recipe['rate']}/5 par {detailed_recipe['nb_comments']} personnes"
)
print(f"""
        Temps de cuisson : {detailed_recipe["cook_time_min"]} min. |
        Temps de préparation : {detailed_recipe["prep_time_min"]} min. |
        Temps total : {detailed_recipe["total_time_min"]} min.
    """)
print(f"Difficulté : '{detailed_recipe['difficulty']}'")
print(f"Budget : '{detailed_recipe['budget']}'")

print(f"\nIngrédient(s) pour {detailed_recipe['recipe_quantity']} :")
for ingredient in detailed_recipe["ingredients"]:
    print(f"- {ingredient['name']} ({ingredient['quantity']} {ingredient['unit']})")

print("\nÉtapes :")
for step in detailed_recipe["steps"]:
    print(f"# {step}")

if detailed_recipe["author_tip"]:
    print(f"\nNote de l'auteur :\n{detailed_recipe['author_tip']}")
