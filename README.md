# API Marmiton (Python)

[![CI](https://github.com/COP-AMACO/scraping-marmiton/actions/workflows/ci.yml/badge.svg)](https://github.com/COP-AMACO/scraping-marmiton/actions/workflows/ci.yml)

Ce projet permet de rechercher et d'obtenir des recettes du site [marmiton.org](https://www.marmiton.org/) via une API Python non officielle (web scraper). 

C'est un *fork* d'un projet existant [python-marmiton](https://github.com/remaudcorentin-dev/python-marmiton) développé par [Corentin Remaud](https://github.com/remaudcorentin-dev).


## Installation :

```PowerShell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```


## Référence de l'API

- Fonction `Marmiton.search` :

Cette fonction permet de simuler une recherche sur le site.

#### Paramètres de recherche :

| Paramètre | Type     | Obligatoire | Description                                   | Valeurs possibles                                                                                                   |
|-----------|----------|-------------|-----------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| `aqt`     | `string` | ✅         | Mots-clés de recherche (séparés par un espace) |                                                                                                                    |
| `dt`      | `string` | ❌         | Type de plat                                   | `accompagnement`, `amusegueule`, `boisson`, `confiserie`, `conseil`, `dessert`, `entree`, `platprincipal`, `sauce` |
| `exp`     | `int`    | ❌         | Prix du plat                                   | `1` (pas cher), `2` (moyen), `3` (cher)                                                                            |
| `dif`     | `int`    | ❌         | Difficulté de la recette                       | `1` (très facile), `2` (facile), `3` (moyenne), `4` (avancée)                                                      |
| `prt`     | `int`    | ❌         | Particularité de la recette                    | `1` (végétarien), `2` (sans gluten), `3` (vegan), `4` (sans lactose), `5` (équilibrée)                             |
| `rct`     | `int`    | ❌         | Type de cuisson                                | `1` (Four), `2` (Plaque), `3` (Sans cuisson), `4` (Micro-ondes), `5` (Barbecue/Plancha)                            |
| `ttlt`    | `int`    | ❌         | Temps total en minutes                         | `15` (≤ 15 minutes), `30` (≤ 30 minutes), `45` (≤ 45 minutes)                                                                                                   |

#### Réponse :

Elle retourne la liste de recettes (dictionnaires) correspondant aux critères de recherche.

| Champ 	    | Type 	   | Description 	                                    |
|---------------|----------|-------------	                                    |
| `name`        | `string` | Nom de la recette            	                    |
| `url`         | `string` | URL du détail de la recette                        |
| `image`       | `string` | Image de la recette (si elle existe)               |
| `rate`        | `float`  | Note de la recette entre 0 et 5 (par défaut 0.0)   |
| `nb_comments` | `int`    | Nombre de commentaire de la recette (par défaut 0) |


- Fonction `Marmiton.get` :

Cette fonction permet d'obtenir les détails d'une recette à partir de son URL. Elle retourne un dictionnaire avec les informations détaillées de la recette.

| Champ             | Type           | Description                                                   |
|-------------------|----------------|---------------------------------------------------------------|
| `url`             | `string`       | URL de la recette détaillée                                   |
| `name`            | `string`       | Nom de la recette                                             |
| `plate_type`      | `string`       | Type de plat (ex : "platprincipal", "entree", etc.)           |
| `is_vegetarian`   | `bool`         | Recette végétarienne ou non                                   |
| `is_gluten_free`  | `bool`         | Recette sans gluten ou non                                    |
| `is_vegan`        | `bool`         | Recette vegan ou non                                          |
| `ingredients`     | `list[dict]`   | Liste des ingrédients avec nom, quantité, unité et image      |
| `author`          | `string`       | Nom de l'auteur de la recette                                 |
| `author_tip`      | `string`       | Astuce ou note laissée par l'auteur                           |
| `steps`           | `list[string]` | Liste des étapes de la recette                                |
| `image_recipe`    | `string`       | Image principale de la recette (URL)                          |
| `images`          | `list[string]` | Liste d'images de la recette ou des ingrédients (URL)         |
| `rate`            | `float`        | Note de la recette sur 5                                      |
| `difficulty`      | `string`       | Catégorie de difficulté                                       |
| `budget`          | `string`       | Catégorie de budget                                           |
| `cook_time_min`   | `int`          | Temps de cuisson de la recette en minutes                     |
| `prep_time_min`   | `int`          | Temps de préparation estimé en minutes                        |
| `total_time_min`  | `int`          | Temps total estimé (cuisson + préparation) en minutes         |
| `recipe_quantity` | `str`          | Indication de la quantité pour laquelle la recette est prévue |
| `nb_comments`     | `string`       | Nombre de commentaires ou avis laissés par les utilisateurs   |
