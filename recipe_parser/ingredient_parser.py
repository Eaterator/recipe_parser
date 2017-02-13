from nltk import sent_tokenize, word_tokenize, pos_tag, RegexpParser
from nltk.tree import Tree
from nltk.stem import WordNetLemmatizer
from fractions import Fraction
from recipe_parser.text2fraction import Text2Fraction
from recipe_parser.text2num import text2num
import re

# TODO lemmatizer is very slow to load the first time, may need to run this as a service for the actual web app
LEMMATIZER = WordNetLemmatizer()
AMOUNT_PATTERN = re.compile(r'\(.*?\)')
GRAMMAR = r"""
    Amount: {<CD.*>+<DT|PP|JJ>*<NN|NNS>?}

    NPI:    {<NN|NNS|VB.*|JJ>+}
            {<DT|PP\$>?<JJ.*|VBN.*>*<NN>+}
            {<NNP>+}
"""
TEXT_CONVERSION_FUNCTIONS = [
            lambda x: Fraction(x[0]),
            lambda x: Text2Fraction.text_to_fraction(x[0]),
            lambda x: text2num(x[0])
        ]


# may best best roll own numerical converter specialized for
class ParsedValuesMixin:

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


class Ingredient(ParsedValuesMixin):
    primary = None
    modifier = None


class Amount(ParsedValuesMixin):
    value = None
    unit = None


class ParsedIngredient:
    ingredient = None
    amount = None
    amounts = None
    multiple_amounts = False

    def __init__(self, *args):
        for arg in args:
            if isinstance(arg, Ingredient):
                self.ingredient = arg
            elif isinstance(arg, Amount):
                self.amount = arg
            elif isinstance(arg, list) and len(arg) > 0 and isinstance(arg[0], Amount):
                self.amounts = arg

    def _determine_best_amount(self):
        pass

    @property
    def parsed_ingredient(self):
        if self.amounts and not self.amount:
            self._determine_best_amount()
        return self


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
        clean_grammar = cls._clean_grammar(grammar)
        cls._create_grammar(clean_grammar)
        return cls.__instances[clean_grammar].parse

    def _parse_sentence_tree(self, text):
        tagged_sentences = [pos_tag(s) for s in [word_tokenize(ss) for ss in sent_tokenize(text)]]
        return self._sentence_parser.parse(tagged_sentences[0])

    @staticmethod
    def _clean_grammar(grammar):
        return grammar.strip()

    def parse(self, text):
        text = text.lower()
        amount_data = [tree for tree in
                       [self._parse_sentence_tree(i) for i in AMOUNT_PATTERN.findall(text)]
                       if isinstance(tree, Tree) and tree.label() == 'Amount'
                       ]
        re.sub(AMOUNT_PATTERN, '', text)
        sentence_tree = self._parse_sentence_tree(text)
        amount_data.extend([i for i in sentence_tree if isinstance(i, Tree) and i.label() == 'Amount'])
        # tkinter py-3 required for pretty graph of sentence parse tree:
        # sentence_tree.draw()
        # return self._parse_sentence_tree(text)
        return ParsedIngredient(
            self._find_ingredient(sentence_tree),
            self._find_amounts(amount_data)
        )

    def _find_amounts(self, sentence_tree):
        amounts = []  # find list of CD tags to evaluate
        units = []  # find
        for item in sentence_tree:
            amounts.append(self._convert_from_text(item))
            for tag in item[::-1]:
                if tag[1] in ['NN', 'NNS']:
                    units.append(tag[0])
                    break
                units.append(None)

        return [Amount(value=a, unit=LEMMATIZER.lemmatize(u)) for a, u in zip(amounts, units)]

    @staticmethod
    def _convert_from_text(amount_tree):
        values = []
        for a in amount_tree:
            if a[1] == 'CD':
                for func in TEXT_CONVERSION_FUNCTIONS:
                    try:
                        values.append(func(a))
                        break
                    except ValueError:
                        pass
        return sum(values)

    @staticmethod
    def _find_ingredient(sentence_tree):
        for item in sentence_tree[::-1]:
            if isinstance(item, Tree) and item.label() == 'NPI':
                primary = ' '.join(LEMMATIZER.lemmatize(i[0]) for i in item if i[1] in ['NN', 'NNS'])
                modifiers = ' '.join(LEMMATIZER.lemmatize(i[0]) for i in item if i[1] not in ['NN, NNS'])
                return Ingredient(
                    **dict(
                        primary=primary,
                        modifier=modifiers,
                    )
                )
        return None


if __name__ == '__main__':
    parse_func = IngredientParser.get_parser()
    x = parse_func("1 1/2 cup vegetable oil")
