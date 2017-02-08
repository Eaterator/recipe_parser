#Recipe Parser
Package contains helper functions to create parsers to extract data from the recipes, and join the Eaterator pipeline
from scraping -> text files (JSON) -> recipe parsing (here) -> insert to models/DB. The current approach uses NLTK
and its POS tagging and sentence chunking to detect amounts (CD for numerical values- including word forms), and
compound nounds (<JJ>*<NN> or <NNP>) types to detech ingredients. Some more logic is required to detech the <NN>
that represents the measurement amount <NN> associated with the <CD> value. Also, special consideration may also be
required for the case where the <NN> for measurement amount does not exist (i.e. '3 lemons').

##Requirements
NLTK and Python (version 3.5.2).