from .ChordFingering import ChordFingering
from random import randint

def fretwise_distance(current: ChordFingering, next: ChordFingering):
    """
    Return the average fret distance between two chords
    Can be in the range [0, 20] (ish)
    """
    # Subtraction is defined as the difference between average fret
    return abs(current - next)


def count_common_tones(current: ChordFingering, next: ChordFingering):
    """
    Return the inverse of the count (can be 0) of common tones between two chords

    Returns 2 if no common tones and 1 / # of common tones if some common tones
    """
    return current.common_tones(next)


def stringwise_distance(current: ChordFingering, next: ChordFingering):
    """
    Return the average string difference between two chords

    Can be in the range of [0, 2] for four note chords
    """
    return abs(current.average_string() - next.average_string())


def continuous_motion(current: ChordFingering, next: ChordFingering):
    """
    Takes in two chords and returns the motion
    Motion is down the guitar neck (high fret -> low fret)
    TODO: make motion stoccastic for down or up as a global value
    Returns 0 for correct motion and 1 for incorrect motion
    """
    return 0 if current - next > 0 else 1
    

def total_edge_weight(current, next):
    """
    Return the weighted sum of the functions above between two chords
    """
    fretwise = fretwise_distance(current, next)
    common_tones = count_common_tones(current, next)
    stringwise = stringwise_distance(current, next)
    motion = continuous_motion(current, next)

    return (fretwise * 1) + (common_tones * 5) + (stringwise * 4) + (motion * 3)