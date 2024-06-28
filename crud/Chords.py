import math
from sqlalchemy import text
from collections import defaultdict

def get_chord_shapes(db):
    select_sql = text('SELECT id, chord_type, chord_fingering FROM chord_shape')
    result = db.execute(select_sql)
    rows = result.fetchall()

    c_shapes = defaultdict(list)

    for row in rows:
        id = row[0]
        type = row[1]
        fingering = row[2]

        converted_fingering = [-1 if e == 'x' else int(e) for e in fingering.split('-')]

        c_shapes[type].append((id, converted_fingering))

    return c_shapes


def get_chords_played(email, db):
    res = {}

    select_sql = text('''
        SELECT chord_type, chord_fingering, chord_root_pos, cpp.id, datetime
        FROM users AS u
        JOIN chord_progression_played AS cpp ON cpp.player_id=u.email
        JOIN chord_played AS chp ON cpp.id=chp.chord_progression_played_id
        JOIN chord_shape AS cs ON chp.chord_id=cs.id
        WHERE u.email=:email
    ''')
    result = db.execute(select_sql, {'email': email})
    rows = result.fetchall()

    for row in rows:
        chord_type = row[0]
        chord_fingering = row[1]
        chord_root_pos = row[2]
        chord_prog_played_id = row[3]
        datetime = row[4]

        chord_transposed, root_letter = transpose_chord(chord_fingering, chord_root_pos)

        if chord_prog_played_id not in res:
            # Initialize with a timestamp and an empty list
            res[chord_prog_played_id] = {
                'timestamp': datetime,
                'fingerings': []
            }

        res[chord_prog_played_id]['fingerings'].append({
            'chord_letter': root_letter,
            'chord_type': chord_type,
            'chord_fingering': chord_transposed,
            'datetime': datetime
        })

    return res


def transpose_chord(c_fingering: str, chord_root_pos: int):
    """
    Returns the transposed chord in the correct format and the root note letter
    """
    root_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    res = []
    diff_to_root = math.inf

    for note in c_fingering.split('-'):
        if note == 'x':
            res.append(-1)
            continue

        note_val = int(note)
        if diff_to_root == math.inf:
            # Will be negative if the root position is on the left of the c major shape
            diff_to_root = chord_root_pos - note_val

        res.append(note_val + diff_to_root)

        
    return res, root_notes[diff_to_root]