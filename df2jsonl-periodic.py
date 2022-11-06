import pandas as pd
from tqdm import tqdm
from df2jsonl import prompt

tqdm.pandas()

meta = pd.read_csv('e-gmd-q/info-matrix-text-periodic.csv')

# filter rows where note_text is not of type str
meta = meta[meta['note_text'].apply(lambda x: type(x) == str)]

# filter values from meta where time_signature is not 4-4
meta = meta[meta['time_signature'] == '4-4']
# filter values from meta where beat_type is not beat
meta = meta[meta['beat_type'] == 'beat']

# print the number of unique values in the note_text column
print(meta['note_text'].nunique(), "unique completions")

def composite_completion(note_text, bpm):
    # return f"bpm={bpm}. {note_text}"
    return note_text

# create a new composite completion column
meta['completion'] = meta.progress_apply(lambda row: composite_completion(row['note_text'], row['bpm']), axis=1)

# create a new prompt column
meta['prompt'] = meta.progress_apply(lambda row: prompt(row['style'], row['kit_name']), axis=1)

# make a new dataframe with only the columns we need
df = meta[['prompt', 'completion']]

# append '###' to the end of each completion
df['completion'] = df['completion'].apply(lambda x: " " + x + " ###")

# append -> to the end of each prompt
df['prompt'] = df['prompt'].apply(lambda x: x + " ->")

# deduplicate based on completions
df = df.drop_duplicates(subset=['completion'])

df.to_csv('final-egmd-periodic.csv', index=False)

# write to jsonl file
df.to_json('jsonl/drums-periodic.jsonl', orient='records', lines=True)

# openai tools fine_tunes.prepare_data -f drums-periodic.jsonl
# openai api fine_tunes.create -t drums-periodic.jsonl -m davinci --n_epochs 2 --suffix "autodrummer-v6"