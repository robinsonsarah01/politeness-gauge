import os, operator
import nltk
import enron_email_parse as eep

"""
From http://www2.sims.berkeley.edu/courses/is290-2/f04/assignments/assignment4.html

Inside are directories 1, 2, 3, 4, 5, 6, 7, 8, corresponding to the coarse genres (top-level category 1). The 
messages in each directory were assigned to the corresponding coarse genre. For each message, identified by 
numeric ID which matches the "database ID" from the Web interface, you will find a ".txt" file, which contains 
the raw text of the message, including original headers, and a ".cats" file, which contains a line like 
"n1,n2,n3" for each category that message is assigned to. n1 is the top-level category number; n2 is the 
second-level category number; and n3 is the number of times this message was assigned to this category. This 
file format is also described briefly in the file categories.txt, which lists the categories for you. All the 
files have unique names, so you can move them all into one directory if you would prefer to work with them that 
way instead of in genre-separated directories.
"""

# category dictionaries are defined as cat[coarse] = [ list of subcats in this category ]
 
# categories we've decided are polite
polite_cats = {}
polite_cats['1'] = [ '1', '3', '4', '5', '6' ]
polite_cats['2'] = [ '3', '5', '8' ]
polite_cats['3'] = [ str(x) for x in range(1,14) ] # everything in coarse category 3 (ie all of 1.1)
polite_cats['4'] = [ '4', '6' ]

# categories we've decided are impolite
impolite_cats = {}
impolite_cats['1'] = [ '2' ]
impolite_cats['2'] = [ '11', '12' ]
impolite_cats['3'] = []
impolite_cats['4'] = [ '7', '9', '13', '14', '16', '19' ]

# categories we've decided to ignore
ignored_cats = {}
ignored_cats['1'] = [ '7', '8' ]
ignored_cats['2'] = [ '1', '2', '4', '6', '7', '9', '10', '13' ]
ignored_cats['3'] = []
ignored_cats['4'] = [ '1', '2', '3', '5', '8', '10', '11', '12', '15', '17', '18' ]


# ngram dictionaries are defined as cat[n-gram] = count of its appearances in this category
# unigrams, bigrams, and trigrams are the keys; they are represented as strings (words and spaces)
polite_ngrams = {}

impolite_ngrams = {}

selected_polite_ngrams = []


# we have a set of all the ngrams -- find the total count by adding their appearances in the ngram dicts
total_ngrams = set()


# lists of file numbers in the polite or impolite categories
# each entry in the list is a full relative filepath from . to the email file
polite_files = []

impolite_files = []


def categorize_emails():
    """
    Loop through all of the files in enron_with_cats\[1-6] and mark them as polite or impolite.
    """
    for i in range(1,7): # 1 - 6, because we ignore 1.7 and 1.8
        filepath = os.path.join("enron_with_categories",str(i))
        filelist = os.listdir(filepath)
        filelist.sort() # may not be necessary, do it anyway
        i = 0
        num_files = len(filelist)
        while i < num_files:
            cats_file = filelist[i]
            email_file = filelist[i+1]
            type = process_cats( os.path.join(filepath,cats_file) )
            email_filepath = os.path.join(filepath, email_file)
            if type == "polite":
                polite_files.append(email_filepath)
            elif type == "impolite":
                impolite_files.append(email_filepath)
            # else:
                # print "ignoring file", email_file
            i += 2


def process_cats(cat_file):
    """
    Given the path to a .cats file of email categories, returns "polite", "impolite", or "neither".
    """
    f = file(cat_file, 'r')
    lines = f.readlines()
    f.close()
    
    # keep track of the counts for each category
    polite, impolite, ignored = 0, 0, 0
    
    for line in lines:
        line = line.strip()
        # major is the major category (major.x)
        # sub is the minor category (x.sub)
        # num is how many people assigned the email to this category
        major,sub,num = line.split(",")
        num = int(num)
        if sub in polite_cats[major]:
            polite += num
        elif sub in impolite_cats[major]:
            impolite += num
        else:
            ignored += num
    
    if polite > impolite:
        return "polite"
    elif impolite > polite:
        return "impolite"
    # ignore a file if polite & impolite counts are equal
    return "neither"


