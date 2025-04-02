##Written by Aaron Arendt
##AITTSMaker © 2024 by Aaron Arendt is licensed under CC BY-NC-SA 4.0 

##Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International

##This license requires that reusers give credit to the creator. It allows reusers to distribute, remix, adapt, and build upon the material in any medium or format, for noncommercial purposes only. If others modify or adapt the material, they must license the modified material under identical terms.

import sys
import re

def main():
    if sys.argv[1].find('.html') >= 0:
        format_html()
    elif sys.argv[1].find('.txt') >= 0:
        make_audio()

def format_html():

              
    try:
        f = open(sys.argv[1])
        text = f.read()
    except:
        try:
            f = open(sys.argv[1],encoding='utf-8')
            text = f.read()
        except:
            f = open(sys.argv[1],encoding='ansi')
            text = f.read()
            
    f.close()
    
    m = re.search(r'<body[\s\S]*</body>',text)
    if m is not None:
        text = text[m.start():m.end()]#Get just the story and cut out the html gunk

    text = text.replace('\n',' ')

    text = re.sub(r'\t',r' ',text) #tabs
    
    text = re.sub(r'(<i>|<em>|<I>|<EM>)',r'#ZXCV@',text)#prepare the rate changes
    text = re.sub(r'(</i>|</em>|</I>|</EM>)',r'@VCXZ#',text)
    text = re.sub(r'(<p>|</p>|<div>|</div>|<br>|<br/>|<P>|</P>|<DIV>|</DIV>|<BR>|<BR/>|<p[^>]*>|<P[^>]*>)',r'\n\n',text)#get the spacing
    text = re.sub(r'<HR[^>]*>|<hr[^>]*>',r'***',text)#spans for section pauses
    text = re.sub(r'<[^>]*>',r'',text)#get rid of all other tags
    
    text = text.replace('&quot;','"')

    text = text.replace('&amp;','&')
    
    text = text.replace('Ã©','é')
    
    text = text.replace('Ã','à')
    
    text = text.replace('&nbsp;',' ')
    
    text = text.replace('â€¦','…')
    
    text = text.replace('â€“','–')    
    
    text = text.replace('â€”','—') #this is the long kind    
    
    text = text.replace('“','"')
    
    text = text.replace('”','"')
    
    text = re.sub(r'\r\n',r'\n',text)
    
    text = re.sub(r'\n +\n',r'\n\n',text)    
    
    text = re.sub(r'#ZXCV@\s*@VCXZ#','',text) #this gets rid of italics stuff right next to each other.
    text = text.replace('""','"') #sometimes weird stuff like this happens?
    
    #now to change " into “ ”
    text = re.sub(r'(")(.*?)(")',r'“\2”',text) #do all normal safe quote pairs
    text = re.sub(r'(.)"( |\n)',r'\1”\2',text) #find straggling end quotes
    text = re.sub(r'( |\n)"(.)',r'\1“\2',text) #find straggling start quotes
    
    text = re.sub(r'#ZXCV@',r'<i>',text)#bring back all the tags
    text = re.sub(r'@VCXZ#',r'</i>',text)
    
    #do some simple text replaces
    text = text.replace('Mr. ', 'Mister ')
    text = text.replace('Mrs. ', 'Misses ')
    text = text.replace('Ms. ', 'Mizz ')
    text = re.sub(r'\n\n—\n\n',r'\n\n***\n\n',text)
    text = text.replace('—',', ')
    
    print('Possible quotes for emphasis: ' + str(len(re.findall(r'(“)([^\r\n.?…,!“”]+[^\r\n.?…,!“”–-])(”)([^\r\n])',text))))
    print('Orphaned start quotes: ' + str(len(re.findall(r'“[^“”\n]+\n',text))))
    print('Orphaned end quotes: ' + str(len(re.findall(r'(”[^“”\n]+”)|(\n[^“”\n]+”)',text))))
    print('Leftover straight quotes: ' + str(len(re.findall(r'"',text))))
    
    if len(re.findall(r'"',text)) > 0:
        print('Fixing leftover straight quotes...')
        #turn any leftovers to end quotes
        #text = text.replace(r'"',r'”')
        text = text.replace(r'"',r'')
        print('Updated stats...')
        print('Possible quotes for emphasis: ' + str(len(re.findall(r'(“)([^\r\n.?…,!“”]+[^\r\n.?…,!“”–])(”)([^\r\n])',text))))
        print('Orphaned start quotes: ' + str(len(re.findall(r'“[^“”\n]+\n',text))))
        print('Orphaned end quotes: ' + str(len(re.findall(r'(”[^“”\n]+”)|(\n[^“”\n]+”)',text))))
        print('Leftover straight quotes: ' + str(len(re.findall(r'"',text))))
            
    
    #fix quotes as emphasis
    text = re.sub(r'(“)([^\r\n.?…,!“”]+[^\r\n.?…,!“”–])(”)([^\r\n])',r'<i>\2</i>\4',text)
    print('Possible quotes for emphasis: ' + str(len(re.findall(r'(“)([^\r\n.?…,!“”]+[^\r\n.?…,!“”–])(”)([^\r\n])',text))))
    
    
    #fix orphaned open quotes 
    text = re.sub(r'(“[^“”\n]+)(\n)',r'\1”\2',text)
    print('Orphaned start quotes: ' + str(len(re.findall(r'“[^“”\n]+\n',text))))
    #fix orphaned end quotes
    text = re.sub(r'(\n)([^“”\n]+”)',r'\1“\2',text)
    text = re.sub(r'(”)([^“”\n]+”)',r'\1“\2',text)
    print('Orphaned end quotes: ' + str(len(re.findall(r'(”[^“”\n]+”)|(\n[^“”\n]+”)',text))))
    print('Leftover straight quotes: ' + str(len(re.findall(r'"',text))))
    
    text = text.replace('“', '<pitch>“')
    text = text.replace('”', '”</pitch>')
    text = text.replace('<i>', '<rate>')
    text = text.replace('</i>', '</rate>')
    
    text = re.sub(r'    ',r' ',text)
    
    for i in range(50):
        text = re.sub(r'\n\n\n',r'\n\n',text)
    
    text = text.replace('…', ' <silence msec="1000"/> ')
    text = text.replace('...', ' <silence msec="1000"/> ')
    text = text.replace('***', ' <silence msec="3000"/> ')
    text = text.replace('* * *', ' <silence msec="3000"/> ')
    text = text.replace('. . .', ' <silence msec="3000"/> ')
    text = text.replace('OoOoO', ' <silence msec="3000"/> ')
    text = text.replace('*Chapter', 'End Of Chapter.\n\nCHAPTER END *Chapter')
    text = text.replace('\n\nJump to top\n\n', '\n\nEnd of Chapter.\n\nCHAPTER END')
    text = text.replace('\n\nView Online','')
    #t = re.sub(r' +; ?\n\n','\n\n', text) #sometimes there are leftover punctuation, which causes problems.
    if len(re.findall(r'next chapter\s+chapter list',text)) > 0:
        text = re.sub(r'next chapter\s+chapter list\s+', r'End of Chapter.\n\nCHAPTER END', text)
        text = re.sub(r'\s+previous chapter', r'\n\n', text)
        text = text.replace('(back to chapter list)', '\n\n')
    
    text = re.sub(r'(\S)\s+End of Chapter.',r'\1\n\nEnd of Chapter.',text)
    
    for i in range(10):
        if text[0:1] == '\n' or text[0:1] == ' ':
            text = text[1:]
    
    
    s = open(sys.argv[2],'w')
    #print(text[325892:326895])
    s.write(text)
    s.close()
    
    count_words(sys.argv[2])
    
