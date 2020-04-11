from collections import Counter, defaultdict, deque
from typing import List, Dict
from typing import Counter as C, DefaultDict as DD, Deque as Deq, Tuple
import numpy as np
import sys
sys.path.append('..')
from corpus_preprocessing import utils

UNK_CHARACTER = 'UNK_CHARACTER'
END_CHARACTER = 'END_CHARACTER'


def filter_stage_directions(scenes: List[utils.Scene]):
    # FIXME this function is written in procedural style
    # and produces side effects
    """
    Filters list of scenes and deletes stage directions
    Params:
        scenes -- a list of scenes
    """
    for scene in scenes:
        scene.actions = list(filter(
                            lambda x: not isinstance(x, utils.StageDirection),
                            scene.actions))


def generate_character_to_id_dict(scenes: List[utils.Scene],
                                  top_k_characters: int) -> Dict[str, int]:
    """
    Generates the dict to map characters to their ids
    Params:
        scenes -- a list of scenes
        top_k_characters -- how much ids will be given to characters
    """
    actor_counter: C[str] = Counter()

    for scene in scenes:
        for action in scene.actions:
            actor_counter[action.actor] += 1

    character_to_id = {
        actor[0]: index for index, actor in enumerate(
            [
                (UNK_CHARACTER, 0),
                (END_CHARACTER, 0),
            ] + actor_counter.most_common(top_k_characters))
    }
    return character_to_id


def generate_id_to_character_dict(scenes: List[utils.Scene],
                                  top_k_characters: int) -> Dict[int, str]:
    """
    Generates the dict to map characters to their ids
    Params:
        scenes -- a list of scenes
        top_k_characters -- how much ids will be given to characters
    """
    actor_counter: C[str] = Counter()

    for scene in scenes:
        for action in scene.actions:
            actor_counter[action.actor] += 1

    id_to_character = {
        index: actor[0] for index, actor in enumerate(
            [
                (UNK_CHARACTER, 0),
                (END_CHARACTER, 0),
            ] + actor_counter.most_common(top_k_characters))
    }
    return id_to_character


def scenes_to_character_sequences(
        scenes: List[utils.Scene],
        character_to_id: Dict[str, int]) -> List[List[int]]:
    """
    Generates list of lists of character ids
    Params:
        scenes -- a list of scenes
        character_to_id -- the dict to map characters to their ids
    """
    character_sequences: List[List[int]] = []

    for scene in scenes:
        sequence: List[int] = []

        for action in scene.actions:
            if action.actor in character_to_id:
                sequence.append(character_to_id[action.actor])
            else:
                sequence.append(character_to_id[UNK_CHARACTER])

        character_sequences.append(sequence)

    return character_sequences


def count_ngrams(
        rows: List[List[int]],
        n: int,
        character_to_id: Dict[str, int]) -> DD[Tuple[int, ...], C[int]]:
    """
    Generates dict with ngrams
    This dict is a mapping from prefix to counter of suffixes
    Params:
        rows -- list of character ids
        n -- length of n-gram
        character_to_id -- the dict to map characters to their ids
    """
    counts: DD[Tuple[int, ...], C[int]] = defaultdict(Counter)
    for row in rows:
        q: Deq[int] = deque(maxlen=n-1)
        for character in [
            character_to_id[UNK_CHARACTER]]*(n-1) + \
                row + \
                [character_to_id[END_CHARACTER]]:
            if len(q) == n - 1:
                counts[tuple(q)][character] += 1
            q.append(character)
    return counts


class MarkovCharacterChoice:
    """
    Simple Markov model to choose next character
    """
    # TODO type annotations
    def __init__(self, lines, n, character_to_id):
        assert n >= 1
        self.n = n
        counts = count_ngrams(lines, self.n, character_to_id)
        self.character_to_id = character_to_id
        self.probs: DD[Tuple[int, ...], C[int]] = defaultdict(Counter)

        for prefix in counts:
            _s = sum(counts[prefix].values())
            for key, value in counts[prefix].items():
                self.probs[prefix][key] = value / _s

    def get_possible_next_characters(self, prefix):
        prefix = prefix[max(0, len(prefix) - self.n + 1):]
        prefix = [
            self.character_to_id[UNK_CHARACTER]
        ] * (self.n - 1 - len(prefix)) + prefix
        return self.probs[tuple(prefix)]

    def get_next_character_prob(self, prefix, next_token):
        return self.get_possible_next_characters(prefix).get(next_token, 0)


def perplexity(chm, rows, character_to_id, min_logprob=np.log(10 ** -50.)):
    """
    Metrics for character sequence generation
    Params:
        chm -- character model instance
        rows -- list of character ids
        character_to_id -- the dict to map characters to their ids
        min_logprob -- minimal logprob is used to avoid of
                       float32/float64 precision errors
    """
    # TODO type annotations
    log_res = 0
    for row in rows:
        buf = row + [character_to_id[END_CHARACTER]]
        for i in range(len(buf)):
            prob = chm.get_next_character_prob(buf[:i], buf[i])
            if prob == 0:
                log_res += min_logprob
            else:
                log_res += max(
                    min_logprob,
                    np.log(prob)
                )

    return np.exp(log_res * (-1 / sum(map(lambda x: len(x), rows))))


def get_next_character(chm, prefix, temperature=1.0):
    """
    Generates next character based on prefix
    Params:
        chm -- character model instance
        prefix -- list of previous character ids
        temperature -- measure of generator randomness
    """
    # TODO type annotations
    if temperature == 0:
        return chm.get_possible_next_characters(prefix).most_common(1)[0][0]

    candidates = list(map(lambda x: (x[1] ** (1/temperature), x[0]),
                      chm.get_possible_next_characters(prefix).items()))

    ps = np.array(list(map(lambda x: x[0], candidates)))
    ps /= np.sum(ps)
    return np.random.choice(list(map(lambda x: x[1], candidates)), 1, p=ps)[0]
