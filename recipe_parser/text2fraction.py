FRACTIONS = {
    'half': 1/2,
    'havles': 1/2,
    'halve': 1/2,
    'quarter': 1/4,
    'eighth': 1/8,
    'qtr.': 1/4,
    'qtr': 1/4,
}


class Text2Fraction:

    @staticmethod
    def text_to_fraction(text):
        if text in FRACTIONS:
            return FRACTIONS[text]
        return 0