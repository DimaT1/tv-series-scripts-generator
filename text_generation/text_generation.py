from collections import Counter
from nltk.tokenize import WordPunctTokenizer
import numpy as np
from character_choice import UNK_CHARACTER


UNK = '__UNK__'
BOS = '__BOS__'
EOS = '__EOS__'


def tokenize(x):
    tokenizer = WordPunctTokenizer()
    return ' '.join(map(str.lower, tokenizer.tokenize(x)))


def tokenize_scenes(scenes):
    # FIXME this function is written in procedural style
    # and produces side effects
    for scene in scenes:
        for action in scene.actions:
            action.line = tokenize(action.line)


def generate_vocab(scenes):
    vocab = Counter()
    for scene in scenes:
        for action in scene.actions:
            for word in action.line.split():
                vocab[word] += 1
    return vocab


def generate_word_to_id(vocab, top_k=10_000):
    return {
        y: x for x, y in enumerate(
            [
                BOS,
                EOS,
                UNK
            ] + list(map(lambda x: x[0], vocab.most_common(top_k))))}


def generate_id_to_word(vocab, top_k=10_000):
    return {
        x: y for x, y in enumerate(
            [
                BOS,
                EOS,
                UNK
            ] + list(map(lambda x: x[0], vocab.most_common(top_k))))}


def words_to_ids(line: str, word_to_id, sentence_len=50) -> np.array:
    res = [word_to_id[BOS]]
    line = line.split()
    for i in range(sentence_len - 2):
        if i < len(line):
            word = line[i]
        else:
            word = EOS
        if word not in word_to_id:
            word = UNK
        res.append(word_to_id[word])
    return np.array(res)


def ids_to_words(arr: np.array, id_to_word) -> str:
    res = []
    for id in arr:
        res.append(id_to_word[id])
    return ' '.join(filter(lambda x: x not in {BOS, EOS, UNK}, res))


def generate_trainable_data(scenes, character_to_id, word_to_id):
    data = []

    for scene in scenes:
        buf = []
        for action in scene.actions:
            character_id = UNK_CHARACTER
            if action.actor in character_to_id:
                character_id = character_to_id[action.actor]
            text = words_to_ids(action.line, word_to_id)

            buf.append((character_id, text))
        data.append(buf)

    return data
