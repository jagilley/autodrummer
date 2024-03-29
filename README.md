# autodrummer
**_A text-to-audio model for generating text-conditioned drum beats._**

## how it works
autodrummer is a transformer model created by converting the MIDI data from Google Magenta's [E-GMD dataset](https://magenta.tensorflow.org/datasets/e-gmd) to a specialized variant of plaintext upon which to train a transformer. This repo covers everything necessary to convert the raw MIDI data from E-GMD into tokens for the transformer.

## installation
1. Download the [E-GMD dataset](https://magenta.tensorflow.org/datasets/e-gmd) and place it in this repo in a folder named `e-gmd`
2. `git clone https://github.com/angelfaraldo/pymidifile` _within this repo_ and replace its `quantize.py` with this repo's version of `quantize.py`. _you have to run quantize.py from the autodrummer repo directory, not the pymidifile repo directory, or else you'll get import errors._
3. run `pip install -r requirements.txt`

## current workflow (to prepare data for your own finetune)
1. `pymidifile/quantize.py`: quantize the MIDI data in the e-gmd dataset and convert it to matrices representing `(drum_code, hit_time)` pairs
2. `matrix2text.py`: convert said matrices into plaintext
3. `df2jsonl.py`: convert dataframe of plaintext to `jsonl` file
4. *train model here*
5. `txt2audio.py` **or** `evaluator.py`: convert back from plaintext to audio

## contact
[Jasper on Twitter](https://twitter.com/0xjasper)
