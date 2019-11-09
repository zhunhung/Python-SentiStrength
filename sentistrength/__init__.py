import subprocess
import shlex
import os.path
import sys
import pandas as pd
from os import getcwd

class PySentiStr:
    def __init__(self):
        pass
        
    def setSentiStrengthPath(self, ss_Path):
        self.SentiStrengthLocation = ss_Path

    def setSentiStrengthLanguageFolderPath(self, sslf_Path):
        # Ensure it has a forward slash at the end
        if sslf_Path[-1] != '/':
            sslf_Path += '/'
        self.SentiStrengthLanguageFolder = sslf_Path

    def getSentiment(self, df_text, score='scale'):
        if not hasattr(self, 'SentiStrengthLocation'):
            assert False, "Set path using setSentiStrengthPath(path) function."

        if not hasattr(self, 'SentiStrengthLanguageFolder'):
            assert False, "Set path using setSentiStrengthLanguageFolderPath(path) function."

        if type(df_text) != pd.Series:
            df_text = pd.Series(df_text)
        df_text = df_text.str.replace('\n','')
        df_text = df_text.str.replace('\r','')
        conc_text = '\n'.join(df_text)
        p = subprocess.Popen(shlex.split("java -jar '" + self.SentiStrengthLocation + "' stdin sentidata '" + self.SentiStrengthLanguageFolder + "' trinary"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        b = bytes(conc_text.replace(" ","+"), 'utf-8')
        stdout_byte, stderr_text = p.communicate(b)
        stdout_text = stdout_byte.decode("utf-8")
        stdout_text = stdout_text.rstrip().replace("\t"," ")
        stdout_text = stdout_text.replace('\r\n','')
        senti_score = stdout_text.split(' ')

        try:
            senti_score = list(map(float, senti_score))
        except ValueError:
            raise ValueError("SentiStrengthLanguageFolderPath is set as '{}'. Ensure it is correct and ends with a forward slash '/'".format( self.SentiStrengthLanguageFolder))

        senti_score = [int(i) for i in senti_score]
        if score == 'scale': # Returns from -1 to 1
            senti_score = [sum(senti_score[i:i+2])/4 for i in range(0, len(senti_score), 3)]
        elif score == 'binary': # Return 1 if positive and -1 if negative
            senti_score = [1 if senti_score[i] >= abs(senti_score[i+1]) else -1 for i in range(0, len(senti_score), 3)]
        elif score == 'trinary': # Return Positive and Negative Score and Neutral Score
            senti_score = [tuple(senti_score[i:i+3]) for i in range(0, len(senti_score), 3)]
        elif score == 'dual': # Return Positive and Negative Score
            senti_score = [tuple(senti_score[i:i+2]) for i in range(0, len(senti_score), 3)]
        else:
            return "Argument 'score' takes in either 'scale' (between -1 to 1) or 'binary' (two scores, positive and negative rating)"
        return senti_score

