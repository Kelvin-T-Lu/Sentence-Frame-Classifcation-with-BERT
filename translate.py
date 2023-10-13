## Install googletrans first using one of the methods below:
# pip install googletrans==4.0.0-rc1
# pip install googletrans==3.1.0a0
# pip install google_trans_new

# import google_trans_new
# from google_trans_new import google_translator
from deep_translator import GoogleTranslator
import pandas as pd
from datetime import datetime
# see available languages with the below
# print(google_trans_new.LANGUAGES)



def apply_translate(translator, text):
    output = translator.translate(text)

    return output

def reverse_translate(reverse_translator, text):
    output = reverse_translator.translate(text)
    return output

def main():
    og_df = pd.read_csv('final_data_v2.csv')

    target_lang = "fr"
    translator = GoogleTranslator(source='auto', target=target_lang)
    reverse_translator = GoogleTranslator(source=target_lang, target="en")



    # Apply initial translation.
    translate_df = og_df.copy()
    translate_df["sentence"] = translate_df["sentence"].apply(lambda x: None)
    translate_df["language"] = target_lang
    print(translate_df.head())

    # Reverse translation for paraphasing. 
    reverse_translate_df = translate_df.copy()
    reverse_translate_df["language"] = "sloppy"

    # Output DF
    output_df = pd.concat([translate_df, reverse_translate_df], axis=0)
    print(len(output_df))
    print(output_df.head())
    print(output_df.tail())


if __name__ == "__main__":
    main()
