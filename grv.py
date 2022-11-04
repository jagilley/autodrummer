import groover
from groover import RhythmClassifier
from glob import glob
import miditoolkit
from miditoolkit.midi import parser as mid_parser
from miditoolkit.midi import containers as ct
import numpy as np

midi_list = glob('test-drums-2/*.midi')

midi_list = [mid_parser.MidiFile(i) for i in midi_list]

# truncate each file to 4 bars
midi_list_truncated = []
for midi in midi_list:
    beat_resol = midi.ticks_per_beat
    end = beat_resol * 4 * 4
    midi.dump('test-drums-2/truncated/efslieh.midi', segment=[(0, end)])

r = RhythmClassifier()

ds = r.get_pitched_dataset(midi_list)


print(ds.shape)

print(ds[0])