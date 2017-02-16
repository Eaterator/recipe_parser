import nltk
from abc import ABCMeta, abstractclassmethod
from nltk.tag import SequentialBackoffTagger

MEASUREMENT_TAG = 'MM'
FRACTION_TAG = 'CD'
KEY_MODIFIERS = ['.', 's']
MAIN_INGREDIENT_TAG = 'NN'


class Tagger:
    """
    General abstract class allowing for class wrappers around taggers. The __isntance attribute is used to create and
    initialize the tagger to ensure setup only occurs once on package import. _create_tagger initializes the tagger,
    and get_tagger returns an instance of the tagger.
    """
    __metaclass__ = ABCMeta

    @abstractclassmethod
    def get_tagger(cls, backoff=None):
        raise NotImplementedError()

    @abstractclassmethod
    def _create_tagger(cls):
        raise NotImplementedError()


class DefaultTagger(Tagger):
    """
    Default tagger defaults to nltk treebank tagger for all other tags.
    """
    __tagger = None

    @classmethod
    def get_tagger(cls, backoff=None):
        if not cls.__tagger:
            cls._create_tagger(backoff=backoff)
        return cls.__tagger

    @classmethod
    def _create_tagger(cls, backoff=None):
        cls.__tagger = nltk.data.load('taggers/maxent_treebank_pos_tagger/english.pickle')
        cls.__tagger._taggers = [cls.__tagger]


class NumericalTagger(Tagger):
    """
    This tagger assures that numbers and fractions are tagged with the proper label.
    """
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
    """
    Tagger chooses a subset of very common ingredients and ensures that they are tagged as nouns.
    """
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
    """
    Provides an interface wrapper around an extended NLTK SeqeuntialBackoffTagger that uses look-ahead in the token
    string to implement a rough bigram tagger. Use case is for where modifiers are necessary for an ingredeint. I.e.
    red pepper as opposed to red potato.
    """
    __tagger = None

    @classmethod
    def get_tagger(cls, backoff=None):
        if not cls.__tagger:
            cls._create_tagger(backoff=backoff)
        return cls.__tagger

    @classmethod
    def _create_tagger(cls, backoff=None):
        model = set()
        for word in BIGRAM_INGREDIENTS:
            model.add(word)
        cls.__tagger = cls.BigramTagger(model, backoff=backoff)

    class BigramTagger(SequentialBackoffTagger):
        """
        Extends NLTK sequential tagger by calling base __init__ and uses a model where any token occuring before the
        model is tagged as a Noun as well. I.e. pepper is in the BIGRAM word so in 'x y z pepper', z will always be
        tagged as a noun.
        """

        def __init__(self, model, backoff=None):
            self._model = model
            self._taggers = [self]
            SequentialBackoffTagger.__init__(self, backoff)

        def choose_tag(self, tokens, index, history):
            if index < len(tokens) - 1:
                if tokens[index+1] in self._model:
                    return MAIN_INGREDIENT_TAG
            return None


class IngredientRegexpTagger(Tagger):
    """
    Regexp tagger that converts ingredient modifiers like 'chopped' and 'boneless' into the desired format (i.e.
    not nouns) so that they are not included as the primary ingredients.
    """
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
    """
    A class that could implement conversion utilities. This will come in hand to implement a common base unit for
    determining the importance of the ingredient in the recipe, prioritizing the ingredients that make up the bulk
    of the recipe by mass.
    """
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
    'pepper',
    'onions',
]

# TODO implement a conversion utility here?
CONVERSIONS = {
}
