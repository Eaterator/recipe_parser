DEFAULT_UNKNOWN_AMOUNT = 0.2
DEFAULT_UNITLESS = 0.2
MAXIMUM_UNKNOWN_PERCENT_AMOUNT = 0.1


class AmountPercentConverter:

    def calculate_percent_amounts(self, recipe_ingredients):
        """
        Updates recipe_ingredients to fill in the percent amounts of each ingredient.
        :param recipe_ingredients: a list of RecipeIngredient to be modified
        :return
        """
        amounts = [ri.ingredient_amount for ri in recipe_ingredients]
        units = [ri.amount_units for ri in recipe_ingredients]
        is_unknown = [False] * len(amounts)
        for i, amount in enumerate(amounts):
            amounts[i], is_unknown[i] = self._convert_units(amount, units[i])
        total_amounts = sum(amounts)
        redis_amount = 0
        for i, (ri, a) in enumerate(zip(recipe_ingredients, amounts)):
            amount = a / total_amounts
            if amount < MAXIMUM_UNKNOWN_PERCENT_AMOUNT and is_unknown[i]:
                ri.percent_amount = MAXIMUM_UNKNOWN_PERCENT_AMOUNT
                redis_amount += amount - MAXIMUM_UNKNOWN_PERCENT_AMOUNT
            else:
                ri.percent_amount = amount
        redis_amount = redis_amount / sum(is_unknown) if sum(is_unknown) > 0 else 0
        for i, _ in enumerate(recipe_ingredients):
            recipe_ingredients[i].percent_amount = amounts[i] + redis_amount if not is_unknown[i] else amounts[i]
        return

    @staticmethod
    def _convert_units(amount, unit):
        if amount and unit:
            return amount / CONVERSION_LOOKUP[unit], False
        elif amount and not unit:
            return amount * DEFAULT_UNITLESS, True
        return DEFAULT_UNKNOWN_AMOUNT, True


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
        'milligram': 220000,
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

CONVERSION_LOOKUP = {k: v for k, v in CONVERSIONS['cup'].items()}
