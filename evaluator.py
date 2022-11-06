from txt2audio import text_to_audio
from pydub.playback import play
from pydub import AudioSegment
import pandas as pd
from tqdm import tqdm
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]
# finetune = "davinci:ft-personal:autodrummer-v5-2022-11-04-22-34-07"
finetune = "davinci:ft-personal:autodrummer-v6-2022-11-06-19-49-37"

def get_note_text(prompt):
    prompt = prompt + " ->"
    # get completion from finetune
    response = openai.Completion.create(
        engine=finetune,
        prompt=prompt,
        temperature=0.4,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###"]
    )
    return response.choices[0].text.strip()

prompt = "rock funk hybrid"

test_text = get_note_text(prompt)

# test_text = "kick none kick none snr none hh snr hh snr kick none snr none hh snr kick none kick none snr none hh snr hh snr kick kick snr none hh"

print(test_text)
print(len(test_text.split(" ")))

audio = text_to_audio(test_text, 135, periodic=True)
play(audio)
# save audio
audio.export(f"model-outs/{prompt}-{test_text.replace(' ', '')}.wav", format="wav")

exit()

meta = pd.read_csv("e-gmd-q/info-matrix-text-multiple.csv")

# filter rows where note_text is not of type str
meta = meta[meta['note_text'].apply(lambda x: type(x) == str)]

def longest_common_subsequence_of_lists(a,b):
    m = [[0] * (1 + len(b)) for i in range(1 + len(a))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(a)):
        for y in range(1, 1 + len(b)):
            if a[x - 1] == b[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return a[x_longest - longest: x_longest]

# check how much test_text overlaps with any of meta.note_text

max_overlap = 0
for i, row in tqdm(meta.iterrows(), total=len(meta)):
    # check overlap between test_text and row.note_text

    # split into words
    test_text_words = test_text.split(" ")
    row_text_words = row.note_text.split(" ")

    # get overlap between lists
    overlap = longest_common_subsequence_of_lists(test_text_words, row_text_words)

    # get overlap percentage
    overlap_percentage = len(overlap) / len(test_text_words)
    if overlap_percentage > max_overlap:
        max_overlap = overlap_percentage

if max_overlap > 0.7:
    print("\033[91m" + str(max_overlap) + "\033[0m")
else:
    print(max_overlap)

# save the audio
# audio.export("funk.wav", format="wav")