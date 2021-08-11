from textblob import *

def load_samples():
    with open('words/swenglish_sample.txt') as sample_file:
        sample_sentences = set(sample_file.read().split('\n'))

    return sample_sentences

discounted_words = ['yeah', 'man', 'google', 'lootspec','']

# The reason we have short swedish words here is that google refuses to identify words below 3 characters.
def get_swenglish_data(short_swedish_words, sentence):
    swedish_amount = 0
    english_amount = 0
    undetectable_words_amount = 0
    swenglish_verdict = "unknown"
    swenglish_data = {}

    list_of_words = sentence.replace(',', '').replace('.','').split(' ')

    # TextBlob.detect_language() requires a string with at least 3 characters, and some words don't count
    for word in list_of_words:
        if word in discounted_words:
            list_of_words.remove(word)
            undetectable_words_amount += 1
    
    total_words = len(list_of_words)

    for word in list_of_words:
        blob = TextBlob(word)
        if len(word) >= 3:
            result = blob.detect_language() # Uses google API
        elif word.lower() in short_swedish_words:
            result = "sv"
        else:
            result = "unknown"

        if result == "sv":
            swedish_amount += 1
        elif result == "en":
            english_amount += 1
    
    """
    
    How to detect swenglish?
    There needs to be a mix of swedish and english

    We have identified swenglish can happen with huge ratios, or lower ratios.
    As high as 90% swedish or 66% english or 8.3% english, etc

    So how do we determine it?
    Perhaps we shall test a few approaches.

    Approach "ratio":
        min ratio, max ratio for swedish
        min ratio, max ratio for english

    Approach "raw" or "keep it simple stupid:
        At least 3 words
        At least both english and swedish detected
    """

    if total_words >= 3 and swedish_amount > 0 and english_amount > 0:
        swenglish_verdict = "swenglish"
    elif swedish_amount == 0 and english_amount > 0:
        swenglish_verdict = "english"    
    elif english_amount == 0 and swedish_amount > 0:
        swenglish_verdict = "swedish"
    elif english_amount == 0 and swedish_amount == 0:
        swenglish_verdict = "unknown"

    if total_words != 0:
        swedish_ratio = swedish_amount / total_words
        english_ratio = english_amount / total_words
    else:
        swedish_ratio = 0
        english_ratio = 0
        

    swenglish_data["text"] = sentence
    swenglish_data["swenglish_verdict"] = swenglish_verdict
    swenglish_data["swedish_ratio"] = swedish_ratio
    swenglish_data["english_ratio"] = english_ratio
    swenglish_data["swedish_words"] = swedish_amount
    swenglish_data["english_words"] = english_amount
    swenglish_data["total_words"] = total_words
    swenglish_data["undetectable_words_amount"] = undetectable_words_amount

    return swenglish_data

def print_swenglish_data(swenglish_data):
    for key, value in swenglish_data:
        print(key, ' : ', value)

def is_swenglish_by_ratio(min, max, swenglish_data):
    english_ratio = swenglish_data["english_ratio"]
    if english_ratio > min and english_ratio < max:
        return True
    else:
        return False

def is_swenglish_by_verdict(sentence):
    swenglish_data = get_swenglish_data(sentence)
    return swenglish_data["verdict"] == "swenglish"

if __name__ == '__main__':
    sample_sentences = load_samples()

    for sample in sample_sentences:
        swenglish_data = get_swenglish_data(sentence=sample)
        print_swenglish_data(swenglish_data)