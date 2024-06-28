import math
from .ArpeggioFingering import ArpeggioFingering
import random

def note_distance(note1: tuple[int, int], note2: tuple[int, int]):
    """
    Both notes are a tuple of (string, fret)
    Prioritize string = 10*fret
    """
    return (10 * abs(note1[0]-note2[0])) + abs(note1[1]-note2[1])

def order_arpeggio(arpeggio_list: list[ArpeggioFingering]) -> list[tuple]:
    """
    Order the arpeggios by selecting a 
    random staring note for the first chord
    Then, select the note that is closest to some note in the next chord
    Make that note the ending note and the next chord note the starting note
    Randomly order the other two notes
    """
    ordered_notes = []
    current_arpeggio_idx = 0
    current_arpeggio_fingering = list(arpeggio_list[0].fingering)
    starting_note_idx = random.randint(0, 2)
    ordered_notes.append(current_arpeggio_fingering[starting_note_idx])

    while current_arpeggio_idx < len(arpeggio_list) - 1:
        # find the end note
        next_arpeggio_fingering = list(arpeggio_list[current_arpeggio_idx + 1].fingering)
        closest_current_idx = -1
        closest_next_idx = -1
        dist = math.inf
        for i in range(len(current_arpeggio_fingering)):
            if i == starting_note_idx:
                continue
            for j in range(len(next_arpeggio_fingering)):
                cur_dist = note_distance(current_arpeggio_fingering[i], next_arpeggio_fingering[j])
                if cur_dist < dist:
                    dist = cur_dist
                    closest_current_idx = i
                    closest_next_idx = j

        # add the middle two notes
        # TODO randomize
        for i in range(len(current_arpeggio_fingering)):
            if i != starting_note_idx and i != closest_current_idx:
                ordered_notes.append(current_arpeggio_fingering[i])

        # Add the end note
        ordered_notes.append(current_arpeggio_fingering[closest_current_idx])

        # set the starting note idx to the next idx
        starting_note_idx = closest_next_idx
        # add the next starting note in
        ordered_notes.append(next_arpeggio_fingering[starting_note_idx])
        # set the current fingering to the next fingering
        current_arpeggio_fingering = next_arpeggio_fingering

        current_arpeggio_idx += 1

    # Now loop through and add the final notes from the final arpeggio (not the starting note)
    for i in range(len(current_arpeggio_fingering)):
        if i != starting_note_idx:
            ordered_notes.append(current_arpeggio_fingering[i])
    
    return ordered_notes

def print_ordered_notes(ordered_notes: list[tuple]):
    t = ['|' for _ in range(6)]
    for i in range(len(ordered_notes)):
        string, fret = ordered_notes[i]
        for j in range(6):
            t[j] += '-'
        for j in range(6):
            if j == 5 - string:
                t[j] += str(fret)
            else:
                t[j] += ''.join(['-' for _ in range(len(str(fret)))])
        for j in range(6):
            t[j] += '-'

    for line in t:
        print(line)