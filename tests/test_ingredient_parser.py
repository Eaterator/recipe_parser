from unittest import TestCase, main as run_tests
from recipe_parser.ingredient_parser import IngredientParser

DEBUG_PRINT = True


class TestIngredientParser(TestCase):

    def setUp(self):
        self.parser = IngredientParser.get_parser()

    # def test_text_to_fraction(self):
    #     pass
    #
    # def test_text_to_number(self):
    #     pass
    #
    # def test_fraction_to_number(self):
    #     pass

    def test_ingredient_parser(self):
        for ingredient_text, expected_ingredient, expected_amount in \
                zip(TEST_INGREDIENTS, EXPECTED_INGREDIENTS, EXPECTED_AMOUNTS):
            if DEBUG_PRINT:
                print('test case: ' + ingredient_text)
            parsed_ingredient = self.parser(ingredient_text)
            ingredient_data = parsed_ingredient.parsed_ingredient
            if DEBUG_PRINT:
                print('Ingredient Primary : {0}'.format(ingredient_data.ingredient.primary))
                print('Ingredient Modifier: {0}'.format(ingredient_data.ingredient.modifier))
                print('Ingredient Amount  : {0}'.format(ingredient_data.amount.value))
                print('Ingredient Unit    : {0}'.format(ingredient_data.amount.unit))
                print('\n\n')
            self.assertEqual(ingredient_data.ingredient.primary, expected_ingredient['ingredient'])
            self.assertEqual(ingredient_data.ingredient.modifier, expected_ingredient['modifiers'])
            self.assertEqual(ingredient_data.amount.value, expected_amount['value'])
            self.assertEqual(ingredient_data.amount.unit, expected_amount['unit'])


TEST_INGREDIENTS = [
    '1/2 cup vegetable oil',
    '3 pounds chicken breast',
    '4 (4 pounds) skinless, boneless chicken breasts',
    '4 small red potatoes',
    '1 tablespoon salt',
    '1 1/2 tbl pepper',
    '1 green pepper',
    '5 banana peppers',
    '1 red pepper',
]

EXPECTED_INGREDIENTS = [
    dict(modifiers='vegetable', ingredient='oil'),
    dict(modifiers='', ingredient='chicken breast'),
    dict(modifiers='skinless boneless', ingredient='chicken breast'),
    dict(modifiers='small red', ingredient='potato'),
    dict(modifiers='', ingredient='salt'),
    dict(modifiers='', ingredient='pepper'),
    dict(modifiers='', ingredient='green pepper'),
    dict(modifiers='', ingredient='banana pepper'),
    dict(modifiers='', ingredient='red pepper')
]

EXPECTED_AMOUNTS = [
    dict(value=0.5, unit='cup'),
    dict(value=3, unit='pound'),
    dict(value=4, unit='pound'),
    dict(value=4, unit=''),
    dict(value=1, unit='tablespoon'),
    dict(value=1.5, unit='tbl'),
    dict(value=1, unit=''),
    dict(value=5, unit=''),
    dict(value=1, unit='')
]


if __name__ == '__main__':
    run_tests()
