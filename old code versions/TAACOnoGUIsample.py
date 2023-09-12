#sample for using TAACO without the GUI:
import os
#set working directory to the same directory as TAACOnoGUI.py
os.chdir('/Users/kristopherkyle/Desktop/Programming/GitHub/LCR-ADS-Lab/TAACO/TAACO 2.1.0 Python 3/')

#import TAACO
from TAACOnoGUI import runTAACO

#assign variables (by default this is all variables except source text-based variables)
#to obtain diagnostic information, change the last two variables ("outputTagged" and "outputDiagnostic" to True) #see below for brief description of options
sampleVars = {"sourceKeyOverlap" : False, "sourceLSA" : False, "sourceLDA" : False, "sourceWord2vec" : False, "wordsAll" : True, "wordsContent" : True, "wordsFunction" : True, "wordsNoun" : True, "wordsPronoun" : True, "wordsArgument" : True, "wordsVerb" : True, "wordsAdjective" : True, "wordsAdverb" : True, "overlapSentence" : True, "overlapParagraph" : True, "overlapAdjacent" : True, "overlapAdjacent2" : True, "otherTTR" : True, "otherConnectives" : True, "otherGivenness" : True, "overlapLSA" : True, "overlapLDA" : True, "overlapWord2vec" : True, "overlapSynonym" : True, "overlapNgrams" : True, "outputTagged" : False, "outputDiagnostic" : False}
#run program. Format is input directory, output filename, variable dictionary, gui (True or False, defaults to False), and path to source text (defaults as False)
runTAACO("Ellipse_Sample/","packageTest.csv",sampleVars)

runTAACO("/Users/kristopherkyle/Desktop/Programming/GitHub/Clones/ELLIPSE-Corpus/ellipseSingle/","20230810_noGui2.1.1.csv",sampleVars)

### Variable dictionary explanation: ###

## source overlap indices: ##
# sourceKeyOverlap - When a source text is provided, calculate key word overlap between target text and source text
# sourceLSA - When a source text is provided, calculate semantic similarity (via LSA) between target text and source text
# sourceLDA - When a source text is provided, calculate semantic similarity (via LDA) between target text and source text
# sourceWord2vec - When a source text is provided, calculate semantic similarity (via Word2Vec) between target text and source text

## word types to consider: ##
# wordsAll - Calculate indices (overlap and ttr) for all words
# wordsContent - Calculate indices (overlap and ttr) for content words
# wordsFunction - Calculate indices (overlap and ttr) for function words
# wordsNoun - Calculate indices (overlap and ttr) for nouns
# wordsPronoun - Calculate indices (overlap and ttr) for pronouns
# wordsArgument - Calculate indices (overlap and ttr) for arguments
# wordsVerb - Calculate indices (overlap and ttr) for verbs
# wordsAdjective - Calculate indices (overlap and ttr) for adjectives
# wordsAdverb - Calculate indices (overlap and ttr) for adverbs

## types of overlap: ##
# overlapSentence - Calculate sentence to sentence overlap
# overlapParagraph - Calculate paragraph to paragraph overlap
# overlapAdjacent - Calculate overlap for adjacent sections (sentences or paragraphs)
# overlapAdjacent2 - Calculate overlap for two adjacent sections (sentences or paragraphs)
# otherTTR - Calculate TTR
# otherConnectives - Calculate connective indicidence indices
# otherGivenness - Calculate givenness indices
# overlapLSA - Calculate semantic similarity (LSA) across text sections
# overlapLDA - Calculate semantic similarity (LDA) across text sections
# overlapWord2vec - Calculate semantic similarity (Word2vec) across text sections
# overlapSynonym - Calculate synonym overlap across text sections
# overlapNgrams - Include ngram indices
# outputTagged - Output tagged representation of each text
# outputDiagnostic - Output diagnostic file (number of words, sentences, paragraphs, etc. per file)