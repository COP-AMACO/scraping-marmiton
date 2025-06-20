# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import re
import ssl

from marmiton.parse_duration import parse_duration_to_minutes


class RecipeNotFound(Exception):
	pass


class Marmiton(object):

	@staticmethod
	def search(query_dict):
		"""
		Search recipes parsing the returned html data.
		Options:
			'aqt': string of keywords separated by a white space  (query search)
		Optional options :
			'dt': "accompagnement" | "amusegueule" | "boisson" | "confiserie" | "conseil" | "dessert" | "entree" | "platprincipal" | "sauce"  (plate type)
			'exp': 1 | 2 | 3  (plate expense 1: cheap, 3: expensive)
			'dif': 1 | 2 | 3 | 4  (recipe difficultie 1: very easy, 4: advanced)
			'prt': 1 | 2 | 3 | 4 | 5  (recipe particularity 1: vegetarian, 2: gluten-free, 3: vegan, 4: lactose-free, 5: balanced recipes)
			'rct': 1 | 2 | 3 | 4 | 5  (cooking type: 1: Oven, 2: Stovetop, 3: No-cook, 4: Microwave, 5: Barbecue/Plancha)
			'ttlt': 15 | 30 | 45  (total time in minutes: less than or equal to 15, 30, or 45)
		"""
		base_url = "http://www.marmiton.org/recettes/recherche.aspx?"
		query_url = urllib.parse.urlencode(query_dict)

		url = base_url + query_url

		try:
			handler = urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
			opener = urllib.request.build_opener(handler)
			response = opener.open(url)
			html_content = response.read()
		except Exception as e:
			raise RecipeNotFound("Error: " + str(e))

		soup = BeautifulSoup(html_content, 'html.parser')

		search_data = []

		articles = soup.find_all("a", href=True)
		articles = [a for a in articles if a["href"].startswith("https://www.marmiton.org/recettes/recette")]

		iterarticles = iter(articles)
		for article in iterarticles:
			data = {}
			try:
				data["name"] = article.find("h4").get_text().strip(' \t\n\r')
				data["url"] = article['href']
				try:
					data["rate"] = article.find("span").get_text().split("/")[0]
				except Exception as e0:
					pass
				try:
					data["image"] = article.find('img')['data-src']
				except Exception as e1:
					try:
						data["image"] = article.find('img')['src']
					except Exception as e1:
						pass
					pass
			except Exception as e2:
				pass
			if data:
				search_data.append(data)

		return search_data

	@staticmethod
	def _get_name(soup):
		"""
		Returns the name of the recipe.
		"""
		return soup.find("h1").get_text().strip(' \t\n\r')
	
	@staticmethod
	def _get_type(soup):
		"""
		Returns the type of the recipe.
		Types are: "accompagnement", "amusegueule", "boisson", "confiserie", "dessert", "entree", "platprincipal", "sauce" or ""
		"""
		tagsList = soup.find_all(True, {"class": "modal__tag"})
		for tag in tagsList:
			tagText = tag.get_text().strip(' \t\n\r').lower()
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
		"""
		Returns True if the recipe is vegetarian, False otherwise.
		"""
		tagsList = soup.find_all(True, {"class": "modal__tag"})
		for tag in tagsList:
			tagText = tag.get_text().strip(' \t\n\r').lower()
			if tagText == "vegetarian":
				return True
		return False
	
	@staticmethod
	def _get_is_gluten_free(soup):
			"""
			Returns True if the recipe is gluten-free, False otherwise.
			"""
			tagsList = soup.find_all(True, {"class": "modal__tag"})
			for tag in tagsList:
					tagText = tag.get_text().strip(' \t\n\r').lower()
					if tagText == "gluten free":
							return True
			return False

	@staticmethod
	def _get_is_vegan(soup):
			"""
			Returns True if the recipe is vegan, False otherwise.
			"""
			tagsList = soup.find_all(True, {"class": "modal__tag"})
			for tag in tagsList:
					tagText = tag.get_text().strip(' \t\n\r').lower()
					if tagText == "recettes vegan":
							return True
			return False

	@staticmethod
	def _get_ingredients(soup):
		"""
		Returns a list of ingredients for the recipe.
		"""
		return [item.get_text().strip(' \t\n\r').replace("\xa0", " ") for item in soup.find_all("span", {"class": "ingredient-name"})]

	@staticmethod
	def _get_author(soup):
		"""
		Returns the name of the author of the recipe.
		"""
		return soup.find("span", {"class": "recipe-author-note__author-name"}).get_text().strip(' \t\n\r')

	@staticmethod
	def _get_author_tip(soup):
		"""
		Returns the author's tip for the recipe.
		"""
		return soup.find("div", {"class": "mrtn-hide-on-print recipe-author-note"}).find("i").get_text().replace("\xa0", " ").replace("\r\n", " ").replace("  ", " ").replace("« ", "").replace(" »", "")

	@staticmethod
	def _get_steps(soup):
		"""
		Returns a list of preparation steps for the recipe.
		"""
		return [step.parent.parent.find("p").get_text().strip(' \t\n\r') for step in soup.find_all("span", text=re.compile("^Étape"))]

	@staticmethod
	def _get_image_recipe(soup):
		"""
		Returns the main image URL of the recipe.
		"""
		# Main picture of the recipe (some recipes do not have a main picture)
		imgComponent = soup.find("img", {"id": "recipe-media-viewer-main-picture"})
		if imgComponent is not None:
			return imgComponent.get("data-src")
		# Return the first thumbnail of the recipe
		# There are multiple pictures resolution, so we take the last one (the biggest one)
		return soup.find("img", {"id": "recipe-media-viewer-thumbnail-0"}).get("data-srcset").split(",")[-1].strip().split(" ")[0]
	
	@staticmethod
	def _get_images(soup):
		"""
		Returns a list of image URLs associated with the recipe (not only the main image of the recipe).
		"""
		return [img.get("data-src") for img in soup.find_all("img", {"height": 150}) if img.get("data-src")]

	@staticmethod
	def _get_rate(soup):
		"""
		Returns the recipe rate as a string.
		"""
		return float(soup.find("span", {"class" : "recipe-header__rating-text"}).get_text().split("/")[0])

	@classmethod
	def _get_difficulty(cls, soup):
		"""
		Returns the difficulty level of the recipe.
		"""
		difficulty_text = soup.find_all("div", {"class": "recipe-primary__item"})[1].find("span").get_text().strip(' \t\n\r')
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
		"""
		Returns the budget level of the recipe.
		"""
		budget_text = soup.find_all("div", {"class": "recipe-primary__item"})[2].find("span").get_text().strip(' \t\n\r')
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
		"""
		Returns the cooking time for the recipe (in minutes).
		"""
		cook_time = soup.find_all(text=re.compile("Cuisson"))[0].parent.next_sibling.next_sibling.get_text()
		return parse_duration_to_minutes(cook_time)

	@staticmethod
	def _get_prep_time_min(soup):
		"""
		Returns the preparation time for the recipe (in minutes).
		"""
		preparation_time = soup.find_all(text=re.compile("Préparation"))[1].parent.next_sibling.next_sibling.get_text().replace("\xa0", " ")
		return parse_duration_to_minutes(preparation_time)
	
	@classmethod
	def _get_total_time_min(cls, soup):
		"""
		Returns the total time for the recipe (in minutes).
		"""
		total_time = soup.find_all("div", {"class": "recipe-primary__item"})[0].find("span").get_text().strip(' \t\n\r')
		return parse_duration_to_minutes(total_time)

	@staticmethod
	def _get_recipe_quantity(soup):
		"""
		Returns the recipe quantity or number of servings.
		"""
		divRecipeQuantity = soup.find("div", {"class": "mrtn-recette_ingredients-counter"})
		return divRecipeQuantity["data-servingsnb"] + " " + divRecipeQuantity["data-servingsunit"]
	
	@staticmethod
	def _get_nb_comments(soup):
		"""
		Returns the number of comments on the recipe.
		"""
		return int(soup.find("div", {"class" : "recipe-header__comment"}).find("a").get_text().strip(' \t\n\r').split(" ")[0])

	@classmethod
	def get(cls, url):
		"""
		'url' from 'search' method.
		 ex. "https://www.marmiton.org/recettes/recette_boeuf-bourguignon_18889.aspx"
		"""

		try:
			handler = urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
			opener = urllib.request.build_opener(handler)
			response = opener.open(url)
			html_content = response.read()
		except urllib.error.HTTPError as e:
			raise RecipeNotFound if e.code == 404 else e

		soup = BeautifulSoup(html_content, 'html.parser')

		elements = [
			{"name": "name", "default_value": ""},
			{"name": "type", "default_value": ""},
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
			{"name": "recipe_quantity", "default_value": ""},
			{"name": "nb_comments", "default_value": 0},
		]

		data = {"url": url}
		for element in elements:
			try:
				data[element["name"]] = getattr(cls, "_get_" + element["name"])(soup)
			except:
				data[element["name"]] = element["default_value"]
		return data
