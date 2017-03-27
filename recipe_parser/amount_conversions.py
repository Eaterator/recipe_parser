DEFAULT_UNKNOWN_AMOUNT = 0.2
DEFAULT_UNITLESS = 0.2


class AmountPercentConverter:

    def calculate_percent_amounts(self, recipe_ingredients):
        """
        Updates recipe_ingredients to fill in the percent amounts of each ingredient.
        :param recipe_ingredients: a list of RecipeIngredient to be modified
        :return
        """
        amounts = [ri.ingredient_amount for ri in recipe_ingredients]
        units = [ri.amount_units for ri in recipe_ingredients]
        for i, amount in enumerate(amounts):
            amounts[i] = self._convert_units(amount, units[i])
        total_amounts = sum(amounts)
        for ri, a in zip(recipe_ingredients, amounts):
            ri.percent_amount = a/total_amounts
        return

    @staticmethod
    def _convert_units(amount, unit):
        if amount and unit:
            return amount / CONVERSIONS[unit]
        elif amount and not unit:
            return amount * DEFAULT_UNITLESS
        return DEFAULT_UNKNOWN_AMOUNT


CONVERSIONS = {
    'cup': {
        'gill': 2,
        'ounce': 8,
        'tablespoon': 16,
        'teaspoon': 48,
        'cup': 1,
        'pint': 0.5,
        'quart': 0.25,
        'gallon': 0.0625,
        'millilitre': 236.588,
        'litre': 0.236588,
        'decilitre': 2.36588,
        'pound': 0.52159,
        'milligram': 0.220,
        'gram': 220,
        'kilogram': 0.220,
        'pinch': 768,
        'dash': 385,
        'touch': 1000,
        'handful': 0.415,
        'taste': 500,
        'can': 1.6,
        'stick': 0.5,
        'a': 8
    }
}