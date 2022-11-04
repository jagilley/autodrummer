import pandas as pd
from tqdm import tqdm

tqdm.pandas()

meta = pd.read_csv('e-gmd-q/info-matrix-text-multiple.csv')

# filter rows where note_text is not of type str
meta = meta[meta['note_text'].apply(lambda x: type(x) == str)]

# filter rows where 'note_text' begins with 'none'
meta = meta[~meta['note_text'].str.startswith('n')]

# get only rows in meta such that 'note_text' begins with 'kick'
meta = meta[meta['note_text'].str.startswith('k')]

# filter out rows where every word in note_text is the same
meta = meta[meta['note_text'].apply(lambda x: len(set(x.split(" "))) > 1)]

# filter out rows for which words one through four are the same
meta = meta[meta['note_text'].apply(lambda x: len(set(x.split(" ")[:4])) > 1)]

# filter values from meta where time_signature is not 4-4
meta = meta[meta['time_signature'] == '4-4']
# filter values from meta where beat_type is not beat
meta = meta[meta['beat_type'] == 'beat']

# remove rows such that note_text.split(" ") < 30
meta = meta[meta['note_text'].apply(lambda x: len(x.split(" ")) > 30)]

# remove rows such that note_text.split(" ") is not divisible by 4
meta = meta[meta['note_text'].apply(lambda x: len(x.split(" ")) % 4 == 0)]

# count the number of rows in meta such that 'none' makes up the majority of the 'note_text' column
# print(meta[meta['note_text'].str.count('none') > 16].shape[0])

# filter out such rows
meta = meta[meta['note_text'].str.count('n') <= 16]

# print the number of unique values in the note_text column
print(meta['note_text'].nunique(), "unique completions")

def composite_completion(note_text, bpm):
    # return f"bpm={bpm}. {note_text}"
    return note_text

# create a new composite completion column
meta['completion'] = meta.progress_apply(lambda row: composite_completion(row['note_text'], row['bpm']), axis=1)

def prompt(style, kit_name):
    # remove numeric values from style
    style = ''.join([i for i in style if not i.isdigit()])
    style = style.replace("/", " ")
    # lowercase kit_name
    kit_name = kit_name.lower()
    # remove parentheses from kit_name
    kit_name = kit_name.replace("(", "")
    kit_name = kit_name.replace(")", "")
    kit_name = " " + kit_name
    # if "custom" in kit_name:
    #     kit_name = ""
    kit_name = kit_name.replace("custom", "")
    kit_name = kit_name.replace("kit", "")
    kit_name = kit_name.strip()
    return f"{style} {kit_name}"
    # return style

# create a new prompt column
meta['prompt'] = meta.progress_apply(lambda row: prompt(row['style'], row['kit_name']), axis=1)

# make a new dataframe with only the columns we need
df = meta[['prompt', 'completion']]

# append '###' to the end of each completion
# df['completion'] = df['completion'].apply(lambda x: " " + x + " ###")

# append -> to the end of each prompt
# df['prompt'] = df['prompt'].apply(lambda x: x + " ->")

# group by duplicate completions and print the number of unique prompts for each completion
# print(df.groupby('completion')['prompt'].nunique().sort_values(ascending=False))

# print all prompts that have completion ' k n r n s n r s r s k k s n r n k n r n s n r s r s k n s n r ###'
# print(df[df['completion'] == ' k n r n s n r s r s k k s n r n k n r n s n r s r s k n s n r ###']['prompt'].unique())

# deduplicate based on completions
df = df.drop_duplicates(subset=['completion'])

df.to_csv('final-egmd.csv', index=False)

# write to jsonl file
df.to_json('drums.jsonl', orient='records', lines=True)

# openai tools fine_tunes.prepare_data -f drums.jsonl
# openai api fine_tunes.create -t drums.jsonl -m davinci --n_epochs 2 --suffix "autodrummer-v4"