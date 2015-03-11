# encoding: utf-8
import re
from lxml.html import fromstring

# we expect you to override in response to necessary.
# but need customize not necessarily.
def not_body_rate(sect):
    # not_body_rate() takes account of not_body_rate.
    # return value has to be float or integer.
    return 0


# for scoring layout block according to the emergence position of its layout block
def lbscore(sect, factor):
    text = sect.a_droped_text
    # At least link-removed content has to have 20 charactors.
    if len(text) == 0 or len(text) < 20 * sect.num_of_a:
        text = u''
    score = len(text) * factor
    rate = not_body_rate(sect)
    if rate > 0:
        score *= (0.72 ** rate)
    return score


# clusters continuous high score blocks
def lbcluster(sects, score = lbscore, threshold = 100, continuous_factor = 1.62, decay_factor = .93):
    factor = 1.0
    continuous = 1.0
    clusts = [{'sections': [], 'body': u'', 'points': 0}]
    for sect in sects:
        if len(clusts[-1]['body']) > 0:
            continuous /= continuous_factor
        factor *= decay_factor
        points = score(sect, factor)
        if points * continuous > threshold:
            clusts[-1]['sections'].append(sect)
            clusts[-1]['body']   += "\n" + sect.body if sect.body == u'' else sect.body
            clusts[-1]['points'] += points
            continuous = continuous_factor
        elif points > threshold:
            clusts.append({'sections': [sect], 'body': sect.body, 'points': points})
            continuous = continuous_factor
    return clusts

