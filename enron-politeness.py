import os
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
polite_cats[1] = [ 1, 3, 4, 5, 6 ]
polite_cats[2] = [ 3, 5, 8 ]
polite_cats[3] = [ x for x in range(1,14) ] # everything in coarse category 3 (ie all of 1.1)
polite_cats[4] = [ 4, 6 ]

# categories we've decided are impolite
impolite_cats = {}
impolite_cats[1] = [ 2 ]
impolite_cats[2] = [ 11, 12 ]
impolite_cats[3] = []
impolite_cats[4] = [ 7, 9, 13, 14, 16, 19 ]

# categories we've decided to ignore
ignored_cats = {}
ignored_cats[1] = [ 7, 8 ]
ignored_cats[2] = [ 1, 2, 4, 6, 7, 9, 10, 13 ]
ignored_cats[3] = []
ignored_cats[4] = [ 1, 2, 3, 5, 8, 10, 11, 12, 15, 17, 18 ]


# ngram dictionaries are defined as cat[n-gram] = count of its appearances in this category
polite_ngrams = {}

impolite_ngrams = {}


# TODO loop through all of the files in enron_with_cats\[1-6]



def tokenize_email(email_path):
    """
    Tokenize an email's body.
    
    email_path: the relative path to the email text file.
    """
    header, body = eep.parse_email(email_file)
    tokens = nltk.word_tokenize(body)
    clean_tokens = []
    for word in tokens:
    	if word.isalnum() or word == ".":
    		clean_tokens.append(word.lower())
    
    
def get_ngrams(tokens, is_polite):
	"""
	Given a list of tokens, get trigram, bigram, and unigram counts.
	
	is_polite: whether this email falls into the politeness category or if it's impolite instead.
	"""
	for word in tokens:
		pass
	
	pass    
    

if __name__ == "__main__":
    # curr_path = os.getcwd()
    email_file = os.path.join("enron_with_categories","1","7664.txt")
    # os.path.join(curr_path, email_file)
    tokens = tokenize_email(email_file)
    get_ngrams(tokens, True)