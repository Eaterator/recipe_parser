from unittest import TestCase, main as run_tests
from recipe_parser import TAGGER
from recipe_parser.ingredient_tagger import MEASUREMENT_TAG as MEASUREMENT, FRACTION_TAG as FRACTION,\
    MAIN_INGREDIENT_TAG as MAIN_INGREDIENT
from recipe_parser import TOKENIZER, sent_tokenize
from recipe_parser.ingredient_tagger import MEASUREMENTS, NUMERICAL
from random import Random

RANDOM_SEED = 42
RAND = Random()
RAND.seed(RANDOM_SEED)
RANDOM_TEST_SIZE = 100
DEBUG_PRINT = False


class TestIngredientTagger(TestCase):

    def setUp(self):
        self.tagger = TAGGER

    def test_specific_tagging_rules(self):
        for text, expected in zip(TAGGING_INPUT, EXPECTED_TAGS):
            tagged = [self.tagger.tag(s) for s in [TOKENIZER(ss) for ss in sent_tokenize(text)]][0]
            if DEBUG_PRINT:
                print(tagged)
            self.assertEqual(tuple(i[1] for i in tagged), expected)

    def test_automated_tagging_rules(self):
        for _ in range(RANDOM_TEST_SIZE):
            text = ' '.join([
                RAND.choice(RANDOM_AMOUNTS),
                RAND.choice(RANDOM_UNITS),
                RAND.choice(RANDOM_MODIFIERS),
                RAND.choice(RANDOM_INGREDIENTS)
            ])
            tagged = [self.tagger.tag(s) for s in [TOKENIZER(ss) for ss in sent_tokenize(text)]][0]

            if DEBUG_PRINT:
                print(tagged)
            self.assertTrue(tagged[0][1] == FRACTION)
            self.assertTrue(tagged[1][1] == MEASUREMENT)
            self.assertTrue(tagged[2][1] not in ['CD', 'MM'])
            self.assertTrue(tagged[-1][1] in ['NN', 'NNS'])


TAGGING_INPUT = [
    '1/2 cup vegetable oil',                # 1
    '2 cups of vegetable oil',              # 2
    'pinch of salt',                        # 3
    'litre of water',                       # 4
    'liter of chicken stock',               # 5
    '5 quarts of stock',                    # 6
    'an egg',                               # 7
    'a melon',                              # 8
    '5 chicken bullion cubes',              # 9
    '5 skinless boneless chicken breasts'   # 10
]

EXPECTED_TAGS = [
    (FRACTION, MEASUREMENT, 'JJ', 'NN'),            # 1
    (FRACTION, MEASUREMENT, 'IN', 'JJ', 'NN'),      # 2
    (MEASUREMENT, 'IN', 'NN'),                      # 3
    (MEASUREMENT, 'IN', 'NN'),                      # 4
    (MEASUREMENT, 'IN', MAIN_INGREDIENT, 'NN'),     # 5
    (FRACTION, MEASUREMENT, 'IN', 'NN'),            # 6
    (MEASUREMENT, 'NN'),                            # 7
    (MEASUREMENT, 'NN'),                            # 8
    (FRACTION, MAIN_INGREDIENT, 'NN', 'NNS'),       # 9
    (FRACTION, 'JJ', 'JJ', MAIN_INGREDIENT, 'NNS')  # 10
]

RANDOM_AMOUNTS = []
for item in NUMERICAL:
    if len(item.split()) < 2:
        RANDOM_AMOUNTS.append(item)

RANDOM_UNITS = []
for key, items in MEASUREMENTS.items():
    RANDOM_UNITS.append(key)
    for item in items:
        if len(item.split()) < 2:
            RANDOM_UNITS.append(item)

RANDOM_MODIFIERS = [
    'chopped',
    'finely',
    'chopped',
    'boneless',
    'skinless',
    'large',
]

RANDOM_INGREDIENTS = [
    'chicken',
    'beef',
    'fish',
    'stock',
    'steak',
    'flank steak',
    'bullion cubes',
    'onions',
    'red peppers'
]

if __name__ == '__main__':
    run_tests()
