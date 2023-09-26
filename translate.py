## Install googletrans first using one of the methods below:
# pip install googletrans==4.0.0-rc1
# pip install googletrans==3.1.0a0
# pip install google_trans_new

import googletrans
from googletrans import Translator

# see available languages with the below
print(googletrans.LANGUAGES)

# Init
translator = Translator()

# Call to translate and get output
output = translator.translate("I love natural language processing", src='en', dest='fr')
print(output.text)
