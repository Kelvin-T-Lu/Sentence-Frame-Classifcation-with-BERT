## Install googletrans first using one of the methods below:
# pip install googletrans==4.0.0-rc1
# pip install googletrans==3.1.0a0
# pip install google_trans_new

# import google_trans_new
# from google_trans_new import google_translator
from deep_translator import GoogleTranslator
import pandas as pd
from datetime import datetime
from tqdm import tqdm
# see available languages with the below
# print(google_trans_new.LANGUAGES)



def apply_translate(translator, text):
    output = translator.translate(text)

    return output

def reverse_translate(reverse_translator, text):
    output = reverse_translator.translate(text)
    return output

def one_translate_cycle(target_lang, reverse_lang = "en"):

    # Orignial final_data frame.
    # og_df = pd.read_csv('./data/para_data.csv')
    og_df = pd.read_csv('./data/seed_para.csv')


    translator = GoogleTranslator(source= "en", target=target_lang)
    reverse_translator = GoogleTranslator(source=target_lang, target=reverse_lang)
    
    # Apply initial translation.
    translate_df = og_df.copy()
    print("applying translate...")
    translate_df["sentence"] = translate_df["sentence"].apply(
        lambda sentence: apply_translate(translator, sentence))
    translate_df["language"] = target_lang
    translate_df["transform"] = translate_df["transform"].apply(
        lambda x: f"{x};{target_lang}")
    print(translate_df.head())

    # Reverse translation for paraphasing.
    reverse_translate_df = translate_df.copy()
    print("applying reverse translate...")

    reverse_translate_df["sentence"] = reverse_translate_df["sentence"].apply(
        lambda sentence: reverse_translate(reverse_translator, sentence))

    reverse_translate_df["language"] = reverse_lang
    reverse_translate_df["transform"] = reverse_translate_df["transform"].apply(lambda x: f"{x};{reverse_lang}")

    # Output DF write
    augmented_df = pd.read_csv('./data/seed_augmented_df.csv')
    # augmented_df["transform"] = "en"
    output_df = pd.concat([augmented_df, translate_df, reverse_translate_df],
                          axis=0, ignore_index=True)
    print(len(output_df))
    print(output_df.head())
    print(output_df.tail())

    print("writing ...")
    timestamp_str = datetime.now().strftime('%d-%m-%y-%H_%M')
    # output_df.to_csv(f"./data/augmented_df_{timestamp_str}.csv")
    output_df.to_csv(f"./data/seed_augmented_df.csv", index=False)

def main():

    # target_lang = "zh-TW"
    # reverse_lang = "en"


    langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    print(langs_dict)

    # English (eng), Mandarin Chinese (cmn), Hindi (hin), Telugu (tel), Nepali (nep), Bengali (ben), Greek (ell),
    # German(deu), Swahili(swa)

    # Google translate acronym for langauges
    print("LANG CHOICES")
    print(["en", "zh-CN", "zh-TW", "hi", "te", "ne", "bn", "el", "de", "sw"])

    # lang_options = ["zh-CN", "ne", "hi", "te", "ne", "bn",
                    # "el", "de", "sw", "ru", "tr", "it"]
    # lang_options = ["ru", "tr", "it"]
    # lang_options = ["zh-CN"]
    lang_options = ["it"]

    
    for i in tqdm(range(len(lang_options))):
        lang = lang_options[i]
        try:
            print(f"Currently on {lang} cycle")
            one_translate_cycle(target_lang = lang, reverse_lang="en")
        except Exception as e:
            with open("error_logs.txt", "a") as f:
                f.write(f"{lang} failed : {e}")
            
            continue

    # return

    

if __name__ == "__main__":
    main()