def make_audio():
    ####
    #command line arguments x.py "C:/path/to/text.txt" 1(chapter to skip to)
    import torch
    from TTS.api import TTS
    import os
    import subprocess
    import shutil
    import sox
    import numpy as np
    
    sample_rate = 24000
    
    tsf = sox.Transformer()
    tsf.set_globals(verbosity=1)
    
    s100 = np.zeros(int(sample_rate * 100/1000))
    s200 = np.zeros(int(sample_rate * 200/1000))
    s500 = np.zeros(int(sample_rate * 500/1000))
    s1000 = np.zeros(int(sample_rate * 1000/1000))
    s1200 = np.zeros(int(sample_rate * 1200/1000))
    s3000 = np.zeros(int(sample_rate * 3000/1000))
    
    #filename for later when we are making the chapters    
    fileName = os.path.basename(sys.argv[1])
    fileName = fileName[0:len(fileName)-4]
    fileName = fileName + " - "
    
    spk = "p284" #p273 #248 #280 #284
    
    if torch.cuda.is_available():
        device = "cuda" 
        print("Using CUDA")
    else:
        device = "cpu"
        print("Using CPU")
    
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    #quick controls for italics and commas
    spaceCommas = False
    removeShortEmphasis = False
    silencePeriods = True
    
    n = len(sys.argv)
    skip=0
    if n > 2:
        skip = int(sys.argv[2])
    
    #get all the text from the file
    try:
        f = open(sys.argv[1])
        text = f.read()
    except:
        try:
            f = open(sys.argv[1],encoding='utf-8')
            text = f.read()
        except:
            f = open(sys.argv[1],encoding='ansi')
            text = f.read()
            
    f.close()
    
    ###For now, we don't work with italics, but I've left the option open in the future
    text = text.replace("  ZXCV  ","")
    text = text.replace("  VCXZ  ","")
    text = text.replace("ZXCV","")
    text = text.replace("VCXZ","")
    
    ##get rid of short bursts of italics text, sounds bad.
    if removeShortEmphasis:
        text = re.sub(r'(<rate>|<rate absspeed="-3"\/?>)(.{1,10})(<\/rate>|<rate absspeed="0"\/>)',r'\2',text)
    ##For when you just want them all gone.
    #text = re.sub(r'<rate[^<>]*>',r'',text)
    #text = re.sub(r'</rate>',r'',text)
    
    #I found that text feels a bit stilted between dialogue and narration, so i'm adding a quick silence after
    #text = text.replace("</pitch>","</pitch> <silence msec=\"200\"/> ")
    
    
    #Get rid of some text that doesn't play well
    text = text.replace(" - ",", ")
    text = text.replace(" – ",", ")
    text = re.sub(r'([a-zA-Z]): ',r'\1, ',text)
    text = re.sub(r'([a-zA-Z]); ',r'\1, ',text)
    text = text.replace("(",", ")
    text = text.replace(")",", ")
    text = text.replace("‘","'")
    text = text.replace("“","\"")
    text = text.replace("”","\"")
    text = text.replace("   ","  ")
    text = text.replace("   ","  ")
    text = text.replace("   ","  ")
    text = text.replace("   ","  ")
    text = text.replace(" ,",",")
    text = text.replace(" ,",",")
    text = text.replace(" ,",",")
    text = text.replace(" ,",",")
    text = text.replace(",  ",", ")
    text = text.replace(",  ",", ")
    text = text.replace(",  ",", ")
    text = text.replace(",  ",", ")
    text = re.sub(r',([a-zA-Z])',r', \1',text)
    text = text.replace("?,","?")
    text = text.replace(".,",".")
    text = text.replace("!,","!")
    text = text.replace(",,",",")
    #These repleacements helps xtts-2, really fucks up periods in dialogue, and angle closing quotes especially.
    text = text.replace(".”</pitch>","</pitch>")
    text = text.replace("”</pitch>","</pitch>")
    text = text.replace("<pitch>“","<pitch>")
    text = text.replace("<pitch absmiddle=\"5\">“","<pitch absmiddle=\"5\">")
    text = text.replace(".\"</pitch>","</pitch>")
    text = text.replace("\"</pitch>","</pitch>")
    text = text.replace("<pitch>\"","<pitch>")
    text = text.replace("<pitch absmiddle=\"5\">\"","<pitch absmiddle=\"5\">")
    text = text.replace("‘","")
    text = text.replace("’","'")
    if silencePeriods:
        text = re.sub(r'(\S)[\.]([\s])?',r'\1 <silence msec="200"> \2',text)
    
    #here, we run the replacement text pairs
    f = open("replacements.txt",encoding='utf-8')
    rep = f.read()
    rep = rep.split("\n")
    for pair in rep:
        print(pair)
        ft = pair[0:pair.index("=")]
        rt = pair[pair.index("=")+1:]
        text = re.sub(r'(\b)'+ft+r'(\b)',r'\1'+rt+r'\2',text)
        text = re.sub(r'(\b)'+ft.lower()+r'(\b)',r'\1'+rt.lower()+r'\2',text,0, re.IGNORECASE)
    
    #Master control for pauses between sentences
    text = re.sub(r'(\S[\.\!\?])(\s)',r'\1 <silence msec="200">\2',text)
    text = text.replace('</pitch>','</pitch> <silence msec="200">')
    #before we were separating sentences via commas, but i changed it after i got better at
    #keeping problem sentences that begin with commas from happening.
    text = re.sub(r'([,.!?>]),',r'\1',text)
    #on second thought though, I like the consistency of pauses with commas, so, I put it back in.
    if spaceCommas:
        text = re.sub(r'(\S[\,]) ',r'\1 <silence msec="100">',text)
    
    #lets add silences in after every paragraph.
    text = re.sub(r'\r\n\r\n','<silence msec="1000"/>',text)
    text = re.sub(r'\n\n','<silence msec="1000"/>',text)
    
    #this cuts down on the characters between CHAPTER END and the title of the next chapter.
    #just so we don't accidentally get silences at the start
    text= re.sub(r'(CHAPTER END)(\s+)(\S)',r'\1\3',text)
    
    chapters = []
    chapters = text.split("CHAPTER END")
    chapnum=0
    
    for chp in chapters:
        chapnum = chapnum + 1
        if skip > chapnum:
            continue
        text = chp[re.search(r'\S',chp).start():]
        #this causes a silence at the start, which is no good
        if text.startswith('<pitch absmiddle="5"></pitch> <silence msec="200">'):
            text = text[50:]
        
        #weird problems if we start with silence.
        #if text.startswith("<"):
        #    text = "begin.  " + text
            
        #finish every chapter with 3 seconds of silence
        text = text + '<silence msec="3000"/>'
        
        ##the way the code works now is that every time it comes to a new tag, it checks and alters the state of reading.
        ##and that, in turn, affects the status of each clip
        ##this way, we can have dialogue and rate changes accounted for easily
        sentences = {}
        clip = {}
        clip["text"]=""
        #only above 0 for specific silences.
        clip["sil"]=0
        clip["nar"]=True
        clip["slow"]=False
        #keeps track of if we are currently in a narration state or a dialogue state
        isNarration=True
        #Slow state or normal state
        isSlow=False
        #index for sentences
        i = 0
        #basically a text cursor
        txtIndex = 0
        #the tally of all files we have made
        allFiles = []        
        
        print("Begin cutting text.")
        #when cutting up the text, we will do it tag to tag.  This way, we can easily know the state of each clip.
        while len(text) > 0:
            clip={}
            #when we get to this pitch clip, we know dialogue is starting, so we turn off the narration state
            if text.startswith("<pitch absmiddle=\"5\">") or text.startswith("<pitch>"):
                txtIndex = text.find(">")
                text= text[txtIndex+1:]
                isNarration=False
                continue
            #and when we hit a pitch close, turn narration on, and take a quick pause
            elif text.startswith("</pitch>"):
                txtIndex = text.find(">")
                text= text[txtIndex+1:]
                isNarration=True
                continue
            #when we get to this rate clip, we know italics text has begun, and so we can now slow the text
            elif text.startswith("<rate absspeed=\"-3") or text.startswith("<rate>"):
                txtIndex = text.find(">")
                text= text[txtIndex+1:]
                isSlow=True
                continue
            #and when we hit a rate close, turn speed to normal.
            elif text.startswith("</rate>") or text.startswith("<rate absspeed=\"0\"/>"):
                txtIndex = text.find(">")
                text= text[txtIndex+1:]
                isSlow=False
                continue
            #silences are special, so we only render the silence itself then move on to the next text pull
            elif text.startswith("<silence msec=\"100\""):
                txtIndex = text.index(">")
                clip["text"]=""
                clip["sil"]=100
                text = text[txtIndex+1:]
            elif text.startswith("<silence msec=\"200\""):
                txtIndex = text.index(">")
                clip["text"]=""
                clip["sil"]=200
                text = text[txtIndex+1:]
            elif text.startswith("<silence msec=\"500\""):
                txtIndex = text.index(">")
                clip["text"]=""
                clip["sil"]=500
                text = text[txtIndex+1:]
            elif text.startswith("<silence msec=\"1000\""):
                txtIndex = text.index(">")
                clip["text"]=""
                clip["sil"]=1000
                text = text[txtIndex+1:]
            elif text.startswith("<silence msec=\"1200\""):
                txtIndex = text.index(">")
                clip["text"]=""
                clip["sil"]=1200
                text = text[txtIndex+1:]
            elif text.startswith("<silence msec=\"3000\""):
                txtIndex = text.index(">")
                clip["text"]=""
                clip["sil"]=3000
                text = text[txtIndex+1:]
            #lastly, we go to either the next tag, or the end of the body of text
            #fyi, .index (vs .find) will throw an exception when no result is found, and find returns a -1
            else:
                txtIndex = getNextIndex(text) 
                clip["text"] = text[0:txtIndex]
                #isNarration=True
                clip["sil"]=0
                text = text[txtIndex:]
                
            #this is where we set all the common state material we can
            if not clip["text"] == "":
                #getting rid of problematic text at the beginnings of texts, which causes missed text synthesizing at the end
                try:
                    clip["text"]= clip["text"][re.search(r'[^\s,]',clip["text"]).start():]
                except:
                    clip["text"]= clip["text"]
                
            clip["nar"]=isNarration
            clip["slow"]=isSlow
            sentences[i]=clip
            i = i+1
        
        print("Begin tts process.")
        #this is where the clip creation happens    
        concat = np.zeros(int(sample_rate * 200/1000))
        for i in sentences:
            clip = sentences[i]
            print("synth:=="+clip["text"]+"==")
            
            #this is how we are keeping track of all the things we might want to do to a clip.
            #originally this was an outside process, but it's handled internally now.
            #so, we could make do with using the clip state information, i figured we might as well make use of
            #the process as-is
            addons = ""
            if not clip["nar"]:
                addons = addons + "p"
            if clip["slow"]:
                addons = addons + "r"
            filepath = f"{i:05d}"+addons
            
            if clip["sil"]==3000:
                concat = np.concatenate([concat,s3000])
                continue
            if clip["sil"]==1200:
                concat = np.concatenate([concat,s1200])
                continue
            if clip["sil"]==1000:
                concat = np.concatenate([concat,s1000])
                continue
            if clip["sil"]==500:
                concat = np.concatenate([concat,s500])
                continue
            if clip["sil"]==200:
                concat = np.concatenate([concat,s200])
                continue
            if clip["sil"]==100:
                concat = np.concatenate([concat,s100])
                continue
            ##I don't think we need to do anything else but skip these texts now, but i'll leave the original code just in case.
            if len(re.findall("[a-zA-Z0-9]",clip["text"])) <= 0 or clip["text"] == "'" or clip["text"] == "\"":
                continue
                #shutil.copyfile("s200.wav", filepath+".wav")
                #allFiles.append(filepath+".wav")
                #continue
                
            ##The final safeguard
            #If, after everything I've done, we STILL get sentences that start with a comma, this will stop it.
            #It checks if the first instance of a comma happens before the first alpha character
            ifa = None
            match = re.search(r'[a-zA-Z]', clip["text"])
            if match is not None:
                ifa = match.start()
                if clip["text"].find(',') > -1 and clip["text"].find(',') < ifa:
                    clip["text"] = clip["text"][ifa:]
                    
            #get rid of trailing spaces
            while clip["text"][-1] == ' ':
                clip["text"] = clip["text"][:len(clip["text"])-1]
                
            ##End of sentence hallucinations
            #Especially on short sentences, it tends to hallucinate.  You can curtail this by
            # having an underscore at the end if there is no punctuation at the end
            if clip["text"][-1].isalpha() and clip["text"][-1] != 'a' and clip["text"][-1] != 'A' and clip["text"][-1] != 'e' and clip["text"][-1] != 'i' and clip["text"][-1] != 'I' and clip["text"][-1] != 'o' and clip["text"][-1] != 'u' and clip["text"][-1] != 'y' and clip["text"][-1] != 'd' and clip["text"][-1] != 's':
                clip["text"] = clip["text"] + "_"

            #clip generation
            try:
                wav = tts.tts(text=clip["text"], speaker_wav="p248.wav", language="en")
            except:
                #sometimes it will cut up sentenbces badly.  We try again, but we take out anything potentially problematic.
                clip["text"] = re.sub(r'[\'"]',r'',clip["text"])
                wav = tts.tts(text=clip["text"], speaker_wav="p248.wav", language="en")
            #else:
                #tts.tts_to_file(text=clip["text"], speaker="p227", file_path=f"{i:05d}"+".wav")
            #Here, we do pitch or rate changes to the file depending on what it needs.  the pitch changes work on a formula
            #so, to go up one notch, (x being the number of notches) the value is 2^(x/12)
            tsf.clear_effects()
            if filepath.find("p") >= 0:
                #filters = filters + "pitch 100"
                tsf.pitch(1)
            else:
                #filters = filters + "pitch -100"
                tsf.pitch(-1)
            
            if filepath.find("r") >= 0:
                #filters = filters + " " +"tempo 0.80"
                tsf.tempo(0.80,'s')
                #filters = "rubberband=pitch=0.89089871814033930474022620559051"
            else:
                #filters = filters + " " +"tempo .92"
                tsf.tempo(0.92,'s')
            
            #helps trim out weird long pauses around italics.        
            #filters = filters + " silence -l 0 -1 0.1 1%"
            tsf.silence(-1,0)
            tsf.silence(-1,0.1,0.1)
            
            #I have to do this bit here otherwise it's not treated as a proper numpy array
            wav = np.concatenate([wav])
            wav = tsf.build_array(input_array=wav, sample_rate_in=sample_rate)
            
            #add a bit of silence to the end of every text generation, and att it to the whole.
            concat = np.concatenate([concat,wav,s200])

        #tsf.clear_effects()
        #tsf.equalizer(315, 1, -6)
        #tsf.equalizer(640, 1, -3)
        #tsf.equalizer(6100, 1, 1.5)
        #concat = tsf.build_array(input_array=concat, sample_rate_in=sample_rate)
        tsf.clear_effects()
        outputname = fileName + f"{chapnum:03d}" + ".mp3"
        tsf.build_file(input_array=concat,output_filepath=outputname,sample_rate_in=sample_rate)
        
