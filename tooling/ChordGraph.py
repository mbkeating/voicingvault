from .ArpeggioFingering import ArpeggioFingering
from .Voicings import Voicings
from .ChordFingering import ChordFingering
from .edge_weight import total_edge_weight
from heapq import heappop, heappush
from math import inf
from random import randint

class ChordGraph:
    def __init__(self, arpeggios: bool = False):
        """
        Initialize a graph with an adjacency list and one node (source)
        """
        self.adj_list = dict()
        if not arpeggios:
            # Working with chords
            # Initialize the source array
            source_fingerings = [-1, -1, -1, -1, -1, -1]

            # Randomize a position in the source array for a fresh set of chord voicings (allows for regeneration)
            source_fingerings[randint(0, 5)] = randint(1, 22)

            self.source = ChordFingering(chord_shape_id=None, root_note_pos=max(source_fingerings), fingering=source_fingerings, layer=0)
            
            self.sink = ChordFingering(chord_shape_id=None, root_note_pos=-2, fingering=[-2, -2, -2, -2, -2, -2], layer=0)
        else:
            self.source = ArpeggioFingering({(-1, -1)})
            self.sink = ArpeggioFingering({(-2, -2)})
        self.adj_list[self.source] = []
        self.current_layer = [self.source]


    def add_chord(self, voicings: Voicings, chord_name: str, layer: int, arpeggios: bool = False) -> None:
        """
        Adds all fingerings for a chord to the end of the graph
        Connect each previous chord fingering to this chord
        With the weight from edge_weight
        """
        next_layer = []

        if not arpeggios:
            # Voice chords
            relevant_voicings = voicings.get_chord_voicings(chord_name, layer)
        else:
            # Voice arpeggios
            relevant_voicings = voicings.get_arpeggio_voicings(chord_name)

        for voicing in relevant_voicings:
            # Loop through each of the current layer to add an edge
            for current_layer_voicing in self.current_layer:
                # Edge case check to see if our current layer voicing is source
                #if current_layer_voicing == self.source:
                    # Simply set it to zero
                #    cur_edge_weight = 0
                #else:
                cur_edge_weight = total_edge_weight(current=current_layer_voicing, next=voicing)

                # Add the tuple of (next chord voicing, edge weight between current and next voicing) to the adjacency list
                self.adj_list[current_layer_voicing].append((cur_edge_weight, voicing))

            # Now add the voicing to the adjacency list and to the next current layer
            self.adj_list[voicing] = []
            next_layer.append(voicing)

        # We can now set the current layer to the next layer
        self.current_layer = next_layer


    def add_sink(self) -> None:
        """
        Add the sink node to the end of the graph which is connected to all the fingerings for the last chord
        """
        for current_layer_voicing in self.current_layer:
            self.adj_list[current_layer_voicing].append((0, self.sink))

        self.adj_list[self.sink] = []


    def shortest_path(self) -> dict:
        """
        Use dijstras algorithm to find the shortest path in the graph

        Return the path as a list of chord fingerings
        """
        
        priority_queue = []
        prev = dict()
        # Keep distances in a dict too for faster lookup
        dist = dict()

        # Initialize previous to have source with a previous of None
        prev[self.source] = None
        
        for vertex in self.adj_list.keys():
            if vertex == self.source:
                heappush(priority_queue, (0, vertex))
                dist[vertex] = 0
            else:
                heappush(priority_queue, (inf, vertex))
                dist[vertex] = inf
        
        while len(priority_queue) > 0:
            # Get vertex with the minimum distance
            u_dist, u_value = heappop(priority_queue)

            if u_dist > dist[u_value]:
                # We've already been here
                continue
            # Early exit: if we've found sink, we can exit
            # TODO: make sure this is correct
            # if u_value == 'sink':
            #     return prev

            for neighbor in self.adj_list[u_value]:
                # Unwrap neighbor tuple
                edge_weight, voicing = neighbor
                cur_distance = dist[u_value] + edge_weight

                if cur_distance < dist[voicing]:
                    dist[voicing] = cur_distance
                    heappush(priority_queue, (cur_distance, voicing))
                    prev[voicing] = u_value

        return prev


    def reconstruct_path(self, shortest_path_prev) -> list[ChordFingering]:
        """
        Take in the shortest path previous values found from the shortest_path function 
        and reconstruct the shortest path from source to sink
        """
        cur = self.sink
        path = []
        while shortest_path_prev[cur] != self.source:
            previous = shortest_path_prev[cur]
            path.insert(0, previous)
            cur = previous

        return path

    
    def __str__(self):
        return str(self.adj_list)