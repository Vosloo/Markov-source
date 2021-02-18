from random import choices
from typing import Tuple

class MarkovSource:
    def __init__(self, markov_type: int, text, supress_status=False):
        self._markov_type = markov_type
        self._text = text
        self._supress_status = supress_status
        self._prob, self._cond_prob = self._calculate_prob()


    def _calculate_cond(self, prob: dict, pair_prob: dict) -> dict:
        """
        Calculates conditional probabilities based on probability of single seq and pair_probability.
        """
        cond_prob = {}
        for pair, probability in pair_prob.items():
            key = pair[:self._markov_type]
            query = prob.get(key, None)
            if query is None:
                raise Exception("Something went wrong")

            cond_prob[f"{key}{pair[self._markov_type:]}"] = probability / query

        return cond_prob


    def _calculate_prob(self) -> Tuple[dict, dict]:
        """
        Calculates probability for characters in text.
        """
        if not self._supress_status:
            print(f"Calculating probabilities for order no.{self._markov_type}, please stand by...")

        prob = {}
        pair_prob = {}
        for ind, char in enumerate(self._text):
            if not self._supress_status and ind == len(self._text) // 4:
                print("Status: 25%") 
            elif not self._supress_status and ind == len(self._text) // 2:
                print("Status: 50%")
            elif not self._supress_status and ind == 3 * len(self._text) // 4:
                print("Status: 75%")

            # Probability of previous sequence
            string = char
            # Just in range of $markov_type because it's probability of $markov_type last chars
            for i in range(1, self._markov_type):
                if ind + i >= len(self._text):
                    break
                string += self._text[ind + i]

            query = prob.get(string, None)
            if query is not None:
                prob[string] += 1
            else:
                prob[string] = 1

            # Probability of pairs
            string = char
            for i in range(1, self._markov_type + 1):
                if ind + i >= len(self._text):
                    break
                string += self._text[ind + i]

            query = pair_prob.get(string, None)
            if query is not None:
                pair_prob[string] += 1
            else:
                pair_prob[string] = 1

        prob_len = sum(prob.values())
        prob = {k: v / prob_len for k, v in prob.items()}
        pair_prob = {k: v / prob_len for k, v in pair_prob.items()}

        if self._markov_type == 0:
            cond_prob = prob
        else:
            cond_prob = self._calculate_cond(prob, pair_prob)

        if not self._supress_status:
            print("Status: 100%")

        return prob, cond_prob


    def _next(self, previous_seq) -> str:
        """
        Returns next character based on previous sequence
        """
        options = {
            key[self._markov_type:]: value for key, value in self._cond_prob.items()
            if previous_seq in key[:self._markov_type]
        }

        if self._markov_type == 0:
            del options[' ']

        return ''.join(choices(list(options.keys()), list(options.values())))


    def get_chars(self, no_chars, start_phrase='') -> str:
        """
        Returns sequence with number of given characters based on markov information source.
        """
        if no_chars < 1:
            raise Exception("No of characters too small!")

        output = start_phrase
        for i in range(len(start_phrase), self._markov_type):
            previous_markov = MarkovSource(i, self._text)

            if previous_markov._markov_type > 0:
                last_seq = output[-self._markov_type:]
            else:
                last_seq = ''

            output += previous_markov._next(last_seq)

        if not self._supress_status:
            print("Generating characters, please stand by...")

        start = max(len(start_phrase), self._markov_type)
        for i in range(start, no_chars):
            if not self._supress_status and i == no_chars // 4:
                print("Status: 25%") 
            elif not self._supress_status and i == no_chars // 2:
                print("Status: 50%")
            elif not self._supress_status and i == 3 * no_chars // 4:
                print("Status: 75%")

            output += self._next(output[-self._markov_type:])

        if not self._supress_status:
            print("Status: 100%")

        return output