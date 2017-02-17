from recipe_parser.ingredient_tagger import Tagger
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from fractions import Fraction
from recipe_parser.text_to_fraction import Text2Fraction
from recipe_parser.text_to_num import text2num
import re

#  iterates over all subclasses of abstract Tagger, and a cascading tagger using a backoff for the primary (_tagger[-1])
_taggers = sorted(Tagger.__subclasses__(), key=lambda sub_class: getattr(sub_class, 'PRECEDENCE'), reverse=True)
for i in range(len(_taggers)):
    _taggers[i] = _taggers[i].get_tagger(backoff=_taggers[i-1] if i > 0 else None)
TAGGER = _taggers[-1]


LEMMATIZER = WordNetLemmatizer()
TOKENIZER = word_tokenize  # RegexpTokenizer('(?u)\W+|\$[\d\.]+|\S+').tokenize
AMOUNT_PATTERN = re.compile(r'\(.*?\)')
GRAMMAR = r"""
    Amount: {<CD.*>+<.*>*?<MM>?}
            {<CD.*>+.*?<CD>+?}
    NPI:    {<NN|NNS|VB.*|JJ|MOD>+}
            {<DT|PP\$>?<JJ.*|VBN.*|MOD>*<NN>+}
            {<NNP>+}
"""
# functions to try to convert text to numbers. Note that the conversion ends on the first function
TEXT_TO_NUM_CONVERSION_FUNCTIONS = [
    lambda x: Fraction(x[0]),
    lambda x: Text2Fraction.text_to_fraction(x[0]),
    lambda x: text2num(x[0]),
    lambda x: any(i[0] in ['a', 'an', 'single'] for i in x)
]