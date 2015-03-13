# encoding: utf-8
import re
from sect import cluster
from lxml.html import fromstring

# we expect you to override in response to necessary.
# but need customize not necessarily.
def not_body_rate(block):
    # not_body_rate() takes account of not_body_rate.
    # return value has to be float or integer.
    return 0


# for scoring layout block according to the emergence position of its layout block
def lbscore(block, factor):
    text = block.a_droped_text
    # At least link-removed content has to have 20 charactors.
    if len(text) == 0 or len(text) < 20 * block.num_of_a:
        text = u''
    score = len(text) * factor
    rate = not_body_rate(block)
    if rate > 0:
        score *= (0.72 ** rate)
    return score


# for scoring title according to the emergence position and header element
def lbttlscore(block, factor):
    # calculate title score
    # define 40 as title regular length
    text = re.compile('\s').sub('', block.text)
    if not len(text):
        return 0
    score = (factor / len(block.text)) * 100
    m = re.compile(r'<h([1-6]).*?>', re.DOTALL).match(block.body)
    if m:
        # h1 - h6
        score *= float(6.0 / float(m.groups()[0])) * 4.63
    return score


# clusters continuous high score blocks
def lbcluster(blocks, score = lbscore, threshold = 100, continuous_factor = 1.62, decay_factor = .93):
    factor = 1.0
    continuous = 1.0
    clusts = [cluster()]
    for b in blocks:
        if len(clusts[-1].body) > 0:
            continuous /= continuous_factor
        if len(b.text) == 0 or len(b.a_droped_text) == 0:
            continue
        factor *= decay_factor
        points  = score(b, factor)
        if points * continuous > threshold:
            clusts[-1].append(b).add_score(points * continuous)
            continuous = continuous_factor
        elif points > threshold:
            clusts.append(cluster([b], points))
            factor = 1.0
            continuous = continuous_factor
    return clusts

