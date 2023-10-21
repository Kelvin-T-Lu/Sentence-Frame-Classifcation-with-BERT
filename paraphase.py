from transformers import PegasusForConditionalGeneration, PegasusTokenizerFast
import csv
import pandas as pd
from tqdm import tqdm

def get_paraphrased_sentences(model, tokenizer, sentence, num_return_sequences=5, num_beams=5):
  # tokenize the text to be form of a list of token IDs
  inputs = tokenizer([sentence], truncation=True,
                     padding="longest", return_tensors="pt")
  # generate the paraphrased sentences
  outputs = model.generate(
      **inputs,
      num_beams=num_beams,
      num_return_sequences=num_return_sequences,
  )
  # decode the generated sentences using the tokenizer to get them back to text
  return tokenizer.batch_decode(outputs, skip_special_tokens=True)

def get_paraphase_rows(template_dict, sent):
    # Convert sentence to csv dict format.
    temp_row = template_dict.copy()
    temp_row["sentence"] = sent

    return temp_row

def main():

    print("Initializing models... ")
    model = PegasusForConditionalGeneration.from_pretrained(
        "tuner007/pegasus_paraphrase")

    tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")

    # Generate paraphrased sentences. 
    print("Generating paraphrased sentences...")
    output_rows = []
    # with open("./data/final_data_v2.csv", "r") as csv_file:
    with open("./data/seed.csv", "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # For each row, generate n_sentences generated sentences. 
        n_sentences = 5
        # counter = 0
        csv_list = list(csv_reader)
        for i in tqdm(range(len(csv_list))):
            # print(f"Progress - Working on row {counter}")
            row = csv_list[i]
            output_sentences = get_paraphrased_sentences(model, tokenizer, row["sentence"], num_return_sequences= n_sentences)
            # print(output_sentences)
            
            pack_rows = [row for i in range(n_sentences)]
            output_rows += list(map(get_paraphase_rows, pack_rows, output_sentences))
            
            # print(len(output_rows))
            # counter+=1
            # break
    paraphase_df = pd.DataFrame(output_rows)
    paraphase_df["transform"] = "en;para"
    # Output DF write
    print("reading augmented_df...")
    augmented_df = pd.read_csv('./data/seed.csv')
    augmented_df["transform"] = "en"
    print("writing output...")
    output_df = pd.concat([augmented_df, paraphase_df],
                          axis=0, ignore_index=True)
    print(len(output_df))
    output_df.to_csv(f"./data/seed_augmented_df.csv", index=False)




    
    pass

if __name__ == "__main__":
    main()