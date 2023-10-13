## Install googletrans first using one of the methods below:
# pip install googletrans==4.0.0-rc1
# pip install googletrans==3.1.0a0
# pip install google_trans_new

# import google_trans_new
# from google_trans_new import google_translator
from deep_translator import GoogleTranslator
# see available languages with the below
# print(google_trans_new.LANGUAGES)

# Init
translator = GoogleTranslator(source='auto', target='fr')

# Call to translate and get output
output = translator.translate(
    "I love natural language processing")
print(output)
