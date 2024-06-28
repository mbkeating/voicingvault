"""
Main entry for tooling
Gets the best fingering pattern for a chord progression
"""

from .Voicings import Voicings
from .ChordGraph import ChordGraph
from .arpeggio_ordering import order_arpeggio

def generate_from_name(type):
    """
    Experimental: generate c arpeggio from type
    Use a greedy approach
    Assume that users can only stretch three frets
    have a start note that you choose
    if the next valid note is within three frets, do that
    Otherwise go to the next string

    Return all fingerings of Ctype for guitar
    """
    starting_notes = ['E', 'A', 'D', 'G', 'B', 'E']
    notes_ordered = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    neck = [[] for _ in range(6)]
    for i in range(len(starting_notes)):
        starting_num = notes_ordered.index(starting_notes[i])
        neck[i] = [n % 12 for n in range(starting_num, starting_num + 22)]

    arpeggio_types = {
        'maj7': [0, 4, 3, 4],
        'min7': [0, 3, 4, 3],
        '7': [0, 4, 3, 3],
    }

    c_index = notes_ordered.index('C')

    def generate(starting_string, starting_fret):
        """
        TODO: Make this a backtracking recursive algo to get all possible arpeggios from a starting position
        """
        shape = arpeggio_types[type]
        current_pos = (starting_string, starting_fret)
        res = set()
        for s in shape:
            cur_string, cur_fret = current_pos
            # Keep it to at most 3 out
            if cur_fret + s < starting_fret + 4:
                current_pos = (cur_string, cur_fret + s)
                res.add(current_pos)
            else:
                # Get the amount we need to move back by taking the root notes minus each other
                lower_string_idx = notes_ordered.index(starting_notes[cur_string])
                higher_string_idx = notes_ordered.index(starting_notes[cur_string + 1])
                starting_note_difference = (higher_string_idx - lower_string_idx) % 12
                # print(starting_note_difference, lower_string_idx, higher_string_idx)
                # Our new fret is the current fret with the lowest notes differences included and our arpeggio increase value
                current_pos = (cur_string + 1, cur_fret - starting_note_difference + s)
                res.add(current_pos)

        return res
    
    all_fingerings = []
    for i in range(3):
        for j in range(len(neck[0])):
            if neck[i][j] == c_index:
                all_fingerings.append(generate(i, j))

    return all_fingerings

"""     
c_major_shapes_arpeggios = {
    'maj7': [
        {(5, 3), (4, 2), (4, 5), (3, 4)},
    ],
    'min7': [
        {(5, 3), (5, 6), (4, 5), (3, 3)}
    ],
    '7': [
        {(5, 3), (4, 2), (4, 5), (3, 3)}
    ],
}
"""
c_major_shapes_arpeggios = {
    'maj7': generate_from_name('maj7'),
    'min7': generate_from_name('min7'),
    '7': generate_from_name('7')
}


def process_chord_progression(chord_list, c_major_shapes):
    """
    Takes in a list of chord names
    Return the best fingering pattern to play the chord list
    """
    chord_graph = ChordGraph()

    voicings = Voicings(c_major_shapes=c_major_shapes)

    for i, chord in enumerate(chord_list):
        chord_graph.add_chord(voicings=voicings, chord_name=chord, layer=i)

    chord_graph.add_sink()

    shortest_path_prev = chord_graph.shortest_path()

    return chord_graph.reconstruct_path(shortest_path_prev)


def process_arpeggio_progression(chord_list):
    """
    Takes in a list of arpeggio names
    Return the best fingering pattern to play the arpeggio list
    """
    chord_graph = ChordGraph(arpeggios=True)
    voicings = Voicings(c_major_shapes=c_major_shapes_arpeggios)

    for chord in chord_list:
        chord_graph.add_chord(voicings=voicings, chord_name=chord, layer=0, arpeggios=True)

    chord_graph.add_sink()

    shortest_path_prev = chord_graph.shortest_path()

    path = chord_graph.reconstruct_path(shortest_path_prev)

    return order_arpeggio(path)