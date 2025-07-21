import json

from marmiton import Marmiton, RecipeNotFound
from plats import PLATS


def scrape_recipes():
    """Scrapes recipes from Marmiton website based on the PLATS list.

    Returns:
        list: List of scraped recipes
    """
    print("=" * 50)
    print("SCRAPING DES RECETTES MARMITON")
    print("=" * 50)

    recipes = []
    for index, plat in enumerate(PLATS):
        print(f"\t[{index + 1}/{len(PLATS)}] Recherche de la recette pour '{plat}'...")
        query_options = {
            "aqt": plat,  # Query keywords - separated by a white space
        }
        try:
            query_result = Marmiton.search(query_options)
        except RecipeNotFound:
            print(f"\tNo recipe found for '{plat}'")
            continue

        if not query_result:
            print(f"\tNo recipe found for '{plat}'")
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
            print(f"\tNo recipe found for '{plat}'")
            continue

    # Save the result to a JSON file
    try:
        with open("recipes.json", "w", encoding="utf-8") as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"\tErreur lors de l'enregistrement des recettes : {e}")
    return recipes


def extract_unique_ingredients(recipes):
    """Extracts all unique ingredients from recipes and saves them to ingredients.json.

    Args:
        recipes (list): List of recipe dictionaries
    """
    print("\n" + "=" * 50)
    print("EXTRACTION DES INGRÉDIENTS UNIQUES")
    print("=" * 50)

    # Iterate through all recipes
    seen_ingredient_ids = set()  # Set to store IDs of ingredients already seen
    unique_ingredients = []
    for recipe in recipes:
        ingredients = recipe.get("ingredients", [])
        # Iterate through all ingredients in the recipe
        for ingredient in ingredients:
            ingredient_id = ingredient.get("id")
            # If the ingredient hasn't been seen yet, add it
            if ingredient_id and ingredient_id not in seen_ingredient_ids:
                seen_ingredient_ids.add(ingredient_id)
                unique_ingredients.append(
                    {
                        "id": ingredient.get("id", ""),
                        "name": ingredient.get("name", ""),
                        "image": ingredient.get("image", ""),
                    }
                )
    # Sort the list by ingredient name
    unique_ingredients.sort(key=lambda x: x["name"].lower())

    # Calculate the average length of IDs
    if unique_ingredients:
        avg_id_length = sum(len(ing["id"]) for ing in unique_ingredients) / len(
            unique_ingredients
        )
        print(f"\tLongueur moyenne des id : {avg_id_length:.2f}")

    # Save to ingredients.json
    try:
        with open("ingredients.json", "w", encoding="utf-8") as f:
            json.dump(unique_ingredients, f, ensure_ascii=False, indent=2)
        print(f"\t{len(unique_ingredients)} ingrédients uniques sauvegardés")
    except Exception as e:
        print(f"\tErreur lors de la sauvegarde des ingrédients : {e}")


if __name__ == "__main__":
    recipes = scrape_recipes()
    extract_unique_ingredients(recipes)
