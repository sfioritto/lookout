"""
Naive Bayesian Filter implementation.
"""
import urllib2
import re
from operator import itemgetter
from BeautifulSoup import BeautifulSoup as bs

separator = re.compile("[^a-zA-Z0-9,'$-]")
numbers = re.compile("^\d+$")
html_tags = ["p", "html", "div", "id", "a", "title", "tr", "span", "li", "class", "href", "com", "td", "www", "http"]

class Bayes:

    def __init__(self, gtext, rtext):
        self.good = create_count_hash(gtext)
        self.rejected = create_count_hash(rtext)
        self.rhash = {}
        
    @property
    def prejected(self):
        return self.nrejected / (self.nrejected + self.ngood)

    @property
    def ngood(self):
        return float(sum([self.good[key] for key in self.good.keys()]))

    @property
    def nrejected(self):
        return float(sum([self.rejected[key] for key in self.rejected.keys()]))


    def good_count(self, word):
        """
        The number of times this word appears
        in the corpus of relevant blurbs times
        2 to weight the calculation towards
        relevant.
        """
        return get_count(word, self.good) * 2


    def bad_count(self, word):
        """
        The number of times this word appears
        in the corpus of irrelevant blurbs.
        """
        return get_count(word, self.rejected)


    def rejected_given_word(self, word):
        """
        Calculate the odds a message is rejected
        given one word.
        P(Rejected|word) = ( P(word|Rejected)P(Rejected) ) / P(Good)
        """
        ngood = self.good_count(word)
        nbad = self.bad_count(word)

        if self.rhash.has_key(word):
            return self.rhash[word]
        else:
            # get a lot more rejected messages than good, so .6 is weighted to favor that.
            p = min((self.bad_count(word) / self.nrejected), .01) * self.prejected
            pw = p + (self.good_count(word) / self.ngood)
            if p == 0 and pw == 0:
                #most data is from rejected emails, so a new word is slightly more
                #likely to be relevant.
                prob = .4 
            else:
                prob = min(p/pw, .99)
            self.rhash[word] = prob
            return prob


    def rejected_given_text(self, text):
        """
        Given some text figure out what the odds
        are that it should be rejected.
        """
        tokens = []
        for t in tokenize(text):
            ngood = self.good_count(t)
            nbad = self.bad_count(t)
            if ngood + nbad > 5:
                tokens.append(t)

        probs = sorted([self.rejected_given_word(t) for t in tokens])[-15:]
        rejected = reduce(lambda x, y: x * y, probs)
        notrejected = reduce(lambda x, y: x * (1 - y), probs)
        return rejected / (rejected + notrejected)


def valid_token(token):
    if token and not numbers.match(token) and token not in html_tags:
        return True
    else:
        return False


def tokenize(text):
    tokens = [token for token in separator.split(text) if valid_token(token)]
    return tokens


def create_count_hash(text):
    """
    Take some text, split it into tokens
    and create a dictionary of token -> count,
    where count is the number of times the token
    occurred in the text.
    """
    words = {}
    tokens = tokenize(text)
    for token in tokens:
        try:
            words[token] = float(words[token] + 1)
        except KeyError:
            words[token] = float(1)
    return words


def get_count(word, words):
    try:
        return words[word]
    except KeyError:
        return 0


def get_text(blurb, fetch=True):
    text = ""
    for key in blurb.keys():
        if key != "rejected" and key != "url":
            text = text + blurb[key].encode("utf-8")
    if fetch:
        try:
            f = urllib2.urlopen(blurb['url'].encode("utf-8"))
            html = f.read()
            nodes = bs(html).findAll(text=True)
            text = text + "".join(nodes).encode("utf-8")
            f.close()
        except:
            text = text
    return text
    
    
    
