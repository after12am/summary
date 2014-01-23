# -*- coding: utf-8 -*-
import re, os, sys
import networkx as nx
import nltk
from collections import defaultdict
from pprint import pprint


stopwords = nltk.corpus.stopwords.words('english')


class _BigramTokenizer(object):
    
    def __init__(self):
        self.measures = nltk.collocations.BigramAssocMeasures()
        self.finder = nltk.collocations.BigramCollocationFinder
    
    def tokenize(self, words):
        finder = self.finder.from_words(words)
        finder.apply_freq_filter(2)
        finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in stopwords)
        return finder.nbest(self.measures.likelihood_ratio, 10)


class _Measure(object):
    
    def __init__(self, text):
        self.text = self.normalize(text)
        self.sentences = None
        self.lemmatizer = nltk.WordNetLemmatizer()
    
    def normalize(self, text):
        norm = text.lower()
        # norm = to_unicode(norm)
        # norm = to_unicode_if_htmlentity(norm)
        # return norm
        return norm
    
    def find_high_freq(self, num = 30):
        words = self.find_words()
        words = sorted(words, key=lambda x: x[1], reverse = True)
        return words[:num]
    
    def find_words(self):
        words = nltk.word_tokenize(self.text)
        words = [re.sub(r'\.$', '', w).lower() for w in words]
        bigrams = self.find_bigrams(words, True)
        bigrams = [item for item in bigrams if item[1] > 2]
        # text except bigrams
        text = self.text
        for bi, count in bigrams:
            text = text.replace(bi, '')
        # get words except bigrams
        words = nltk.word_tokenize(text)
        words = [re.sub(r'\.$', '', w).lower() for w in words if len(w) > 3 and not w in stopwords]
        # lemmatize words
        words = [self.lemmatizer.lemmatize(w) for w in words]
        freq = defaultdict(int)
        for w in words:
            freq[w] += 1
        return freq.items() + bigrams
    
    def find_bigrams(self, words, no_duplicate = False):
        # get candidates of bigram
        tokenizer = _BigramTokenizer()
        bigrams = tokenizer.tokenize(words)
        # count frequency of each bigrams
        freq = [[bi, self.text.count(' '.join(bi))] for bi in bigrams]
        # not allowed to use duplicate word
        if no_duplicate:
            freq = sorted(freq, key=lambda x: x[1])
            unique = []
            for i, item in enumerate(freq):
                duplicate = False
                for j in range(i + 1, len(freq)):
                    if len(set(item[0]) & set(freq[j][0])) > 0:
                        duplicate = True
                if not duplicate:
                    unique.append(item)
            freq = unique
        return [(' '.join(bi), count) for bi, count in freq]
    
    def divide_into_senteces(self, cache = True):
        if cache and isinstance(self.sentences, list):
            return self.sentences
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(self.text)
        # remove period from end of sentence
        sentences = [re.sub(r'\.$', '', sentence) for sentence in sentences]
        self.sentences = sentences
        return self.sentences



class _KeyGraph(nx.Graph):
    
    def __init__(self, measure):
        super(_KeyGraph, self).__init__()
        self.measure = measure
        self.foundations = None
    
    def find_foundations(self, cache = True):
        if cache and isinstance(self.foundations, list):
            return self.foundations
        foundations = list(nx.find_cliques(self))
        foundations = self.reduce_cliques(foundations)
        self.foundations = foundations
        return self.foundations
    
    def reduce_cliques(self, cliques):
        for i, clique in enumerate(cliques):
            for j in range(i + 1, len(cliques)):
                for word in clique:
                    if word in cliques[j]:
                        cliques[i] = list(set(cliques[i] + cliques[j]))
                        del cliques[j]
                        return self.reduce_cliques(cliques)
        return cliques
    
    def calculate_collocations(self, words):
        co = []
        for i, item in enumerate(words):
            for j in range(i + 1, len(words)):
                co.append((item, words[j], self.co(item, words[j])))
        # filter by frequency of collocation
        co = [item for item in co if item[2] > 0]
        # order by frequency
        return sorted(co, key=lambda x: x[2], reverse=True)
    
    def co(self, word1, word2):
        score = 0
        for sentence in self.measure.divide_into_senteces():
            if ' %s ' % word1 in sentence:
                if ' %s ' % word2 in sentence.replace(word1, ''):
                    score += 1
        return score
    
    def co2(self, word, PG):
        score = 0
        for sentence in self.measure.divide_into_senteces():
            for node in PG:
                if word is not node:
                    if ' %s ' % word in sentence:
                        if ' %s ' % node in sentence.replace(word, ''):
                            score += 1
                            break
        return score
    
    def high_key(self, words, num = 12):
        keys = [self.key(w) for w in words];
        keys = sorted(keys, key=lambda x: x[1], reverse=True)
        return keys[:num]
    
    def key(self, word):
        foundations = self.find_foundations()
        co2 = [self.co2(word, PG) for PG in foundations]
        key = sum(co2)
        return (word, key)
    
    def c(self, word1, word2):
        score = 0
        for sentence in self.measure.divide_into_senteces():
            if ' %s ' % word1 in sentence:
                if ' %s ' % word2 in sentence.replace(word1, ''):
                    score += 1
        return score
    
    def draw(self):
        import matplotlib.pyplot as plt
        nx.draw(self)
        plt.show()
    
    def prune_week_edges(self):
        for edge in self.edges():
            self.prune_edge(edge[0], edge[1])
    
    def prune_edge(self, edge1, edge2):
        self.remove_edge(edge1, edge2)
        if nx.has_path(self, source=edge1, target=edge2):
            self.add_edge(edge1, edge2)



def find_keywords(text, debug = False):
    
    measure = _Measure(text)
    keygraph = _KeyGraph(measure)
    
    words = [w for w, count in measure.find_high_freq()]
    for w in words:
        keygraph.add_node(w)
    
    co = keygraph.calculate_collocations(words)
    co = [item for item in co if item[2] > 1]
    for edge in co:
        keygraph.add_edge(edge[0], edge[1])
    keygraph.prune_week_edges()
    
    keys = keygraph.high_key(words, 12)
    for key in keys:
        keygraph.add_node(key[0])
    words1 = [word for word, count in keys]
    
    words2 = []
    for foundation in keygraph.find_foundations():
        words2 += foundation
    words2 = words2
    
    columns = []
    for word1 in words1:
        for word2 in words2:
            columns.append((word1, word2, keygraph.c(word1, word2)))
    
    for edge in columns:
        if edge[2] > 0:
            keygraph.add_edge(edge[0], edge[1], color='red')
    keygraph.prune_week_edges()
    
    columns = [(word, sum([score for w1, w2, score in columns if w1 is word])) for word in words1]\
            + [(word, sum([score for w1, w2, score in columns if w2 is word])) for word in words2]
    
    keywords = defaultdict(int)
    for word1 in list(set(words1 + words2)):
        for word2, score in columns:
            if word1 is word2:
                keywords[word1] += score
    
    keywords = sorted(keywords.items(), key=lambda x: x[1], reverse = True)
    
    if debug:
        keygraph.draw()
    
    # return [('word1', 'score1'), ('word2', 'score2')...]
    return keywords[:10]
    
    
    

def main():
    text = open('sample.txt', 'r').read()
    pprint(find_keywords(text))

if __name__ == '__main__': main()

