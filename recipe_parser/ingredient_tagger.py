import nltk
from abc import ABCMeta, abstractclassmethod

MEASUREMENT_TAG = 'MM'
FRACTION_TAG = 'CD'
KEY_MODIFIERS = ['.', 's']
MAIN_INGREDIENT_TAG = 'NN'


class Tagger:
    __metaclass__ = ABCMeta

    @abstractclassmethod
    def get_tagger(cls, backoff=None):
        raise NotImplementedError()

    @abstractclassmethod
    def _create_tagger(cls):
        raise NotImplementedError()


class DefaultTagger(Tagger):
    __tagger = None

    @classmethod
    def get_tagger(cls, backoff=None):
        if not cls.__tagger:
            cls._create_tagger(backoff=backoff)
        return cls.__tagger

    @classmethod
    def _create_tagger(cls, backoff=None):
        cls.__tagger = nltk.data.load('taggers/maxent_treebank_pos_tagger/english.pickle')


class NumericalTagger(Tagger):
    __tagger = None

    @classmethod
    def get_tagger(cls, backoff=None):
        if not cls.__tagger:
            cls._create_tagger(backoff=backoff)
        return cls.__tagger

    @classmethod
    def _create_tagger(cls, backoff=None):
        model = {}
        for fraction in NUMERICAL:
            model[fraction] = FRACTION_TAG
        for i in range(50):
            model[str(i)] = FRACTION_TAG
        cls.__tagger = nltk.tag.UnigramTagger(model=model, backoff=backoff)


class MainIngredientTagger(Tagger):
    __tagger = None

    @classmethod
    def get_tagger(cls, backoff=None):
        if not cls.__tagger:
            cls._create_tagger(backoff=backoff)
        return cls.__tagger

    @classmethod
    def _create_tagger(cls, backoff=None):
        model = {}
        for ingredient in MAIN_INGREDIENTS:
            model[ingredient] = MAIN_INGREDIENT_TAG
        cls.__tagger = nltk.tag.UnigramTagger(model=model, backoff=backoff)


class BigramIngredientTagger(Tagger):
    __tagger = None

    @classmethod
    def get_tagger(cls, backoff=None):
        if not cls.__tagger:
            cls._create_tagger(backoff=backoff)
        return cls.__tagger

    @classmethod
    def _create_tagger(cls, backoff=None):
        model = {}
        for ingredient in BIGRAM_INGREDIENTS:
            model[ingredient] = MAIN_INGREDIENT_TAG
        cls.__tagger = nltk.tag.BigramTagger(model=model, backoff=backoff)


class IngredientRegexpTagger(Tagger):
    __tagger = None
    patterns = [
        (r'.*ing$', 'VB'),
        (r'.*ed', 'MOD'),
        (r'.*less', 'JJ')
    ]

    @classmethod
    def get_tagger(cls, backoff=None):
        if not cls.__tagger:
            cls._create_tagger(backoff=backoff)
        return cls.__tagger

    @classmethod
    def _create_tagger(cls, backoff=None):
        cls.__tagger = nltk.tag.RegexpTagger(cls.patterns, backoff=backoff)


class MeasurementTagger(Tagger):
    __tagger = None

    @classmethod
    def get_tagger(cls, backoff=None):
        if not cls.__tagger:
            cls._create_tagger(backoff=backoff)
        return cls.__tagger

    @classmethod
    def _create_tagger(cls, backoff=None):
        model = {}
        for key, item_list in MEASUREMENTS.items():
            cls._add_modified_key_to_dict(model, item_list + [key])
        cls.__tagger = nltk.tag.UnigramTagger(model=model, backoff=backoff)

    @staticmethod
    def _add_modified_key_to_dict(model, item_list, key_modifiers=KEY_MODIFIERS):
        for item in item_list:
            model[item] = MEASUREMENT_TAG
            for m in key_modifiers:
                model[item+m] = MEASUREMENT_TAG


class Unit:

    def __init__(self, *args, **kwargs):
        pass

    def convert(self):
        pass


MEASUREMENTS = {
    'gill': [
        'gill',
    ],
    'ounce': [
        'fluid ounce',
        'ounce',
        'oz',
    ],
    'tablespoon': [
        'T',
        'tbl',
        'tbs',
        'tbsp',
    ],
    'teaspoon': [
        't',
        'tsp',
    ],
    'cup': [
        'c',
    ],
    'pint': [
        'p',
        'pt',
        'fl pt',
        'fluid pint',
    ],
    'quart': [
        'q',
        'qt',
        'fl qt',
        'fluid quart',
    ],
    'gallon': [
        'g',
        'gal'
    ],
    'millilitre': [
        'milliliter',
        'ml',
        'cc',
    ],
    'litre': [
        'liter',
        'l'
    ],
    'decilitre': [
        'dl',
        'deciliter',
    ],
    'pound': [
        'lb',
        '#',
    ],
    'milligram': [
        'milligramme',
        'mg',
    ],
    'gram': [
        'g',
        'gramme',
    ],
    'kilogram': [
        'kilogramme',
        'kg',
    ],
    'pinch': [
        'pinches',
    ],
    'dash': [
        'dashes',
    ],
    'touch': [
        'touches',
    ],
    'handful': [
    ],
    'taste': [
    ],
    'can': [
    ],
    'stick': [
    ],
    'a': [
        'an',
        'single',
        'couple',
    ]
}

NUMERICAL = [
    '1/2',
    '1/4',
    '1/5',
    '1/6',
    '1/7',
    '1/8',
    '1/9',
    '1/10',
    'half',
    'halfs',
    'halve',
    'halves',
    'quarter',
    'quarters',
    'fifth',
    'fifths',
    'sixth',
    'sixths',
    'eighth',
    'eigths',
    'one half',
    'one quarter',
]

MAIN_INGREDIENTS = [
    'chicken',
    'beef',
    'shrimp',
    'veal',
    'quail',
    'poultry',
    'scallops',
    'prawns',
    'fish',
    'salmon',
    'halibut',
    'tuna',
    'steak',
    'potatoes',
    'potato',
]

BIGRAM_INGREDIENTS = [
    (('green',), 'pepper'),
    (('red',), 'pepper'),
]

# TODO implement a conversion utility here?
CONVERSIONS = {
}
