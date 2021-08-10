def load_english_words():
    with open('words/english_words.txt') as word_file:
        valid_words = set(word_file.read().split())
    
    return valid_words

def load_samples():
    with open('words/swenglish_sample.txt') as sample_file:
        sample_sentences = set(sample_file.read().split('\n'))

    return sample_sentences

def get_swenglish_data(english_words, sentence):
    swenglish_data = {}

    words = sentence.split(' ')
    amount_of_words = len(words)
    amount_of_detected_english_words = 0
    for word in words:
        if word in english_words:
            amount_of_detected_english_words += 1
    
    if amount_of_words != 0 or amount_of_detected_english_words != 0:
        english_ratio = amount_of_detected_english_words / amount_of_words
    else:
        english_ratio = 0
    
    swenglish_data["text"] = sentence
    swenglish_data["english_ratio"] = english_ratio
    swenglish_data["total_words"] = amount_of_words
    swenglish_data["english_words"] = amount_of_detected_english_words

    return swenglish_data

def is_swenglish_by_ratio(min, max, swenglish_data):
    english_ratio = swenglish_data["english_ratio"]
    if english_ratio > min and english_ratio < max:
        return True
    else:
        return False

def is_swenglish_easy(loaded_english_words, sentence):
    swenglish_data = get_swenglish_data(loaded_english_words, sentence)
    is_swenglish = is_swenglish_by_ratio(swenglish_data)
    return is_swenglish 


def print_swenglish_data(swenglish_data):
    
    print("english words: " + str(swenglish_data["english_words"]))
    print("total words: " + str(swenglish_data["total_words"]))
    print("english ratio: " + str(swenglish_data["english_ratio"]))

if __name__ == '__main__':
    loaded_english_words = load_english_words()
    sample_sentences = load_samples()
    # demo print

    for sample in sample_sentences:

        swenglish_data = get_swenglish_data(english_words=loaded_english_words, sentence=sample)

        print(sample)
        print("english words: " + str(swenglish_data["english_words"]))
        print("total words: " + str(swenglish_data["total_words"]))
        print("english ratio: " + str(swenglish_data["english_ratio"]))
        print("-----------------------------------")