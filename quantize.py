from argparse import ArgumentParser
from reformat_midi import *
from tqdm import tqdm
import pdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

meta = pd.read_csv('e-gmd-q/info.csv')

# filter values from meta where time_signature is not 4-4
meta = meta[meta['time_signature'] == '4-4']
# filter values from meta where beat_type is not beat
meta = meta[meta['beat_type'] == 'beat']

# midi_files = folderfiles(args.input, ext='.midi', recursive=args.recursive)
midi_files = meta['midi_filename'].values

if __name__ == '__main__':
    matrices = [None] * len(midi_files)

    try:
        for i, midi_file in tqdm(enumerate(midi_files), total=len(midi_files)):
            # get tempo and time signature from meta
            tempo = meta[meta['midi_filename'] == midi_file]['bpm'].values[0]

            midi_file = os.path.join("e-gmd-q", midi_file)

            try:
                reformat_midi(midi_file, verbose=False, write_to_file=True, override_time_info=False, manual_tempo=tempo)
            except EOFError:
                print("EOFError: " + midi_file)
                continue
            matrix = mid_to_matrix(midi_file)
            quantizer = quantize_matrix(matrix, stepSize=0.25, quantizeOffsets=True, quantizeDurations=False)

            quantizer = [(i[0], i[1]) for i in quantizer if i[1] < 32]
            matrices[i] = quantizer

            """
            # plot quantized matrix
            for triplet in quantizer[:32]:
                # substitute midi numbers for mappings
                # triplet[0] = inverse_mapping[triplet[0]]
                plt.plot(triplet[1], triplet[0], 'ro')

            plt.show()
            """
            


    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting.")

    meta['q_matrices'] = matrices

    meta.to_csv('e-gmd-q/info-with-matrix.csv', index=False)