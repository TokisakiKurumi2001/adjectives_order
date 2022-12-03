# Import libraries
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier


class CategorizeADJ:
    def __init__(self):
        # Loading GloVe
        print("Initializing GloVe embedding")
        self.embed_dict = {}
        with open('./glove.6B.200d.txt', 'r') as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = np.asarray(values[1:], 'float32')
                self.embed_dict[word] = vector
        print("Initialized GloVe embedding")

        # Loading dataset
        print("Initializing ADJ class data")
        self.data = pd.read_csv('./adj_category.csv')
        print("Initialized ADJ class data")

        # Loading dataset for KNN
        print("Initializing KNN")
        self.le = preprocessing.LabelEncoder()
        self.le.fit(self.data.Class.unique().tolist())
        y = self.le.transform(self.data.Class.values.tolist())

        words = self.data.Word.values.tolist()
        X = np.array([self.embed_dict[word] for word in words])

        self.neigh = KNeighborsClassifier(n_neighbors=3)
        self.neigh.fit(X, y)
        print("Initialized KNN")

    def infer(self, word):
        idx = self.data[self.data['Word'] == word].Class.tolist()
        if len(idx) == 0:
            try:
                embed_vector = self.embed_dict[word]
                return self.le.inverse_transform(self.neigh.predict(embed_vector.reshape(1, -1))).tolist()[0]
            except:
                return 'Origin'
        else:
            return idx[0]


if __name__ == "__main__":
    categorizer = CategorizeADJ()
    print(categorizer.infer('amazing'))
    print(categorizer.infer('huge'))
    print(categorizer.infer('new'))
    print(categorizer.infer('oval'))
    print(categorizer.infer('magenta'))
    print(categorizer.infer('British'))
    print(categorizer.infer('metal'))
