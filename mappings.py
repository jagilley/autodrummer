
inverse_mapping_old = {
    36: 'kick',
    38: 'snr', # snare
    42: 'hh', # hihat
    48: 'tom',
    49: 'csh', # crash
    51: 'ride',
    39: 'clap',
    56: 'cbl', # cowbell
    75: 'claves',
    64: 'conga',
    70: 'maracas',
    76: 'guiro',
    69: 'cabasa',
    60: 'bongo',
    37: 'shkr', # shaker
    54: 'tamb', # tambourine
    81: 'triangle',
    49: 'cymbal',
    35: 'kick', # bass drum of some kind
    55: 'spl', # splash cymbal
    0: 'none',
    46: 'hh_open', # hihat_open
    44: 'hh', # hihat_pedal
    40: 'snr', # snare_rimshot
    43: 'tom_high_floor',
    -1: 'none',
    22: 'kick', # VERIFY
    58: 'vibraslap',
    53: 'ride_bell',
    50: 'tom_high',
    59: 'ride_2',
    45: 'tom_low',
    47: 'tom_low_mid',
}


inverse_mapping = {
    36: 'k', # kick
    22: 'k', # VERIFY
    35: 'k', # bass drum of some kind
    38: 's', # snare
    40: 's', # snare_rimshot
    42: 'h', # hihat
    48: 't', # tom
    49: 'c', # crash
    51: 'r', # ride
    59: 'r', # ride_2
    39: 'l', # clap
    56: 'b', # cowbell
    37: 'z', # shaker
    54: 'a', # tambourine
    81: 'i', # triangle
    49: 'y', # cymbal
    55: 'p', # splash cymbal
    46: 'j', # hihat_open
    44: 'h', # hihat_pedal
    43: 'u', # tom_high_floor
    50: 'w', # tom_high
    45: 'x', # tom_low
    47: 'q', # tom_low_mid
    58: 'v', # vibraslap
    53: 'd', # ride_bell
    0: 'n', # none
    -1: 'n', # none
}

mappings = {
    "k": "drum-samples/kick.wav",
    "s": "drum-samples/snare.wav",
    "h": "drum-samples/hihat.wav",
    "c": "drum-samples/cymbal.wav",
    "y": "drum-samples/cymbal.wav",
    "l": "drum-samples/clap.wav",
    'r': "drum-samples/ride.wav",
    'j': "drum-samples/hihat-open.wav",
    'a': "drum-samples/tambourine.wav",
    'z': "drum-samples/shaker.wav",
}

replacements = {
    "hh_closed": "hh",
    "hh_open": "hh",
}

replacement_chars = {
    "p": "y", # splash cymbal to cymbal
}