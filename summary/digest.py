# -*- coding: utf-8 -*-
import os, sys
import json
import nltk
import numpy
from pprint import pprint

N = 100 # words num
CLUSTER_THRESHOLD = 5 # distance of words
TOP_SENTENCES = 5 # summurized sentences num

def _score_sentences(sentences, important_words):
    scores = []
    sentence_idx = -1
    
    for s in [nltk.tokenize.word_tokenize(s) for s in sentences]:
        
        sentence_idx += 1
        word_idx = []
        
        for w in important_words:
            try:
                # compute position of important word in this sentence
                word_idx.append(s.index(w))
            except ValueError, e:
                # not include w in this sentence
                pass
        
        word_idx.sort()
        
        # not include important word at all
        if len(word_idx) == 0:
            continue
        
        # Calculate the cluster using the threshold of maximum distance
        # for two consecutive words with an index of words
        clusters = []
        cluster = [word_idx[0]]
        i = 0
        while i < len(word_idx):
            if word_idx[i] - word_idx[i - 1] < CLUSTER_THRESHOLD:
                cluster.append(word_idx[i])
            else:
                clusters.append(cluster[:])
                cluster = [word_idx[i]]
            i += 1
        clusters.append(cluster)
        
        # calculates a score for each cluster.
        # The maximum score of the cluster is the score for the statement.
        max_cluster_score = 0
        for c in clusters:
            significant_words_in_cluster = len(c)
            total_words_in_cluster = c[-1] - c[0] + 1
            score = 1.0 * significant_words_in_cluster * \
                significant_words_in_cluster / total_words_in_cluster
            if score > max_cluster_score:
                max_cluster_score = score
        scores.append((sentence_idx, score))
    return scores


def summarize(text):
    sentences = [s.strip() for s in nltk.tokenize.sent_tokenize(text)]
    normalized_sentences = [s.lower() for s in sentences]
    
    words = [w.lower() for sentence in normalized_sentences \
        for w in nltk.tokenize.word_tokenize(sentence) if len(w) > 2]
    
    fdist = nltk.FreqDist(words)
    
    top_n_words = [w[0] for w in fdist.items() \
        if w[0] not in nltk.corpus.stopwords.words('english')][:N]
    
    scored_sentences = _score_sentences(normalized_sentences, top_n_words)
    
    avg = numpy.mean([s[1] for s in scored_sentences])
    std = numpy.std([s[1] for s in scored_sentences])
    mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences if score > avg + 0.5 * std]
    
    top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-TOP_SENTENCES:]
    top_n_scored = sorted(top_n_scored, key=lambda s: s[0])
    
    return dict(top_n_summary = [sentences[idx] for (idx, score) in top_n_scored], \
            mean_scored_summary = [sentences[idx] for (idx, score) in mean_scored])

def main():
    
    result = summarize(u"""
Joan Rivers, the raspy loudmouth who pounced on America’s obsessions with flab, face-lifts, body hair and other blemishes of neurotic life, including her own, in five decades of caustic comedy that propelled her from nightclubs to television to international stardom, died on Thursday in Manhattan. She was 81.

Her daughter, Melissa Rivers, confirmed her death. A spokeswoman, Judy Katz, said the cause had not yet been determined.

Ms.Rivers died at Mount Sinai Hospital, where she had been taken last Thursday from an outpatient surgery clinic after going into cardiac arrest and losing consciousness, the authorities said. The State Health Department is investigating the circumstances that led to her death, a state official said Thursday.

Ms.Rivers had been in the clinic for a minor procedure on her vocal cords, according to a spokesman. Her daughter said Tuesday that her mother was on life support and Wednesday that she was out of intensive care.

Ms.Rivers was one of America’s first successful female stand-up comics in an aggressive tradition that had been almost exclusively the province of men, from Don Rickles to Lenny Bruce. She was a role model and an inspiration for tough-talking comedians like Roseanne Barr, Sarah Silverman and countless others.
    """)
    
    pprint(result)

if __name__ == '__main__':
    main()

