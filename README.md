# API Marmiton (Python)

[![CI](https://github.com/COP-AMACO/scraping-marmiton/actions/workflows/ci.yml/badge.svg)](https://github.com/COP-AMACO/scraping-marmiton/actions/workflows/ci.yml)

Ce projet permet de rechercher et d'obtenir des recettes du site [marmiton.org](https://www.marmiton.org/) via une API Python non officielle (web scraper).

C'est un *fork* d'un projet existant [python-marmiton](https://github.com/remaudcorentin-dev/python-marmiton) développé par [Corentin Remaud](https://github.com/remaudcorentin-dev).


## Installation :

```PowerShell
# PowerShell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Command prompt
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```


## Référence de l'API :

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
| `ingredients`     | `list[dict]`   | Liste des ingrédients avec id, nom, quantité, unités (singulier et pluriel) et image      |
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
| `quantity` | `dict`          | Indication de la quantité pour laquelle la recette est prévue (nombre et unité) |
| `nb_comments`     | `int`       | Nombre de commentaires ou avis laissés par les utilisateurs   |


## Tests et couverture de code :

Ce projet utilise [tox](https://tox.readthedocs.io/) pour automatiser les tests sur différents environnements Python ou pour automatiser les vérifications de code. Pour lancer tous les tests via tox, exécutez simplement :

```bash
tox
```

Il est aussi possible de lancer les tests sur un environnement spécifique pour tester certaines choses en isolation :

```bash
tox -e test
tox -e check_format
tox -e lint
```

#### Tests unitaires :

Les tests unitaires sont utilisés afin de s'assurer du bon fonctionnement des fonctions annexes (`extract_id_from_url`, `parse_duration_to_minutes`, `simplify_string`). Pour exécuter les tests, utilisez la commande suivante :

```bash
# Exécuter tous les tests unitaires
pytest
# Exécuter les tests d'un fichier en particulier
pytest tests/test_parse_duration.py
```

#### Couverture de code :

Vous pouvez également exécuter les tests avec une couverture de code pour voir quelles parties du code sont couvertes par les tests :

```bash
coverage run -m pytest
coverage report -m --fail-under=100
```

*Cette commande produit un rapport détaillé en HTML dans le dossier `htmlcov`.*

#### Format de code :

Le format du code est automatiquement vérifié lors de l'exécution des tests. De plus, il est possible d'utiliser un *hook* de pré-commit pour formater le code avant de le valider. Pour l'activer et l'utiliser manuellement, exécutez la commande suivante :

```bash
pre-commit install
pre-commit run --all-files
```

*NOTE: Il est nécessaire d'avoir installé [pre-commit](https://pre-commit.com/) pour utiliser cette fonctionnalité.*

#### CI/CD :

Le projet utilise GitHub Actions pour automatiser les tests et la vérification du code à chaque *push* ou *pull request* sur la branche `master`.
