import pydub
from pydub import AudioSegment
from tqdm import tqdm
from pydub.playback import play
import os
from mappings import mappings, replacements

def bpm_to_ms(bpm):
    return 60000 / 2 / bpm

def text_to_audio(text, bpm):
    buffer_length = bpm_to_ms(bpm)
    audio = AudioSegment.silent(duration=0)

    notes_list = text.split(" ")
    for i in range(len(notes_list)):
        note = notes_list[i]
        # deduplicate characters in note
        note = "".join(set(note))
        notes_list[i] = note

    for note in notes_list:
        to_add = None
        for char in note:
            if char in mappings:
                if not to_add:
                    to_add = AudioSegment.from_wav(mappings[char])
                else:
                    if char in mappings:
                        new_audio = AudioSegment.from_wav(mappings[char])
                        # get length of new_audio
                        new_length = len(new_audio)
                        # get length of to_add
                        to_add_length = len(to_add)
                        # if new_length is longer than to_add_length
                        if new_length > to_add_length:
                            # add silence to to_add
                            to_add += AudioSegment.silent(duration=new_length - to_add_length)
                        # if to_add_length is longer than new_length
                        elif to_add_length > new_length:
                            # add silence to new_audio
                            new_audio += AudioSegment.silent(duration=to_add_length - new_length)
                        
                        to_add = to_add.overlay(new_audio)
            elif char == "n":
                to_add = AudioSegment.silent(duration=buffer_length)
            else: # everything else is a clap
                print('could not find mapping for ' + char)
                to_add = AudioSegment.from_wav(mappings["l"])

        if len(to_add) < buffer_length:
            to_add = to_add + AudioSegment.silent(duration=buffer_length - len(to_add))
        elif len(to_add) > buffer_length:
            to_add = to_add[:buffer_length]
        
        audio = audio + to_add
    return audio

if __name__=="__main__":
    # import pandas as pd
    # meta = pd.read_csv("e-gmd-q/info.csv")
    # # shuffle the df
    # meta = meta.sample(frac=1).reset_index(drop=True)
    # # render text_to_audio for every note_text and bpm in meta
    # for i, row in tqdm(meta.iterrows(), total=len(meta)):
    #     filename = row["midi_filename"].split("/")[-1].split(".")[0]
    #     filename = filename[filename.find("_")+1:]
    #     output_path = "renderings/" + filename + ".wav"
    #     if os.path.exists(output_path):
    #         continue
    #     audio = text_to_audio(row["note_text"], row["bpm"])
    #     audio.export(output_path, format="wav")

    test_text = "yrk n kr n hrs n hr s hr sh kr n hrs n hr s hrk n hkr n hsr n hr s hr s khr k shr n hr"
    # test_text = "kl n kh k ks k kl n h h l n ksh h kl n kh h kl k ksh kh kl n kh h l n ksh h kl n"
    audio = text_to_audio(test_text, 135)
    play(audio)

    # import pandas as pd
    # df = pd.read_csv("e-gmd-q/info-matrix-text-multiple.csv")
    # for i, row in tqdm(df.iterrows(), total=len(df)):
    #     audio = text_to_audio(row["note_text"], 140)
    #     play(audio)
