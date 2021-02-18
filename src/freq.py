def calculate_prob(dir_name, file_name, extension):
    """
    Generates probability of all characters in a given sample file.
    """
    with open(dir_name + file_name + extension, 'r') as sample_file:
        text: str = sample_file.readline()

    length = 0
    freq = {}
    for char in text:
        length += 1

        no_cases = freq.get(char, None)
        if no_cases is not None:
            freq[char] += 1
        else:
            freq[char] = 0

    freq = {k: v for k, v in sorted(freq.items(), key=lambda val: val[1], reverse=True)}

    prob = {}
    for k, v in freq.items():
        prob[k] = v / length

    return prob