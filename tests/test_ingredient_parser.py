from unittest import TestCase, main as run_tests
from recipe_parser.ingredient_parser import IngredientParser


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
            print('test case: ' + ingredient_text)
            parsed_ingredient = self.parser(ingredient_text)
            ingredient_data = parsed_ingredient.parsed_ingredient

            print(ingredient_data.ingredient.primary)
            print(ingredient_data.ingredient.modifier)
            print(ingredient_data.amount.value)
            print(ingredient_data.amount.unit)
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
    '1 red pepper',
]

EXPECTED_INGREDIENTS = [
    dict(modifiers='vegetable', ingredient='oil'),
    dict(modifiers='', ingredient='chicken breast'),
    dict(modifiers='skinless boneless', ingredient='chicken breast'),
    dict(modifiers='small red', ingredient='potatoes'),
    dict(modifiers='', ingredient='salt'),
    dict(modifiers='', ingredient='pepper'),
    dict(modifiers='green', ingredient='pepper'),
    dict(modifiers='red', ingredient='pepper')
]

EXPECTED_AMOUNTS = [
    dict(value=0.5, unit='cup'),
    dict(value=3, unit='pound'),
    dict(value=4, unit='pound'),
    dict(value=4, unit=None),
    dict(value=1, unit='tablespoon'),
    dict(value=1.5, unit='tbl'),
    dict(value=1, unit=None),
    dict(value=1, unit=None)
]


if __name__ == '__main__':
    run_tests()
