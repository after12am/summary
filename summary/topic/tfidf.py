import os, sys, re

def get_words(doc):
    splitter = re.compile(r'\W*')
    words = [s.lower() for s in splitter.split(doc)\
        if len(s) > 2 and len(s) < 20]
    count = {}
    for w in words:
        count.setdefault(w, 0)
        count[w] += 1
    return dict(count)

def tf(words, return_num=10):
    scores = {}
    sig = sum(list(words.values()))
    for w in words:
        scores[w] = str(words[w] / float(sig))[:6]
    items = []
    for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        items.append((k, v))
    return items[:return_num]

def idf():
    # not implement. 
    # If you want to implement idf, I recommend to use wiki database.
    # see https://dumps.wikimedia.org/ 
    return 1

def tfidf():
    print "not implement.\n" 
    print "If you want to implement idf, I recommend to use wiki database.\n" 
    print "see https://dumps.wikimedia.org/\n"
    pass

def main():
    title = u'Ming Mecca Heart of a video synthesizer and the brain of a videogame console'
    body = u'''
    Ming Mecca combines the heart of a video synthesizer and the brain of a videogame console. Created with love for all things retrofuture, an ontological toy and a videogame easel, Ming Mecca brings to you fingertips a comprehensive set of classic videogame design parameters, from details like object location and animation, to big-picture elements like game rules and level geography.

    You can turn off gravity at the flick of a switch, or scroll through seasons at the turn of a knob. Populate your world with exotic creatures, then modulate their identities with random voltage. Set objects in motion and use their collision to trigger cosmological events elsewhere in your modular. Experiment with quantum position, step sequence destructible terrain, and patch wormholes into parallel dimensions. With Ming Mecca, your modular transforms into a reality synthesizer.

    The device assets are easily replaceable via the SD Card. You can create your own palettes, tile maps, and bitmaps using their text-based World Pack format. You can also control your world manually by connecting an NES-compatible gamepad and create platforming physics or use all four directional pad outputs to create free moving space shooters.

    The system includes 160 192 pixel resolution via standard composite NTSC output with full 60 FPS progressive video output and 2 4 simultaneous colours 2 16 palettes 86 total colours programmable and custom 32 addressable bitmaps.

    Jordan Bartee: designer, engineer, programmer, digimancer
    Chris Novello: transdimensional wayfarer
    Molly Roberts: electronic biologist

    Project Page
    '''
    # expect: Games Chris Novello console device Interface Jordan Bartee Molly Roberts programming retro retrofuture texture
    print tf(get_words(title + body))

if __name__ == '__main__': main()