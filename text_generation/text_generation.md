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

### Character choice
One of the main tasks is to determine which character should say a line at each moment of the script.

We will use perplexity as a measure of how well does our model approximate true probability distribution behind the data. Better models have smaller perplexity.

To compute perplexity on one character line sequence, we use:
$$
    {\mathbb{P}}(cl_1 \dots cl_N) = P(cl_1, \dots, cl_N)^{-\frac1N} = \left( \prod_t P(cl_t \mid cl_{t - n}, \dots, cl_{t - 1})\right)^{-\frac1N},
$$

This number can quickly get too small for float32/float64 precision, so we will first compute log-perplexity (from log-probabilities) and then take the exponent.

#### Simple choice using Markov chains
Let's assume that there is no dependency between the character and the previous lines told. We will try to detect the true sequence using only character sequence.

All popular characters will be given 
Once we can count N-grams, we can build a probabilistic language model.
The simplest way to compute probabilities is in proporiton to counts:

$$ P(w_t | prefix) = { Count(prefix, w_t) \over \sum_{\hat w} Count(prefix, \hat w) } $$

The output perplexity is low enough to use this technique to generate scripts.

#### Improved techniques

## Stage directions
We will not generate stage directions at this work: there is about 4k samples. The data is very noisy and unstructured. There is no background to become good at stage directions generation using this data.
