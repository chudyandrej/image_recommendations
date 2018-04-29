import os
import json
import re
import random
import gensim.models.keyedvectors as word2vec

import nltk
from collections import Counter

PATH_IMG_TAGS = './data/img_label.json'
MODELS_PATH = './model/'

# First start program
# nltk.download(["brown", "webtext", "words", "stopwords"])
# nltk.download(["punkt", "averaged_perceptron_tagger", "maxent_ne_chunker", "vader_lexicon", "wordnet", "tagsets"])

class Recommender:

    def __init__(self):
        self.image_to_tags = {}
        self.tag_to_images = {}

        self.word_model = word2vec.KeyedVectors.load_word2vec_format(MODELS_PATH + "GoogleNews-vectors-negative300.bin",
                                                                     binary=True)


        self.load_data()

    def load_data(self):
        if not os.path.exists(PATH_IMG_TAGS):
            print("Image to tag json not found!")
            exit(1)

        with open(PATH_IMG_TAGS, 'r') as the_file:
            raw_json = the_file.read()

        self.image_to_tags = json.loads(raw_json)
        self.set_tag_to_images()

    def set_tag_to_images(self):
        for key, tags_str in self.image_to_tags.items():
            tags_raw = re.split("\s*,\s*|\s+", tags_str)

            for tag in tags_raw:
                tag = tag.lower()
                try:
                    self.word_model.get_vector(tag)
                except:
                    continue

                if tag in self.tag_to_images:
                    self.tag_to_images[tag].append(key)
                else:
                    self.tag_to_images[tag] = [key]

        print("Loaded " + str(len(self.tag_to_images.keys())) + " tags")

    def recommend_image(self, text, count=12):
        images = []
        nouns = get_nouns(text, 4)
        for noun in nouns:
            try:
                tag = self.word_model.most_similar_to_given(noun, list(self.tag_to_images.keys()))
            except KeyError:
                continue
            print("Noun " + noun + " found tag " + tag)
            images += self.tag_to_images[tag]

        if len(images) < count:
            return images

        return random.sample(images, count)


def token_counts(tokens):
    counts = Counter(tokens)
    sorted_counts = sorted(counts.items(), key=lambda count: count[1], reverse=True)
    return sorted_counts


def get_nouns(text, top_n):
    tagged_concatenated = []
    sentences = nltk.sent_tokenize(text)
    tokens = [nltk.word_tokenize(sent) for sent in sentences]
    tagged = [nltk.pos_tag(sent) for sent in tokens]
    for sent in tagged:
        tagged_concatenated += sent
    nouns_tag = list(filter(lambda x: x[1] == "NN" or x[1] == "NNS", tagged_concatenated))
    top_n_nouns = token_counts(list(map(lambda x: x[0].lower(), nouns_tag)))[:top_n]
    return list(map(lambda x: x[0], top_n_nouns))
