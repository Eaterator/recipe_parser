from unittest import TestCase, main as run_tests
from recipe_parser.amount_conversions import AmountPercentConverter, MAXIMUM_UNKNOWN_PERCENT_AMOUNT


class IngredientRecipe:

    ingredient_amount = 0
    amount_units = ''
    percent_amount = 0

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestAmountConverter(TestCase):

    def test_conversion(self):
        converter = AmountPercentConverter()
        ingredient_amounts = [1, 2, 3, 4, 5, 700, None]
        amount_units_list = ['cup', 'pound', 'kilogram', None, None, None]

        ingredient_recipes = [IngredientRecipe(**dict(ingredient_amount=ia, amount_units=au))
                              for ia, au in zip(ingredient_amounts, amount_units_list)]
        converter.calculate_percent_amounts(ingredient_recipes)

        self.assertLessEqual(ingredient_recipes[-1].percent_amount, MAXIMUM_UNKNOWN_PERCENT_AMOUNT)
        self.assertLessEqual(ingredient_recipes[-1].percent_amount, MAXIMUM_UNKNOWN_PERCENT_AMOUNT)
        self.assertAlmostEquals(sum([i.percent_amount for i in ingredient_recipes]), 1)

if __name__ == '__main__':
    run_tests()
