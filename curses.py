curses = [
    "anal"
    ,"anus"
    ,"arse"
    ,"ass"
    ,"asshat"
    ,"ballsack"
    ,"bastard"
    ,"bitch"
    ,"biatch"
    ,"blowjob"
    ,"blow job"
    ,"bollock"
    ,"bollok"
    ,"boner"
    ,"boob"
    ,"breasticles"
    ,"bugger"
    ,"bum"
    ,"butt"
    ,"clitoris"
    ,"cock"
    ,"coon"
    ,"crap"
    ,"cunt"
    ,"damn"
    ,"dick"
    ,"dildo"
    ,"dyke"
    ,"fag"
    ,"feck"
    ,"fellate"
    ,"fellatio"
    ,"felching"
    ,"fuck"
    ,"f u c k"
    ,"fudgepacker"
    ,"fudge packer"
    ,"flange"
    ,"goddamn"
    ,"hell"
    ,"jerk"
    ,"jizz"
    ,"knobend"
    ,"knob end"
    ,"labia"
    ,"lmao"
    ,"lmfao"
    ,"motherfucker"
    ,"muff"
    ,"nigger"
    ,"nigga"
    ,"omg"
    ,"penis"
    ,"piss"
    ,"poop"
    ,"prick"
    ,"pube"
    ,"pussy"
    ,"scrotum"
    ,"sex"
    ,"shit"
    ,"slut"
    ,"smegma"
    ,"spunk"
    ,"tit"
    ,"tosser"
    ,"turd"
    ,"twat"
    ,"vagina"
    ,"wank"
    ,"whore"
    ,"wtf"
]

# add spaces around each curse
# so that we don't accidentally pick up parts of other words
curses = [ " " + x + " " for x in curses ] 

def curses_foiled_again(to_check):
    """
    Check for the existence of swearwords in the input text.
    
    Returns the number of curses.
    This does not catch curses inside of other words, or used as verbs (ie, 'fucked'),
        but we chose to err on the side of caution.
    """
    to_check = to_check.lower()
    to_check = " " + to_check + " " # get the words at the beginning and end
    num_curses = 0
    for word in curses:
        num_curses += to_check.count(word)
    
    return num_curses

if __name__ == "__main__":
    test = "fuck shit goddamn why aren't you doing that recommendation dudebro i trusted you motherfucker"
    print test
    print "there are at least", curses_foiled_again(test), "swear words in this sentence."