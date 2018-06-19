from collections import Counter
from stopwords import get_stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import string
import glob
import os
import random

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stopwords('en')



atheism = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/atheism/", '*'))
autos = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/autos/", '*'))
baseball = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/baseball/", '*'))
christian = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/christian/", '*'))
crypto = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/crypto/", '*'))
electronics = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/electronics/", '*'))
graphics = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/graphics/", '*'))
guns = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/guns/", '*'))
hockey = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/hockey/", '*'))
mac = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/mac/", '*'))
medical = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/medical/", '*'))
mideast = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/mideast/", '*'))
motorcycles = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/motorcycles/", '*'))
pc = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/pc/", '*'))
politics = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/politics/", '*'))
religion = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/religion/", '*'))
space = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/space/", '*'))
windows = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/windows/", '*'))
xwindows = glob.glob(os.path.join("C:/Users/SanketN/Documents/IU/AI/part2/train/xwindows/", '*'))


topic_names = ["atheism", "autos", "baseball", "christian","crypto","electronics","graphics","guns","hockey","mac","medical","mideast","motorcycles","pc","politics","religion","space","windows","xwindows"]

'''

def print_topics(beta_file, vocab_file, nwords = 25):

    # get the vocabulary

    vocab = file(vocab_file, 'r').readlines()
    # vocab = map(lambda x: x.split()[0], vocab)
    vocab = map(lambda x: x.strip(), vocab)

    # for each line in the beta file

    indices = range(len(vocab))
    topic_no = 0
    for topic in file(beta_file, 'r'):
        print 'topic %03d' % topic_no
        topic = map(float, topic.split())
        indices.sort(lambda x,y: -cmp(topic[x], topic[y]))
        for i in range(nwords):
            print '   %s' % vocab[indices[i]]
        topic_no = topic_no + 1
        print '\n'

if (__name__ == '__main__'):

    if (len(sys.argv) != 4):
        print 'usage: python topics.py <beta-file> <vocab-file> <num words>\n'
        sys.exit(1)

    beta_file = sys.argv[1]
    vocab_file = sys.argv[2]
    nwords = int(sys.argv[3])
    print_topics(beta_file, vocab_file, nwords)
'''

def read_files(directory):
    newf = []
    for filename in directory:
        with open(filename,'rb') as hf:
           newf.append(hf.read())
    return newf

doc_set = [read_files(atheism),read_files(autos)]
#    ,read_files(baseball),read_files(christian),read_files(crypto),read_files(electronics)
#           ,read_files(graphics),read_files(guns),read_files(hockey),read_files(mac),read_files(medical),read_files(mideast),read_files(motorcycles),read_files(pc),read_files(pc),
#           read_files(pc),read_files(politics),read_files(religion),read_files(space),read_files(windows),read_files(xwindows)]


for i in doc_set:

    # clean and tokenize document string
    for line in i:
        raw = ' '.join(i).lower()
        tokens = tokenizer.tokenize(raw)


#    tokened = [x.decode('ISO-8859-1') for x in tokens]

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]

#    print stopped_tokens






document_topic_counts = [Counter() for _ in stopped_tokens]


topic_word_counts = [Counter() for _ in range(20)]


topic_counts = [0 for _ in range(20)]


document_lengths = map(len, stopped_tokens)

distinct_words = set(word for document in stopped_tokens for word in document)
#print distinct_words

W = len(distinct_words)
print W

print document_lengths

D = len(stopped_tokens)
print D



def sample_from(weights):
    """returns i with probability weights[i] / sum(weights)"""
    total = sum(weights)
    rnd = total * random.random()
    for i, w in enumerate(weights):
        rnd -= w
        if rnd <= 0: return i


def p_topic_given_document(topic, d, alpha=0.1):
    """the fraction of words in document _d_ that are assigned to _topic_ (plus some smoothing)"""
    return ((document_topic_counts[d][topic] + alpha) / (document_lengths[d] + 20 * alpha))

def p_word_given_topic(word, topic, beta=0.1):
    """the fraction of words assigned to _topic_ that equal _word_ (plus some smoothing)"""
    return ((topic_word_counts[topic][word] + beta) / (topic_counts[topic] + W * beta))

def topic_weight(d, word, k):
    """given a document and a word in that document, return the weight for the kth topic"""
    return p_word_given_topic(word, k) * p_topic_given_document(k, d)


def choose_new_topic(d, word):
    return sample_from([topic_weight(d, word, k) for k in range(20)])

random.seed(0)
document_topics = [[random.randrange(20) for word in document] for document in stopped_tokens]

for d in range(D):
    for word, topic in zip(stopped_tokens[d], document_topics[d]):
        document_topic_counts[d][topic] += 1
        topic_word_counts[topic][word] += 1
        topic_counts[topic] += 1

for iter in range(1000):
    for d in range(D):
        for i, (word, topic) in enumerate(zip(stopped_tokens[d], document_topics[d])):

            # remove this word / topic from the counts so that it doesn't influence the weights
            document_topic_counts[d][topic] -= 1
            topic_word_counts[topic][word] -= 1
            topic_counts[topic] -= 1
            document_lengths[d] -= 1

            # choose a new topic based on the weights
            new_topic = choose_new_topic(d, word)
            document_topics[d][i] = new_topic

            # and now add it back to the counts
            document_topic_counts[d][new_topic] += 1
            topic_word_counts[new_topic][word] += 1
            topic_counts[new_topic] += 1
            document_lengths[d] += 1

for k, word_counts in enumerate(topic_word_counts):
    for word, count in word_counts.most_common():
        if count > 0: print k, word, count


for document, topic_counts in zip(stopped_tokens, document_topic_counts):
    print document
    for topic, count in topic_counts.most_common():
        if count > 0:
            print topic_names[topic], count,
    print