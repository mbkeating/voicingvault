class ChordFingering:
    def __init__(self, chord_shape_id, root_note_pos, fingering):
        """
        Initialize a single chord fingering with a name

        The fingering is a len 6 array with the following string associations
        [E, A, D, G, B, E]

        -1 means that the note is muted
        """
        self.chord_shape_id = chord_shape_id
        self.root_note_pos = root_note_pos
        self.fingering = fingering


    def average_string(self):
        """
        Returns the average of all of the string indices that are played
        for example, if the A, D, G, B strings are played 
        the average would be (1 + 2 + 3 + 4) / 4 = 2.5
        """
        string_idx_total = 0
        string_count_total = 0

        for i in range(6):
            if self.fingering[i] != -1:
                string_idx_total += i
                string_count_total += 1

        return string_idx_total / string_count_total


    def common_tones(self, other):
        if not isinstance(other, ChordFingering):
            return 0

        common_tone_count = 0
        for i in range(6):
            if self.fingering[i] != -1 and self.fingering[i] == other.fingering[i]:
                common_tone_count += 1
        
        if common_tone_count == 0:
            return 2

        return 1 / common_tone_count


    def __sub__(self, other):
        """
        Returns the average fret of self - the avg fret of other
        """
        if not isinstance(other, ChordFingering):
            return 0

        total_fret_self = 0
        total_strings_self = 0
        total_fret_other = 0
        total_strings_other = 0

        for i in range(6):
            if self.fingering[i] != -1:
                total_fret_self += self.fingering[i]
                total_strings_self += 1
            if other.fingering[i] != -1:
                total_fret_other += other.fingering[i]
                total_strings_other += 1

        return (total_fret_self / total_strings_self) - (total_fret_other / total_strings_other)


    def __lt__(self, other):
        """
        No real logic here, just need to define some concept of less than for dijkstras
        """
        if not isinstance(other, ChordFingering):
            return False

        return self.fingering[0] < other.fingering[0]


    def __eq__(self, other):
        """
        Returns true if self and other have matching fingerings for all 6 strings
        """
        if not isinstance(other, ChordFingering):
            return False

        for i in range(6):
            if self.fingering[i] != other.fingering[i]:
                return False
        return True


    def __hash__(self):
        # Hash as 1 * (low e fret + 1) + 10 * (a fret + 1) + 100 * (d fret + 1) ...
        total = 0
        for i in range(len(self.fingering)):
            if self.fingering[i] >= 0:
                total += (self.fingering[i] + 1) * (10 ** i)
        return total

    
    def __repr__(self):
        return '|'.join([str(f) for f in self.fingering]) + ' ' + str(self.root_note_pos) + ' ' + str(self.chord_shape_id)