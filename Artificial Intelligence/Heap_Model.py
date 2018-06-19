# Create character Frequencies
import urllib2
target_url = 'http://www.gutenberg.org/files/55893/55893-0.txt'

f = urllib2.urlopen(target_url).read()

symbol = "abcdefghijklmnopqrstuvwxyz .',!?"

for key in symbol:
    print (key, f.count(key))

#Code for creating Hoffmann Codes
import queue

class Huff_Node(object):
    def __init__(self, left=None, right=None, root=None):
        self.left = left
        self.right = right

symbfreq = [(7592, 'a'), (1510, 'b'), (2424, 'c'), (4012, 'd'), (11780, 'e'),(2248, 'f'), (2250, 'g'), (5550, 'h'),
            (6199, 'i'), (140, 'j'), (706, 'k'), (4127, 'l'), (2035, 'm'), (6786, 'n'), (7751, 'o'), (1686, 'p'), (119, 'q'),
            (6504, 'r'), (6109, 's'), (8670, 't'), (2693, 'u'), (844, 'v'), (2055, 'w'), (125, 'x'), (1777, 'y'), (59, 'z'),
            (21204, ' '), (921, '.'), (1804, ','), (21, '!'), (6, '?'), (9, "'")]

def build_heap(freqs):
    pq = queue.PriorityQueue()
    for i in freqs:
        pq.put(i)
    while pq.qsize() > 1:
        right, left = pq.get(), pq.get()
        node = Huff_Node(left, right)
        pq.put((right[0]+left[0], node))
    return pq.get()

node = build_heap(symbfreq)

def assign_code(node, prefix="", Huffcode={}):

    if isinstance(node[1].left[1], Huff_Node):
        assign_code(node[1].left,prefix+"0", Huffcode)
    else:
        Huffcode[node[1].left[1]]=prefix+"0"

    if isinstance(node[1].right[1],Huff_Node):
        assign_code(node[1].right,prefix+"1", Huffcode)
    else:
        Huffcode[node[1].right[1]]=prefix+"1"

    return(Huffcode)

Huffcode = assign_code(node)

print ("Symbol\tWeight\tHuffman Code")
for i in symbfreq:
    print (i[1], i[0], Huffcode[i[1]])