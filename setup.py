from setuptools import setup

setup(
    name="scraping-marmiton",
    version="0.4.2",
    description="Script permettant de récupérer des recettes du site Marmiton.org",
    packages=["marmiton"],
    url="https://github.com/remaudcorentin-dev/python-marmiton",
    author="Corentin Remaud",
    author_email="remaudcorentin.dev@gmail.com",
    license="MIT",
    zip_safe=False,
    install_requires=["bs4"],
)
