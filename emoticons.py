import twokenize as tw
import re

# define our own slightly more limited version of the emoticon regex
# adapted from twokenize.py

# things we need to deal with separately
our_bfLeft = u"(0|[oO]|[vV]|\\$|[tT]|[xX]|;|@|\\^|\\*)".encode('utf-8')
our_basicface = "(?:" +our_bfLeft+tw.bfCenter+ ")|" +tw.s3+ "|" +tw.s4+ "|" +tw.s5

pattern = tw.regex_or(
    # myleott: Standard version  :) :( :] :D :P
    "(?:>|)?" + tw.regex_or(tw.normalEyes, tw.wink) + tw.regex_or(tw.noseArea,"[Oo]") + tw.regex_or(tw.tongue+r"(?=\W|$|RT|rt|Rt)", tw.otherMouths+r"(?=\W|$|RT|rt|Rt)", tw.sadMouths, tw.happyMouths),

    # myleott: reversed version (: D:  use positive lookbehind to remove "(word):"
    # myleott: because eyes on the right side is more ambiguous with the standard usage of : ;
    tw.regex_or("(?<=(?: ))", "(?<=(?:^))") + tw.regex_or(tw.sadMouths,tw.happyMouths,tw.otherMouths) + tw.noseArea + tw.regex_or(tw.normalEyes, tw.wink) + "(?:<|)?",

    our_basicface,

    # myleott: o.O and O.o are two of the biggest sources of differences
    #          between this and the Java version. One little hack won't hurt...
    tw.oOEmote
)


pattern = unicode(pattern).decode('utf-8')
reg = re.compile(pattern, re.UNICODE)
# print reg

def get_emoticon_count(text):
    """
    Get an approximate number of emoticons contained in the input text.
    
    We can't return the actual emoticons, so we return the number.
    Result is a list of mostly empty strings for some reason,
    but this is good enough for our purposes.
    """
    result = reg.findall(text)
    return len(result)

if __name__ == "__main__":
    # testing
    print get_emoticon_count("hello world :) :D =D no [: nope no helLO o.o what is tihs \n what :} {: :]]]")
    print get_emoticon_count("Hello! My name is bob :) I am applying for a job. Thanks, bob.")
    