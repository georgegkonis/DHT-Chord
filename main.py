import hashlib

import numpy
import pandas as pd

event_ids_df = pd.read_excel(r'EventID.xlsx')
complete_data_df = pd.read_excel(r'globalterrorismdb_0221dist.xlsx')
event_id_numpy = event_ids_df.to_numpy()
complete_data_numpy = complete_data_df.to_numpy()

hashedID = []
N = 256  # SPACE
n = 8  # eight nodes
m = 8  # number of fingers

# hashing the information and storing it in arrays
# https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists
for x in event_id_numpy:
    hashedID.append((int(hashlib.sha1(x).hexdigest(), 16)))

# we transform our array into a numpy array
hashedID = numpy.array(hashedID)

# the completeArray array consists of the hashed ids of the events on column [0][0][i]
# and the rest of the data in column [1][0][i]
completeArray = [[hashedID], [numpy.array(complete_data_numpy)]]

# https://www.tutorialspoint.com/generating-random-number-list-in-python
# for now we will choose our own nodes
node_ids = [0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240]


# https://www.tutorialspoint.com/python/python_nodes.html
# https://www.geeksforgeeks.org/self-in-python-class/
# https://stackoverflow.com/questions/24041940/defining-numpy-array-in-the-init-function-of-a-class
# we build our Node class that contains all the attributes our node will need
class Node:

    def __init__(self, id=None):
        self.id = id
        self.data_ids = []
        self.data_ids_mod = []
        self.dataval = []
        self.fingers = []
        # self.data = {}
        self.nextval = None


print(node_ids)

print(len(completeArray[0][0]))


# function that creats a node's fingers
def create_fingers(node_id):
    temp_index = 0
    # we first find the node through the id given
    # we care for the index of the node in the array node_ids[]
    for g in range(len(nodes)):
        if node_id == nodes[g].id:
            # this is the index we end up with
            temp_index = g
            break
    # then we use the the minimum difference technic from the store_data_in_node function
    # to locate the node each finger is pointing to
    # for m fingers
    temp_finger = 0
    for i in range(1, m + 1):
        # first we increment our temporary finger location as instructed by the chord theory
        temp_finger = nodes[temp_index].id + pow(2, (i - 1))
        # in order to accomplish a chord circle we need to reset our temp finger when it exceeds N
        # or else the last nodes will always point their fingers at 0
        if temp_finger > N:
            temp_finger = temp_finger - N
        # we set our minimum diff as the max value possible so that we can begin its calculation
        min_diff_fingers = N
        temp_difference_index = 0
        for h in range(len(node_ids)):
            if min_diff_fingers > node_ids[h] - temp_finger > 0:
                temp_difference_index = h
                min_diff_fingers = node_ids[h] - temp_finger
        # after the minimum difference for the fingers is calculated we input the node id the finger points to
        # into the array fingers[] we have created in our node class
        nodes[temp_index].fingers.append(node_ids[temp_difference_index])


# function that takes a certain event id and determines and determines in which node the data is stored
def store_data_in_node(element):
    for k in range(len(element[0][0])):
        min_diff = N
        temp = 0
        # we run a for loop that calculates the minimum difference between our event id and the nodes
        for h in range(len(node_ids)):
            if min_diff > node_ids[h] - (element[0][0][k] % N) > 0:
                temp = h
                min_diff = node_ids[h] - (element[0][0][k] % N)
        # after the minimum difference is calculated we input our desired data and id's in our node
        nodes[temp].data_ids.append(element[0][0][k])
        nodes[temp].data_ids_mod.append((element[0][0][k]) % N)
        nodes[temp].dataval.append(element[1][0][k])


# Now we initialize the nodes with this loop
nodes = []
for j in range(len(node_ids)):
    nodes.append(Node(node_ids[j]))
# Then with this loop we connect them with their successors
for j in range(len(node_ids)):
    if j != len(node_ids) - 1:
        nodes[j].nextval = nodes[j + 1]
    else:
        nodes[j].nextval = nodes[0]

store_data_in_node(completeArray)

for l in range(len(nodes)):
    create_fingers(nodes[l].id)

# loop that prints out the data of each node
for j in range(len(node_ids)):
    if j != len(node_ids) - 1:
        # the node object
        print('NODE:', nodes[j])
        # the successore node object
        print('NEXT NODE:', nodes[j].nextval)
        # the node id
        print('ID:', nodes[j].id)
        # the successor node id
        print('NEXT NODE ID:', nodes[j + 1].id)
        # the list of hashed event id's
        print('DATALIST:', nodes[j].data_ids[1])
        # the list of hashed and modded event id's
        # these values are the ones used to make the comparison
        # that determines in which node the data will be transfered
        print('DATALIST MODDED IDS:', nodes[j].data_ids_mod[1])
        # the data the come with each data id
        print('DATA:', nodes[j].dataval[1])
        # the nodes the node's fingers point to
        print('FINGERS', nodes[j].fingers)
        print('\n')
    else:
        # the node object
        print('NODE:', nodes[j])
        # the successore node object
        print('NEXT NODE:', nodes[j].nextval)
        # the node id
        print('ID:', nodes[j].id)
        # the successor node id
        print('NEXT NODE ID:', nodes[0].id)
        # the list of hashed event id's
        print('DATALIST:', nodes[j].data_ids[1])
        # the list of hashed and modded event id's
        # these values are the ones used to make the comparison
        # that determines in which node the data will be transfered
        print('DATALIST MODDED IDS:', nodes[j].data_ids_mod[1])
        # the data the come with each data id
        print('DATA:', nodes[j].dataval[1])
        # the nodes the node's fingers point to
        print('FINGERS', nodes[j].fingers)
        print('\n')
