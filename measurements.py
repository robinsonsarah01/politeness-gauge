import emoticons, curses, enron_politeness, polite_phrases


counts = {
    "curses": 0
    ,"emoticons": 0
    ,"politeness": 0
}


def clean_text(input):
    """
    TODO do more of this
    Remove punctuation that messes up word tokenization.
    """
    clean_input = input
    if not input[-1].isalnum():
        clean_input = input[:-1] + " " + input[-1]
        
    # TODO maybe deal with contractions?
    
    return clean_input


def get_scores(input_text):
    """
    Get all of the various politeness scores and return them in a dictionary.
    """
    input_text = clean_text(input_text)
    
    tokens = enron_politeness.tokenize_text(input_text)
    enron_score = enron_politeness.get_enron_politeness_score(tokens)
    phrases_score = polite_phrases.excuse_me_sir(input_text)
    counts["politeness"] = enron_score + phrases_score
    
    counts["curses"] = curses.curses_foiled_again(input_text)
    
    counts["emoticons"] = emoticons.get_emoticon_count(input_text)
    
    print input_text.count(".")
    counts["input_len"] = len(tokens) - input_text.count(".")
    
    print counts["politeness"], counts["input_len"], "--", float(counts["politeness"]) / counts["input_len"]
    
    return counts
    
    
def get_overall_score():
    """
    Based on current counts, calculate an overall politeness score.
    """
    score = 50
    if counts["input_len"] != 0:
        # politeness score on n-grams is relative to input length
        # out of 75 to make the top politeness score something like 50 -- then top overall score ~100
        score += ( float(counts["politeness"]) / counts["input_len"] ) * 75
    score -= counts["curses"] * 10
    score -= counts["emoticons"] * 4
    return score
    
    
if __name__ == "__main__":
    input = "Thank you for contacting me! I'm generally free in the mornings before 11 and in the afternoons after 4 on weekdays; is there any time that would be most convenient to meet to discuss the job? thank you,"
    print get_scores(input)
    print get_overall_score()
    print
    input = "wtf prof i told you i needed that damn recommendation like today. fuck!!! >:O dude like wtf"
    print get_scores(input)
    print get_overall_score()