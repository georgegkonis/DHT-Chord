import hashlib

from dht_node import Node
import pandas as pd

FILE_PATH = '../files/global_terrorism_data.xlsx'
SHEET_NAME = 'Data'

KEY_BITS = 32  # The number of bits in a key.
CHORD_NODES = 8  # The number of nodes in the chord.


class ChordRing:

    def __init__(self):
        self.node_dict = {}
        self.node_list = []
        self.first_node = None
        self.last_node = None
        self.total_nodes = 0

        self.create_nodes()

    def create_nodes(self):
        total_space = 2 ** KEY_BITS
        node_space = total_space // CHORD_NODES
        prev_node = None

        for key in range(node_space - 1, total_space, node_space):
            new_node = Node(key)

            if prev_node is not None:
                new_node.predecessor = prev_node
                prev_node.successor = new_node
            self.node_dict[key] = new_node
            self.node_list.append(new_node)
            prev_node = new_node

        self.total_nodes = len(self.node_dict)
        self.first_node = self.node_dict[node_space - 1]
        self.last_node = self.node_dict[total_space - 1]

        self.first_node.predecessor = self.last_node
        self.last_node.successor = self.first_node

        for node in self.node_dict.values():
            i = 1
            while i < self.total_nodes:
                index = self.node_list.index(node) + i
                if index >= len(self.node_list):
                    index -= len(self.node_list)
                node.fingers.append(self.node_list[index])
                i *= 2

    def load_data(self):
        node = self.first_node
        df = pd.read_excel(FILE_PATH, SHEET_NAME)
        np = df.to_numpy()
        key_list = []
        for line in np:
            # Hash the key.
            key = str(line[0]).encode('utf-8')
            key = hashlib.sha1(key).hexdigest()
            key = int(key, 16) % 2 ** KEY_BITS
            key_list.append(key)
            print(hex(key))
        key_set = set(key_list)

        # Check for duplicates
        print(len(df))
        print(len(key_list))
        print(len(key_set))


    def print_nodes(self):
        i = 0
        for node in self.node_dict.values():
            print('Node Index:         ' + str(i))
            print('Node Key:           ' + str(node.key))
            print('Previous Node Key:  ' + str(node.predecessor.key))
            print('Next Node Key:      ' + str(node.successor.key))
            print('Finger Node Keys:   ', end='')
            print(*node.fingers, sep=', ')
            print()
            i += 1
        print('Total Nodes: ' + str(self.total_nodes))


chord_ring = ChordRing()
chord_ring.load_data()


