import re
from nltk import sent_tokenize, RegexpParser
from nltk.tree import Tree
from string import punctuation
from recipe_parser import TAGGER, LEMMATIZER, TOKENIZER, AMOUNT_PATTERN, GRAMMAR, TEXT_TO_NUM_CONVERSION_FUNCTIONS
from recipe_parser.text_to_num import NumberException

AMOUNT_TRANSLATOR = str.maketrans('', '', punctuation)
punctuation = ''.join(c for c in punctuation if c not in '/()')
TEXT_CLEANER = str.maketrans('', '', punctuation)


class ParsedValuesMixin:
    """
    Mixin to allow the instatiating Ingredient and Amount classes with a dict type
    """
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


class Ingredient(ParsedValuesMixin):
    primary = None
    modifier = None


class Amount(ParsedValuesMixin):
    value = None
    unit = None


class ParsedIngredient:
    """
    Class to hold the structure of a parsed ingredient.
    ingredient: An instance of an ingredient
    amount: An instance of an amount
    amounts: A list of Amount type if more than one amount was parsed from the result
    """
    ingredient = None
    amount = None
    amounts = None

    def __init__(self, *args):
        """
        Various arguments are allows that can include a combination of Ingredient, Amount,
        or a variable number of Amount type
        :param args: a single an ingredient and an Amount (or list of Amounts)
        """
        for arg in args:
            if isinstance(arg, Ingredient):
                self.ingredient = arg
            elif isinstance(arg, Amount):
                self.amount = arg
            elif isinstance(arg, list) and len(arg) > 0 and isinstance(arg[0], Amount):
                self.amounts = arg

    def _determine_best_amount(self):
        """
        Function to choose the most appropriate parsed amount. Sets the internal amount member to this selected value.
        :return:
        """
        # TODO determine better way to select amount, based on unit parser
        self.amount = self.amounts[0] if self.amounts else self.amount

    @property
    def parsed_ingredient(self):
        """
        Returns an instance of itself but ensures an amount and ingredient exists (if possible)
        :return:
        """
        if self.amounts and not self.amount:
            self._determine_best_amount()
        return self


class IngredientParser:
    """
    A class to parse text into the desired in gredient format. Uses NLTK principles to tag an ingredient and
    extract an ingredient, its modifiers, and the amount. Utilizes the ingredient_tagger (__init__ TAGGER) for
    POS tagging, and creates partitions into the amount and ingredient using a Regexp of POS tags. Returns a
    ParsedIngredient type
    """
    __instances = dict()

    def __init__(self, grammar):
        self._sentence_parser = RegexpParser(grammar)
        self._pos_tagger = TAGGER

    @classmethod
    def _create_grammar(cls, clean_grammar):
        if clean_grammar not in cls.__instances:
            cls.__instances[clean_grammar] = cls(grammar=clean_grammar)

    @classmethod
    def get_parser(cls, grammar=GRAMMAR):
        clean_grammar = cls._clean_grammar(grammar)
        cls._create_grammar(clean_grammar)
        return cls.__instances[clean_grammar].parse

    def _parse_sentence_tree(self, text):
        tagged_sentences = [self._pos_tagger.tag(s) for s in [TOKENIZER(ss) for ss in sent_tokenize(text)]]
        return self._sentence_parser.parse(tagged_sentences[0])

    @staticmethod
    def _clean_grammar(grammar):
        return grammar.strip()

    def parse(self, text):
        text = text.lower()
        amount_data = [tree[0] if tree.label() == 'S' else tree for tree in
                       [self._parse_sentence_tree(i.translate(AMOUNT_TRANSLATOR)) for i in AMOUNT_PATTERN.findall(text)]
                       ]
        re.sub(AMOUNT_PATTERN, '', text)
        sentence_tree = self._parse_sentence_tree(text.translate(TEXT_CLEANER))
        print(sentence_tree)
        amount_data.extend([i for i in sentence_tree if isinstance(i, Tree) and i.label() == 'Amount'])
        return ParsedIngredient(
            self._find_ingredient(sentence_tree),
            self._find_amounts(amount_data)
        ).parsed_ingredient

    def _find_amounts(self, sentence_tree):
        amounts = []  # find list of CD tags to evaluate
        units = []  # find
        for item in sentence_tree:
            amounts.append(self._convert_from_text(item))
            for tag in item[::-1]:
                if tag[1] == 'MM':
                    units.append(tag[0])
                    break
                units.append('')
        return [Amount(value=a, unit=LEMMATIZER.lemmatize(u)) for a, u in zip(amounts, units)]

    @staticmethod
    def _convert_from_text(amount_tree):
        values = []
        for a in amount_tree:
            if a[1] == 'CD':
                for func in TEXT_TO_NUM_CONVERSION_FUNCTIONS:
                    try:
                        value = func(a)
                        if not value:
                            raise ValueError()
                        values.append(value)
                        break
                    except (ValueError, NumberException):
                        pass
        return sum(values)

    @staticmethod
    def _find_ingredient(sentence_tree):
        for item in sentence_tree[::-1]:
            if isinstance(item, Tree) and item.label() == 'NPI':
                primary = ' '.join(LEMMATIZER.lemmatize(i[0]) for i in item
                                   if i[1] in ['NN', 'NNS', 'VBN'] and i[0] != ' ')
                modifiers = ' '.join(LEMMATIZER.lemmatize(i[0]) for i in item
                                     if i[1] not in ['NN', 'NNS', 'VBN'] and i[0] != ' ')
                return Ingredient(
                    **dict(
                        primary=primary,
                        modifier=modifiers,
                    )
                )
        return None