def count_words(filetoread):
    import re
    from spylls.hunspell import Dictionary
    dictionaryUS = Dictionary.from_files('dict/en_US')
    dictionaryCA = Dictionary.from_files('dict/en_CA')
    f = open(filetoread)
    text = f.read()
    f.close()
    words = re.findall(r'\w+\'?\w+', text.lower())
    f = open("ignore.txt")
    ig = f.read()
    ig = ig.split("\n")
    unknown = []
    for i in set(words):
        if dictionaryUS.lookup(i) is False or dictionaryCA.lookup(i) is False:
            if not i.lower() in ig:
                unknown.append(i)
            
    
    dict_word = {}
    
    for i in words:
        if i in unknown and len(i)>1:
            if i in dict_word:
                dict_word[i] = dict_word[i] + 1
            else:
                dict_word[i] = 1
    
    sorted_list = []
    
    for i in dict_word:
        sorted_list.append((int(dict_word[i]),str(i)))
        
    sorted_list = sorted(sorted_list, key=lambda times: times[0],reverse=True)
    f = open(filetoread+"_unknown_words.txt",'w')
    
    did_100=False
    did_5=False
    did_1=False
    
    for i in sorted_list:
        f.write(i[1])
        if i[0] < 100 and did_100 is False:
            f.write('\n\n')
            did_100 = True
        elif i[0] < 5 and did_5 is False:
            f.write('\n\n')
            did_5 = True
        elif i[0] == 1 and did_1 is False:
            f.write('\n\n')
            did_1 = True
        else:
            f.write(", ")
    
    f.close()

def getNextIndex(text):
    txtIndex = text.find("<")
    if txtIndex >= 240 and text.find(",") > 0 and text.find(",") < 240:
        txtIndex = text.find(",")+1
    if txtIndex < 0:
        txtIndex = len(text)
    return txtIndex
    

if __name__ == "__main__":
    main()

