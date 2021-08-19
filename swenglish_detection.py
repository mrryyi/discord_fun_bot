from textblob import *
import time

def load_samples():
    with open('words/swenglish_sample.txt') as sample_file:
        sample_sentences = set(sample_file.read().split('\n'))

    return sample_sentences

# Words we will pretend doesn't exist
discounted_words = ['yeah','man','google','lootspec','imorrn','immorn','boten','loot','spec','vault','trinket','trinkets','loostspec','raid',
                    'fast','racing','yhea','oliver', 'lol']


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


# The reason we have short swedish words here is that google refuses to identify words below 3 characters.
def get_swenglish_data(short_swedish_words, sentence):
    swenglish_data = {}
    swenglish_data["text"] = sentence
    swenglish_data["swenglish_verdict"] = "unknown"
    swenglish_data["swedish_ratio"] = 0
    swenglish_data["english_ratio"] = 0
    swenglish_data["swedish_amount"] = 0
    swenglish_data["english_amount"] = 0
    swenglish_data["english_words"] = []
    swenglish_data["swedish_words"] = []
    swenglish_data["total_words"] = 0
    swenglish_data["undetectable_words_amount"] = 0
    swenglish_data["text"] = sentence
    
    # Don't risk adding a quote like: "Jag gillar det här citatet: "I am become death.""
    if "\"" in sentence or "'" in sentence or "“" in sentence:
        return swenglish_data
        
    list_of_words = sentence.replace(',', '').replace('.','').split(' ')
    
    # We remove discounted words here, so that before we go calling googles API,
    # we have already made sure it's a list of at least 3 words.
    # Otherwise, we could go detect 2 words using the API for no reason, since
    # one of our requirements are to have at least 3 words in total.
    for word in list_of_words:
        if word in discounted_words or (word not in short_swedish_words and len(word) < 3):
            list_of_words.remove(word)
            swenglish_data["undetectable_words_amount"] += 1

    swenglish_data["total_words"] = len(list_of_words)

    # Since one requirement for verdict is that there are at least 3 words
    # And we don't want to check absurdly long texts
    if len(list_of_words) < 3 or len(list_of_words) > 12:
        return swenglish_data

    for word in list_of_words:
        # TextBlob.detect_language() requires a string with at least 3 characters
        if len(word) >= 3:
            blob = TextBlob(word)
            try:
                result = blob.detect_language() # Uses google API
                time.sleep(1)
            except:
                print("Too many req")
                break # give up
        elif word.lower() in short_swedish_words:
            result = "sv"
        else:
            result = "unknown"

        if result == "sv":
            swenglish_data["swedish_amount"] += 1
            swenglish_data["swedish_words"].append(word)
        elif result == "en":
            swenglish_data["english_amount"] += 1
            swenglish_data["english_words"].append(word)

    if swenglish_data["total_words"] >= 3 and swenglish_data["swedish_amount"] > 0 and swenglish_data["english_amount"] > 0:
        swenglish_data["swenglish_verdict"] = "swenglish"
    elif swenglish_data["swedish_amount"] == 0 and swenglish_data["english_amount"] > 0:
        swenglish_data["swenglish_verdict"] = "english"    
    elif swenglish_data["english_amount"] == 0 and swenglish_data["swedish_amount"] > 0:
        swenglish_data["swenglish_verdict"] = "swedish"
    
    if swenglish_data["total_words"] != 0:
        swenglish_data["swedish_ratio"] = swenglish_data["swedish_amount"] / swenglish_data["total_words"]
        swenglish_data["english_ratio"] = swenglish_data["english_amount"] / swenglish_data["total_words"]

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