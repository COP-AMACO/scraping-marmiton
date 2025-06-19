from marmiton import Marmiton, RecipeNotFound
import json
import time

plats = [
    "Ratatouille",
    "Couscous royal",
    "Sushi",
    "Tartiflette",
    "Pad Thaï",
    "Lasagnes",
    "Chili con carne",
    "Tajine de poulet aux citrons confits",
    "Boeuf bourguignon",
    "Pho",
    "Moussaka",
    "Biryani",
    "Paella",
    "Burger maison",
    "Bibimbap",
    "Quiche lorraine",
    "Soupe miso",
    "Tacos al pastor",
    "Fondue savoyarde",
    "Gnocchis à la sauce gorgonzola",
    "Poulet au curry",
    "Ceviche de poisson",
    "Carbonara",
    "Dal indien",
    "Shakshuka",
    "Poulet Yassa",
    "Fish and chips",
    "Risotto aux champignons",
    "Ramen",
    "Galettes bretonnes",
    "Boeuf Stroganoff",
    "Salade niçoise",
    "Pizza Margherita",
    "Poulet Tikka Masala",
    "Kebab maison",
    "Canelones catalans",
    "Falafels avec houmous",
    "Gâteau de viande (meatloaf)",
    "Gratin dauphinois",
    "Tartare de saumon",
    "Soupe à l'oignon",
    "Tagliatelles au pesto",
    "Curry thaï rouge aux crevettes",
    "Accras de morue",
    "Tempura de légumes",
    "Choucroute garnie",
    "Salade de quinoa aux légumes grillés",
    "Côtelettes d'agneau au romarin",
    "Empanadas",
    "Tarte tomate-moutarde"
]

if __name__ == "__main__":
    recipes = []
    for index, plat in enumerate(plats):
        print(f"[{index + 1}/{len(plats)}] Recherche de la recette pour '{plat}'...")
        query_options = {
            "aqt": plat,  # Query keywords - separated by a white space
        }
        try:
            query_result = Marmiton.search(query_options)
        except RecipeNotFound as e:
            print(f"No recipe found for '{plat}'")
            continue

        if not query_result:
            print(f"No recipe found for '{plat}'")
            continue

        main_recipe_url = query_result[0]['url']

        try:
            detailed_recipe = Marmiton.get(main_recipe_url)  # Get the details of the first returned recipe
        except RecipeNotFound as e:
            print(f"No recipe found for '{plat}'")
            continue
        recipes.append(detailed_recipe)
        time.sleep(1 + (index % 3) * 0.5)


    # Enregistrer le résultat dans un fichier JSON
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)
