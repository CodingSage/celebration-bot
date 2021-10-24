import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag, word_tokenize, RegexpParser

from queue import Queue

import random

chunker = RegexpParser("""
                       NP: {<DT>?<JJ>*<NN>}    
                       P: {<IN>}               
                       V: {<V.*>}              
                       PP: {<p> <NP>}          
                       VP: {<V> <NP|PP>*}
                       """)

exclamations = [
    "Congratulations",
    "Wow",
    "Bravo",
    "Well done"
]

greetings = [
    "Welcome",
    "Well met",
    "Hello",
    "Hi"
]

def celebrate(user, text):
    tagged = _get_pos_tags(text)
    (nouns, verbs) = _extract_nouns_verbs(tagged)
    return _generate_sentence(user, nouns, verbs)

def _extract_nouns_verbs(tagged):
    nouns = []
    verbs = []
    for tag in tagged:
        if tag[1][0] == 'N':
            nouns.append(tag[0])
        elif tag[1][0] == 'V':
            verbs.append(tag[0])
    
    return (nouns, verbs)

def _generate_sentence(user, nouns, verbs):
    name = user if len(nouns) == 0 else ', '.join(nouns)
    exclamation_index = random.randint(0, len(exclamations)-1)
    exclaim = exclamations[exclamation_index]
    action = "good going with the " + ', '.join(verbs)
    return exclaim + "!" + name + " " + action + "!"

def _get_pos_tags(text):
    return pos_tag(word_tokenize(text))

def _parse_text(text):
    tagged = _get_pos_tags(text)
    parse_tree = chunker.parse(tagged)
    print(parse_tree)
    return parse_tree

def _parse_nouns_verbs(tree):
    nouns = []
    verbs = []

    visited = set()
    q = Queue()
    q.put(tree[0])

    # TODO complete this
    while not q.empty():
        node = q.get()
        visited.add(node)
        if node.label()[0] == 'N':
            nouns.append(node.label())

    return (nouns, verbs)

def run_tests():
    tests = [
        ("foobar", "Welcome Blah!"),
        ("foobar", "Blah just completed their first task!"),
        ("foobar", "I just took a huge dump!")
    ]

    for test in tests:
        print("\n")
        print(_get_pos_tags(test[1]))
        print("test: " + test[1] + " \ncelebration-bot: " + celebrate(test[0], test[1]))
