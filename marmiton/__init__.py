# -*- coding: utf-8 -*-

import re
import ssl
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

from marmiton.extract_id_from_url import extract_id_from_url
from marmiton.parse_duration import parse_duration_to_minutes
from marmiton.simplify_string import simplify_string


class RecipeNotFound(Exception):
    pass


class Marmiton(object):
    @staticmethod
    def search(query_dict):
        """Search recipes by parsing the returned HTML data.

        Options:
            'aqt': string of keywords separated by a white space (query search)

        Optional options:
            'dt': "accompagnement" | "amusegueule" | "boisson" | "confiserie" |
                  "conseil" | "dessert" | "entree" | "platprincipal" | "sauce"
                  (plate type)

            'exp': 1 | 2 | 3
                   (plate expense: 1 = cheap, 2 = medium, 3 = expensive)

            'dif': 1 | 2 | 3 | 4
                   (recipe difficulty: 1 = very easy, ..., 4 = advanced)

            'prt': 1 | 2 | 3 | 4 | 5
                   (recipe particularity: 1 = vegetarian, 2 = gluten-free,
                   3 = vegan,  4 = lactose-free, 5 = balanced)

            'rct': 1 | 2 | 3 | 4 | 5
                   (cooking type: 1 = Oven, 2 = Stovetop, 3 = No-cook,
                   4 = Microwave, 5 = Barbecue/Plancha)

            'ttlt': 15 | 30 | 45
                    (total time in minutes: <= 15, 30, or 45)
        """

        domain = "https://www.marmiton.org"
        base_url = domain + "/recettes/recherche.aspx?"
        query_url = urllib.parse.urlencode(query_dict)

        url = base_url + query_url

        try:
            handler = urllib.request.HTTPSHandler(
                context=ssl._create_unverified_context()
            )
            opener = urllib.request.build_opener(handler)
            response = opener.open(url)
            html_content = response.read()
        except Exception as e:
            raise RecipeNotFound("Error: " + str(e))

        soup = BeautifulSoup(html_content, "html.parser")

        search_data = []

        articles = soup.find_all("a", href=True)
        articles = [a for a in articles if a["href"].startswith("/recettes/recette_")]

        iterarticles = iter(articles)
        for article in iterarticles:
            data = {}
            try:
                data["name"] = article.get_text().strip(" \t\n\r")
                data["url"] = domain + article["href"]
            except Exception:
                pass
            if data:
                search_data.append(data)
        return search_data

    @staticmethod
    def _get_name(soup):
        """Returns the name of the recipe."""
        return soup.find("h1").get_text().strip(" \t\n\r")

    @staticmethod
    def _get_plate_type(soup):
        """Returns the type of the recipe.

        Plate types are: "accompagnement", "amusegueule", "boisson", "confiserie",
                        "dessert", "entree", "platprincipal", "sauce" or ""
        """
        tagsList = soup.find_all(True, {"class": "modal__tag"})
        for tag in tagsList:
            tagText = tag.get_text().strip(" \t\n\r").lower()
            if tagText == "accompagnement":
                return "accompagnement"
            elif tagText == "amuse-gueule":
                return "amusegueule"
            elif tagText == "boisson":
                return "boisson"
            elif tagText == "confiserie":
                return "confiserie"
            elif tagText == "dessert":
                return "dessert"
            elif tagText == "entrée":
                return "entree"
            elif tagText == "plat principal":
                return "platprincipal"
            elif tagText == "sauce":
                return "sauce"
        return ""

    @staticmethod
    def _get_is_vegetarian(soup):
        """Returns True if the recipe is vegetarian, False otherwise."""
        tagsList = soup.find_all(True, {"class": "modal__tag"})
        for tag in tagsList:
            tagText = tag.get_text().strip(" \t\n\r").lower()
            if tagText == "vegetarian":
                return True
        return False

    @staticmethod
    def _get_is_gluten_free(soup):
        """Returns True if the recipe is gluten-free, False otherwise."""
        tagsList = soup.find_all(True, {"class": "modal__tag"})
        for tag in tagsList:
            tagText = tag.get_text().strip(" \t\n\r").lower()
            if tagText == "gluten free":
                return True
        return False

    @staticmethod
    def _get_is_vegan(soup):
        """Returns True if the recipe is vegan, False otherwise."""
        tagsList = soup.find_all(True, {"class": "modal__tag"})
        for tag in tagsList:
            tagText = tag.get_text().strip(" \t\n\r").lower()
            if tagText == "recettes vegan":
                return True
        return False

    @staticmethod
    def _get_ingredients(soup):
        """Returns a list of ingredients for the recipe. Each item is a dictionary with
        keys:

        - 'id': the ID extracted from image URL or simplified name of the ingredient
        - 'name': the name of the ingredient
        - 'quantity': the quantity of the ingredient
        - 'unit': the unit of measurement for the ingredient
        - 'image': the image URL of the ingredient
        """
        ingredients = []
        for element in soup.find_all("div", {"class": "card-ingredient"}):
            ingredient_name = element.find("span", {"class": "ingredient-name"})
            ingredient_quantity = element.find("span", {"class": "count"})
            ingredient_unit = element.find("span", {"class": "unit"})
            ingredient_img = element.find("img")

            # Return the first image URL of the ingredient. There are multiple pictures
            # resolution, so we take the last one (the biggest one)
            image_url = ""
            if ingredient_img and ingredient_img.get("data-srcset"):
                image_url = (
                    ingredient_img.get("data-srcset")
                    .split(",")[-1]
                    .strip()
                    .split(" ")[0]
                )

            # Extract the name of the ingredient and format it
            # (first letter uppercase, the rest lowercase)
            name = (
                ingredient_name.get_text().strip(" \t\n\r")[:1].upper()
                + ingredient_name.get_text().strip(" \t\n\r")[1:]
                if ingredient_name
                else ""
            )

            # Extract ID from image URL or use simplify_string
            ingredient_id = extract_id_from_url(image_url)
            if ingredient_id is None:
                ingredient_id = simplify_string(name)

            ingredient_quantity = (
                ingredient_quantity.get_text().strip(" \t\n\r")
                if ingredient_quantity
                else None
            )
            if ingredient_quantity == "":
                ingredient_quantity = None
            if ingredient_quantity:
                ingredient_quantity = float(ingredient_quantity)

            unitSingular = (
                ingredient_unit.get("data-unitsingular").strip(" \t\n\r")
                if ingredient_unit
                else ""
            )
            unitPlural = (
                ingredient_unit.get("data-unitplural").strip(" \t\n\r")
                if ingredient_unit
                else ""
            )

            ingredients.append(
                {
                    "id": ingredient_id,
                    "name": name,
                    "quantity": ingredient_quantity,
                    "unit_singular": unitSingular,
                    "unit_plural": unitPlural,
                    "image": image_url,
                }
            )
        return ingredients

    @staticmethod
    def _get_author(soup):
        """Returns the name of the author of the recipe."""
        return (
            soup.find("span", {"class": "recipe-author-note__author-name"})
            .get_text()
            .strip(" \t\n\r")
        )

    @staticmethod
    def _get_author_tip(soup):
        """Returns the author's tip for the recipe."""
        return (
            soup.find("div", {"class": "mrtn-hide-on-print recipe-author-note"})
            .find("i")
            .get_text()
            .replace("\xa0", " ")
            .replace("\r\n", " ")
            .replace("  ", " ")
            .replace("« ", "")
            .replace(" »", "")
        )

    @staticmethod
    def _get_steps(soup):
        """Returns a list of preparation steps for the recipe."""
        return [
            step.parent.parent.find("p").get_text().strip(" \t\n\r")
            for step in soup.find_all("span", text=re.compile("^Étape"))
        ]

    @staticmethod
    def _get_image_recipe(soup):
        """Returns the main image URL of the recipe."""
        # Main picture of the recipe (some recipes do not have a main picture)
        imgComponent = soup.find("img", {"id": "recipe-media-viewer-main-picture"})
        if imgComponent is not None:
            return imgComponent.get("data-src")
        # Return the first thumbnail of the recipe. There are multiple pictures
        # resolution, so we take the last one (the biggest one)
        return (
            soup.find("img", {"id": "recipe-media-viewer-thumbnail-0"})
            .get("data-srcset")
            .split(",")[-1]
            .strip()
            .split(" ")[0]
        )

    @staticmethod
    def _get_images(soup):
        """Returns a list of image URLs associated with the recipe (not only the main
        image of the recipe)."""
        return [
            img.get("data-src")
            for img in soup.find_all("img", {"height": 150})
            if img.get("data-src")
        ]

    @staticmethod
    def _get_rate(soup):
        """Returns the recipe rate as a string."""
        return float(
            soup.find("span", {"class": "recipe-header__rating-text"})
            .get_text()
            .split("/")[0]
        )

    @classmethod
    def _get_difficulty(cls, soup):
        """Returns the difficulty level of the recipe."""
        difficulty_text = (
            soup.find_all("div", {"class": "recipe-primary__item"})[1]
            .find("span")
            .get_text()
            .strip(" \t\n\r")
        )
        if difficulty_text == "très facile":
            return "very_easy"
        elif difficulty_text == "facile":
            return "easy"
        elif difficulty_text == "moyenne":
            return "medium"
        elif difficulty_text == "difficile":
            return "advanced"
        else:
            return ""

    @classmethod
    def _get_budget(cls, soup):
        """Returns the budget level of the recipe."""
        budget_text = (
            soup.find_all("div", {"class": "recipe-primary__item"})[2]
            .find("span")
            .get_text()
            .strip(" \t\n\r")
        )
        if budget_text == "bon marché":
            return "cheap"
        elif budget_text == "moyen":
            return "medium"
        elif budget_text == "assez cher":
            return "expensive"
        else:
            return ""

    @staticmethod
    def _get_cook_time_min(soup):
        """Returns the cooking time for the recipe (in minutes)."""
        cook_time = soup.find_all(text=re.compile("Cuisson"))[
            0
        ].parent.next_sibling.next_sibling.get_text()
        return parse_duration_to_minutes(cook_time)

    @staticmethod
    def _get_prep_time_min(soup):
        """Returns the preparation time for the recipe (in minutes)."""
        preparation_time = (
            soup.find_all(text=re.compile("Préparation"))[1]
            .parent.next_sibling.next_sibling.get_text()
            .replace("\xa0", " ")
        )
        return parse_duration_to_minutes(preparation_time)

    @classmethod
    def _get_total_time_min(cls, soup):
        """Returns the total time for the recipe (in minutes)."""
        total_time = (
            soup.find_all("div", {"class": "recipe-primary__item"})[0]
            .find("span")
            .get_text()
            .strip(" \t\n\r")
        )
        return parse_duration_to_minutes(total_time)

    @staticmethod
    def _get_quantity(soup):
        """Returns the recipe quantity or number of servings."""
        divRecipeQuantity = soup.find(
            "div", {"class": "mrtn-recette_ingredients-counter"}
        )
        return {
            "count": divRecipeQuantity["data-servingsnb"],
            "unit": divRecipeQuantity["data-servingsunit"] or None,
        }

    @staticmethod
    def _get_nb_comments(soup):
        """Returns the number of comments on the recipe."""
        return int(
            soup.find("div", {"class": "recipe-header__comment"})
            .find("a")
            .get_text()
            .strip(" \t\n\r")
            .split(" ")[0]
        )

    @classmethod
    def get(cls, url):
        """'url' from 'search' method.

        ex. "https://www.marmiton.org/recettes/recette_boeuf-bourguignon_18889.aspx"
        """

        try:
            handler = urllib.request.HTTPSHandler(
                context=ssl._create_unverified_context()
            )
            opener = urllib.request.build_opener(handler)
            response = opener.open(url)
            html_content = response.read()
        except urllib.error.HTTPError as e:
            raise RecipeNotFound if e.code == 404 else e

        soup = BeautifulSoup(html_content, "html.parser")

        elements = [
            {"name": "name", "default_value": ""},
            {"name": "plate_type", "default_value": ""},
            {"name": "is_vegetarian", "default_value": False},
            {"name": "is_gluten_free", "default_value": False},
            {"name": "is_vegan", "default_value": False},
            {"name": "ingredients", "default_value": []},
            {"name": "author", "default_value": "Anonyme"},
            {"name": "author_tip", "default_value": ""},
            {"name": "steps", "default_value": []},
            {"name": "image_recipe", "default_value": ""},
            {"name": "images", "default_value": []},
            {"name": "rate", "default_value": 0.0},
            {"name": "difficulty", "default_value": ""},
            {"name": "budget", "default_value": ""},
            {"name": "cook_time_min", "default_value": 0},
            {"name": "prep_time_min", "default_value": 0},
            {"name": "total_time_min", "default_value": 0},
            {"name": "quantity", "default_value": ""},
            {"name": "nb_comments", "default_value": 0},
        ]

        data = {"url": url}
        for element in elements:
            try:
                data[element["name"]] = getattr(cls, "_get_" + element["name"])(soup)
            except Exception:
                data[element["name"]] = element["default_value"]
        return data
