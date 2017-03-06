from distutils.core import setup
from setuptools import find_packages

setup(
    name='recipe-parser',
    version='0.1',
    description="Parser for ingredients and quantities in a recipe using NLTK and heuristics",
    url="https://github.com/Eaterator/recipe_parser",
    author="Lucas Currah",
    license="MIT",
    keywords="recipe ingredient quantity cooking parser",
    packages=find_packages(exclude=['tests*', 'docs'])
)
