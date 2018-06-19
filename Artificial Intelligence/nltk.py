import HTMLParser
import re
import nltk
nltk.download('sentiwordnet')
nltk.download("wordnet", "C:/Python27/nltk_data/")
nltk.download('punkt')
nltk.download('stopwords')   # import stopwords
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import sentiwordnet as swn
from nltk.tag import pos_tag
htmlParser = HTMLParser.HTMLParser()

#Tweets extracted from Streaming API
tweet = "@realDUmbridge Marauder? You must be thinking of The Butcher of Benghazi and odummer? 1.7 Billion to Iran? https://t.co/1SZKwz01ne"
#tweet = "@seanhannity Does the fact that I can go from curly to straight bother you? Are you upset, your hair isn't as versatile as mine? https://t.co/jIYjnzNuQu"
#tweet = "So THIS happened a few weeks ago!! Yaaasss!! My homie @offleashseoulreal and I gettin it in!!! https://t.co/uevoE45hkU"
#tweet = "I was going to go to the gym buuuut midterms are kicking my butt"
#tweet= "@OfficialRezz WOWWW THIS IS SUCH A GOOD SIGN! I'M DOING A PRESENTATION FOR MY FINAL ON HARP SEALS TODAY THANK YOU SPACE MOM"
#tweet = "#partners #womenofwinston #winstonway @ Atherton, California https://t.co/zSghFdCxuP"
#tweet = "@KennethBokor Ya'all are dressed so formal. Is this new look part of the new format?"

#Change sentence case to lower
tweet_lower = tweet.lower()

#Tag the html link in the tweet
parsedTweet = htmlParser.unescape(tweet_lower)
#print(parsedTweet)

#Remove the fullstop from the sentence
fullstop_pattern = re.compile("\. ")
tweet_dot = re.sub(fullstop_pattern, "", parsedTweet)
#print tweet_v1

#Remove the html link
url_pattern = re.compile("http\S+")
tweet_v1 = re.sub(url_pattern, "", tweet_dot)
#print tweet_v1

#Remove usernames
username_pattern = re.compile("@\S+")
tweet_v2=re.sub(username_pattern, "", tweet_v1)
#print tweet_v2

#Remove comma's
comma_pattern = re.compile("\,")
tweet_v3=re.sub(comma_pattern, "", tweet_v2)
#print tweet_v3

#Change n't to not
short_pattern = re.compile("n't")
tweet_v4=re.sub(short_pattern, " not", tweet_v3)
#print tweet_v4

#Change it's to it is
apostopy_pattern = re.compile("it's")
tweet_v5=re.sub(apostopy_pattern, "it is", tweet_v4)
#print tweet_v5

#Change 're to are
shorten_pattern = re.compile("u're")
tweet_v6=re.sub(shorten_pattern, "u are", tweet_v5)
#print tweet_v6

#Change i'm to I am
short1_pattern = re.compile("i'm")
tweet_v7=re.sub(short1_pattern, "i am", tweet_v6)
#print tweet_v7

#Change Yaaaassss to Yes
Yes_pattern = re.compile("y[a]+[s]+")
tweet_v8=re.sub(Yes_pattern, "yes", tweet_v7)
#print tweet_v8

#Change Nooooo to No
No_pattern = re.compile("n[o]+")
tweet_v9=re.sub(No_pattern, "No", tweet_v8)
#print tweet_v8

#Change buuuutttt to but
But_pattern = re.compile("b[u]+")
tweet_v10=re.sub(But_pattern, "bu", tweet_v9)
#print tweet_v10

#Change woooowwww to wow
wow_pattern = re.compile("w[o]+[w]+")
tweet_v11=re.sub(wow_pattern, "wow", tweet_v10)
#print tweet_v11

#Change hiiiiissss to his
his_pattern = re.compile("h[i]+[s]+")
tweet_v12=re.sub(his_pattern, "his", tweet_v11)
#print tweet_v12

#Change ya'all to you all
youall_pattern = re.compile("ya'all")
tweet_v13=re.sub(youall_pattern, "you all", tweet_v12)
#print tweet_v13

#Change getting to getting
gettin_pattern = re.compile("gettin")
tweet_v14=re.sub(gettin_pattern, "getting", tweet_v13)
#print tweet_v14

#Remove hashtag
hashtag_pattern = re.compile("#\S+")
tweet_v15=re.sub(hashtag_pattern, "", tweet_v14)
print tweet_v15


# returns a list of the words in the sentence.
tokens = nltk.tokenize.word_tokenize(tweet_v15)
print "tokens: ", tokens

# Extract english stopwords
stop = nltk.corpus.stopwords.words('english')
new_sentence = []
for word in tokens:
    if word not in stop:
        new_sentence.append(word)

print "The sentence has been reduced from :", tweet, " : to : ", new_sentence

#Part of Speech Tagging
pos_text = pos_tag(new_sentence)
print pos_text
#Initialize scores
pos_score = neg_score = 0
for word, tag in pos_text:
    senti_yes = None
    if 'NN' in tag and swn.senti_synsets(word, 'n'):
        senti_yes = swn.senti_synsets(word, 'n')[0]
    elif 'VB' in tag and swn.senti_synsets(word, 'v'):
        senti_yes = swn.senti_synsets(word, 'v')[0]
    elif 'JJ' in tag and swn.senti_synsets(word, 'a'):
        senti_yes = swn.senti_synsets(word, 'a')[0]
    elif 'RB' in tag and swn.senti_synsets(word, 'r'):
        senti_yes = swn.senti_synsets(word, 'r')[0]
    # if senti-synset is found, i.e. score is greater than 0
    if senti_yes:
        # add scores for all found synsets
        pos_score += senti_yes.pos_score()
        neg_score += senti_yes.neg_score()

print "Positive Score",pos_score
print "Negative Score",neg_score

#If overall positive score is greater than 0 then it a positive sentence otherwise negative
if pos_score - neg_score > 0:
    print "This sentence has a positive sentiment."
elif pos_score - neg_score < 0:
    print "This sentence has a negative sentiment."
else:
    print "Sentiment for this sentence cannot be determined."


