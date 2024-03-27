class ArpeggioFingering:
    def __init__(self, fingering):
        """
        A fingering for an arpeggio is a set of tuples

        Where each tuple is (string, fret)
        """
        self.fingering = fingering


    def average_string(self):
        """
        Returns the average string over the fingering
        """
        string_total = 0
        
        for string, _ in self.fingering:
            string_total += string

        return string_total / len(self.fingering)

    
    def common_tones(self, other):
        if not isinstance(other, ArpeggioFingering):
            return 0

        common_tone_count = 0

        # loop over all possible pairs of self and other fingerings and count equals
        for f in self.fingering:
            # fingering is a set of tuples so we can check for contains
            if f in other.fingering:
                common_tone_count += 1

        if common_tone_count == 0:
            return 2

        return 1 / common_tone_count

    
    def __sub__(self, other):
        """
        Returns the average fret of self - the avg fret of other
        """
        if not isinstance(other, ArpeggioFingering):
            return 0

        total_fret_self = 0
        total_fret_other = 0

        for _, fret in self.fingering:
            total_fret_self += fret

        for _, fret in other.fingering:
            total_fret_other += fret

        return (total_fret_self / len(self.fingering)) - (total_fret_other / len(other.fingering))


    def __lt__(self, other):
        """
        Need to define less than for djikstras so make it based off the first fretted note in the list
        """
        if not isinstance(other, ArpeggioFingering):
            return False

        # This is dumb
        for string, fret in self.fingering:
            one_self = string * fret
            break

        for string, fret in other.fingering:
            one_other = string * fret
            break

        return one_self < one_other

    
    def __eq__(self, other):
        """
        Returns true if the fingerings are the same set
        """
        # Use the symmetric difference
        return len(self.fingering.symmetric_difference(other.fingering)) == 0

    
    def __hash__(self):
        # TODO: make sure that this actually works as a hash
        total = 0
        for string, fret in self.fingering:
            total += int((fret ** string) % fret)

        return total


    def __repr__(self):
        return '|'.join(str(string) + ',' + str(fret) for string, fret in self.fingering)