from nltk import sent_tokenize, word_tokenize, pos_tag, RegexpParser
import re

GRAMMAR = r"""
    NP: {<DT|PP\$>?<JJ>*<NN>}
        {<NNP>+}
"""


class IngredientParser:

    __instances = dict()

    def __init__(self, grammar):
        self._sentence_parser = RegexpParser(grammar)

    @classmethod
    def _create_grammer(cls, clean_grammar):
        if clean_grammar not in cls.__instances:
            cls.__instances[clean_grammar] = cls(grammar=clean_grammar)

    @classmethod
    def get_parser(cls, grammar=GRAMMAR):
        clean_grammar = cls._clean_grammer(grammar)
        cls._create_grammer(clean_grammar)
        return cls.__instances[clean_grammar].parse

    def _parse_sentence_tree(self, text):
        tagged_sentences = [pos_tag(s) for s in [word_tokenize(ss) for ss in sent_tokenize(text)]]
        return self._sentence_parser.parse(tagged_sentences[0])

    @staticmethod
    def _clean_grammer(grammar):
        return grammar.strip()

    def parse(self, text):
        sentence_tree = self._parse_sentence_tree(text)
        print(sentence_tree)
        # tkinter py-3 required for pretty graph of sentence parse tree:
        # sentence_tree.draw()


if __name__ == '__main__':
    parse_func = IngredientParser.get_parser()
    parse_func("1 1/2 cup vegetable oil")
