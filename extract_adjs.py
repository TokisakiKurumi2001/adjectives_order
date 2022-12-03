import spacy


class ExtractADJ:
    def __init__(self):
        print("Initializing Spacy")
        self.nlp = spacy.load("en_core_web_sm")
        print("Initialized Spacy")

    def find_adjs(self, text):
        doc = self.nlp(text)

        list_of_adjs = []
        adjs = []
        list_of_pos_s = []
        pos_s = []
        previous_pos = None
        span_idx = []
        start = True
        tokens = []

        def add_word(text, pos):
            length = len(adjs)
            adjs.append(text)
            pos_s.append(pos)
            return length

        for i, token in enumerate(doc):
            tokens.append(token.text)
            pos = token.pos_
            text = token.text
            tag = token.tag_
            if pos == 'ADJ':
                add_word(text, f"{pos}_{tag}")
                if start:
                    span_idx.append(i)
                    start = False
            else:
                dep = token.dep_
                if dep == 'amod':
                    add_word(text, f"{pos}_{tag}")
                    pos = 'ADJ'
                elif tag == 'VBG' and previous_pos == 'ADJ':
                    add_word(text, f"{pos}_{tag}")
                    pos = 'ADJ'
                elif pos in ['NOUN', 'PROPN']:
                    next_token = doc[i+1]
                    if next_token.tag_ == 'VBG' or next_token.pos_ == 'ADJ':
                        add_word(text, f"{pos}_{tag}")
                        pos = 'ADJ'
                    else:
                        if len(adjs) > 0:
                            list_of_adjs.append(adjs)
                            list_of_pos_s.append(pos_s)
                            adjs = []
                            pos_s = []
                            span_idx.append(i)
                            start = True
            previous_pos = pos
        if not start:
            # has not reach the end yet, add the length of the sentence in token
            span_idx.append(i)
        return (list_of_adjs, list_of_pos_s, span_idx, tokens)


# correct_my_str = "My brother bought a delicious big old square green sleeping leathery American bag."
if __name__ == "__main__":
    correct_my_str = "My brother bought a delicious big old square green American leathery sleeping bag."
    extractor = ExtractADJ()
    adjs, pos_s = extractor.find_adjs(correct_my_str)
    print(adjs)
    print(pos_s)
