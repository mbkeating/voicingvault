from math import inf
from .ChordFingering import ChordFingering
from .ArpeggioFingering import ArpeggioFingering

class Voicings:
    def __init__(self, c_major_shapes):
        """
        """
        self.c_major_shapes = c_major_shapes
        self.distance_dict = {
            'C': 0,
            'C#': 1,
            'D': 2,
            'D#': 3,
            'E': 4,
            'F': 5,
            'F#': 6,
            'G': 7,
            'G#': 8,
            'A': 9,
            'A#': 10,
            'B': 11
        }


    def parse_chord_name(self, chord_name):
        """
        Return the chord name and chord type
        """
        if chord_name[1] == '#':
            # Sharp note
            return chord_name[0:2], chord_name[2:]
        
        return chord_name[0], chord_name[1:]


    def get_bass_note(self, chord_shape: list[int]) -> int:
        """
        Return the lowest index string in the chord with a fret value (not -1)
        """
        for c in chord_shape:
            if c != -1:
                return c

        return None


    def get_chord_voicings(self, chord_name) -> list[ChordFingering]:
        """
        Gets all chord fingering possibilities for the chord name
        """
        chord_fingerings = []

        chord_root, chord_type = self.parse_chord_name(chord_name)

        relevent_shapes = self.c_major_shapes[chord_type]

        for chord_shape_id, shape in relevent_shapes:
            new_fingering = []
            # Keep track of the minimum fretted value. If it's 13 or greater we can mod 12 the chord
            min_fretted = inf
            # Loop through all the strings in the shape and add it to the fingering (shifted)
            root_note_pos = -1

            for s in shape:
                if s == -1:
                    new_fingering.append(-1)
                else:
                    new_fret = s + self.distance_dict[chord_root]
                    new_fingering.append(new_fret)
                    # For tracking with db
                    if root_note_pos == -1:
                        root_note_pos = new_fret

                    if new_fret < min_fretted:
                        min_fretted = new_fret

            if min_fretted > 12:
                root_note_pos = -1
                for i in range(6):
                    if new_fingering[i] != -1:
                        new_fingering[i] -= 12
                        if root_note_pos == -1:
                            root_note_pos = new_fingering[i]

            chord_fingerings.append(ChordFingering(chord_shape_id=chord_shape_id, root_note_pos=root_note_pos, fingering=new_fingering))

        return chord_fingerings


    def get_arpeggio_voicings(self, arpeggio_name) -> list[ArpeggioFingering]:
        """
        Gets all arpeggio fingering possibilities for the chord name
        """
        arpeggio_fingerings = []

        chord_root, chord_type = self.parse_chord_name(arpeggio_name)

        relevent_shapes = self.c_major_shapes[chord_type]

        for shape in relevent_shapes:
            new_fingering = set()
            # Keep track of the minimum fretted value. If it's 13 or greater we can mod 12 the chord
            min_fretted = inf
            # Loop through all the strings in the shape and add it to the fingering (shifted)
            for string, fret in shape:
                    new_fret = fret + self.distance_dict[chord_root]
                    new_fingering.add((string, new_fret))
                    if new_fret < min_fretted:
                        min_fretted = new_fret

            if min_fretted > 12:
                # TODO: when you have more time do this in memory if possible
                newer_fingering = set()
                for string, fret in new_fingering:
                    newer_fingering.add((string, fret - 12))


            arpeggio_fingerings.append(ArpeggioFingering(fingering=new_fingering))

        return arpeggio_fingerings