from tooling.process_progression import process_chord_progression, process_arpeggio_progression
from tooling.arpeggio_ordering import print_ordered_notes


if __name__ == "__main__":
    chord_list = ['A#min7', 'D7', 'G#maj7', 'Cmaj7']

    best_path = process_arpeggio_progression(chord_list=chord_list)

    print_ordered_notes(best_path)

    # best_path = process_chord_progression(chord_list=chord_list)

    # print(best_path)