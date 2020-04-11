# Text generation

## Character lines
We have got about 60k character lines. The top speakers are:

 - Rachel (9189 lines)
 - Ross (9011 lines)
 - Monica (8335 lines)
 - Chandler (8301 lines)
 - Joey (8116 lines)
 - Phoebe (7402 lines)
 - Mike (359 lines)
 - All (334 lines)
 - Richard (254 lines)
 - Janice (210 lines)

Some characters (Janice for example) have repetitive ("Oh... my... God...") lines, so we can generate them with the obvious lack of data.

We will train several different seq2seq models to imitate dialogs: several models per each character.  We will also describe an approach to predict who will talk at each moment of the play.

### Text generation

The TV script generation problem can be shown as a dialogue system problem, where each dialogue has a lot of participants.

We will use different techniques to generate text. The main problem is that we have not enough data to train a good generator from scratch using only transcripts.

There are two diametrically opposite approaches on text generation with low datasets:

1. To use simple models, which can handle low amounts of data.
2. To augment our data or to use some pretrained models, which have some additional information about the world. We can use more complex models in this case.

An important aspect of dialogue response generation is how to evaluate the quality of the generated answers. Recent works in dialogue systems use adopted metrics from machine translation.

There is shown that these metrics correlate very weakly (or do not correlate at all) with human judgements.
These metrics do encourage the appearance of words of the source sequence in the response, while normal dialogue does not require this.

#### Simple n-gram approach.

We can use a simple n-gram language model to generate text. We will use simple WordPunct tokenizer, provided by nltk.
We take top n tokens sorted by frequency, all other tokens will be changed to unknown.
The idea is to learn the frequency of tokens followed by each possible prefix of length $n$ in the dataset.

The problem is that such language models do not "remember" tokens occurred earlier than last $n$ tokens. Such low instantaneous memory can become an issue for dialogue systems.

Also this type of models can have no "intuition" or "augmented information about the world". The model will repeat the most popular patterns (token chains) in text, but it's generalization ability is very low.


#### Recurrent neural networks for dialogue systems.

Recent time in the past the two main RNN architectures were invented for text processing: GRU and LSTM. These architectures are invented to eliminate two main RNN problems: the problem of vanishing and exploding gradients.

__LSTM__ (Long Short Term Memory)

__GRU__ (Gated Recurrent Unit) networks

There also is an individual technique, __backpropagation through time__, which is used for RNN training.

Now we are using GRU with Bahdanau attention.

### Character choice

One of the main tasks is to determine which character should say a line at each moment of the script.

We will use perplexity as a measure of how well does our model approximate true probability distribution behind the data. Better models have smaller perplexity.

To compute perplexity on one character line sequence, we use:
$$
    {\mathbb{P}}(cl_1 \dots cl_N) = P(cl_1, \dots, cl_N)^{-\frac1N} = \left( \prod_t P(cl_t \mid cl_{t - n}, \dots, cl_{t - 1})\right)^{-\frac1N},
$$

This number can quickly get too small for float32/float64 precision, so we will first compute log-perplexity (from log-probabilities) and then take the exponent.

#### Simple choice using Markov chains.

Let's assume that there is no dependency between the character and the previous lines told. We will try to detect the true sequence using only character sequence.

All popular characters will be given unique ids.
Once we can count N-grams, we can build a probabilistic language model.
The simplest way to compute probabilities is in proporiton to counts:

$$ P(w_t | prefix) = { Count(prefix, w_t) \over \sum_{\hat w} Count(prefix, \hat w) } $$

Models with Laplace smoothing are expected to have lower perplexity:

$$ P(w_t | prefix) = { Count(prefix, w_t) + \delta \over \sum_{\hat w} (Count(prefix, \hat w) + \delta) } $$

There also is a Kneser-Ney smoothing, which is a State of The Art algorithm for today.
It can be computed recurrently, for n>1:

$$P_{kn}(w_t | prefix_{n-1}) = { \max(0, Count(prefix_{n-1}, w_t) - \delta) \over \sum_{\hat w} Count(prefix_{n-1}, \hat w)} + \lambda_{prefix_{n-1}} \cdot P_{kn}(w_t | prefix_{n-2})$$

The output perplexity is low enough to use this technique to generate scripts:

| Model  | Smoothing  | Perplexity |
| :---:  | :--------: | ---------: |
| 1-gram | None       | 10.91214   |
| 2-gram | None       | 11.13090   |
| 3-gram | None       | 32.90798   |
| 1-gram | Laplace    | 10.27697   |
| 2-gram | Laplace    |  9.34600   |
| 3-gram | Laplace    | 17.28860   |
| 1-gram | Kneser-Ney |  9.84830   |
| 2-gram | Kneser-Ney |  8.14304   |
| 3-gram | Kneser-Ney | 12.50320   |

One of the reasons of good (comparing to language modeling) n-gram perplexity here is that the amount of characters is much lower than the amount of words in any language (even the semantic primes language by Anna Wierzbicka is has more tokens and their usage patterns are much more complex).

#### Improved techniques.

## Stage directions
We will not generate stage directions at this work: there is about 4k samples. The data is very noisy and unstructured. There is no background to become good at stage directions generation using this data.
