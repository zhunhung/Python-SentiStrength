import subprocess
import shlex
import os.path
import sys
import pandas as pd
from os import getcwd

class PySentiStr:
    def __init__(self):
        self.SentiStrengthLocation = os.path.join(getcwd(),"SentiStrength.jar")
        self.SentiStrengthLanguageFolder = os.path.join(getcwd(),"SentiStrengthData/")

        if not os.path.isfile(self.SentiStrengthLocation):
            print("SentiStrength not found at: ", SentiStrengthLocation,'\nSet path using setSentiStrengthPath(path) function.')
        if not os.path.isdir(self.SentiStrengthLanguageFolder):
            print("SentiStrength data folder not found at: ", SentiStrengthLanguageFolder,'\nSet path using setSentiStrengthLanguageFolderPath(path) function.')

    def setSentiStrengthPath(self, ss_Path):
        self.SentiStrengthLocation = ss_Path

    def setSentiStrengthLanguageFolderPath(self, sslf_Path):
        self.SentiStrengthLanguageFolder = sslf_Path

    def getSentiment(self, df_text, score='scale'):
        # Able to take in single string or list of string and convert into pandas Series
        if type(df_text) != pd.Series:
            df_text = pd.Series(df_text)
        df_text = df_text.str.replace('\n','')
        df_text = df_text.str.replace('\r','')
        conc_text = '\n'.join(df_text)
        p = subprocess.Popen(shlex.split("java -jar '" + self.SentiStrengthLocation + "' stdin sentidata '" + self.SentiStrengthLanguageFolder + "'"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        b = bytes(conc_text.replace(" ","+"), 'utf-8')
        stdout_byte, stderr_text = p.communicate(b)
        stdout_text = stdout_byte.decode("utf-8")
        stdout_text = stdout_text.rstrip().replace("\t"," ")
        stdout_text = stdout_text.replace('\r\n','')
        senti_score = stdout_text.split(' ')
        if score == 'scale':
            senti_score = list(map(int, senti_score))
            senti_score = [sum(senti_score[i:i+2])/4 for i in range(0, len(senti_score), 2)]
        elif score == 'binary': # Return Positive and Negative Score
            senti_score = list(map(int, senti_score))
            senti_score = [tuple(senti_score[i:i+2]) for i in range(0, len(senti_score), 2)]
        else:
            return "Argument 'score' takes in either 'scale' (between -1 to 1) or 'binary' (two scores, positive and negative rating)"
        return senti_score

