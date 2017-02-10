from nltk import sent_tokenize, word_tokenize, pos_tag, RegexpParser
from fractions import Fraction
import re

GRAMMAR = r"""
    NPI: {<DT|PP\$>?<JJ>*<NN>}
        {<NNP>+}
    Amount: {<CD>*<DT|CC>*?<NN>?}
"""
# TODO need to consider non-numerical numbers (i.e. one, two) and also 'half'
# text2num will work for numerical words, but doesn't implement fractions
#
# may best best roll own numerical converter specialized for


class Ingredient:
    primary = None
    Modifier = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Amount:
    value = None
    unit = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ParsedIngredient:
    ingredient = Ingredient()
    amount = Amount()

    def __init__(self, *args):
        for arg in args:
            if isinstance(arg, Ingredient):
                self.ingredient = arg
            elif isinstance(arg, Amount):
                self.amount = arg


class IngredientParser:

    __instances = dict()

    def __init__(self, grammar):
        self._sentence_parser = RegexpParser(grammar)

    @classmethod
    def _create_grammar(cls, clean_grammar):
        if clean_grammar not in cls.__instances:
            cls.__instances[clean_grammar] = cls(grammar=clean_grammar)

    @classmethod
    def get_parser(cls, grammar=GRAMMAR):
        clean_grammar = cls._clean_grammer(grammar)
        cls._create_grammar(clean_grammar)
        return cls.__instances[clean_grammar].parse

    def _parse_sentence_tree(self, text):
        tagged_sentences = [pos_tag(s) for s in [word_tokenize(ss) for ss in sent_tokenize(text)]]
        return self._sentence_parser.parse(tagged_sentences[0])

    @staticmethod
    def _clean_grammer(grammar):
        return grammar.strip()

    def parse(self, text):
        sentence_tree = self._parse_sentence_tree(text)
        return ParsedIngredient(
            self._find_ingredient(sentence_tree),
            self._find_amount(sentence_tree)
        )
        # print(sentence_tree)
        # tkinter py-3 required for pretty graph of sentence parse tree:
        # sentence_tree.draw()

    @staticmethod
    def _find_amount(sentence_tree):
        amounts = None  # find list of CD tags to evaluate
        unit = None  # find
        try:
            amount = sum([float(Fraction(a) for a in amounts)])
        except ValueError:
            amount = (text2num(' '.join(amounts)))
        return Amount(
            **dict(
                value=amount,
                unit=unit,
            )
        )

    @staticmethod
    def _find_ingredient(sentence_tree):
        ingredient = None
        modifiers = []
        return Ingredient(
            **dict(
                primary=ingredient,
                modifiers=modifiers
            )
        )


if __name__ == '__main__':
    parse_func = IngredientParser.get_parser()
    parse_func("1 1/2 cup vegetable oil")
