# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import re
import ssl


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

		handler = urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
		opener = urllib.request.build_opener(handler)
		response = opener.open(url)
		html_content = response.read()

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
		return soup.find("span", {"class" : "recipe-header__rating-text"}).get_text().split("/")[0]

	@staticmethod
	def _get_nb_comments(soup):
		"""
		Returns the number of comments on the recipe.
		"""
		return soup.find("div", {"class" : "recipe-header__comment"}).find("a").get_text().strip(' \t\n\r').split(" ")[0]

	@classmethod
	def _get_total_time(cls, soup):
		"""
		Returns the total time for the recipe.
		"""
		return soup.find_all("div", {"class": "recipe-primary__item"})[0].find("span").get_text().strip(' \t\n\r')

	@classmethod
	def _get_difficulty(cls, soup):
		"""
		Returns the difficulty level of the recipe.
		"""
		return soup.find_all("div", {"class": "recipe-primary__item"})[1].find("span").get_text().strip(' \t\n\r')

	@classmethod
	def _get_budget(cls, soup):
		"""
		Returns the budget level of the recipe.
		"""
		return soup.find_all("div", {"class": "recipe-primary__item"})[2].find("span").get_text().strip(' \t\n\r')

	@staticmethod
	def _get_cook_time(soup):
		"""
		Returns the cooking time for the recipe.
		"""
		return soup.find_all(text=re.compile("Cuisson"))[0].parent.next_sibling.next_sibling.get_text()

	@staticmethod
	def _get_prep_time(soup):
		"""
		Returns the preparation time for the recipe.
		"""
		return soup.find_all(text=re.compile("Préparation"))[1].parent.next_sibling.next_sibling.get_text().replace("\xa0", " ")

	@staticmethod
	def _get_recipe_quantity(soup):
		"""
		Returns the recipe quantity or number of servings.
		"""
		divRecipeQuantity = soup.find("div", {"class": "mrtn-recette_ingredients-counter"})
		return divRecipeQuantity["data-servingsnb"] + " " + divRecipeQuantity["data-servingsunit"]

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
			{"name": "ingredients", "default_value": []},
			{"name": "author", "default_value": "Anonyme"},
			{"name": "author_tip", "default_value": ""},
			{"name": "steps", "default_value": []},
			{"name": "images", "default_value": []},
			{"name": "rate", "default_value": ""},
			{"name": "difficulty", "default_value": ""},
			{"name": "budget", "default_value": ""},
			{"name": "cook_time", "default_value": ""},
			{"name": "prep_time", "default_value": ""},
			{"name": "total_time", "default_value": ""},
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
