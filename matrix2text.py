import pandas as pd
from tqdm import tqdm
import pdb
from mappings import inverse_mapping, replacement_chars

tqdm.pandas()

def matrix_to_text(matrix, truncate=32):
    if matrix is None:
        return None
    length = int(matrix[-1][1] * 4)

    notes_reduce = [] * length

    # group by quantized start time
    notes = {}
    for triplet in matrix:
        key = int(triplet[1] * 4)
        if key not in notes:
            notes[key] = []
        notes[key].append(triplet[0])

    # convert notes dict to list in order of note time
    for i in range(length):
        if i in notes:
            notes_reduce.append(notes[i])
        else:
            notes_reduce.append([])
    
    # notes_reduce = [min(i) if len(i) > 0 else -1 for i in notes_reduce]

    # convert notes_reduce to list of numbers
    # notes_reduce = [inverse_mapping[value] if value in inverse_mapping.keys() else "l" for value in notes_reduce]
    notes_reduce = ["".join([inverse_mapping[value] if value in inverse_mapping.keys() else "l" for value in values]) if len(values) > 0 else "n" for values in notes_reduce]
    
    # remove all elements in the array before the first occurrence of an element that includes the letter 'k'
    try:
        notes_reduce = notes_reduce[notes_reduce.index(next(filter(lambda x: "k" in x, notes_reduce))):]
    except StopIteration:
        pass

    # remove all duplicate characters in each note
    notes_reduce = ["".join(set(note)) for note in notes_reduce]

    order_list = list(inverse_mapping.values())
    # order the notes according to order_list
    notes_reduce = ["".join(sorted(note, key=lambda x: order_list.index(x))) for note in notes_reduce]


    notes_reduce_string = " ".join(notes_reduce[:(truncate-1)])
    for old, new in replacement_chars.items():
        notes_reduce_string = notes_reduce_string.replace(old, new)

    return notes_reduce_string

if __name__=="__main__":
    matrix_df = pd.read_csv('e-gmd-q/info-with-matrix.csv')

    # evaluate strings in q_matrices column to list of tuples

    def eval_to_list(x):
        if type(x) == str:
            return eval(x)
        else:
            return None

    matrix_df['q_matrices'] = matrix_df['q_matrices'].progress_apply(eval_to_list)

    matrix_df['note_text'] = matrix_df.progress_apply(lambda row: matrix_to_text(row['q_matrices']), axis=1)

    # deduplicate by note_text column
    matrix_df = matrix_df.drop_duplicates(subset=['note_text'])

    matrix_df.to_csv('e-gmd-q/info-matrix-text-multiple.csv', index=False)