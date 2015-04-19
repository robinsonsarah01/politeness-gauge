polite_unigrams = [
    "definitely"
    ,"surely"
    ,"absolutely"
    ,"certainly"
    ,"fantastic"
    ,"inconvenience"
    ,"pardon"
    ,"hope"
    ,"seem"
    ,"perhaps"
    ,"excuse"
    ,"prefer"
    ,"please"
    ,"sorry"
    ,"assure"
    ,"if"
]

# polite_bigrams = [
    # "rest assured"
    
# ]

polite_phrases = [ " " + x + " " for x in polite_unigrams ]

def excuse_me_sir(to_check):
    """
    Check for the existence of pre-defined polite words in the input string.
    
    Returns the number of polite words.
    Does not catch 
    """
    to_check = to_check.lower()
    to_check = " " + to_check + " " # get the words at the beginning and end
    num_polite = 0
    # we can do this because all of the polite phrases are unigrams
    for word in polite_phrases:
        num_polite += to_check.count(word)
    
    return num_polite

if __name__ == "__main__":
    test = "hello sir please excuse the inconvenience but i was wondering if you "
    print test
    print "there are at least", excuse_me_sir(test), "polite words in this sentence."
