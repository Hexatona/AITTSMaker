By using this software you agree to the terms in license.txt.

How to use

1)  Install miniconda, and run it

2) create conda env to use, and run it

conda create --name coquitts python=3.9

conda activate coquitts

3) install the coquitts library

Download the latest source code from here:  https://github.com/coqui-ai/TTS

go into the directory:  pip install .

4) install the right pytorch from here:  https://pytorch.org/get-started/locally/

5)  install the other libraries:

pip install spylls

pip install chardet

5) Put FFMPEG and SOX in the directory.

6)  App Usage:  (make sure you open up miniconda, activate the coquitts environnt, and naviate to the directory of this program.)

a)  format a story from html to text

python AITTSMaker.py "C:\AITTSMaker\Examples\The Wonderful Wizard of Oz.html" "C:\AITTSMaker\Examples\The Wonderful Wizard of Oz.txt"

this will get you the text file plus a set of words it doesn't know.  listen to them and see what needs fixing.  try out replacements, and put the replacements in replacements.txt

b)  python AITTSMaker.py "C:\AITTSMaker\Examples\The Wonderful Wizard of Oz.txt"

this will start the audiobook process, making tons and tons of small files, rolling them up, and moving on to the next chapter

TIPS N TRICKS

1)  Chapters end at: CHAPTER END        <-have the next chapter start literally right after that, or it can die.
2)  Delete angled quotes before generation, the engine can sometimes kinda suck with them.  Also, - dashes not between words it gets sucky with too.
3)  The tags it cares about are <rate>, </rate> <pitch>, </pitch>, <silence msec="1000"/>, and <silence msec="3000"/>
4)  How do I get this epub into html?  There's services that do that online, but you can also use calibre.  Personally I recommend pandoc (another command line tool), it's great.
5)  What if I want to skip ahead to a specific chapter?  
 python AITTSMaker.py "C:\AITTSMaker\Examples\The Wonderful Wizard of Oz.txt" 7 <- starts at chapter 7.
6)  Other voices:  I included (in best) a selection of voices with it I think perform very well.  But any 6 seconds or so of a clean wav file will do.  It will clone the voice.

My best advice to you is that you take the first chapter, slap it into a different text file, and generate that first.  Listen to it, see what it sounds like, and then tweak the document or word replacements before you just try for the whole thing.  It will save you a lot of headache.

OH NO IT DID A BAD

1)  Unrecognised characters - sometimes it freaks out with accented characters.  replace them with regular characters.
2)  Why is my whole chapter sounding  incredibly slow?  Short answer, because the first generated audio bit was silence.  Probably a few carriage returns or something before the actual text starts.  Make sure text is litrerally the first part of the file.
3)  It sometimes freaks out at the end of a sentence!?  Yeah, not sure why it does that.  Work in progress.  (You should have seen what happened when a sentence began with a comma, and there was a 2nd comma later - was absolutely wild)
