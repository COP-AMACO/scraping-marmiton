from marmiton import Marmiton, RecipeNotFound
import json
import time

plats = [
    "Spaghetti bolognaise", "Ratatouille", "Tacos al pastor", "Sushi", "Couscous",
    "Pad thaï", "Poulet tikka masala", "Lasagnes", "Boeuf bourguignon", "Falafels",
    "Chili con carne", "Paella", "Ramen", "Burger maison", "Pizza margherita",
    "Gnocchis à la crème", "Soupe pho", "Bibimbap", "Tajine de poulet", "Curry vert thaï",
    "Biryani", "Gratin dauphinois", "Croque-monsieur", "Quiche lorraine", "Tartiflette",
    "Fondue savoyarde", "Bouillabaisse", "Poke bowl", "Moussaka", "Ceviche",
    "Carbonade flamande", "Cassoulet", "Empanadas", "Kefta", "Feijoada",
    "Poutine", "Rôti de porc", "Pâtes carbonara", "Soupe miso", "Okonomiyaki",
    "Kebab", "Salade niçoise", "Taboulé", "Galettes bretonnes", "Crêpes salées",
    "Banh mi", "Polenta au fromage", "Sarma (chou farci)", "Rouleaux de printemps", "Nasi goreng",
    "Laksa", "Katsu curry", "Bulgogi", "Risotto aux champignons", "Sarma turque",
    "Tortilla espagnole", "Fajitas", "Soupe minestrone", "Yakitori", "Boeuf Stroganoff",
    "Choucroute", "Clafoutis salé", "Tandoori", "Mac & cheese", "Wellington végétarien",
    "Lentilles aux saucisses", "Poulet basquaise", "Gaspacho", "Salade de pâtes", "Salade grecque",
    "Riz cantonais", "Tofu sauté", "Gyoza", "Onigiri", "Boulettes suédoises",
    "Hachis parmentier", "Tartare de thon", "Osso buco", "Mafé", "Brochettes de légumes",
    "Tteokbokki", "Calamars frits", "Soupe de potiron", "Salade d’endives", "Galettes de légumes",
    "Chakchouka", "Pain pita garni", "Gratin de courgettes", "Soupe à l’oignon", "Oeufs cocotte",
    "Fish and chips", "Katsu sando", "Riz pilaf", "Poulet au citron", "Harira",
    "Farfalle au pesto", "Bruschetta", "Tortellini ricotta épinards", "Khao pad", "Pizza napolitaine",
    "Kitchari", "Tamagoyaki", "Soupe de lentilles", "Poêlée de légumes", "Croquettes de poisson",
    "Olives marinées", "Tapenade", "Houmous", "Guacamole", "Tzatziki",
    "Nems", "Samoussas", "Mini quiches", "Feuilletés au fromage", "Bruschetta",
    "Rillettes de thon", "Gressins au jambon cru", "Blinis au saumon", "Mini brochettes tomates mozzarella", "Falafels",
    "Empanadas", "Mini croque-monsieur", "Mini burgers", "Oignons frits", "Tortilla roulée au fromage",
    "Beignets de crevettes", "Toasts tapenade et chèvre", "Saucisson sec", "Fromage en cubes", "Chips de légumes",
    "Nuggets de poulet", "Accras de morue", "Gyozas", "Pakoras", "Mini cakes salés",
    "Pois chiches grillés", "Popcorn salé", "Amandes grillées", "Mini rouleaux de printemps", "Mini samoussas légumes",
    "Quesadillas coupées", "Sardines grillées sur toast", "Pain pita et dips", "Mini tartines nordiques", "Crostinis variés",
    "Crackers et fromage", "Mini tacos", "Patatas bravas", "Feuilletés aux épinards", "Tartinade de betterave",
    "Petits roulés jambon fromage", "Tempura de légumes", "Muffins salés", "Toast d’avocat", "Pommes de terre grenaille",
    "Riz sauté aux légumes", "Chili sin carne", "Curry de pois chiches", "Poulet au citron et quinoa",
    "Ratatouille", "Tajine de légumes", "Bibimbap sans sauce soja (ou avec tamari)", "Salade de lentilles",
    "Soupe de potiron au lait de coco", "Galettes de sarrasin aux champignons", "Poisson grillé et patates douces",
    "Boeuf sauté aux légumes", "Salade de quinoa et feta", "Omelette aux herbes", "Soupe miso sans miso d’orge",
    "Homard grillé au beurre citronné", "Risotto aux truffes", "Filet de bœuf Rossini", "Paella aux fruits de mer",
    "Tournedos de bœuf aux morilles", "Sushi au thon rouge et anguille", "Foie gras poêlé sur pain brioché",
    "Côte de veau aux girolles", "Chateaubriand sauce béarnaise", "Carré d’agneau en croûte d’herbes",
    "Noix de Saint-Jacques poêlées au safran", "Canard laqué à la pékinoise", "Coquilles Saint-Jacques gratinées",
    "Wellington de bœuf", "Caviar et blinis de sarrasin", "Tartare de bœuf à l’italienne",
    "Salade caprese", "Soupe froide de concombre", "Velouté de potimarron", "Carpaccio de bœuf", "Carpaccio de saumon",
    "Gaspacho andalou", "Taboulé libanais", "Ceviche de poisson", "Salade de quinoa", "Œufs mimosa",
    "Tartare de thon", "Soupe miso", "Salade de lentilles", "Avocat crevettes", "Salade grecque",
    "Velouté d’asperges", "Soupe de légumes", "Rouleaux de printemps", "Tartine avocat œuf poché", "Salade de crudités",
    "Tzatziki avec pain pita", "Houmous et crudités", "Salade de carottes râpées", "Rillettes de saumon", "Blinis au saumon fumé",
    "Salade de tomates anciennes", "Bruschetta aux légumes", "Mini brochettes de crevettes", "Velouté de courgettes", "Soupe de champignons",
    "Avocat farci au thon", "Tartare de légumes", "Mini tarte fine aux oignons", "Terrine de légumes", "Panna cotta salée au parmesan",
    "Salade de betteraves et chèvre", "Œuf cocotte aux épinards", "Petite quiche aux poireaux", "Crème de petits pois", "Velouté de patates douces",
    "Cappuccino de champignons", "Mini flans de légumes", "Tartelette tomates moutarde", "Caviar d’aubergine", "Salade d’endives aux noix",
    "Betteraves marinées", "Toasts tapenade", "Salade d’artichauts", "Soupe thaï citronnelle", "Mini clafoutis salés",
    "Purée de pommes de terre", "Riz pilaf", "Gratin dauphinois", "Frites maison", "Ratatouille",
    "Légumes rôtis au four", "Polenta crémeuse", "Pâtes à l’huile d’olive et herbes", "Semoule de couscous", "Quinoa aux légumes",
    "Haricots verts à l’ail", "Pommes de terre grenaille", "Purée de patates douces", "Chou sauté à l’asiatique", "Épinards à la crème",
    "Galettes de légumes", "Salade verte croquante", "Boulgour aux herbes", "Maïs grillé", "Champignons sautés",
    "Pesto", "Salsa verde", "Sauce soja sucrée", "Tzatziki", "Chimichurri", "Raita", "Mayonnaise au citron", "Sauce barbecue", "Romesco", 
    "Gremolata", "Sauce au yaourt", "Aïoli", "Sauce moutarde miel", "Sauce tomate épicée", "Pesto rosso", "Sauce aux champignons",
    "Sauce au fromage bleu", "Sauce aux poivrons rouges", "Sauce aux herbes", "Sauce au curry", "Sauce à l’ail rôti",
    "Sauce au poivre vert", "Sauce aux câpres", "Sauce à la moutarde ancienne", "Sauce au fromage blanc", "Ketchup",
    "Tiramisu", "Crème brûlée", "Baklava", "Mochi", "Pavlova", "Tarte Tatin", "Pudding au caramel", "Cheesecake", "Gulab jamun", 
    "Sorbet aux fruits", "Churros", "Cannelés", "Brownie", "Panna cotta", "Clafoutis", "Knafeh", "Riz au lait", "Mille-feuille", 
    "Pastel de nata", "Apple pie", "Beignets", "Tarte au citron meringuée", "Semifreddo", "Éclair au chocolat", "Profiteroles", 
    "Lamington", "Tarte au chocolat", "Banoffee pie", "Glace vanille", "Kouglof", "Trifle", "Flan pâtissier", "Baba au rhum", 
    "Soufflé au chocolat", "Poire Belle-Hélène", "Crêpes Suzette", "Nougat glacé", "Cassata sicilienne", "Strudel aux pommes", 
    "Tapioca au lait de coco", "Mille-crêpes", "Halva", "Charlotte aux fraises", "Kheer", "Gâteau basque", "Mont-Blanc", 
    "Carrot cake", "Tarte à la rhubarbe", "Madeleines", "Brigadeiro"
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
            # Get the details of the first returned recipe
            detailed_recipe = Marmiton.get(main_recipe_url) 
            # Verify if we don't have a recipe with the same name already
            if any(recipe['name'] == detailed_recipe['name'] for recipe in recipes):
                continue
            recipes.append(detailed_recipe)
        except RecipeNotFound as e:
            print(f"No recipe found for '{plat}'")
            continue
        #time.sleep(1 + (index % 3) * 0.5)


    # Enregistrer le résultat dans un fichier JSON
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)
