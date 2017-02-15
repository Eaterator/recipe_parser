from recipe_parser.ingredient_tagger import MeasurementTagger, IngredientRegexpTagger, DefaultTagger, NumericalTagger,\
    MainIngredientTagger, BigramIngredientTagger
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, sent_tokenize
from fractions import Fraction
from recipe_parser.text2fraction import Text2Fraction
from recipe_parser.text2num import text2num
import re


default_tagger = DefaultTagger.get_tagger()
regexp_tagger = IngredientRegexpTagger.get_tagger(backoff=default_tagger)
fraction_tagger = NumericalTagger.get_tagger(backoff=regexp_tagger)
main_ingredient_tagger = MainIngredientTagger.get_tagger(backoff=fraction_tagger)
bigram_ingredient_tagger = BigramIngredientTagger.get_tagger(backoff=main_ingredient_tagger)
TAGGER = MeasurementTagger.get_tagger(backoff=bigram_ingredient_tagger)

LEMMATIZER = WordNetLemmatizer()
TOKENIZER = word_tokenize  # RegexpTokenizer('(?u)\W+|\$[\d\.]+|\S+').tokenize  # word_tokenize
AMOUNT_PATTERN = re.compile(r'\(.*?\)')
GRAMMAR = r"""
    Amount: {<CD.*>+<.*>*?<MM>?}
            {<CD.*>+.*?<CD>+?}
    NPI:    {<NN|NNS|VB.*|JJ|MOD>+}
            {<DT|PP\$>?<JJ.*|VBN.*|MOD>*<NN>+}
            {<NNP>+}
"""
TEXT_TO_NUM_CONVERSION_FUNCTIONS = [
    lambda x: Fraction(x[0]),
    lambda x: Text2Fraction.text_to_fraction(x[0]),
    lambda x: text2num(x[0]),
    lambda x: any(i[0] in ['a', 'an'] for i in x)
]