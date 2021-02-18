from zero_order import ZeroOrder
from first_order import FirstOrder
from markov import MarkovSource
from freq import calculate_prob

output_dir = 'output/'

prob_dir = 'probabilities/'
prob_file = 'prob_'
extension = '.txt'

no_samples = 3
sample_dir = 'samples/'
sample_name = 'sample_'


def average_len(seq: str) -> int:
    """
    Returns average length of a given sequence rounded to int.
    """
    words = seq.split(' ')
    while '' in words:
        words.remove('')

    average = sum(len(word) for word in words) / len(words)
    
    return round(average)


def generate_zero(no_chars=10**3, file_save=True):
    """
    Generates zero-order approximation based on 
    homogenous probabilities of characters.
    """
    zero_order = ZeroOrder()
    output = zero_order.get_chars(no_chars)

    if file_save:
        with open(output_dir + "zero" + extension, 'w+') as out_file:
            out_file.write(output)

    return output


def _generate_prob():
    """
    Generates probabilities for first-order aprox and save them to file.\n
    Function called automatically during generate_first.
    """
    for i in range(no_samples):
        prob = calculate_prob(sample_dir, sample_name + str(i), extension)

        with open(prob_dir + prob_file + str(i) + extension, 'w+') as pfile:
            pfile.write(str(prob))


def generate_first(no_chars=10**3, sample_num='2', file_save=True):
    """
    Generates first-order approximation depending of 
    frequency of characters in each sample file.
    """
    _generate_prob()

    with open(prob_dir + prob_file + sample_num + extension, 'r') as pfile:
        prob = eval(pfile.read())
    
    first_order = FirstOrder(prob)
    output = first_order.get_chars(no_chars)

    if file_save:
        with open(output_dir + f"first_{sample_num}" + extension, 'w+') as out_file:
            out_file.write(output)
    
    return output


def generate_markov(markov_order: int, no_chars=1000, start_phrase='', 
                    sample_num='2', file_save=True) -> str:
    """
    Generates sequence with number of given characters based on
    markov information source with given order on a given sample file.\n
    Note that the sample file must be present in samples directory and named: 
    sample_[...].txt where [...] is a sample's number.\n
    Output can be also saved if specified so.
    """
    with open(sample_dir + sample_name + sample_num + extension, 'r') as ftext:
        text = ftext.read()

    markov = MarkovSource(markov_order, text)
    output = markov.get_chars(no_chars, start_phrase)

    if file_save:
        with open(output_dir + f"markov_{markov_order}" + extension, 'w+') as outfile:
            outfile.write(output)
    
    return output


def generate():
    # General note - sample_2 is 10 times bigger than sample_1 and sample_0 so it takes much more time to complete
    averages = ["Average word length:\n"]

    output = generate_zero()
    averages.append(f"zero_avg: {str(average_len(output))}\n")

    output = generate_first()
    averages.append(f"first_avg: {str(average_len(output))}\n")

    output = generate_markov(1)
    averages.append(f"markov_1_avg: {str(average_len(output))}\n")

    output = generate_markov(3)
    averages.append(f"markov_3_avg: {str(average_len(output))}\n")

    output = generate_markov(5, start_phrase='probability')
    averages.append(f"markov_5_avg: {str(average_len(output))}\n")

    with open(output_dir + "averages" + extension, 'w+') as favg:
        favg.writelines(averages)


if __name__ == "__main__":
    generate()

    ## Testing
    # generate_markov(8, start_phrase='i will frown as i pass by', sample_num='1')
    # generate_markov(12, start_phrase='i will frown as i pass by', sample_num='1')