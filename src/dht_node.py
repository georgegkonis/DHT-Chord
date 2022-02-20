class Node:

    # Initializes a new node.
    def __init__(self, node_key):
        self.key = node_key
        self.data = {}
        self.successor = None
        self.predecessor = None
        self.fingers = []

    # Returns a string representation of this node.
    def __str__(self) -> str:
        return str(self.key)

    # Sets the successor node's predecessor, to this node.
    def notify(self):
        self.successor.predecessor = self

    # TODO not implemented
    def stabilize(self):
        print(self.key)

    # TODO has a few exceptions
    # Finds and returns the suitable successor node, for the given data-key.
    def find_successor(self, data_key):
        if self.predecessor.key < data_key <= self.key:
            return self
        if self.predecessor.key > self.key >= data_key:
            return self
        if self.key < data_key <= self.successor.key:
            return self.successor
        node = self.find_closest_preceding_node(data_key)
        return node.find_successor(data_key)

    def find_closest_preceding_node(self, data_key):
        m = len(self.fingers)
        for i in reversed(range(m)):
            if self.key < self.fingers[i].key < data_key:
                return self.fingers[i]
        return self

