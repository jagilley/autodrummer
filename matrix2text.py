import pandas as pd
from tqdm import tqdm
import pdb
from mappings import inverse_mapping, replacement_chars

tqdm.pandas()

def matrix_to_notes_reduce(matrix, truncate=32):
    if matrix is None:
        return None
    length = int(matrix[-1][1] * 4)

    # only keep notes such that notes[1] < truncate // 4
    matrix = [note for note in matrix if len(note) > 0 and note[1] < truncate // 4]

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

    # remove all elements in the array before the first occurrence of an element that includes any of 36, 22, or 35

    # find first occurrence of 36, 22, or 35
    first_occurrence = None
    for i, note in enumerate(notes_reduce):
        if 36 in note or 22 in note or 35 in note:
            first_occurrence = i
            break
    
    if first_occurrence is not None:
        notes_reduce = notes_reduce[first_occurrence:]
    
    return notes_reduce

def matrix_to_periods(matrix, truncate=32):
    if matrix is None:
        return None
    
    notes_reduce = matrix_to_notes_reduce(matrix, truncate=truncate)
    
    notes_reduce = notes_reduce[:truncate]

    periods = [None] * 6
    # periods[0] = all notes repeating every 1/16th note
    # periods[1] = all notes repeating every 1/8th note
    # periods[2] = all notes repeating every 1/4th note
    # periods[3] = all notes repeating every 1/2th note
    # periods[4] = all notes repeating every bar
    # periods[5] = all notes repeating every 2 bars

    for i in range(6):
        period = []
        for j in range(len(notes_reduce)):
            candidate = []
            for k in range(0, len(notes_reduce), 2 ** i):
                idx = (j + k) % len(notes_reduce)
                candidate.append(notes_reduce[idx])
            # get all values occurring in every value in period
            # print(i, j, period)
            # period = all values common to every value in period
            candidate = list(set.intersection(*map(set, candidate)))
            if candidate != [] and candidate != [[]]:
                # print(i, j, candidate)
                for note in candidate:
                    if note != []:
                        period.append((j, inverse_mapping[note]))
            # for every value in period, remove it from every 2**i value in notes_reduce
            for note in candidate:
                for k in range(0, len(notes_reduce), 2 ** i):
                    idx = (j + k) % len(notes_reduce)
                    if note in notes_reduce[idx]:
                        notes_reduce[idx].remove(note)
        periods[i] = period
    
    return periods

def matrix_to_period_text(matrix, truncate=32):
    if matrix is None:
        return None
    periods = matrix_to_periods(matrix, truncate=truncate)
    
    periods_text = []
    for period in periods:
        period_text = []
        for note in period:
            period_text.append(str(note[0]) + ":" + note[1])
        periods_text.append(",".join(period_text))
        if periods_text[-1] == "":
            periods_text[-1] = "None"

    periods_text = "\n".join(periods_text)
    return periods_text

def periods_text_to_linear_text(periods_text):
    periods = periods_text.split("\n")
    periods = [period.split(",") for period in periods]
    periods = [[note.split(":") for note in period] for period in periods]
    # periods = [[(note[0].strip(), note[1]) for note in period] for period in periods]

    length = 32
    linear_array = [[] for _ in range(length)] # change hardcoded 32

    # print(periods)

    for i, period in enumerate(periods):
        multiplier = 2 ** i
        nth_note = f"1/{2 ** (4 - i)}th note"
        for note in period:
            if len(note) == 1:
                note_strip = [note[0].strip()]
            else:
                note_strip = (note[0].strip(), note[1].strip())
            if note_strip[0] != "None" and note_strip[0] != "":
                # print("adding", note[1], "every" , nth_note, "offset", note[0].strip())
                indices_to_add = [int(note_strip[0]) + j * multiplier for j in range(length // multiplier)]
                for idx in indices_to_add:
                    linear_array[idx].append(note_strip[1])
    
    # print(linear_array)
    return notes_reduce_to_text(linear_array, ints_to_notes=False)

def notes_reduce_to_text(notes_reduce, truncate=32, ints_to_notes=True):
    # convert notes_reduce to list of numbers
    # notes_reduce = [inverse_mapping[value] if value in inverse_mapping.keys() else "l" for value in notes_reduce]
    
    # check if notes_reduce arrays are composed of strings or ints
    if ints_to_notes:
        notes_reduce = ["".join([inverse_mapping[value] if value in inverse_mapping.keys() else "l" for value in values]) if len(values) > 0 else "n" for values in notes_reduce]
    
    # remove all elements in the array before the first occurrence of an element that includes the letter 'k'
    # try:
    #     notes_reduce = notes_reduce[notes_reduce.index(next(filter(lambda x: "k" in x, notes_reduce))):]
    # except StopIteration:
    #     pass

    print(notes_reduce)

    # remove all duplicate characters in each note
    notes_reduce = ["".join(set(note)) for note in notes_reduce]

    order_list = list(inverse_mapping.values())
    # order the notes according to order_list
    notes_reduce = ["".join(sorted(note, key=lambda x: order_list.index(x))) for note in notes_reduce]

    # replace all instances of '' with 'n'
    notes_reduce = [note if note != "" else "n" for note in notes_reduce]

    notes_reduce_string = " ".join(notes_reduce[:truncate])

    return notes_reduce_string # linear text

def matrix_to_linear_text(matrix, truncate=32):
    # matrix to linear text
    if matrix is None:
        return None
    notes_reduce = matrix_to_notes_reduce(matrix, truncate=truncate)
    
    return notes_reduce_to_text(notes_reduce, truncate=truncate)

if __name__=="__main__":
    matrix_df = pd.read_csv('e-gmd-q/info-with-matrix.csv')

    # evaluate strings in q_matrices column to list of tuples

    def eval_to_list(x):
        if type(x) == str:
            return eval(x)
        else:
            return None

    matrix_df['q_matrices'] = matrix_df['q_matrices'].progress_apply(eval_to_list)

    matrix_df['note_text'] = matrix_df.progress_apply(lambda row: matrix_to_linear_text(row['q_matrices']), axis=1)

    # deduplicate by note_text column
    matrix_df = matrix_df.drop_duplicates(subset=['note_text'])

    matrix_df.to_csv('e-gmd-q/info-matrix-text-multiple.csv', index=False)

    # period_text = """None
    #     0:r
    #     None
    #     2:k,4:h,6:h,7:s
    #     0:k,4:s,8:h,9:s
    #     0:y,9:h,12:s,16:h,18:h,26:h,27:k,28:s,31:s
    # """

    # print(periods_text_to_linear_text(period_text))