# encoding: utf-8
import re
from lxml.html import fromstring
from pprint import pprint

# we expect you to override in response to necessary.
# but need customize not necessarily.
def not_body_rate(sect):
    # not_body_rate() takes account of not_body_rate.
    # return value has to be float or integer.
    # whether this layout block is a collection of links.
    return 0


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


def lbcluster(sects, score = lbscore, threshold = 100, continuous_factor = 1.62, decay_factor = .93):
    factor = 1.0
    continuous = 1.0
    clusts = [Cluster()]
    for sect in sects:
        if len(clusts[-1].body) > 0:
            continuous /= continuous_factor
        factor *= decay_factor
        points = score(sect, factor)
        if points * continuous > threshold:
            clusts[-1].body += sect.body
            clusts[-1].points += points
            continuous = continuous_factor
        elif points > threshold:
            clusts.append(Cluster(sect.body, points))
            continuous = continuous_factor
    return clusts
    

class Cluster(object):
    
    def __init__(self, body = u'', points = 0):
        self.body   = body
        self.points = points

