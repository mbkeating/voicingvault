from tooling.process_progression import process_chord_progression, process_arpeggio_progression

if __name__ == "__main__":
    chord_list = ['G#maj7', 'Fmin7', 'C#7', 'C7']

    best_path = process_arpeggio_progression(chord_list=chord_list)

    print(best_path)

    # best_path = process_chord_progression(chord_list=chord_list)

    # print(best_path)