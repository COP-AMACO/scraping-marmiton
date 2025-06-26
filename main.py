import json

from marmiton import Marmiton, RecipeNotFound
from plats import PLATS

if __name__ == "__main__":
    recipes = []
    for index, plat in enumerate(PLATS):
        print(f"[{index + 1}/{len(PLATS)}] Recherche de la recette pour '{plat}'...")
        query_options = {
            "aqt": plat,  # Query keywords - separated by a white space
        }
        try:
            query_result = Marmiton.search(query_options)
        except RecipeNotFound:
            print(f"No recipe found for '{plat}'")
            continue

        if not query_result:
            print(f"No recipe found for '{plat}'")
            continue

        main_recipe_url = query_result[0]["url"]

        try:
            # Get the details of the first returned recipe
            detailed_recipe = Marmiton.get(main_recipe_url)
            # Verify if we don't have a recipe with the same name already
            if any(recipe["name"] == detailed_recipe["name"] for recipe in recipes):
                continue
            recipes.append(detailed_recipe)
        except RecipeNotFound:
            print(f"No recipe found for '{plat}'")
            continue
        # time.sleep(1 + (index % 3) * 0.5)

    # Enregistrer le résultat dans un fichier JSON
    with open("recipes.json", "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)
