# encoding: utf-8
import re
import lxml.html
from pprint import pprint

# we expect you to override in response to necessary.
# but need customize not necessarily.
def not_body_rate(section):
    # not_body_rate() takes account of not_body_rate.
    # return value has to be float or integer.
    # whether this layout block is a collection of links.
    return 0


def lbscore(text, factor):
    score = len(text) * factor
    # rate = not_body_rate(token)
    # if rate > 0:
    #     score *= (0.72 ** rate)
    return score


def lbcluster(sections, score = lbscore, threshold = 100, continuous_factor = 1.62, decay_factor = .93):
    factor = 1.0
    continuous = 1.0
    clusts = [LayoutBlock()]
    for section in sections:
        text = section.text
        # At least link-removed content has to have 20 charactors.
        if len(text) == 0 or len(text) < 20 * section.num_of_a:
            text = u''
        if len(clusts[-1].text) > 0:
            continuous /= continuous_factor
        factor *= decay_factor
        if score(text, factor) * continuous > threshold:
            clusts[-1].text  += section.body
            clusts[-1].score += score(text, factor)
            clusts[-1].sections.append(section)
            continuous = continuous_factor
        elif score(text, factor) > threshold:
            clusts.append(LayoutBlock())
            clusts[-1].text  += section.body
            clusts[-1].score += score(text, factor)
            clusts[-1].sections.append(section)
            continuous = continuous_factor
    return clusts
    

class LayoutBlock(object):
    
    def __init__(self):
        self.text   = ''
        self.score  = 0
        self.sections = []
