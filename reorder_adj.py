from extract_adjs import ExtractADJ
from categorize_adj import CategorizeADJ


class ReorderADJ:
    def __init__(self):
        print("Initializing ADJ classifier")
        self.categorizer = CategorizeADJ()
        print("Initialized ADJ classifier")
        print("Initializing ADJ extractor")
        self.extractor = ExtractADJ()
        print("Initialized ADJ extractor")

        self.map = {
            'Opinion': 1,
            'Size': 2,
            'Age': 3,
            'Shape': 4,
            'Colour': 5,
            'Origin': 6,
            'Material': 7,
            'Purpose': 8,
        }

    def __reorder(self, adjs, categories):
        category_numbers = [self.map[category] for category in categories]
        dictionary = {}
        for adj, category_number in zip(adjs, category_numbers):
            dictionary[category_number] = adj
        category_numbers.sort()
        new_adjs = [dictionary[category_number]
                    for category_number in category_numbers]
        return new_adjs

    def reorder_adj(self, text):
        adjs, pos_s, spans, tokens = self.extractor.find_adjs(text)

        correct_adjs = []
        for _adjs, _pos_s in zip(adjs, pos_s):
            if len(_adjs) == 1:
                correct_adjs.append(_adjs)
                continue
            else:
                categories = []
                for adj, pos in zip(_adjs, _pos_s):
                    if pos == 'VERB_VBG':
                        category = 'Purpose'
                    else:
                        category = self.categorizer.infer(adj)
                    categories.append(category)
                correct_adjs.append(self.__reorder(_adjs, categories))

        for adjs in correct_adjs:
            start = spans.pop(0)
            end = spans.pop(0)
            tokens[start:end] = adjs

        return " ".join(tokens)

if __name__ == "__main__":
    reodering = ReorderADJ()
    print(reodering.reorder_adj("Is that your silver Mexican favorite necklace?"))
    print(reodering.reorder_adj("Yesterday, I bought a yellow new car at a dealer."))
    print(reodering.reorder_adj("She was wearing a red amazing coat."))