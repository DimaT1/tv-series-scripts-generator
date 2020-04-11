from collections import Counter
from nltk.tokenize import WordPunctTokenizer
from nltk.translate.bleu_score import corpus_bleu
import numpy as np
from character_choice import UNK_CHARACTER
import tensorflow as tf


UNK = '__UNK__'
BOS = '__BOS__'
EOS = '__EOS__'
L = tf.keras.layers
keras = tf.keras


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
    for _id in arr:
        res.append(id_to_word[_id])
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


class DialogueModel(L.Layer):
    def __init__(self, vocab_size, embedding_dim, n_units, batch_sz):
        super().__init__()

        self.batch_sz = batch_sz
        self.enc_units = self.dec_units = n_units

        self.inc_emb = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.dec_emb = tf.keras.layers.Embedding(vocab_size, embedding_dim)

        self.enc = tf.keras.layers.GRU(self.enc_units,
                                       return_sequences=True,
                                       return_state=True,
                                       recurrent_initializer='glorot_uniform')

        self.dec = tf.keras.layers.GRU(self.dec_units,
                                       return_sequences=True,
                                       return_state=True,
                                       recurrent_initializer='glorot_uniform')

        self.fc = tf.keras.layers.Dense(vocab_size)

        self.W1 = tf.keras.layers.Dense(self.dec_units)
        self.W2 = tf.keras.layers.Dense(self.dec_units)
        self.V = tf.keras.layers.Dense(1)

    def encode(self, inp):
        hidden = tf.zeros((self.batch_sz, self.enc_units))
        x = self.inc_emb(inp)
        output, state = self.enc(x, initial_state=hidden)
        return output, state

    def bahdanau_attention(self, query, values):
        query_with_time_axis = tf.expand_dims(query, 1)
        score = self.V(tf.nn.tanh(
            self.W1(query_with_time_axis) + self.W2(values)))
        attention_weights = tf.nn.softmax(score, axis=1)
        context_vector = attention_weights * values
        context_vector = tf.reduce_sum(context_vector, axis=1)
        return context_vector, attention_weights

    def decode(self, x, hidden, enc_output):
        context_vector, attention_weights = self.bahdanau_attention(
            hidden,
            enc_output
        )
        x = self.embedding(x)
        x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)
        output, state = self.gru(x)
        output = tf.reshape(output, (-1, output.shape[2]))
        x = self.fc(output)
        return x

    def call(self, inp):
        sample_output, sample_hidden = self.encode(inp)
        return self.decode(tf.random.uniform((self.batch_sz, 1)),
                           sample_hidden, sample_output)


def predict_answer(model, character, line, answ):
    pass


def KEDS():
    ## K-Means Evaluation for Dialogue Systems
    pass