def process_polite_emails():
    """
    We ended up with 1615 polite emails and 33 impolite emails,
    so we're going to only deal with the polite features.
    """
    # i = 0
    for email in polite_files:
        tokens = tokenize_email(email)
        get_ngrams(tokens, True, False)
        # if i > 10:
            # break
        # i += 1
        
    spn = sorted(polite_ngrams.items(), key=operator.itemgetter(1))
    num_ngrams = len(spn)
    i = num_ngrams - 1
    while i > (num_ngrams - 401):
        print spn[i][0], spn[i][1]
        i -= 1


def tokenize_email(email_path):
    """
    Tokenize an email's body.
    
    email_path: the relative path to the email text file.
    """
    header, body = eep.parse_email(email_path)
    return tokenize_text(body)


def tokenize_text(tokens):
    tokens = nltk.word_tokenize(tokens)
    clean_tokens = []
    for word in tokens:
        if word.isalnum() or word == ".":
            clean_tokens.append(word.lower())
    
    return clean_tokens

    
def get_ngrams(tokens, is_polite, process_unigrams):
    """
    Given a list of tokens, get trigram, bigram, and unigram counts.

    is_polite: whether this email falls into the politeness category or if it's impolite instead.
    """
    dict = polite_ngrams if is_polite else impolite_ngrams
    num_toks = len(tokens)
    ignored_toks = [ ".", "the", "on", "a", "of", "in", "for" ]
    for i in range(0, num_toks):
        word = tokens[i]
        if word in ignored_toks:
            continue
        # unigram
        if process_unigrams:
            if word not in dict:
                dict[word] = 0
            dict[word] += 1
            total_ngrams.add(word)
        # bigram
        if i+1 < num_toks:
            next_word = tokens[i+1]
            if next_word in ignored_toks:
                continue
            bigram = word + " " + next_word
            if bigram not in dict:
                dict[bigram] = 0
            dict[bigram] += 1
            total_ngrams.add(bigram)
        # trigram
        if i+2 < num_toks:
            next_word = tokens[i+2]
            if next_word in ignored_toks:
                continue
            trigram = word + " " + tokens[i+1] + " " + next_word
            if trigram not in dict:
                dict[trigram] = 0
            dict[trigram] += 1
            total_ngrams.add(trigram)


def get_selected_polite_ngrams():
    """
    Reads selected_polite_ngrams.txt (made of selected polite n-grams generated by this program)
    and puts them in
    """
    f = file('selected_polite_ngrams.txt', 'r')
    lines = f.readlines()
    f.close()
    
    ngrams = []
    for line in lines:
        line = line.strip().split(" ")
        line = line [:-1] # the last thing in the line is the number of times this n-gram occurred
        line = " ".join(line)
        selected_polite_ngrams.append(line)


def get_enron_politeness_score(tokens):
    """
    Input: a list of tokenized email text.
    Returns a score based on the selected polite n-grams from the enron set.
    
    The simple way to do this is to count the occurrences of the n-grams in the input.
    A better way would probably assign weights based on appearances in the original set;
    we might do that in the future, given the time.
    """
    # the simple way 
    count = 0
    num_toks = len(tokens)
    for i in range(0, num_toks):
        word = tokens[i]
        if word == ".":
            continue
        # bigrams
        if i+1 < num_toks:
            next_word = tokens[i+1]
            if next_word == ".":
                continue
            bigram = word + " " + next_word
            if bigram in selected_polite_ngrams:
                count += 1
            # print bigram
        if i+2 < num_toks:
            next_word = tokens[i+2]
            if next_word == ".":
                continue
            trigram = word + " " + tokens[i+1] + " " + next_word
            if trigram in selected_polite_ngrams:
                count += 1
            # print trigram
            
    return count


if __name__ == "__main__":
    # categorize_emails()
    # process_polite_emails()
    get_selected_polite_ngrams()
    # testing examples: 
    tokens = tokenize_text("so idk about you but i would really like this pie. give me this pie. no pie for you. nope.")
    print get_enron_politeness_score(tokens)
    tokens = tokenize_text("i would be very happy if you would let me know about the pie." 
        + " the pie is very important to me. i think that it may be significant to the future of the world.")
    print get_enron_politeness_score(tokens)
