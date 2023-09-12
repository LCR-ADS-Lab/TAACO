#-*- coding: utf-8 -*- 
#(for potential non-ASCII encoding)#Tool for the Automatic Analysis of COhesion

#from __future__ import division
import sys

#import spacy #this is for if spaCy is used
# import Tkinter as tk
# import tkFont
# import tkFileDialog
# import Tkconstants

#From SEANCE:
import tkinter as tk
import tkinter.font
import tkinter.filedialog
import tkinter.constants
import queue
import tkinter.messagebox

import os
import sys
import re
import platform
import glob
import math
from collections import Counter

from threading import Thread

# import os
# import re
# import sys 
# import glob
# import math
# import re
# import platform
# import shutil
#import subprocess
import numpy as np
# from collections import Counter
from operator import itemgetter
# try:
# 	import xml.etree.cElementTree as ET
# except ImportError:
# 	import xml.etree.ElementTree as ET

print("Loading Spacy")
import spacy #add version number here
print("Loading Spacy Model")
nlp = spacy.load("en_core_web_sm") #fast, but less accurate
#nlp = spacy.load("en_core_web_trf") #slower, but more accurate


###THIS IS NEW IN V2.0.1 ###
# from threading import Thread
# import Queue


#This creates a que in which the core TAACO program can communicate with the GUI
dataQueue = queue.Queue() #update to Python 3
#dataQueue = Queue.Queue()

#This creates the message for the progress box (and puts it in the dataQueue)
progress = "...Waiting for Data to Process"
dataQueue.put(progress)

#Def1 is the core TAACO program; args is information passed to TAACO
def start_thread(def1, arg1, arg2, arg3, arg4, arg5): 
	t = Thread(target=def1, args=(arg1, arg2, arg3, arg4,arg5))
	t.start()

#This allows for a packaged gui to find the resource files.
def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		return(os.path.join(sys._MEIPASS, relative))
	return(os.path.join(relative))

prog_name = "TAACO 2.1.1" #updated 2023-08-010

if platform.system() == "Darwin":
	system = "M"
	title_size = 16
	font_size = 14
	geom_size = "425x685"
	color = "#FFFF99"
elif platform.system() == "Windows":
	system = "W"
	title_size = 12
	font_size = 12
	geom_size = "475x675"
	color = "#FFFF99"
elif platform.system() == "Linux":
	system = "L"
	title_size = 12
	font_size = 12
	geom_size = "525x700"
	color = "#FFFF99"

print(system) #updated for Py3

# need to update this. Originally necessary for Stanford CoreNLP
# def start_watcher(def2, count, folder):
# 	t2 = Thread(target=def2, args =(count,folder))
# 	t2.start()

# def watcher(count, folder):
# 	import glob
# 	import time
# 	counter = 1

# 	while count>len(glob.glob(folder+"*")):
# 		#print "Count ", count
# 		#counter = 1
# 		if len(glob.glob(folder+"*")) == 0:
# 			if counter == 1:
# 				output = "Starting Stanford CoreNLP..."
# 				counter+=1
# 			elif counter == 2:
# 				output = "Starting Stanford CoreNLP."
# 				counter+=1
# 			elif counter == 3:
# 				output = "Starting Stanford CoreNLP.."
# 				counter+=1
# 				counter = 1
# 		else:
# 			output = "CoreNLP has tagged " + str(len(glob.glob(folder+"*"))) + " of " + str(count) + " paragraphs."
# 		dataQueue.put(output)
# 		root.update_idletasks()
		
# 		time.sleep(.3) #seconds it waits before checking again  

class MyApp:
	def __init__(self, parent):
		
		#Creates font styles
		helv14= tkinter.font.Font(family= "Helvetica Neue", size=font_size)
		times14= tkinter.font.Font(family= "Lucida Grande", size=font_size)
		helv16= tkinter.font.Font(family= "Helvetica Neue", size = title_size, weight = "bold", slant = "italic")
		#This defines the GUI parent
		
		self.myParent = parent
		
		
		#This creates the header text
		self.spacer1= tk.Label(parent, text= "Tool for the Automatic Analysis of Cohesion", font = helv16, background = color)
		self.spacer1.pack()
		
		#This creates a frame for the meat of the GUI
		self.thestuff= tk.Frame(parent, background =color)
		self.thestuff.pack()
		
		self.myContainer1= tk.Frame(self.thestuff, background = color)
		self.myContainer1.pack(side = tk.RIGHT, expand= tk.TRUE)

		self.labelframe2 = tk.LabelFrame(self.myContainer1, text= "Instructions", background = color)
		self.labelframe2.pack(expand=tk.TRUE)
		
		#This creates the list of instructions.
		self.instruct = tk.Button(self.myContainer1, text = "Instructions", justify = tk.LEFT)
		self.instruct.pack()
		self.instruct.bind("<Button-1>", self.instruct_mess)

		self.checkboxframe = tk.LabelFrame(self.myContainer1, text= "Options", background = color, width = "45")
		self.checkboxframe.pack(expand=tk.TRUE)

		self.sourcetextframe = tk.LabelFrame(self.checkboxframe, text= "Source text analysis (optional)", background = color, width = "45")
		self.sourcetextframe.pack(fill = tk.X, expand=tk.TRUE)
		
		self.summarylabel =tk.LabelFrame(self.sourcetextframe, height = "1", width= "45", padx = "4", text = "Your selected source text:", background = color)
		self.summarylabel.pack(fill = tk.X)

		summary_file_name = "(No Source Text Chosen)"
		
		self.summarylabelchosen = tk.Label(self.summarylabel, height= "1", width= "37", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text = summary_file_name)
		self.summarylabelchosen.pack(side = tk.LEFT)

		self.summary_name = ""
		
		self.summary_button = tk.Button(self.summarylabel)
		self.summary_button.configure(text= "Select")
		self.summary_button.pack(side = tk.LEFT)
		self.summary_button.bind("<Button-1>", self.get_summary_text)
		
		self.source_text_options = tk.LabelFrame(self.sourcetextframe, height = "1", width= "45", padx = "4", text = "Source text options", background = color)
		self.source_text_options.pack(fill = tk.X)
		
		self.st1_var = tk.IntVar()			
		self.st1 = tk.Checkbutton(self.source_text_options, text="Key item overlap", variable=self.st1_var,background = color)
		self.st1.grid(row=1,column=1, sticky = "W")		
		self.st1.deselect()

		self.st2_var = tk.IntVar()			
		self.st2 = tk.Checkbutton(self.source_text_options, text="LSA", variable=self.st2_var,background = color)
		self.st2.grid(row=1,column=2, sticky = "W")		
		self.st2.deselect()

		self.st3_var = tk.IntVar()			
		self.st3 = tk.Checkbutton(self.source_text_options, text="LDA", variable=self.st3_var,background = color)
		self.st3.grid(row=1,column=3, sticky = "W")		
		self.st3.deselect()

		self.st4_var = tk.IntVar()			
		self.st4 = tk.Checkbutton(self.source_text_options, text="Word2vec", variable=self.st4_var,background = color)
		self.st4.grid(row=1,column=4, sticky = "W")		
		self.st4.deselect()

			
		self.type_frame = tk.LabelFrame(self.checkboxframe, text= "Lemma tokens to analyze for lexical overlap and TTR", background = color, width = "45")
		self.type_frame.pack(expand=tk.TRUE)

		self.overlap_frame = tk.LabelFrame(self.checkboxframe, text= "Lexical overlap options", background = color, width = "45")
		self.overlap_frame.pack(fill = tk.X, expand=tk.TRUE)

		self.semantic_frame = tk.LabelFrame(self.checkboxframe, text= "Semantic overlap options", background = color, width = "45")
		self.semantic_frame.pack(fill = tk.X, expand=tk.TRUE)
		
		self.other_frame = tk.LabelFrame(self.checkboxframe, text= "Other indices", background = color, width = "45")
		self.other_frame.pack(fill = tk.X, expand=tk.TRUE)

		self.diag_frame = tk.LabelFrame(self.myContainer1, text= "Diagnostic output options", background = color, width = "45")
		self.diag_frame.pack(expand=tk.TRUE)
				
		self.all_frame = tk.LabelFrame(self.checkboxframe, background = color, width = "45")
		self.all_frame.pack(expand=tk.TRUE)
		
		self.cb1_var = tk.IntVar()			
		self.cb1 = tk.Checkbutton(self.type_frame, text="All", variable=self.cb1_var,background = color)
		self.cb1.grid(row=1,column=1, sticky = "W")		
		self.cb1.select()

		self.cb2_var = tk.IntVar()			
		self.cb2 = tk.Checkbutton(self.type_frame, text="Content", variable=self.cb2_var,background = color)
		self.cb2.grid(row=1,column=2, sticky = "W")		
		self.cb2.select()

		self.cb3_var = tk.IntVar()			
		self.cb3 = tk.Checkbutton(self.type_frame, text="Function", variable=self.cb3_var,background = color)
		self.cb3.grid(row=1,column=3, sticky = "W")		
		self.cb3.deselect()		

		self.cb4_var = tk.IntVar()			
		self.cb4 = tk.Checkbutton(self.type_frame, text="Noun", variable=self.cb4_var,background = color)
		self.cb4.grid(row=1,column=4, sticky = "W")		
		self.cb4.deselect()

		self.cb5_var = tk.IntVar()			
		self.cb5 = tk.Checkbutton(self.type_frame, text="Pronoun", variable=self.cb5_var,background = color)
		self.cb5.grid(row=1,column=5, sticky = "W")		
		self.cb5.deselect()

		self.cb6_var = tk.IntVar()			
		self.cb6 = tk.Checkbutton(self.type_frame, text="Argument", variable=self.cb6_var,background = color)
		self.cb6.grid(row=2,column=1, sticky = "W")		
		self.cb6.select()
		
		self.cb7_var = tk.IntVar()			
		self.cb7 = tk.Checkbutton(self.type_frame, text="Verb", variable=self.cb7_var,background = color)
		self.cb7.grid(row=2,column=2, sticky = "W")		
		self.cb7.select()

		self.cb8_var = tk.IntVar()			
		self.cb8 = tk.Checkbutton(self.type_frame, text="ADJ", variable=self.cb8_var,background = color)
		self.cb8.grid(row=2,column=3, sticky = "W")		
		self.cb8.deselect()

		self.cb9_var = tk.IntVar()			
		self.cb9 = tk.Checkbutton(self.type_frame, text="ADV", variable=self.cb9_var,background = color)
		self.cb9.grid(row=2,column=4, sticky = "W")		
		self.cb9.deselect()

		self.cb10_var = tk.IntVar()			
		self.cb10 = tk.Checkbutton(self.overlap_frame, text="Sentence", variable=self.cb10_var,background = color)
		self.cb10.grid(row=1,column=1, sticky = "W")		
		self.cb10.select()

		self.cb11_var = tk.IntVar()			
		self.cb11 = tk.Checkbutton(self.overlap_frame, text="Paragraph", variable=self.cb11_var,background = color)
		self.cb11.grid(row=1,column=2, sticky = "W")		
		self.cb11.deselect()

		self.cb12_var = tk.IntVar()			
		self.cb12 = tk.Checkbutton(self.overlap_frame, text="Adjacent", variable=self.cb12_var,background = color)
		self.cb12.grid(row=1,column=3, sticky = "W")		
		self.cb12.select()

		self.cb13_var = tk.IntVar()			
		self.cb13 = tk.Checkbutton(self.overlap_frame, text="Adjacent 2", variable=self.cb13_var,background = color)
		self.cb13.grid(row=1,column=4, sticky = "W")		
		self.cb13.deselect()

		self.cb14_var = tk.IntVar()			
		self.cb14 = tk.Checkbutton(self.other_frame, text="TTR", variable=self.cb14_var,background = color)
		self.cb14.grid(row=1,column=1, sticky = "W")		
		self.cb14.deselect()

		self.cb15_var = tk.IntVar()			
		self.cb15 = tk.Checkbutton(self.other_frame, text="Connectives", variable=self.cb15_var,background = color)
		self.cb15.grid(row=1,column=2, sticky = "W")		
		self.cb15.select()

		self.cb16_var = tk.IntVar()			
		self.cb16 = tk.Checkbutton(self.other_frame, text="Givenness", variable=self.cb16_var,background = color)
		self.cb16.grid(row=1,column=3, sticky = "W")		
		self.cb16.deselect()

		#the next three will be in V2.0
		self.cb17_var = tk.IntVar()			
		self.cb17 = tk.Checkbutton(self.semantic_frame, text="LSA", variable=self.cb17_var,background = color)
		self.cb17.grid(row=1,column=1, sticky = "W")		
		self.cb17.deselect()

		self.cb18_var = tk.IntVar()			
		self.cb18 = tk.Checkbutton(self.semantic_frame, text="LDA", variable=self.cb18_var,background = color)
		self.cb18.grid(row=1,column=2, sticky = "W")		
		self.cb18.deselect()

		self.cb19_var = tk.IntVar()			
		self.cb19 = tk.Checkbutton(self.semantic_frame, text="Word2vec", variable=self.cb19_var,background = color)
		self.cb19.grid(row=1,column=3, sticky = "W")		
		self.cb19.deselect()

		self.cb20_var = tk.IntVar()			
		self.cb20 = tk.Checkbutton(self.semantic_frame, text="Synonym overlap", variable=self.cb20_var,background = color)
		self.cb20.grid(row=1,column=4, sticky = "W")		
		self.cb20.deselect()

		self.cb21_var = tk.IntVar()			
		self.cb21 = tk.Checkbutton(self.type_frame, text="N-grams", variable=self.cb21_var,background = color)
		self.cb21.grid(row=2,column=5, sticky = "W")		
		self.cb21.deselect()

		self.cb22_var = tk.IntVar()
		self.cb22 = tk.Checkbutton(self.diag_frame, text="Output tagged files", variable=self.cb22_var,background = color)
		self.cb22.grid(row=1,column=2, sticky = "W")	
		self.cb22.select()

		self.cb23_var = tk.IntVar()
		self.cb23 = tk.Checkbutton(self.diag_frame, text="Output diagnostic file", variable=self.cb23_var,background = color)
		self.cb23.grid(row=1,column=1, sticky = "W")	
		self.cb23.select()

		self.source_text_list = ["null", self.st1_var, self.st2_var,self.st3_var,self.st4_var] #the "null" here was just a filler so the ordered calls would line up

		self.var_list = ["null", self.cb1_var, self.cb2_var,self.cb3_var,self.cb4_var,self.cb5_var,self.cb6_var,self.cb7_var,self.cb8_var,self.cb9_var,self.cb10_var,self.cb11_var,self.cb12_var,self.cb13_var,self.cb14_var,self.cb15_var,self.cb16_var,self.cb17_var,self.cb18_var,self.cb19_var,self.cb20_var,self.cb21_var,self.cb22_var,self.cb23_var]
		
		#the following will replace the lists:
		self.var_dict = {"sourceKeyOverlap" : self.st1_var, "sourceLSA" : self.st2_var, "sourceLDA": self.st3_var, "sourceWord2vec": self.st4_var, "wordsAll" : self.cb1_var, "wordsContent" : self.cb2_var, "wordsFunction" : self.cb3_var, "wordsNoun" : self.cb4_var, "wordsPronoun" : self.cb5_var, "wordsArgument" : self.cb6_var, "wordsVerb" : self.cb7_var, "wordsAdjective" : self.cb8_var, "wordsAdverb" : self.cb9_var, "overlapSentence" : self.cb10_var, "overlapParagraph" : self.cb11_var, "overlapAdjacent" : self.cb12_var, "overlapAdjacent2" : self.cb13_var, "otherTTR" : self.cb14_var, "otherConnectives" : self.cb15_var, "otherGivenness" : self.cb16_var, "overlapLSA" : self.cb17_var, "overlapLDA" : self.cb18_var, "overlapWord2vec" : self.cb19_var, "overlapSynonym" : self.cb20_var, "overlapNgrams" : self.cb21_var, "outputTagged" : self.cb22_var, "outputDiagnostic" : self.cb23_var}

		self.box_list = [self.cb1, self.cb2,self.cb3,self.cb4,self.cb5,self.cb6,self.cb7,self.cb8,self.cb9,self.cb10,self.cb11,self.cb12,self.cb13,self.cb14,self.cb15,self.cb16,self.cb17,self.cb18,self.cb19,self.cb20,self.cb21]



		self.cb_all = tk.Button(self.all_frame, text = "Select All",justify = tk.LEFT)
		self.cb_all.grid(row=1, column = 1, sticky = "W")
		self.cb_all.bind("<Button-1>", self.cb_all_Click)

		self.cb_none = tk.Button(self.all_frame, text = "Select None")
		self.cb_none.grid(row=1, column = 3)
		self.cb_none.bind("<Button-1>", self.cb_none_Click)

		self.button_spacer = tk.Label(self.all_frame, text= "            ", background = color)
		self.button_spacer.grid(row=1, column = 2)

		
		#Creates Label Frame for Data Input area
		self.secondframe= tk.LabelFrame(self.myContainer1, text= "Data Input", background = color)
		self.secondframe.pack(expand=tk.TRUE) 
		
		#Creates default dirname so if statement in Process Texts can check to see
		#if a directory name has been chosen
		self.dirname = ""
		
		#This creates a label for the first program input (Input Directory)
		self.inputdirlabel =tk.LabelFrame(self.secondframe, height = "1", width= "45", padx = "4", text = "Your selected input folder:", background = color)
		self.inputdirlabel.pack()
				
		#Creates label that informs user which directory has been chosen
		directoryprompt = "(No Folder Chosen)"
		self.inputdirchosen = tk.Label(self.inputdirlabel, height= "1", width= "37", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text = directoryprompt)
		self.inputdirchosen.pack(side = tk.LEFT)

		self.button1 = tk.Button(self.inputdirlabel)
		self.button1.configure(text= "Select")
		self.button1.pack(side = tk.LEFT)
		self.button1.bind("<Button-1>", self.button1Click)
		
		self.outdirname = ""
				
		#Creates a label for the second program input (Output Directory)
		self.outputdirlabel = tk.LabelFrame(self.secondframe, height = "1", width= "45", padx = "4", text = "Your selected output filename:", background = color)
		self.outputdirlabel.pack()
				
		#Creates a label that informs sure which directory has been chosen
		outdirectoryprompt = "(No Output Filename Chosen)"
		self.outputdirchosen = tk.Label(self.outputdirlabel, height= "1", width= "37", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text = outdirectoryprompt)
		self.outputdirchosen.pack(side = tk.LEFT)

		#This creates the Output Directory button.
		self.button2 = tk.Button(self.outputdirlabel)
		self.button2["text"]= "Select"
		#This tells the button what to do if clicked.
		self.button2.bind("<Button-1>", self.button2Click)
		self.button2.pack(side = tk.LEFT)
			
		self.BottomSpace= tk.LabelFrame(self.myContainer1, text = "Run Program", background = color)
		self.BottomSpace.pack()

		self.button3= tk.Button(self.BottomSpace)
		self.button3["text"] = "Process Texts"
		self.button3.bind("<Button-1>", self.runprogram)
		self.button3.pack()

		self.progresslabelframe = tk.LabelFrame(self.BottomSpace, text= "Program Status", background = color)
		self.progresslabelframe.pack(expand= tk.TRUE)
		
		self.progress= tk.Label(self.progresslabelframe, height= "1", width= "45", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text=progress)
		self.progress.pack()
		
		self.poll(self.progress)
	
	def cb_all_Click(self, event):
		for items in self.box_list:
			items.select()
	
	def cb_none_Click(self, event):
		for items in self.box_list:
			items.deselect()
			
	def instruct_mess(self, event):
		#import tkMessageBox
		tkinter.messagebox.showinfo("Instructions", "1. Select desired indices\n2. Choose the input folder (where your files are).\n3. Name your output file \n4. Press the 'Process Texts' button.")

	def entry1Return(self,event):
		input= self.entry1.get()
		self.input2 = input + ".csv"
		self.filechosenchosen.config(text = self.input2)
		self.filechosenchosen.update_idletasks()
	
	def get_summary_text(self, event):
		#import tkFileDialog
		self.summary_name = tkinter.filedialog.askopenfilename(parent=root,title='Please select a summary text')
		self.displaysummary_file = '.../'+self.summary_name.split('/')[-1]
		self.summarylabelchosen.config(text = self.displaysummary_file)
		
	#Following is an example of how we can update the information from users...
	def button1Click(self, event):
		#import Tkinter, 
		#import tkFileDialog
		self.dirname = tkinter.filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
		self.displayinputtext = '.../'+self.dirname.split('/')[-1]
		self.inputdirchosen.config(text = self.displayinputtext)
		
	def button2Click(self, event):
		#self.outdirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
		self.outdirname = tkinter.filedialog.asksaveasfilename(parent=root, defaultextension = ".csv", initialfile = "results",title='Choose Output Filename')
		print(self.outdirname)
		if self.outdirname == "":
			self.displayoutputtext = "(No Output Filename Chosen)"
		else: self.displayoutputtext = '.../' + self.outdirname.split('/')[-1]
		self.outputdirchosen.config(text = self.displayoutputtext)
		
	# def runprogram(self, event):
	# 	self.poll(self.progress)
	# 	start_thread(main, self.dirname, self.outdirname, self.summary_name, self.var_list, self.source_text_list)
	
	def runprogram(self, event):
		self.poll(self.progress)
		start_thread(main, self.dirname, self.outdirname, self.var_dict, True, self.summary_name) #the True here is for the GUI

	def poll(self, function):
		
		self.myParent.after(10, self.poll, function)
		try:
			function.config(text = dataQueue.get(block=False))
			
			#root.update_idletasks()
		except queue.Empty:
			pass

#def main(indir, outdir, source_text, var_list, source_list):			

def main(indir, outdir, varDict, gui = False, source_text = False):
	def dqMessage(gui,text):
		if gui == True:
			dataQueue.put(text)
			root.update_idletasks()
		else:
			print(text)

	def checkBoxes(tDict, loKeys):
		nTrue = 0
		for x in loKeys:
			if tDict[x] == True:
				nTrue += 1
		return(nTrue)
	
	#options = []
	if varDict["wordsAll"] not in [True,False]: #convert to boolean if coming from GUI
		for items in varDict:
			if varDict[items].get() == 1:
				varDict[items] = True
			else:
				varDict[items] = False

	#check settings:
	# overlap_box = sum(options[1:8])
	# segment_box = sum([options[10],options[11]])
	# adjacent_box = sum([options[12],options[13]])
	# ttr_box = overlap_box + options[21]
	# all_boxes = sum(options[:21])+sum(source_options)

	overlap_box = checkBoxes(varDict, ["wordsAll","wordsContent","wordsFunction","wordsNoun","wordsPronoun","wordsArgument","wordsVerb","wordsAdjective","wordsAdverb"])
	segment_box = checkBoxes(varDict, ["overlapSentence","overlapParagraph"])
	adjacent_box = checkBoxes(varDict, ["overlapAdjacent","overlapAdjacent2"])
	ttr_box = overlap_box + checkBoxes(varDict, ["otherTTR"])
	all_boxes = checkBoxes(varDict, list(varDict.keys()))

	#interface validation:
	
	if indir == "":
		if gui == True:
			if system == "M":
				tkinter.messagebox.showinfo("Supply Information", "Choose an input directory!")
			else:
				dataQueue.put("Error: Choose an input directory!")
				root.update_idletasks()
	
	elif outdir == "":
		if gui == True:
			if system == "M":
				tkinter.messagebox.showinfo("Choose Output Filename", "Choose an output filename!")
			else:
				dataQueue.put("Error: Choose an output filename!")
				root.update_idletasks()

	elif all_boxes == 0:
		if gui == True:
			if system == "M":
				tkinter.messagebox.showinfo("Choose Indices", "Make an index selection!")
			else:
				dataQueue.put("Error: Make an index selection!")
				root.update_idletasks()

	elif overlap_box != 0 and varDict["otherTTR"] == False and segment_box == 0:
		if gui == True:
			if system == "M":
				tkinter.messagebox.showinfo("Make an Overlap Choice", "Choose Sentence, Paragraph, and/or TTR!")
			else:
				dataQueue.put("Error: Choose Sentence, Paragraph, and/or TTR!")
				root.update_idletasks()

	elif overlap_box != 0 and varDict["otherTTR"] == False and adjacent_box == 0:
		if gui == True:

			if system == "M":
				tkinter.messagebox.showinfo("Make an Overlap Choice", "Choose 'Adjacent' and/or 'Adjacent 2'!")
			else:
				dataQueue.put("Error: Choose 'Adjacent' and/or 'Adjacent 2'!")
				root.update_idletasks()
	
	elif segment_box != 0 and overlap_box == 0:
		if gui == True:

			if system == "M":
				tkinter.messagebox.showinfo("Make an Overlap Choice", "Choose which lemma tokens to analyze!")
			else:
				dataQueue.put("Error: Choose which lemma tokens to analyze!")
				root.update_idletasks()
	
	elif adjacent_box != 0 and overlap_box == 0:
		if gui == True:

			if system == "M":
				tkinter.messagebox.showinfo("Make an Overlap Choice", "Choose which lemma tokens to analyze!")
			else:
				dataQueue.put("Error: Choose which lemma tokens to analyze!")
				root.update_idletasks()
	
	elif varDict["otherTTR"] == True and ttr_box == 0:
		if gui == True:

			if system == "M":
				tkinter.messagebox.showinfo("Make a TTR Choice", "Choose which lemma tokens to analyze!")
			else:
				dataQueue.put("Error: Choose which lemma tokens to analyze!")
				root.update_idletasks()
	
		
	else:
	#if indir is not "" and outdir is not "":
		#V. 1.5 was previously called version 2.0.20
		dqMessage(gui,"Starting TAACO...")

		#thus begins the text analysis portion of the program
		import glob
		import math
		
		# def call_stan_corenlp(class_path, file_list, output_folder, memory, nthreads): #for CoreNLP 3.5.1 (most recent compatible version)
		# 	#mac osx call:
		# 	if system == "M" or system == "L":
		# 		call_parser = "java -cp "+ class_path +"*: -Xmx" + memory + "g edu.stanford.nlp.pipeline.StanfordCoreNLP -threads "+ nthreads + " -annotators tokenize,ssplit,pos,lemma,depparse -filelist " + file_list + " -outputDirectory "+ output_folder
		# 	#windows call:
		# 	elif system == "W":
		# 		call_parser = "java -cp "+ class_path +"*; -Xmx" + memory + "g edu.stanford.nlp.pipeline.StanfordCoreNLP -threads "+ nthreads + " -annotators tokenize,ssplit,pos,lemma,depparse -filelist " + file_list + " -outputDirectory "+ output_folder

		# 	count = len(file(file_list, "rU").readlines())
		# 	folder = output_folder
		# 	print "starting checker"
		# 	start_watcher(watcher, count, folder)
			
		# 	subprocess.call(call_parser, shell=True) #This watches the output folder until all files have been parsed

		def dicter(spread_name,delimiter, lower = False):
			if lower == False:
				spreadsheet = open(resource_path(spread_name),errors = "ignore").read().split("\n")
			if lower == True:
				spreadsheet = open(resource_path(spread_name),errors = "ignore").read().lower().split("\n")
				
			dict = {}
			for line in spreadsheet:
				if line == "":
					continue
				if line[0] == "#":
					continue
				vars = line.split(delimiter)
				if len(vars)<2:
					continue
				dict[vars[0]] = vars[1:]
			
			return(dict)

		def dicter_2(spread_name,delimiter1, delimiter, lower = False):
			if lower == False:
				spreadsheet = open(resource_path(spread_name),errors = "ignore").read().split("\n")
			if lower == True:
				spreadsheet = open(resource_path(spread_name),errors = "ignore").read().lower().split("\n")
				
			dict = {}
			for line in spreadsheet:
				if line == "":
					continue
				if line[0] == "#":
					continue
				head = line.split(delimiter1)[0]
				
				if len(line.split(delimiter1))<2:
					continue
				vars = line.split(delimiter1)[1].split(delimiter)
				if len(vars)<2:
					continue
				dict[head] = vars[1:]
			
			return(dict)
					
		def dict_builder(database_file, number, log = "n", delimiter = "\t"): #builds dictionaries from database files
			dict ={}
			data_file = database_file.lower().split("\n")
			for entries in data_file:  
				if entries == "":
					continue
				if entries[0] == '#': #ignores first line which contains category information
					continue
			
				entries = entries.split(delimiter)
				if log == "n": 
					dict[entries[0]]=float(entries[number])
				if log == "y": 
					if not entries[number] == '0':
						dict[entries[0]]=math.log10(float(entries[number]))

			return(dict)

		def indexer(header_list, index_list, name, index):
			header_list.append(name)
			index_list.append(index)
		
		#This function deals with denominator issues that can kill the program:
		def safe_divide(numerator, denominator):
			if denominator == 0:
				index = 0
			else: index = numerator/denominator
			return(index)

		#This is for single givenness... if a word only occurs once in a text, the counter increases by one
		def single_givenness_counter(text):
			counter = 0
			for item in text:
				if text.count(item) == 1:
					counter+= 1
			return(counter)

		#This is for repeated givenness... if a word occurs more than once in a text, the counter increases by one
		def repeated_givenness_counter(text):
			counter = 0
			for item in text:
				if text.count(item) > 1:
					counter+= 1
			return(counter)

		def n_grammer(text, length, list = None): #updated 2023-08-05
			counter = 0
			ngram_text = []
			for word in text:
				ngram = text[counter:(counter+length)]

				if len(ngram)> (length-1):
					ngram_text.append(" ".join(str(x) for x in ngram))
					# try:
					# 	ngram_text.append(" ".join(str(x) for x in ngram))		
					# except UnicodeEncodeError:
						# ngram_text.append("Encode Error")				
				counter+=1
			if list is not None:
				for item in ngram_text:
					#print item
					list.append(item)
			else:
				return(ngram_text)
		
		
		#revised version (6/19/17):
		def overlap_counter(header_list, index_list, name_suffix, list, seg_1, seg_2):# this completes all overlap functions:
			#print list
			## need to add check to ensure that list is a list of lists
			
			#first we have counters:
			
			n_segments = len(list) #number of sentences or paragraphs
			
			#this next section deals with texts that only have one segment
			if n_segments < 2:
				if seg_1 == True:
					pre_header_list = ["adjacent_overlap_" + name_suffix, "adjacent_overlap_" + name_suffix + "_div_seg", "adjacent_overlap_binary_" + name_suffix]
					for header in pre_header_list: header_list.append(header)
					pre_index_list = [0,0,0]
					for pre_index in pre_index_list: index_list.append(pre_index)
				
				if seg_2 == True:
					pre_header_list = [ "adjacent_overlap_2_"+name_suffix,  "adjacent_overlap_2_" + name_suffix + "_div_seg",  "adjacent_overlap_binary_2_"+ name_suffix]
					for header in pre_header_list: header_list.append(header)					
					pre_index_list = [0,0,0]
					for pre_index in pre_index_list: index_list.append(pre_index)

			
			#this is the "normal" procedure
			else:	
								
				single_overlap_denominator = 0
				double_overlap_denominator = 0
				
				overlap_counter_1 = 0
				overlap_counter_2 = 0
				binary_count_1 = 0
				binary_count_2 = 0
						
				for number in range (n_segments-1):
					#print number, "of", n_segments-1
					next_item_overlap = []#list so that overlap can be recovered for post-hoc
					next_two_item_overlap = []#list so that overlap can be recovered for post-hoc
				

					if number < n_segments -3 or number == n_segments -3: #Make sure we didn't go too far
						for items in set(list[number]):
							single_overlap_denominator +=1
							double_overlap_denominator +=1
							if items in list[number + 1]:
								next_item_overlap.append(items)
	
							if items in list[number + 1] or items in list[number + 2]:
								next_two_item_overlap.append(items)

					else: #Make sure we didn't go too far
						for items in set(list[number]):
							single_overlap_denominator +=1
							if items in list[number + 1]:
								next_item_overlap.append(items)
								
							
					overlap_counter_1 += len(next_item_overlap)
					overlap_counter_2 += len(next_two_item_overlap)
					#print next_two_item_overlap
					if len(next_item_overlap) > 0: binary_count_1 += 1
					if len(next_two_item_overlap) > 0: binary_count_2 += 1
												
				if seg_1 == 1:
					overlap_1_nwords = safe_divide(overlap_counter_1, single_overlap_denominator)			
					overlap_1_nseg = safe_divide(overlap_counter_1, n_segments - 1)
					binary_1_nsent = safe_divide(binary_count_1, n_segments - 1)
					
					pre_header_list = ["adjacent_overlap_" + name_suffix, "adjacent_overlap_" + name_suffix + "_div_seg", "adjacent_overlap_binary_" + name_suffix]
					for header in pre_header_list: header_list.append(header)
					pre_index_list = [overlap_1_nwords, overlap_1_nseg,binary_1_nsent]
					for pre_index in pre_index_list: index_list.append(pre_index)
				
				if seg_2 == 1:
					overlap_2_nwords = safe_divide(overlap_counter_2, double_overlap_denominator)
					overlap_2_nseg = safe_divide(overlap_counter_2, n_segments - 2)
					binary_2_nsent = safe_divide(binary_count_2, n_segments - 2)
					
					pre_header_list = [ "adjacent_overlap_2_"+name_suffix,  "adjacent_overlap_2_" + name_suffix + "_div_seg",  "adjacent_overlap_binary_2_"+ name_suffix]
					for header in pre_header_list: header_list.append(header)					
					pre_index_list = [overlap_2_nwords,overlap_2_nseg,binary_2_nsent]
					for pre_index in pre_index_list: index_list.append(pre_index)
			
		#Revised 6-21-17
		def wordnet_dict_build(target_list, syn_dict):
			counter = len(target_list) #this is the number of paragraphs/sentences in the text
			
			#print "syn_counter", counter
			
			#holder structure:
			target_syn_dict = {}
			
			#creates a version of the text where each word is a list of synonyms:
			for i in range(counter): #iterates as many times as there are sentences/paragraphs in text
				
				if len(target_list[i]) < 1:
					target_syn_dict[i] = []
				else:
					syn_list1=[]
					for item in target_list[i]: #for word in sentence/paragraph
						#print "item: ", item
						if item in syn_dict:
							syns = syn_dict[item]
						else: syns = [item]
						syn_list1.append(syns)
		
					target_syn_dict[i]=syn_list1
			
			return(target_syn_dict)

		#Revised 6-21-17
		def syn_overlap(header_list, index_list, name_suffix, list, syn_dict):
			counter = len(list)		
			if counter < 2:
				syn_counter_norm = 0
			else:
				syn_counter=0
				for i in range(counter-1):
					for items in set(list[i]):
						for item in syn_dict[i+1]:
							if items in item:
								syn_counter +=1
				syn_counter_norm = safe_divide(syn_counter, counter-1) #note these are divided by segments
			header_list.append("syn_overlap_" + name_suffix)
			index_list.append(syn_counter_norm)
		
		#created 6-21-17 replaces regex_count
		def multi_list_counter(header_list, index_list, word_list, target_list, nwords):
			#print target_list
			for lines in word_list:
				if lines[0] == "#":
					continue
				line = lines.split("\t")	
				header_list.append(line[0])
				counter = 0
				for words in line[1:]:
					if words == "":
						continue
					#print words
					word = " " + words + " " # adds space to beginning and end to avoid over-counting (i.e., "forward" should not be a match for the conjunction "for")
					for sentences in target_list: #iterates through sentences to ensure that sentence boundaries are not crossed
						sentence = " " + " ".join(sentences)+ " " #turns list of words into a string, adds a space to the beginning and end
						#print sentence
						counter+= sentence.count(word) #counts list instances in each sentence
						#print words, sentence, sentence.count(words)
				index_list.append(safe_divide(counter,nwords)) #appends normed index to index_list
			
		def ngram_counter(text, ngram_list):
			checker_text = " " + " ".join(text) + " "
			counter = 0
			new_ngram_list = []
			
			for item in ngram_list:
				new_item = " " + item + " "
				new_ngram_list.append(new_item)
				
			for items in new_ngram_list:
				counter += checker_text.count(items)
			return(counter)

		def mattr(header_list, index_list, index_name, text, window_length):
			header_list.append(index_name)
			
			if len(text) < (window_length + 1):
				mattr = safe_divide(len(set(text)),len(text))
				index_list.append(mattr)
			else:
				sum_ttr = 0
				denom = 0
				for x in range(len(text)):
					small_text = text[x:(x + window_length)]
					if len(small_text) < window_length:
						break
					denom += 1
					sum_ttr+= safe_divide(len(set(small_text)),float(window_length)) #safe_divide(float(len(set(small_text))),float(len(small_text)))
				index_list.append(safe_divide(sum_ttr,denom))

		#this needs to be updated to use Spacy and not Stanford CoreNLP
		# def content_pos_dict(xml_file, lemma = "no"):
		# 	if lemma == "no":
		# 		token_get = 0
		# 	if lemma == "yes":
		# 		token_get = 1
	
		# 	dict = {}

		# 	tree = ET.ElementTree(file=xml_file)

		# 	noun_tags = ["NN", "NNS", "NNP", "NNPS"] #consider whether to identify gerunds
		# 	adjectives = ["JJ", "JJR", "JJS"]
		# 	verbs = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
		# 	adverbs = ["RB", "RBR", "RBS"]
		# 	verbs_nouns = ["NN", "NNS", "NNP", "NNPS","VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
		# 	nouns_adjectives = ["NN", "NNS", "NNP", "NNPS","JJ", "JJR", "JJS"]

		# 	pos_word_list = []

		# 	s_noun_text = []
		# 	s_adjective_text = []
		# 	s_verb_text = []
		# 	s_verb_noun_text = []
		# 	s_adverb_text = []
		# 	s_all_text = []
	
		# 	for sentences in tree.iter("sentence"):
		# 		noun_text = []
		# 		adjective_text = []
		# 		verb_text = []
		# 		verb_noun_text = []
		# 		adverb_text = []
		# 		content_text = []
		# 		all_text = []
		
		# 		for tokens in sentences.iter("token"):
		# 			if tokens[4].text in punctuation:
		# 				continue
		# 			all_text.append(tokens[token_get].text.lower())
		# 			if tokens[4].text in noun_tags:
		# 				noun_text.append(tokens[token_get].text.lower())
		# 				verb_noun_text.append(tokens[token_get].text.lower())
		# 			if tokens[4].text in adjectives:
		# 				adjective_text.append(tokens[token_get].text.lower())
		# 			if tokens[4].text in verbs:
		# 				verb_text.append(tokens[token_get].text.lower())
		# 				verb_noun_text.append(tokens[token_get].text.lower())
		# 			if tokens[4].text in adverbs:
		# 				adverb_text.append(tokens[token_get].text.lower())
		
		# 		s_noun_text.append(noun_text)
		# 		s_adjective_text.append(adjective_text)
		# 		s_verb_text.append(verb_text)
		# 		s_verb_noun_text.append(verb_noun_text)
		# 		s_adverb_text.append(adverb_text)
		# 		s_all_text.append(all_text)

		# 	all_noun = [item for sublist in s_noun_text for item in sublist]
		# 	all_adjective = [item for sublist in s_adjective_text for item in sublist]
		# 	all_verb = [item for sublist in s_verb_text for item in sublist]
		# 	all_verb_noun = [item for sublist in s_verb_noun_text for item in sublist]
		# 	all_adverb = [item for sublist in s_adverb_text for item in sublist]
		# 	all_all = [item for sublist in s_all_text for item in sublist]
	
		# 	dict["s_all"] = s_all_text

		# 	dict["noun"] = all_noun
		# 	dict["adj"] = all_adjective
		# 	dict["verb"] = all_verb
		# 	dict["verb_noun"] = all_verb_noun
		# 	dict["adv"] = all_adverb
		# 	dict["all"] = all_all
			
		# 	return dict


		def content_pos_dict_spacy(text, lemma = False): #previously: "xml_file" instead of "text" #updated 08-05-2023
			# if lemma == "no":
			# 	token_get = 0
			# if lemma == "yes":
			# 	token_get = 1
	
			outd = {}

			doc = nlp(text) #process text
			#tree = ET.ElementTree(file=xml_file)

			noun_tags = ["NN", "NNS", "NNP", "NNPS"] #consider whether to identify gerunds
			adjectives = ["JJ", "JJR", "JJS"]
			verbs = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
			adverbs = ["RB", "RBR", "RBS"]
			verbs_nouns = ["NN", "NNS", "NNP", "NNPS","VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
			nouns_adjectives = ["NN", "NNS", "NNP", "NNPS","JJ", "JJR", "JJS"]

			pos_word_list = []

			s_noun_text = []
			s_adjective_text = []
			s_verb_text = []
			s_verb_noun_text = []
			s_adverb_text = []
			s_all_text = []
	
			for sent in doc.sents:
				noun_text = []
				adjective_text = []
				verb_text = []
				verb_noun_text = []
				adverb_text = []
				content_text = []
				all_text = []
		
				for token in sent:
					if lemma == False:
						tok_item  = token.text.lower()
					if lemma == True:
						tok_item  = token.lemma_.lower()
					if token.tag_ in punctuation: #uses a list of punctuation marks
						continue
					all_text.append(tok_item)
					if token.tag_ in noun_tags:
						noun_text.append(tok_item)
						verb_noun_text.append(tok_item)
					if token.tag_ in adjectives:
						adjective_text.append(tok_item)
					if token.tag_ in verbs:
						verb_text.append(tok_item)
						verb_noun_text.append(tok_item)
					if token.tag_ in adverbs:
						adverb_text.append(tok_item)
		
				s_noun_text.append(noun_text)
				s_adjective_text.append(adjective_text)
				s_verb_text.append(verb_text)
				s_verb_noun_text.append(verb_noun_text)
				s_adverb_text.append(adverb_text)
				s_all_text.append(all_text)

			all_noun = [item for sublist in s_noun_text for item in sublist]
			all_adjective = [item for sublist in s_adjective_text for item in sublist]
			all_verb = [item for sublist in s_verb_text for item in sublist]
			all_verb_noun = [item for sublist in s_verb_noun_text for item in sublist]
			all_adverb = [item for sublist in s_adverb_text for item in sublist]
			all_all = [item for sublist in s_all_text for item in sublist]
	
			outd["s_all"] = s_all_text

			outd["noun"] = all_noun
			outd["adj"] = all_adjective
			outd["verb"] = all_verb
			outd["verb_noun"] = all_verb_noun
			outd["adv"] = all_adverb
			outd["all"] = all_all
			
			return(outd)


		# def ngram_pos_dict(xml,lemma = "no"):
		# 	noun_tags = ["NN", "NNS", "NNP", "NNPS"] #consider whether to identify gerunds
		# 	adjectives = ["JJ", "JJR", "JJS"]
		# 	verbs = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
		# 	adverbs = ["RB", "RBR", "RBS"]
		# 	verbs_nouns = ["NN", "NNS", "NNP", "NNPS","VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
		# 	nouns_adjectives = ["NN", "NNS", "NNP", "NNPS","JJ", "JJR", "JJS"]


		# 	if lemma == "no":
		# 		token_get = 0
		# 	if lemma == "yes":
		# 		token_get = 1
	
		# 	def dict_add(dict, list, name, sent = "no"):
		# 		if sent == "yes":
		# 			if name in dict:
		# 				dict[name].append(list)
		# 			else:
		# 				dict[name] = [list]
		# 		if sent == "no":
		# 			if name in dict:
		# 				for items in list:
		# 					dict[name].append(items)
		# 			else:
		# 				dict[name] = list

	
		# 	frequency_dict = {}

		# 	tree = ET.ElementTree(file=xml) #The file is opened by the XML parser

		# 	uni_list = []
		# 	bi_list = []
		# 	tri_list = []
		# 	quad_list = []
	
		# 	n_list_bi= []
		# 	adj_list_bi= []
		# 	v_list_bi= []
		# 	v_n_list_bi= []
		# 	a_n_list_bi= []

		# 	n_list_tri= []
		# 	adj_list_tri= []
		# 	v_list_tri= []
		# 	v_n_list_tri= []
		# 	a_n_list_tri= []

		# 	n_list_quad= []
		# 	adj_list_quad= []
		# 	v_list_quad= []
		# 	v_n_list_quad= []
		# 	a_n_list_quad= []


		# 	for sentences in tree.iter("sentence"):
		
		# 		def lemma_lister(constraint = None):
		# 			list = []
		# 			for tokens in sentences.iter("token"):
		# 				try:
		# 					str(tokens[token_get].text)
		# 				except UnicodeEncodeError:
		# 					continue
		# 				if tokens[token_get].text in punctuation:
		# 					continue
		# 				if constraint == None:
		# 					list.append(tokens[token_get].text.lower())
		# 				else:
		# 					if tokens[4].text in constraint:
		# 						list.append(tokens[token_get].text.lower())
		# 					else:
		# 						list.append("x")
		# 			return list
			
		# 		word_list = lemma_lister()
		
		# 		for items in word_list:
		# 			uni_list.append(items)
				
		# 		n_list = lemma_lister(noun_tags)
		# 		adj_list = lemma_lister(adjectives)
		# 		v_list = lemma_lister(verbs)
		# 		v_n_list = lemma_lister(verbs_nouns)
		# 		a_n_list = lemma_lister(nouns_adjectives)
		
		
		# 		n_grammer(word_list,2,bi_list)
		# 		n_grammer(word_list,3,tri_list)
		# 		n_grammer(word_list,4,quad_list)
		
		# 		n_grammer(n_list, 2, n_list_bi)
		# 		n_grammer(adj_list, 2, adj_list_bi)
		# 		n_grammer(v_list, 2, v_list_bi)
		# 		n_grammer(v_n_list, 2, v_n_list_bi)
		# 		n_grammer(a_n_list, 2, a_n_list_bi)
		
		# 		n_grammer(n_list, 3, n_list_tri)
		# 		n_grammer(adj_list, 3, adj_list_tri)
		# 		n_grammer(v_list, 3, v_list_tri)
		# 		n_grammer(v_n_list, 3, v_n_list_tri)
		# 		n_grammer(a_n_list, 3, a_n_list_tri)

		# 		n_grammer(n_list, 4, n_list_quad)
		# 		n_grammer(adj_list, 4, adj_list_quad)
		# 		n_grammer(v_list, 4, v_list_quad)
		# 		n_grammer(v_n_list, 4, v_n_list_quad)
		# 		n_grammer(a_n_list, 4, a_n_list_quad)
		
		# 	dict_add(frequency_dict, bi_list, "bi_list")
		# 	dict_add(frequency_dict, tri_list, "tri_list")
		# 	dict_add(frequency_dict, quad_list, "quad_list")

		# 	dict_add(frequency_dict, n_list_bi, "n_list_bi")
		# 	dict_add(frequency_dict, adj_list_bi, "adj_list_bi")
		# 	dict_add(frequency_dict, v_list_bi, "v_list_bi")
		# 	dict_add(frequency_dict, v_n_list_bi, "v_n_list_bi")
		# 	dict_add(frequency_dict, a_n_list_bi, "a_n_list_bi")

		# 	dict_add(frequency_dict, n_list_tri, "n_list_tri")
		# 	dict_add(frequency_dict, adj_list_tri, "adj_list_tri")
		# 	dict_add(frequency_dict, v_list_tri, "v_list_tri")
		# 	dict_add(frequency_dict, v_n_list_tri, "v_n_list_tri")
		# 	dict_add(frequency_dict, a_n_list_tri, "a_n_list_tri")

		# 	dict_add(frequency_dict, n_list_quad, "n_list_quad")
		# 	dict_add(frequency_dict, adj_list_quad, "adj_list_quad")
		# 	dict_add(frequency_dict, v_list_quad, "v_list_quad")
		# 	dict_add(frequency_dict, v_n_list_quad, "v_n_list_quad")
		# 	dict_add(frequency_dict, a_n_list_quad, "a_n_list_quad")
	
		# 	return frequency_dict
		
		def ngram_pos_dict_spacy(text,lemma = False): #updated 2023-08-05
			# if lemma == "no":
			# 	token_get = 0
			# if lemma == "yes":
			# 	token_get = 1
	
			def dict_add(tdict, list, name, sent = False):
				if sent == True:
					if name in tdict:
						tdict[name].append(list)
					else:
						tdict[name] = [list]
				if sent == False:
					if name in tdict:
						for items in list:
							tdict[name].append(items)
					else:
						tdict[name] = list

			def lemma_lister(sentence, constraint = None):
				outlist = []
				for token in sentence:
					if lemma == True:
						tok_item = token.lemma_.lower()
					else:
						tok_item = token.text.lower()
					# try:
					# 	str(tokens[token_get].text)
					# except UnicodeEncodeError:
					# 	continue
					if tok_item in punctuation:
						continue
					if constraint == None:
						outlist.append(tok_item)
					else:
						if token.tag_ in constraint:
							outlist.append(tok_item)
						else:
							outlist.append("x")
				return(outlist)

			noun_tags = ["NN", "NNS", "NNP", "NNPS"] #consider whether to identify gerunds
			adjectives = ["JJ", "JJR", "JJS"]
			verbs = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
			adverbs = ["RB", "RBR", "RBS"]
			verbs_nouns = ["NN", "NNS", "NNP", "NNPS","VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
			nouns_adjectives = ["NN", "NNS", "NNP", "NNPS","JJ", "JJR", "JJS"]

			frequency_dict = {}

			#tree = ET.ElementTree(file=xml) #The file is opened by the XML parser
			doc = nlp(text)

			uni_list = []
			bi_list = []
			tri_list = []
			quad_list = []
	
			n_list_bi= []
			adj_list_bi= []
			v_list_bi= []
			v_n_list_bi= []
			a_n_list_bi= []

			n_list_tri= []
			adj_list_tri= []
			v_list_tri= []
			v_n_list_tri= []
			a_n_list_tri= []

			n_list_quad= []
			adj_list_quad= []
			v_list_quad= []
			v_n_list_quad= []
			a_n_list_quad= []


			for sent in doc.sents:
					
				word_list = lemma_lister(sent)
		
				for items in word_list:
					uni_list.append(items)
				
				n_list = lemma_lister(sent,noun_tags)
				adj_list = lemma_lister(sent,adjectives)
				v_list = lemma_lister(sent,verbs)
				v_n_list = lemma_lister(sent,verbs_nouns)
				a_n_list = lemma_lister(sent,nouns_adjectives)
		
		
				n_grammer(word_list,2,bi_list)
				n_grammer(word_list,3,tri_list)
				n_grammer(word_list,4,quad_list)
		
				n_grammer(n_list, 2, n_list_bi)
				n_grammer(adj_list, 2, adj_list_bi)
				n_grammer(v_list, 2, v_list_bi)
				n_grammer(v_n_list, 2, v_n_list_bi)
				n_grammer(a_n_list, 2, a_n_list_bi)
		
				n_grammer(n_list, 3, n_list_tri)
				n_grammer(adj_list, 3, adj_list_tri)
				n_grammer(v_list, 3, v_list_tri)
				n_grammer(v_n_list, 3, v_n_list_tri)
				n_grammer(a_n_list, 3, a_n_list_tri)

				n_grammer(n_list, 4, n_list_quad)
				n_grammer(adj_list, 4, adj_list_quad)
				n_grammer(v_list, 4, v_list_quad)
				n_grammer(v_n_list, 4, v_n_list_quad)
				n_grammer(a_n_list, 4, a_n_list_quad)
		
			dict_add(frequency_dict, bi_list, "bi_list")
			dict_add(frequency_dict, tri_list, "tri_list")
			dict_add(frequency_dict, quad_list, "quad_list")

			dict_add(frequency_dict, n_list_bi, "n_list_bi")
			dict_add(frequency_dict, adj_list_bi, "adj_list_bi")
			dict_add(frequency_dict, v_list_bi, "v_list_bi")
			dict_add(frequency_dict, v_n_list_bi, "v_n_list_bi")
			dict_add(frequency_dict, a_n_list_bi, "a_n_list_bi")

			dict_add(frequency_dict, n_list_tri, "n_list_tri")
			dict_add(frequency_dict, adj_list_tri, "adj_list_tri")
			dict_add(frequency_dict, v_list_tri, "v_list_tri")
			dict_add(frequency_dict, v_n_list_tri, "v_n_list_tri")
			dict_add(frequency_dict, a_n_list_tri, "a_n_list_tri")

			dict_add(frequency_dict, n_list_quad, "n_list_quad")
			dict_add(frequency_dict, adj_list_quad, "adj_list_quad")
			dict_add(frequency_dict, v_list_quad, "v_list_quad")
			dict_add(frequency_dict, v_n_list_quad, "v_n_list_quad")
			dict_add(frequency_dict, a_n_list_quad, "a_n_list_quad")
	
			return(frequency_dict)



		def keyness(target_list, frequency_list_dict, top_perc = None,out_dir = "",keyname = ""): #note that frequency_list_dict should be normed
			list = []
			target_freq = Counter(target_list)
			comp_freq = frequency_list_dict
			xxxx_list = "x x,x x x,x x x x".split(",")	
			for item in target_freq:
				if item == "":
					continue
				freq = target_freq[item]
				if freq < 2:
					continue
		
				tf = target_freq[item]/len(target_list)
				ref_item = item.lower()
				try:
					#print "Item: ",item
					#print "Value: ", comp_freq[item]
					rf = comp_freq[ref_item]/1000000
					perc_dif = ((tf - rf)*100)/rf
					#print "in: ", item
				except KeyError:
					#print "out: ", item
					tf_idf = 1000000 #this will be, in effect, "infinity"
					perc_dif = 1000000 #this will be, in effect, "infinity"

				list.append([item,perc_dif,tf])

			final_list = sorted(list, key=itemgetter(1,2), reverse=True)

			if top_perc == None:
				return_list = final_list

			else:
				return_list = []
				perc = int(len(set(target_list))*top_perc)
				##print perc
				final_list = final_list[:perc]
				for items in final_list:
					if items[0] in xxxx_list:
						continue
					return_list.append(items[0])

			if out_dir !="":
				key_folder = out_dir+"/"+"key_lists"+"/"
				if not os.path.exists(key_folder):
					os.makedirs(key_folder)
	
				outfilename = key_folder + keyname
				key_write = open(outfilename, "w")
				for item in return_list:
					writestring = item + "\n"
					key_write.write(writestring)
				key_write.flush()
				key_write.close()

			return(return_list)				

		def simple_proportion(target_text,ref_text,type,index_name= None,index_list = None,header_list = None): #each text is a list
			length = len(target_text)
			counter = 0
			not_counter = 0
			for items in target_text:
				if items in ref_text:
					counter+=1
				else:
					not_counter+=1
			
			if type == "perc":
				outvar = safe_divide(counter,length)
			if type == "prop":
				outvar = safe_divide(counter,not_counter)

			if header_list is not None:
				header_list.append(index_name)
				index_list.append(outvar)
	
			if header_list is None:
				return(outvar)

		def lsa_similarity(text_list_1,text_list_2,lsa_matrix_dict,index_list = None,index_name= None,header_list = None,lsa_type = "fwd",nvectors = 300):
	
			def vector_av(text_list):
				n_items = 0
				l = []
				for i in range(nvectors):
					l.append(0)
		
				for items in text_list:
					if items not in lsa_matrix_dict:
						continue
					else:
						n_columns = 0
						n_items+=1
						for vector in lsa_matrix_dict[items]:
							l[n_columns] += float(vector)
							n_columns +=1

				#n_columns = 0
				#for items in l:
				#	l[n_columns] = l[n_columns]/n_items
	
				sum_count = 0
				for items in l:
					sum_count += math.pow(items,2)
				sqrt_sum = math.sqrt(sum_count)
			
		
				return([l, sqrt_sum])
		
			list1 = vector_av(text_list_1)
			list2 = vector_av(text_list_2)
	
			try:
				sum_count_2 = 0
				for items in range(len(list1[0])):
					sum_count_2+= (list1[0][items]*list2[0][items])


				cosine_sim = sum_count_2/(list1[1]*list2[1])
	
			except ZeroDivisionError:
				cosine_sim = "null"
		
			if header_list is not None:
				header_list.append(index_name)
				index_list.append(cosine_sim)
	
			if header_list is None:
				#print cosine_sim
				return(cosine_sim)

		def lda_divergence(text_list_1,text_list_2,dict,nvectors = 300):

			def vector_av(text_list):
				n_items = 0
				l = []
				for i in range(nvectors):
					l.append(0)
		
				for items in text_list:
					if items not in dict:
						continue
					else:
						n_columns = 0
						n_items+=1
						for vector in dict[items]:
							l[n_columns] += float(vector)
							n_columns +=1
				try:
					for x in range(len(l)): #normalize for number of words
						l[x] = safe_divide(l[x],n_items)
					
					div = np.linalg.norm(l, ord = 1) #linear algebra normalization - all items in list sum to 1
					for x in range(len(l)):
						l[x] = safe_divide(x,div)

				except ZeroDivisionError:
					l = "null"
				
				return(l)

			def jsdiv(P, Q):
				"""Compute the Jensen-Shannon divergence between two probability distributions.

				Input
				-----
				P, Q : array-like
					Probability distributions of equal length that sum to 1
				"""

				def _kldiv(A, B):
					return(np.sum([v for v in A * np.log2(A/B) if not np.isnan(v)]))

				P = np.array(P)
				Q = np.array(Q)

				M = 0.5 * (P + Q)

				return(0.5 * (_kldiv(P, M) +_kldiv(Q, M)))

		
			list1 = vector_av(text_list_1)
			list2 = vector_av(text_list_2)
			#print list1[:20]
			if list1 == "null" or list2 == "null":
				divergence = "null"
			else:
				divergence = 1 - jsdiv(list1,list2)
				if divergence >= 0: #this silliness controls for some wacky output. This was in Mihai's code... not sure how the wackiness occurs (it is rare)
					divergence = divergence
				else:
					divergence = "null"
			return(divergence)

		def segment_compare(header_list,index_list,text_list_of_lists, seg, name_suffix, lsa_matrix_dict,type = "lsa"): 

			#print list
			## need to add check to ensure that list is a list of lists
			
			#first we have counters:
			
			n_segments = len(text_list_of_lists) #number of sentences or paragraphs
			
			#this next section deals with texts that only have one segment
			if n_segments < (seg+1):
				if seg == 1:
					header_list.append(name_suffix)
					index_list.append(0)
												
				if seg == 2:
					header_list.append(name_suffix)
					index_list.append(0)
	
			#this is the "normal" procedure
			else:	
								
				denominator = 0
				counter = 0

				for number in range(n_segments-seg):
				
					item_list = text_list_of_lists[number] #e.g., sentence 1
					comparison_list = text_list_of_lists[number + 1]#e.g., sentence 2
					if seg == 2:
						for items in text_list_of_lists[number +2]:
							comparison_list.append(items)
					
					#print "item list:", item_list
					#print "comparison_list:", comparison_list
					
					if type == "lsa":
						index = lsa_similarity(item_list,comparison_list,lsa_matrix_dict)
						if index == "null":
							continue
						else:
							counter += index		
							denominator +=1

					if type == "lda":
						index = lda_divergence(item_list,comparison_list,lsa_matrix_dict)
						
						if index == "null":
							continue
						else:
							counter += index		
							denominator +=1
				
				index_list.append(safe_divide(counter,denominator))		
				header_list.append(name_suffix)

		def para_split(textString):
		
			para_t = textString
			while "\t" in para_t:
				para_t = para_t.replace("\t", " ")
			#print "check1"			
			while "  " in para_t:
				para_t = para_t.replace("  ", " ")
			#print "check2"
			while "\t\t" in para_t:
				para_t.replace("\t\t","\t")
			#print "check3"			
			while "\n \n" in para_t:
				para_t = para_t.replace("\n \n", "\n")		
			#print "check4"
			while "\n\n" in para_t:
				para_t = para_t.replace("\n\n", "\n")
		
			if para_t[0] == "\n":
				para_t = para_t[1:]
			if para_t[-1] == "\n":
				para_t = para_t[:-1]
			para_t = para_t.split("\n") # this is a list of strings
			return(para_t)
		

		#################################################################################	
		############################ END DEFINED FUNCTIONS###############################
		#################################################################################

		### THESE ARE PERTINENT FOR ALL IMPORTANT INDICES ####
		noun_tags = ["NN", "NNS", "NNP", "NNPS"] #consider whether to identify gerunds
		proper_n = ["NNP", "NNPS"]
		no_proper = ["NN", "NNS"]
		pronouns = ["PRP", "PRP$"]
		adjectives = ["JJ", "JJR", "JJS"]
		verbs = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
		adverbs = ["RB", "RBR", "RBS"]
		content = ["NN", "NNS", "NNP", "NNPS","JJ", "JJR", "JJS"]
		prelim_not_function = ["NN", "NNS", "NNP", "NNPS","JJ", "JJR", "JJS", "RB", "RBR", "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
		
		#simple_subordinators = "after although as because before if once since that though till unless until whenever wherever whereas whereupon while".split(" ")
		sentence_linkers = "nonetheless therefore although furthermore whereas nevertheless whatever however besides henceforth then if while but until because alternatively meanwhile when notwithstanding whenever moreover as consequently".split(" ")
		sentence_linkers_caveat = "for since after yet so"
		
		order = "next	first	firstly	second	secondly	finally	then".split("\t")
		order_caveat = "before	after".split("\t")
		order_ngram = "to begin with	in conclusion	above all".split("\t")
		
		reason_and_purpose = "therefore hence because as consequently".split(" ")
		reason_and_purpose_caveat = ["since", "so"]
		reason_and_purpose_ngram = ["that is why","for this reason", "for that reason", "because of", "on account of", "so that"]

		all_causal = "although	arise	arises	arising	arose	because	cause	caused	causes	causing	condition	conditions	consequence	consequences	consequent	consequently	due to	enable	enabled	enables	enabling	even then	follow that	follow the	follow this	followed that	followed the	followed this	following that	follows the	follows this	hence	made	make	makes	making	nevertheless	nonetheless	only if	provided that	result	results	so	therefore	though	thus	unless	whenever".split("\t")
		all_causal_caveat = ["since"]
		
		positive_causal = "arise	arises	arising	arose	because	cause	caused	causes	causing	condition	conditions	consequence	consequences	consequent	consequently	due	enable	enabled	enables	enabling	even	follow	followed	following	follows	hence	if	made	make	makes	making	only	provided	result	results	then	therefore	this	thus".split("\t")
		positive_causal_caveat = "since	so".split("\t")
		
		all_logical = "actually	admittedly	also	alternatively	although	anyhow	anyway	because	besides	but	cause	caused	causes	causing	consequence	consequences	consequently	correspondingly	enable	enabled	enables	finally	for	fortunately	further	furthermore	hence	however	if	incidentally	instead	likewise	moreover	nevertheless	next	nonetheless	nor	or	otherwise	rather	secondly	similarly	summarizing	then	therefore	thereupon	though	thus	unless	whereas	while".split("\t")
		all_logical_caveat = "for since so".split(" ")
		all_logical_ngram = "after all	all in all	and conversely	arise from	arise out of	arises from	arises out of	arising from	arising out of	arose from	arose out of	as a final point	as a result	as well	at least	at this point	by contrast	conditional upon	contrasted with	despite the fact that	due to	except that	follow that	follow the	follow this	followed that	followed the	followed this	following that	follows the	follows this	in actual fact	in any case	in any event	in case	in conclusion	in contrast	in fact	in order that	in other words	in short	in sum	it followed that	it follows	it follows that	notwithstanding that	on condition that	on one hand	on the condition that	on the contrary	on the one hand	on the other hand	once again	provided that	purpose of which	pursuant to	summing up	that is	that is to say	to conclude	to return(to	to sum up	to summarize	to take an example	to that end	to these ends	to this end	to those ends	well at any rate".split("\t")
		
		positive_logical = "actually also anyway because besides cause caused causes causing consequence consequences consequently correspondingly enable enabled enables finally fortunately further furthermore hence if incidentally instead likewise moreover next secondly similarly summarizing then therefore thereupon thus while".split(" ")
		positive_logical_caveat = "for since so".split(" ")
		positive_logical_ngram = "after all	all in all	arise from	arise out of	arises from	arises out of	arising from	arising out of	arose from	arose out of	as a final point	as a result	as well	at least	at this point	conditional upon	due to	follow that	follow the	follow this	followed that	followed the	followed this	following that	follows the	follows this	in actual fact	in any case	in any event	in case	in conclusion	in fact	in order that	in other words	in short	in sum	it followed that	it follows	it follows that	on condition that	on one hand	on the condition that	on the one hand	once again	provided that	purpose of which	pursuant to	summing up	that is	that is to say	to conclude	to return to	to sum up	to summarize	to take an example	to that end	to these ends	to this end	to those ends	well at any rate".split("\t")

		all_temporal = "earlier finally first further immediately instantly later meanwhile next presently previously secondly simultaneously since soon suddenly then until when whenever while".split(" ")
		all_temporal_caveat = "as after before".split(" ")
		all_temporal_ngram = "a consequence of	all this time	at last	at once	at the same time	at this moment	at this point	by this time	follow that	following that	from now on	in the meantime	it followed that	it follows	it follows that	now that	on another occasion	once more	so far	the consequence of	the consequences of	the last time	the previous moment	this time	throughout	to that end	up till that time	up to now".split("\t")

		positive_intentional = "desire	desired	desires	desiring	goal	goals	made	make	makes	making	purpose	purposes	want	wanted	wanting	wants".split("\t")
		positive_intentional_caveat = ["by","so"]
		positive_intentional_ngram = "in order	to that end	to these ends	to this end	to those ends".split("\t")
		
		all_positive = "actually	also	and	anyway	arise	arises	arising	arose	as	because	besides	cause	caused	causes	causing	condition	conditions	consequence	consequences	consequent	consequently	correspondingly	desire	desired	desires	desiring	due	earlier	enable	enabled	enables	enabling	even	finally	first	follow	followed	following	follows	fortunately	further	furthermore	goal	goals	hence	if	immediately	incidentally	instantly	instead	likewise	made	make	makes	making	meanwhile	moreover	next	only	provided	presently	previously	purpose	purposes	result	results	secondly	similarly	simultaneously	since	so	soon	suddenly	summarizing	then	therefore	thereupon	throughout	thus	too	want	wanted	wanting	wants	when	whenever	while".split("\t")
		all_positive_caveat = "after	before	by".split("\t")
		all_positive_ngram = "all in all	at last	at least	at once	conditional upon	from now on	in actual fact	in addition	in any case	in any event	in case	in conclusion	in fact	in order	in other words	in short	in sum	on another occasion	on one hand	once more	summing up	well at any rate".split("\t")
		
		all_connective = "actually	admittedly	again	also	alternatively	although	and	anyhow	anyway	arise	arises	arising	arose	as	because	besides	but	cause	caused	causes	causing	condition	conditions	consequence	consequences	consequent	consequently	correspondingly	desire	desired	desires	desiring	enable	enabled	enables	enabling	finally	first	fortunately	further	furthermore	goal	goals	hence	however	if	immediately	incidentally	instead	likewise	made	make	makes	making	meanwhile	moreover	nevertheless	next	nonetheless	nor	or	otherwise	presently	previously	rather	secondly	similarly	simultaneously	since	summarizing	then	therefore	thereupon	though	throughout	thus	too	unless	until	whenever	whereas	while	yet".split("\t")
		all_connective_caveat = "after	before	by so".split("\t")
		all_connective_ngram = "all in all	all this time	at last	at least	at once	at the same time	at this moment	at this point	conditional upon	contrasted with	despite the fact that	due to	except that	follow that	follow the	follow this	followed that	followed the	followed this	following that	follows the	follows this	from now on	in actual fact	in addition	in any case	in any event	in case	in conclusion	in contrast	in fact	in order	in other words	in short	in sum	in the end	in the meantime	it followed that	it follows	it follows that	notwithstanding that	now that	on another occasion	on one hand	on the contrary	on the one hand	on the other hand	once more	provided that	purpose of which	pursuant to	summing up	that is	the last time	the previous moment	this time	to conclude	to return to	to sum up	to summarize	to take an example	to that end	to these ends	to this end	to those ends	up till that time	up to now	well at any rate".split("\t")
		
		#other connectives with no caveats needed:
		basic_connectives = "and	nor	but	or	yet	so".split("\t")
		conjunctions = "and	but".split("\t")
		disjunctions = ["or"]
		coordinating_conjuncts = "yet	so	nor	however	therefore".split("\t")
		addition = "and	also	besides	further	furthermore	too	moreover	in addition	then	another	indeed	likewise".split("\t")
		opposition = "but	however	nevertheless	otherwise	on the other hand	on the contrary	yet	still	maybe	perhaps	instead	except for	in spite of	despite	nonetheless	apart from	unlike	whereas".split("\t")
		determiners = "a	an	the	this	that	these	those".split("\t")
		demonstratives = "this	that	these	those".split("\t")
		all_additive = "after all	again	all in all	also	alternatively	and	anyhow	as a final point	as well	at least	besides	but	by contrast	by the way	contrasted with	correspondingly	except that	finally	first	for example	for instance	fortunately	further	furthermore	however	in actual fact	in addition	in contrast	in fact	in other words	in sum	incidentally	instead	it follows	moreover	next	notwithstanding that	on one hand	on the contrary	on the one hand	on the other hand	or	otherwise	rather	secondly	similarly	summarizing	summing up	that is	thereupon	to conclude	to return to	to sum up	to summarize	to take an example	to these ends	to this end	too	well at any rate	whereas	yet".split("\t")
		negative_logical = "admittedly	alternatively	although	and conversely	anyhow	but	by contrast	contrasted with	despite the fact that	except that	however	in contrast	nevertheless	nonetheless	nor	notwithstanding that	on the contrary	on the other hand	or else	otherwise	rather	though	unless	whereas	yet".split("\t")
		all_negative = "admittedly	alternatively	although	and conversely	anyhow	but	by contrast	contrasted with	despite the fact that	except that	however	in contrast	nevertheless	nonetheless	nor	notwithstanding that	on the contrary	on the other hand	or	otherwise	rather	though	unless	until	whenever	whereas	yet".split("\t")
		###
		
		###Givenness pronouns:
		givenness_prp = "he she her him his they them their himself herself themselves his their it its".split(" ")
		###

		#variable_list = file(resource_path("Connectives_DICT_T4.txt"), 'rU').read().split("\n")
				
		if varDict["overlapLSA"] == True or varDict["sourceLSA"] == True:
			dqMessage(gui,"Loading LSA vector space...")
			lsa_dict = dicter_2(resource_path("COCA_newspaper_magazine_export_LSA.csv"),"\t"," ",lower = True)

		if varDict["overlapLDA"] == True or varDict["sourceLDA"] == True:
			dqMessage(gui,"Loading LDA vector space...")
			lda_dict = dicter_2(resource_path("COCA_newspaper_magazine_export_LDA.csv"),"\t"," ",lower = True)

		if varDict["overlapWord2vec"] == True or varDict["sourceWord2vec"] == True:
			dqMessage(gui,"Loading word2vec vector space...")
			word2vec_dict = dicter_2(resource_path("COCA_newspaper_magazine_export_word2vec.csv"),"\t"," ",lower = True)
		
		wn_noun_dict = dicter(resource_path("wn_noun_2.txt"),"\t")
		wn_verb_dict = dicter(resource_path("wn_verb_2.txt"),"\t")
		adj_word_list = open("adj_lem_list.txt",errors = "ignore").read().split("\n")[:-1]
		
		punctuation = "' . , ? ! ) ( % / - _ -LRB- -RRB- SYM : ;".split(" ")
		punctuation.append('"')

		#filenames - takes from user-designated folder

		inputfile = indir + "/*.txt"
		filenames = glob.glob(inputfile)
		
		outf=open(outdir, "w")
		
		print("outdir:", outdir)
		if source_text != "":
			if system == "M" or system == "L":
				key_out_dir = "/".join(outdir.split("/")[:-1])
		
			elif system == "W":
				key_out_dir = "\\".join(outdir.split("\\")[:-1])
				if len(key_out_dir) == 0:
					key_out_dir = "/".join(outdir.split("/")[:-1])
			print("key_out_dir:", key_out_dir)
		
		if varDict["outputTagged"] == True or varDict["outputDiagnostic"] == True:
			directory = outdir[:-4] + "_diagnostic/" #this is for diagnostic file
			if not os.path.exists(directory):
				os.makedirs(directory)
		
			for the_file in os.listdir(directory): #this cleans out the old diagnostic file (if applicable)
				file_path = os.path.join(directory, the_file)
				os.unlink(file_path)
		
		if varDict["outputDiagnostic"] == True:
			basic_diag_file_name = directory + "_diagnostic_file.csv"
			basic_diag_file = open(basic_diag_file_name, "w")
			
		if not os.path.exists(resource_path("para_files/")):
			os.makedirs(resource_path("para_files/"))
			
		for the_file in os.listdir(resource_path("para_files/")): #this cleans out the old diagnostic file (if applicable)
			file_path = os.path.join(resource_path("para_files/"), the_file)
			os.unlink(file_path)
					
		#Iterates through target files:

		simple_filename_list = [] #this is for later file retrieval
		pre_file_counter = 0
		n_pre_files = len(filenames)
		
		# #source text analysis
		# if source_text != "":
		# 	filenames.append(source_text)
 		# ####

		### Source Text Analysis
		if source_text != "" and varDict["sourceKeyOverlap"] == True:
			
			dqMessage(gui,"Loading COCA Lemma Data...")

			mag_news_uni_list = open(resource_path('mag_news_word_list_lemma_freq.csv'),errors = "ignore").read()
			mag_news_uni_F = dict_builder(mag_news_uni_list, 2)

			mag_news_bi_list = open(resource_path('mag_news_bi_list_lemma_freq.csv'),errors = "ignore").read()
			mag_news_bi_F = dict_builder(mag_news_bi_list, 2)

			mag_news_tri_list = open(resource_path('mag_news_tri_list_lemma_freq.csv'),errors = "ignore").read()
			mag_news_tri_F = dict_builder(mag_news_tri_list, 2)

			mag_news_quad_list = open(resource_path('mag_news_quad_list_lemma_freq.csv'),errors = "ignore").read()
			mag_news_quad_F = dict_builder(mag_news_quad_list, 2)

			#noun
			mag_news_n_bi_list = open(resource_path('mag_news_n_list_bi_lemma_freq.csv'),errors = "ignore").read()
			mag_news_n_bi_F = dict_builder(mag_news_n_bi_list, 2)

			mag_news_n_tri_list = open(resource_path('mag_news_n_list_tri_lemma_freq.csv'),errors = "ignore").read()
			mag_news_n_tri_F = dict_builder(mag_news_n_tri_list, 2)

			mag_news_n_quad_list = open(resource_path('mag_news_n_list_quad_lemma_freq.csv'),errors = "ignore").read()
			mag_news_n_quad_F = dict_builder(mag_news_n_quad_list, 2)

			#adjective
			mag_news_adj_bi_list = open(resource_path('mag_news_adj_list_bi_lemma_freq.csv'),errors = "ignore").read()
			mag_news_adj_bi_F = dict_builder(mag_news_adj_bi_list, 2)

			mag_news_adj_tri_list = open(resource_path('mag_news_adj_list_tri_lemma_freq.csv'),errors = "ignore").read()
			mag_news_adj_tri_F = dict_builder(mag_news_adj_tri_list, 2)

			mag_news_adj_quad_list = open(resource_path('mag_news_adj_list_quad_lemma_freq.csv'),errors = "ignore").read()
			mag_news_adj_quad_F = dict_builder(mag_news_adj_quad_list, 2)

			#verb
			mag_news_v_bi_list = open(resource_path('mag_news_v_list_bi_lemma_freq.csv'),errors = "ignore").read()
			mag_news_v_bi_F = dict_builder(mag_news_v_bi_list, 2)

			mag_news_v_tri_list = open(resource_path('mag_news_v_list_tri_lemma_freq.csv'),errors = "ignore").read()
			mag_news_v_tri_F = dict_builder(mag_news_v_tri_list, 2)

			mag_news_v_quad_list = open(resource_path('mag_news_v_list_quad_lemma_freq.csv'),errors = "ignore").read()
			mag_news_v_quad_F = dict_builder(mag_news_v_quad_list, 2)

			#verb_noun
			mag_news_v_n_bi_list = open(resource_path('mag_news_v_n_list_bi_lemma_freq.csv'),errors = "ignore").read()
			mag_news_v_n_bi_F = dict_builder(mag_news_v_n_bi_list, 2)

			mag_news_v_n_tri_list = open(resource_path('mag_news_v_n_list_tri_lemma_freq.csv'),errors = "ignore").read()
			mag_news_v_n_tri_F = dict_builder(mag_news_v_n_tri_list, 2)

			mag_news_v_n_quad_list = open(resource_path('mag_news_v_n_list_quad_lemma_freq.csv'),errors = "ignore").read()
			mag_news_v_n_quad_F = dict_builder(mag_news_v_n_quad_list, 2)

			#adjective_noun
			mag_news_a_n_bi_list = open(resource_path('mag_news_a_n_list_bi_lemma_freq.csv'),errors = "ignore").read()
			mag_news_a_n_bi_F = dict_builder(mag_news_a_n_bi_list, 2)

			mag_news_a_n_tri_list = open(resource_path('mag_news_a_n_list_tri_lemma_freq.csv'),errors = "ignore").read()
			mag_news_a_n_tri_F = dict_builder(mag_news_a_n_tri_list, 2)

			mag_news_a_n_quad_list = open(resource_path('mag_news_a_n_list_quad_lemma_freq.csv'),errors = "ignore").read()
			mag_news_a_n_quad_F = dict_builder(mag_news_a_n_quad_list, 2)

		#### Source Summary Analysis ####
			dqMessage(gui,"Processing Summary Text..")

			source = open(source_text,errors = "ignore").read().lower()
			#nwords_source = len(source_clean)
		
			# if system == "M" or system == "L":
			# 	tagged_source_name = "parsed_files/" + source_text.split("/")[-1] + ".xml"
		
			# elif system == "W":
			# 	pre_tsn = source_text.split("\\")[-1]
			# 	if "/" in pre_tsn:
			# 		pre_tsn = pre_tsn.split("/")[-1]
			# 	tagged_source_name = "parsed_files\\" + pre_tsn + ".xml"
			
			dqMessage(gui,"Loading Summary Text POS Lists")

			#source_pos_lem_dict = content_pos_dict(resource_path(tagged_source_name),lemma = "yes") #dict of pos lists
			source_pos_lem_dict = content_pos_dict_spacy(source,lemma = True) #dict of pos lists
			dqMessage(gui,"Loading Summary Text Ngram Lists")

			source_ngram_pos_lem_dict = ngram_pos_dict_spacy(source, lemma = True)
		
		## More Source analysis ##
			#model for keyword lists:
		
			mag_news_keywords = keyness(source_pos_lem_dict["all"], mag_news_uni_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_keywords.txt")
			mag_news_n_keywords = keyness(source_pos_lem_dict["noun"], mag_news_uni_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_n_keywords.txt")
			mag_news_v_keywords = keyness(source_pos_lem_dict["verb"], mag_news_uni_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_v_keywords.txt")
			mag_news_v_n_keywords = keyness(source_pos_lem_dict["verb_noun"], mag_news_uni_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_v_n_keywords.txt")
			mag_news_adj_keywords = keyness(source_pos_lem_dict["adj"], mag_news_uni_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_adj_keywords.txt")

			mag_news_bi_keywords = keyness(source_ngram_pos_lem_dict["bi_list"], mag_news_bi_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_bi_keywords.txt")
			mag_news_tri_keywords = keyness(source_ngram_pos_lem_dict["tri_list"], mag_news_tri_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_tri_keywords.txt")
			mag_news_quad_keywords = keyness(source_ngram_pos_lem_dict["quad_list"], mag_news_quad_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_quad_keywords.txt")
			mag_news_n_bi_keywords = keyness(source_ngram_pos_lem_dict["n_list_bi"], mag_news_n_bi_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_n_bi_keywords.txt")
			mag_news_adj_bi_keywords = keyness(source_ngram_pos_lem_dict["adj_list_bi"], mag_news_adj_bi_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_adj_bi_keywords.txt")
			mag_news_v_bi_keywords = keyness(source_ngram_pos_lem_dict["v_list_bi"], mag_news_v_bi_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_v_bi_keywords.txt")
			mag_news_v_n_bi_keywords = keyness(source_ngram_pos_lem_dict["v_n_list_bi"], mag_news_v_n_bi_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_v_n_bi_keywords.txt")
			mag_news_a_n_bi_keywords = keyness(source_ngram_pos_lem_dict["a_n_list_bi"], mag_news_a_n_bi_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_a_n_bi_keywords.txt")
			mag_news_n_tri_keywords = keyness(source_ngram_pos_lem_dict["n_list_tri"], mag_news_n_tri_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_n_tri_keywords.txt")
			mag_news_adj_tri_keywords = keyness(source_ngram_pos_lem_dict["adj_list_tri"], mag_news_adj_tri_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_adj_tri_keywords.txt")
			mag_news_v_tri_keywords = keyness(source_ngram_pos_lem_dict["v_list_tri"], mag_news_v_tri_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_v_tri_keywords.txt")
			mag_news_v_n_tri_keywords = keyness(source_ngram_pos_lem_dict["v_n_list_tri"], mag_news_v_n_tri_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_v_n_tri_keywords.txt")
			mag_news_a_n_tri_keywords = keyness(source_ngram_pos_lem_dict["a_n_list_tri"], mag_news_a_n_tri_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_a_n_tri_keywords.txt")
			mag_news_n_quad_keywords = keyness(source_ngram_pos_lem_dict["n_list_quad"], mag_news_n_quad_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_n_quad_keywords.txt")
			mag_news_adj_quad_keywords = keyness(source_ngram_pos_lem_dict["adj_list_quad"], mag_news_adj_quad_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_adj_quad_keywords.txt")
			mag_news_v_quad_keywords = keyness(source_ngram_pos_lem_dict["v_list_quad"], mag_news_v_quad_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_v_quad_keywords.txt")
			mag_news_v_n_quad_keywords = keyness(source_ngram_pos_lem_dict["v_n_list_quad"], mag_news_v_n_quad_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_v_n_quad_keywords.txt")
			mag_news_a_n_quad_keywords = keyness(source_ngram_pos_lem_dict["a_n_list_quad"], mag_news_a_n_quad_F, top_perc = .1,out_dir = key_out_dir,keyname = "mag_news_a_n_quad_keywords.txt")
		
		file_number = 0	#this is so that the header list works correctly
		for filename in filenames:
			if system == "M" or system == "L":
				simple_filename = filename.split("/")[-1]
			
			elif system == "W":
				simple_filename = filename.split("\\")[-1]
				if "/" in simple_filename:
					simple_filename = simple_filename.split("/")[-1]
			
			#simple_filename_list.append(simple_filename)
			
			pre_file_counter +=1
			
			dqMessage(gui,"TAACO is processing " + str(pre_file_counter) + " of " + str(n_pre_files) + " files")
			
			#simple read text, makes a single string:
			#text= file(filename, 'rU').read()
			text= open(filename, errors = "ignore").read()
			if len(text.split()) <=1:
				continue
	
			#creates paragraph separated version of text (which is a list of paragraphs):
			#print simple_filename

			para_text = para_split(text)

			n_files = len(simple_filename_list)
		
		# for items in simple_filename_list:
		# 	output_filename = items
			
			if varDict["outputTagged"] == True:
				diagname = directory + simple_filename[:-4] + "_diagnostic.txt"
				diag_file = open(diagname, "w")
				diag_file.write("word\tlemma\tPOS\tCW\FW\tother categories\n")
			
			header_list = ["Filename"]
			index_list = []
			
			diag_header_list = ["Filename"]
			diag_index_list = []
			
			# filename1 = ("TAACO is processing " + str(file_number+1) + " of " + str(n_files) + " files") #these lines update the GUI
			# dataQueue.put(filename1)
			# root.update_idletasks()
			
			diagnostic_text = []
			givenness_prp_text = []
			
			#for connectives
			subordinators = []
			sentence_linker_list =[]
			order_list = []
			reason_and_purpose_list = []
			all_causal_list = []
			positive_causal_list = []
			all_logical_list = []
			positive_logical_list = []
			all_temporal_list = []
			positive_intentional_list = []
			all_positive_list = []
			all_connective_list = []
			attended_demonstratives_list = []
			unattended_demonstratives_list = []
			
			
			###
			
			raw_text = [] #all words, not lemmatized
			lemma_text = [] #all words, lemmatized
			content_text=[] #content words, lemmatized
			function_text=[] #function words, lemmatized
			noun_text=[] #nouns
			verb_text=[] #content verbs 
			adj_text=[] #adjectives
			adv_text=[] #adverbs
			prp_text=[] #pronouns
			argument_text=[] #nouns + pronouns		
			
			#for source_text overlap
			all_verb_text = []#ALL verbs
			all_verb_noun_text = []
			all_verb_x_text = []
			noun_x_text = []
			noun_verb_x_text = []
			adj_noun_x_text = []
			adj_x_test = []
			
			para_raw_list=[]
			para_lemma_list=[]
			para_content_list=[]
			para_function_list=[]
			para_pos_noun_list=[] #nouns
			para_pos_verb_list=[] #verbs 
			para_pos_adj_list=[] #adjectives
			para_pos_adv_list=[] #adverbs
			para_pos_prp_list=[] #pronouns
			para_pos_argument_list=[] #nouns + pronouns		

			sent_raw_list=[]
			sent_lemma_list=[]
			sent_content_list=[]
			sent_function_list=[]
			sent_pos_noun_list=[] #nouns
			sent_pos_verb_list=[] #verbs 
			sent_pos_adj_list=[] #adjectives
			sent_pos_adv_list=[] #adverbs
			sent_pos_prp_list=[] #pronouns
			sent_pos_argument_list=[] #nouns + pronouns		

			text_items = {} #this will be the top-level organizer for the text?
			#print "dict:", para_file_dict
			for paragraph in para_text: #iterates through paragraphs
				#print "item", item
				doc = nlp(paragraph)
				#tree = ET.ElementTree(file=item) #this opens the file using an xml parser
				
				raw_list_para=[]
				lemma_list_para=[]
				content_list_para=[]
				function_list_para=[]
				pos_noun_list_para=[] #nouns
				pos_verb_list_para=[] #verbs 
				pos_adj_list_para=[] #adjectives
				pos_adv_list_para=[] #adverbs
				pos_prp_list_para=[] #pronouns
				pos_argument_list_para=[] #nouns + pronouns		

				for sent in doc.sents: #this iterates through sentences
					function_v_list = [] #list of idx that are auxilliary verbs or copular verbs
					subordinators_list = []
					attended_list = []
					
					
					raw_list_sent=[]
					lemma_list_sent=[]
					content_list_sent=[]
					function_list_sent=[]
					pos_noun_list_sent=[] #nouns
					pos_verb_list_sent=[] #verbs 
					pos_adj_list_sent=[] #adjectives
					pos_adv_list_sent=[] #adverbs
					pos_prp_list_sent=[] #pronouns
					pos_argument_list_sent=[] #nouns + pronouns		

					#new in 1.6.0
					#for deps in sentences.iter("dependencies"): #iterates through dependencies
					for token in sent:
						subordinator_check = False
						attended_check = False

						if token.tag_ in punctuation:
							continue
						raw_token = token.text.lower()
						lemma_token = token.lemma_.lower()
						POS_token = token.tag_
						
						diagnostic_token = []
						diagnostic_token.append(raw_token) #raw word
						diagnostic_token.append(lemma_token)	#lemma word
						diagnostic_token.append(POS_token)	#POS Tag
						
						# if token.tag_[:2] in ["VB","MD"] and token.pos_ in ["AUX"]:
						# 	function_v_list.append(token.i)
						# Kris Start here!!!
						if token.dep_ in ["mark"]:
							subordinator_check = True
						if token.dep_ in ["det"]:
							attended_check = True

						#raw words
						raw_text.append(raw_token)
						raw_list_para.append(raw_token)
						raw_list_sent.append(raw_token)
						
						#lemmas
						lemma_text.append(lemma_token)
						lemma_list_para.append(lemma_token)
						lemma_list_sent.append(lemma_token)
						
						if lemma_token in givenness_prp:
							givenness_prp_text.append(lemma_token)
						
						if POS_token in content:
							diagnostic_token.append("CW")
							content_text.append(lemma_token)
							content_list_para.append(lemma_token)
							content_list_sent.append(lemma_token)
						
						if POS_token not in prelim_not_function:
							diagnostic_token.append("FW")
							function_text.append(lemma_token)
							function_list_para.append(lemma_token)
							function_list_sent.append(lemma_token)

						if POS_token in verbs:
							all_verb_text.append(lemma_token)
							all_verb_x_text.append(lemma_token)
							
							if token.tag_[:2] in ["VB","MD"] and token.pos_ in ["AUX"]:
								diagnostic_token.append("FW")
								diagnostic_token.append("aux_or_cop")
								function_text.append(lemma_token)
								function_list_para.append(lemma_token)
								function_list_sent.append(lemma_token)
							else:
								diagnostic_token.append("CW")
								content_text.append(lemma_token)
								content_list_para.append(lemma_token)
								content_list_sent.append(lemma_token)
								
								diagnostic_token.append("VERB")
								verb_text.append(lemma_token)
								pos_verb_list_para.append(lemma_token)
								pos_verb_list_sent.append(lemma_token)
						else: all_verb_x_text.append("x")
						
						if POS_token in noun_tags:
							noun_x_text.append(lemma_token)
							diagnostic_token.append("NOUN")
							noun_text.append(lemma_token)
							pos_noun_list_para.append(lemma_token)
							pos_noun_list_sent.append(lemma_token)
						else: noun_x_text.append("x")
						
						if POS_token in adjectives:
							adj_x_test.append(lemma_token)
							diagnostic_token.append("ADJ")
							adj_text.append(lemma_token)
							pos_adj_list_para.append(lemma_token)
							pos_adj_list_sent.append(lemma_token)
						else: adj_x_test.append("x")
						
						if POS_token in adverbs:
							diagnostic_token.append("ADV")
							adv_text.append(lemma_token)
							pos_adv_list_para.append(lemma_token)
							pos_adv_list_sent.append(lemma_token)
							
							if lemma_token in adj_word_list or (lemma_token[-2:] == "ly" and lemma_token[:-2] in adj_word_list):
								diagnostic_token.append("CW")
								content_text.append(lemma_token)
								content_list_para.append(lemma_token)
								content_list_sent.append(lemma_token)
							else:
								diagnostic_token.append("FW")
								function_text.append(lemma_token)
								function_list_para.append(lemma_token)
								function_list_sent.append(lemma_token)
									
							
						if POS_token in pronouns:
							diagnostic_token.append("PRONOUN")
							prp_text.append(lemma_token)
							pos_prp_list_para.append(lemma_token)
							pos_prp_list_sent.append(lemma_token)
						
						if POS_token in pronouns or POS_token in noun_tags:
							diagnostic_token.append("ARGUMENT")
							argument_text.append(lemma_token)
							pos_argument_list_para.append(lemma_token)
							pos_argument_list_sent.append(lemma_token)
						
						if POS_token in verbs or POS_token in noun_tags:
							noun_verb_x_text.append(lemma_token)
							all_verb_noun_text.append(lemma_token)
						else: noun_verb_x_text.append("x")

						if POS_token in adjectives or POS_token in noun_tags:
							adj_noun_x_text.append(lemma_token)
						else: adj_noun_x_text.append("x")
							
						if token.dep_ in ["mark"]: #this probably needs to be expanded
							diagnostic_token.append("SUBORDINATOR")
							subordinators.append(raw_token)
						
						if raw_token in sentence_linkers:
							sentence_linker_list.append(raw_token)
						if subordinator_check == True and raw_token in sentence_linkers_caveat:
							sentence_linker_list.append(raw_token)

						if raw_token in order:
							order_list.append(raw_token)
						if subordinator_check == True and raw_token in order_caveat:
							order_list.append(raw_token)

						if raw_token in reason_and_purpose:
							reason_and_purpose_list.append(raw_token)
						if subordinator_check == True and raw_token in reason_and_purpose_caveat:
							reason_and_purpose_list.append(raw_token)

						if raw_token in all_causal:
							all_causal_list.append(raw_token)
						if subordinator_check == True and raw_token in all_causal_caveat:
							all_causal_list.append(raw_token)

						if raw_token in positive_causal:
							positive_causal_list.append(raw_token)
						if subordinator_check == True and raw_token in positive_causal_caveat:
							positive_causal_list.append(raw_token)

						if raw_token in all_logical:
							all_logical_list.append(raw_token)
						if subordinator_check == True and raw_token in all_logical_caveat:
							all_logical_list.append(raw_token)

						if raw_token in positive_logical:
							positive_logical_list.append(raw_token)
						if subordinator_check == True and raw_token in positive_logical_caveat:
							positive_logical_list.append(raw_token)

						if raw_token in all_temporal:
							all_temporal_list.append(raw_token)
						if subordinator_check == True and raw_token in all_temporal_caveat:
							all_temporal_list.append(raw_token)

						if raw_token in positive_intentional:
							positive_intentional_list.append(raw_token)
						if subordinator_check == True and raw_token in positive_intentional_caveat:
							positive_intentional_list.append(raw_token)

						if raw_token in all_positive:
							all_positive_list.append(raw_token)
						if subordinator_check == True and raw_token in all_positive_caveat:
							all_positive_list.append(raw_token)

						if raw_token in all_connective:
							all_connective_list.append(raw_token)
						if subordinator_check == True and raw_token in all_connective_caveat:
							all_connective_list.append(raw_token)

						if raw_token in demonstratives:
							#print raw_token
							if attended_check == True:
								attended_demonstratives_list.append(raw_token)
							else:
								unattended_demonstratives_list.append(raw_token)
								diagnostic_token.append("PRONOUN")
								prp_text.append(lemma_token)
								pos_prp_list_para.append(lemma_token)
								pos_prp_list_sent.append(lemma_token)

					
						#leave this next line alone
						diagnostic_text.append(diagnostic_token)
						
					#add sentence lists to full sentence list
					diagnostic_text.append(["\nsentence break\n"]) #adds sentence indicator for diagnostic text
					sent_raw_list.append(raw_list_sent)
					sent_lemma_list.append(lemma_list_sent)
					sent_content_list.append(content_list_sent)
					sent_function_list.append(function_list_sent)
					sent_pos_noun_list.append(pos_noun_list_sent)
					sent_pos_verb_list.append(pos_verb_list_sent)
					sent_pos_adj_list.append(pos_adj_list_sent)
					sent_pos_adv_list.append(pos_adv_list_sent)
					sent_pos_prp_list.append(pos_prp_list_sent)
					sent_pos_argument_list.append(pos_argument_list_sent)
								
				#adds paragraph lists to full paragraph lists
				diagnostic_text.append(["\nparagraph break\n"]) #adds paragraph indicator for diagnostic text
				para_raw_list.append(raw_list_para)
				para_lemma_list.append(lemma_list_para)
				para_content_list.append(content_list_para)
				para_function_list.append(function_list_para)
				para_pos_noun_list.append(pos_noun_list_para)
				para_pos_verb_list.append(pos_verb_list_para)
				para_pos_adj_list.append(pos_adj_list_para)
				para_pos_adv_list.append(pos_adv_list_para)
				para_pos_prp_list.append(pos_prp_list_para)
				para_pos_argument_list.append(pos_argument_list_para)
			
			#basic indices (including simple ttr):	
			
			#For TAACO 2.0: add alternative ttr calculations (e.g., MATTR)
			nsentences = len (sent_lemma_list)
			nparagraphs = len(para_lemma_list)
		
						
			#raw words
			nwords = len(raw_text)
			nprps = len(prp_text)
			nnouns = len(noun_text)

			if varDict["outputDiagnostic"] == True:
					indexer(diag_header_list, diag_index_list, "nwords", nwords)
					indexer(diag_header_list, diag_index_list, "nsentences", nsentences)
					indexer(diag_header_list, diag_index_list, "nparagraphs", nparagraphs)
								
			if varDict["otherTTR"] == True:
				#all words (lemmatized)						
				if varDict["wordsAll"] == True:
					nlemmas = len(lemma_text)
					nlemma_types = len(set(lemma_text))
					ncontent_words= len(content_text)
					ncontent_types= len(set(content_text))
					nfunction_words= len(function_text)
					nfunction_types= len(set(function_text))

					indexer(header_list, index_list, "lemma_ttr", safe_divide(nlemma_types,nlemmas))
					mattr(header_list, index_list, "lemma_mattr", lemma_text, 50)
					
					indexer(header_list, index_list, "lexical_density_tokens", safe_divide(ncontent_words,nlemmas))
					indexer(header_list, index_list, "lexical_density_types", safe_divide(ncontent_types,nlemma_types))
					
					if varDict["outputDiagnostic"] == True:
						indexer(diag_header_list, diag_index_list, "nlemmas", nlemmas)
						indexer(diag_header_list, diag_index_list, "nlemma_types", nlemma_types)
			
				#content_words; note, these are ALL LEMMATIZED!!!			
				if varDict["wordsContent"] == True:	
					indexer(header_list, index_list, "content_ttr", safe_divide(ncontent_types, ncontent_words))
					
					if varDict["outputDiagnostic"] == True:
						indexer(diag_header_list, diag_index_list, "ncontent_words", ncontent_words)
						indexer(diag_header_list, diag_index_list, "ncontent_types", ncontent_types)
			
				#function words; note, these are ALL LEMMATIZED!!!
			
				if varDict["wordsFunction"] == True:			
					indexer(header_list, index_list, "function_ttr", safe_divide(nfunction_types, nfunction_words))
					mattr(header_list, index_list, "function_mattr", function_text, 50)

					if varDict["outputDiagnostic"] == True:
						indexer(diag_header_list, diag_index_list, "nfunction_words", nfunction_words)

				if varDict["wordsNoun"] == True:					
					nnouns_types = len(set(noun_text))
					indexer(header_list, index_list, "noun_ttr", safe_divide(nnouns_types, nnouns))
					
					if varDict["outputDiagnostic"] == True:
						indexer(diag_header_list, diag_index_list, "n_nouns", nnouns)
						indexer(diag_header_list, diag_index_list, "n_noun_types", nnouns_types)

				if varDict["wordsVerb"] == True:					
					nverbs = len(verb_text)
					nverbs_types = len(set(verb_text))
					indexer(header_list, index_list, "verb_ttr", safe_divide(nverbs_types, nverbs))
					
					if varDict["outputDiagnostic"] == True:
						indexer(diag_header_list, diag_index_list, "n_verbs", nverbs)
						indexer(diag_header_list, diag_index_list, "n_verb_types", nverbs_types)

				if varDict["wordsAdjective"] == True:					
					nadjs = len(adj_text)
					nadjs_types = len(set(adj_text))
					indexer(header_list, index_list, "adj_ttr", safe_divide(nadjs_types, nadjs))

					if varDict["outputDiagnostic"] == True:
						indexer(diag_header_list, diag_index_list, "n_adjs", nadjs)
						indexer(diag_header_list, diag_index_list, "n_adj_types", nadjs_types)

				if varDict["wordsAdverb"] == True:					
					nadvs = len(adv_text)
					nadvs_types = len(set(adv_text))
					indexer(header_list, index_list, "adv_ttr", safe_divide(nadvs_types, nadvs))

					if varDict["outputDiagnostic"] == True:
						indexer(diag_header_list, diag_index_list, "n_advs", nadvs)
						indexer(diag_header_list, diag_index_list, "n_adv_types", nadvs_types)

				
				if varDict["wordsPronoun"] == True:					
					nprps_types = len(set(prp_text))
					indexer(header_list, index_list, "prp_ttr", safe_divide(nprps_types, nprps))

					if varDict["outputDiagnostic"] == True:
						indexer(diag_header_list, diag_index_list, "n_prps", nprps)
						indexer(diag_header_list, diag_index_list, "n_prp_types", nprps_types)

				if varDict["wordsArgument"] == True:					
					narguments = len(argument_text)
					narguments_types = len(set(argument_text))
					indexer(header_list, index_list, "argument_ttr", safe_divide(narguments_types, narguments))

					if varDict["outputDiagnostic"] == True:
						indexer(diag_header_list, diag_index_list, "n_arguments", narguments)
						indexer(diag_header_list, diag_index_list, "n_argument_types", narguments_types)


				### N-GRAM INDICES####
				if varDict["overlapNgrams"] == True:
					bigram_lemma_text = n_grammer(lemma_text, 2)
					n_bigram_lemmas = len(bigram_lemma_text)
					n_bigram_lemma_types = len(set(bigram_lemma_text))
					trigram_lemma_text = n_grammer(lemma_text, 3)
					n_trigram_lemmas = len(trigram_lemma_text)
					n_trigram_lemma_types = len(set(trigram_lemma_text))			

					indexer(header_list, index_list, "bigram_lemma_ttr", safe_divide(n_bigram_lemma_types,n_bigram_lemmas))
					indexer(header_list, index_list, "trigram_lemma_ttr", safe_divide(n_trigram_lemma_types,n_trigram_lemmas))
					
					if varDict["outputDiagnostic"] == True:
						indexer(diag_header_list, diag_index_list, "n_bigram_lemmas", n_bigram_lemmas)
						indexer(diag_header_list, diag_index_list, "n_bigram_lemma_types", n_bigram_lemma_types)
						indexer(diag_header_list, diag_index_list, "n_trigram_lemmas", n_trigram_lemmas)
						indexer(diag_header_list, diag_index_list, "n_trigram_lemma_types", n_trigram_lemma_types)
			### END N-GRAM INDICES###
			

			###Begin SENTENCE OVERLAP SECTION###
			
			#Overlap- Counts here are organized by list. For each list there are six counts and two ways to calculate most indices (/nwords or /sent_counter). Comments are given for the first set, all other sets are identical				
			#revised 6/20/17
			if varDict["overlapSentence"] == True:
				if varDict["wordsAll"] == True:
					overlap_counter(header_list, index_list, "all_sent", sent_lemma_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #all words, lemmatized
				if varDict["wordsContent"] == True:
					overlap_counter(header_list, index_list, "cw_sent", sent_content_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #Content Words, Lemmatized
				if varDict["wordsFunction"] == True:
					overlap_counter(header_list, index_list, "fw_sent", sent_function_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #Function Words, Lemmatized
				if varDict["wordsNoun"] == True:
					overlap_counter(header_list, index_list, "noun_sent", sent_pos_noun_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS NOUN, Lemmatized
				if varDict["wordsVerb"] == True:
					overlap_counter(header_list, index_list, "verb_sent", sent_pos_verb_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS Verb, Lemmatized
				if varDict["wordsAdjective"] == True:
					overlap_counter(header_list, index_list, "adj_sent", sent_pos_adj_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS Adj, Lemmatized
				if varDict["wordsAdverb"] == True:
					overlap_counter(header_list, index_list, "adv_sent", sent_pos_adv_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS Adv, Lemmatized
				if varDict["wordsPronoun"] == True:
					overlap_counter(header_list, index_list, "pronoun_sent", sent_pos_prp_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS PRP, Lemmatized
				if varDict["wordsArgument"] == True:
					overlap_counter(header_list, index_list, "argument_sent", sent_pos_argument_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS ARGUMENT (PRP + NOUN)


		###BEGIN PARAGRAPH OVERLAP SECTION###
			if varDict["overlapParagraph"] == True:

				if varDict["wordsAll"] == True:
					overlap_counter(header_list, index_list, "all_para", para_lemma_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #all words, lemmatized
				if varDict["wordsContent"] == True:
					overlap_counter(header_list, index_list, "cw_para", para_content_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #Content Words, Lemmatized
				if varDict["wordsFunction"] == True:
					overlap_counter(header_list, index_list, "fw_para", para_function_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #Function Words, Lemmatized
				if varDict["wordsNoun"] == True:
					overlap_counter(header_list, index_list, "noun_para", para_pos_noun_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS NOUN, Lemmatized
				if varDict["wordsVerb"] == True:
					overlap_counter(header_list, index_list, "verb_para", para_pos_verb_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS Verb, Lemmatized
				if varDict["wordsAdjective"] == True:
					overlap_counter(header_list, index_list, "adj_para", para_pos_adj_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS Adj, Lemmatized
				if varDict["wordsAdverb"] == True:
					overlap_counter(header_list, index_list, "adv_para", para_pos_adv_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS Adv, Lemmatized
				if varDict["wordsPronoun"] == True:
					overlap_counter(header_list, index_list, "pronoun_para", para_pos_prp_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS PRP, Lemmatized
				if varDict["wordsArgument"] == True:
					overlap_counter(header_list, index_list, "argument_para", para_pos_argument_list, varDict["overlapAdjacent"], varDict["overlapAdjacent2"]) #POS ARGUMENT (PRP + NOUN)

			###END PARAGRAPH OVERLAP SECTION###

			###BEGIN WORDNET OVERLAP SECTION###
			if varDict["overlapSynonym"] == True:
				#Syn Sentence Dictionaries
				noun_sent_syn_lemma_dict=wordnet_dict_build(sent_pos_noun_list, wn_noun_dict)
				verb_sent_syn_lemma_dict= wordnet_dict_build(sent_pos_verb_list, wn_verb_dict)

				#Syn Paragraph Dictionaries
				noun_para_syn_lemma_dict=wordnet_dict_build(para_pos_noun_list, wn_noun_dict)
				verb_para_syn_lemma_dict= wordnet_dict_build(para_pos_verb_list, wn_verb_dict)

				#Syn Sentence Overlap Indices
				noun_sent_syn_lemma_overlap = syn_overlap(header_list, index_list, "sent_noun", sent_pos_noun_list,noun_sent_syn_lemma_dict)
				verb_sent_syn_lemma_overlap = syn_overlap(header_list, index_list, "sent_verb", sent_pos_verb_list,verb_sent_syn_lemma_dict)

				#Syn Paragraph Overlap Indices
				noun_para_syn_lemma_overlap = syn_overlap(header_list, index_list, "para_noun", para_pos_noun_list, noun_para_syn_lemma_dict)
				verb_para_syn_lemma_overlap = syn_overlap(header_list, index_list, "para_verb", para_pos_verb_list, verb_para_syn_lemma_dict)

		###END WORDNET OVERLAP SECTION####silence		
		
		### Begin LSA/LDA/Word2vec comparison SECTION ###
		
			if varDict["overlapLSA"] == True:
				segment_compare(header_list,index_list,sent_lemma_list, 1, "lsa_1_all_sent", lsa_dict)
				segment_compare(header_list,index_list,sent_lemma_list, 2, "lsa_2_all_sent", lsa_dict)

				segment_compare(header_list,index_list,para_lemma_list, 1, "lsa_1_all_para", lsa_dict)
				segment_compare(header_list,index_list,para_lemma_list, 2, "lsa_2_all_para", lsa_dict)
			
			if varDict["overlapLDA"] == True:
				segment_compare(header_list,index_list,sent_lemma_list, 1, "lda_1_all_sent", lda_dict,"lda")
				segment_compare(header_list,index_list,sent_lemma_list, 2, "lda_2_all_sent", lda_dict,"lda")

				segment_compare(header_list,index_list,para_lemma_list, 1, "lda_1_all_para", lda_dict,"lda")
				segment_compare(header_list,index_list,para_lemma_list, 2, "lda_2_all_para", lda_dict,"lda")

			if varDict["overlapWord2vec"] == True:
				segment_compare(header_list,index_list,sent_lemma_list, 1, "word2vec_1_all_sent", word2vec_dict)
				segment_compare(header_list,index_list,sent_lemma_list, 2, "word2vec_2_all_sent", word2vec_dict)

				segment_compare(header_list,index_list,para_lemma_list, 1, "word2vec_1_all_para", word2vec_dict)
				segment_compare(header_list,index_list,para_lemma_list, 2, "word2vec_2_all_para", word2vec_dict)
				
			

		### LIST SECTION 
			if varDict["otherConnectives"] == True:
				indexer(header_list, index_list, "basic_connectives", safe_divide(ngram_counter(raw_text, basic_connectives), nwords))
				indexer(header_list, index_list, "conjunctions", safe_divide(ngram_counter(raw_text, conjunctions), nwords))
				indexer(header_list, index_list, "disjunctions", safe_divide(ngram_counter(raw_text, disjunctions), nwords))
				indexer(header_list, index_list, "lexical_subordinators", safe_divide(len(subordinators), nwords))
				indexer(header_list, index_list, "coordinating_conjuncts", safe_divide(ngram_counter(raw_text, coordinating_conjuncts), nwords))
				indexer(header_list, index_list, "addition", safe_divide(ngram_counter(raw_text, addition), nwords))
				indexer(header_list, index_list, "sentence_linking", safe_divide(len(sentence_linker_list), nwords))
				indexer(header_list, index_list, "order", safe_divide((len(order_list) + ngram_counter(raw_text, order_ngram)), nwords))
				indexer(header_list, index_list, "reason_and_purpose", safe_divide((len(reason_and_purpose_list) + ngram_counter(raw_text, reason_and_purpose_ngram)), nwords))
				
				indexer(header_list, index_list, "all_causal", safe_divide(ngram_counter(raw_text, all_causal), nwords))
				indexer(header_list, index_list, "positive_causal", safe_divide(ngram_counter(raw_text, positive_causal), nwords))
				
				indexer(header_list, index_list, "opposition", safe_divide(ngram_counter(raw_text, opposition), nwords))
				indexer(header_list, index_list, "determiners", safe_divide(ngram_counter(raw_text, determiners), nwords))
				indexer(header_list, index_list, "all_demonstratives", safe_divide(ngram_counter(raw_text, demonstratives), nwords))				
				indexer(header_list, index_list, "attended_demonstratives", safe_divide(len(attended_demonstratives_list), nwords))
				indexer(header_list, index_list, "unattended_demonstratives", safe_divide(len(unattended_demonstratives_list), nwords))
				indexer(header_list, index_list, "all_additive", safe_divide(ngram_counter(raw_text, all_additive), nwords))
				indexer(header_list, index_list, "all_logical", safe_divide((len(all_logical_list) + ngram_counter(raw_text, all_logical_ngram)), nwords))
				indexer(header_list, index_list, "positive_logical", safe_divide((len( positive_logical_list) + ngram_counter(raw_text,  positive_logical_ngram)), nwords))
				indexer(header_list, index_list, "negative_logical", safe_divide(ngram_counter(raw_text, negative_logical), nwords))
				indexer(header_list, index_list, "all_temporal", safe_divide((len( all_temporal_list) + ngram_counter(raw_text,  all_temporal_ngram)), nwords))
				indexer(header_list, index_list, "positive_intentional", safe_divide((len( positive_intentional_list) + ngram_counter(raw_text,  positive_intentional_ngram)), nwords))
				indexer(header_list, index_list, "all_positive", safe_divide((len( all_positive_list) + ngram_counter(raw_text,  all_positive_ngram)), nwords))
				indexer(header_list, index_list, "all_negative", safe_divide(ngram_counter(raw_text, all_negative), nwords))
				indexer(header_list, index_list, "all_connective", safe_divide((len( all_connective_list) + ngram_counter(raw_text,  all_connective_ngram)), nwords))

				
		###END DICTIONARY LIST SECTION###	

		###Pronoun/Noun Ratio###
			if varDict["otherGivenness"] == True:
				indexer(header_list, index_list, "pronoun_density", safe_divide((len(givenness_prp_text) + len(unattended_demonstratives_list)), nwords))
				indexer(header_list, index_list, "pronoun_noun_ratio", safe_divide((len(givenness_prp_text) + len(unattended_demonstratives_list)), nnouns))
			
			### GIVENNESS See DEFINED FUNCTIONS for givenness counters###
				indexer(header_list, index_list, "repeated_content_lemmas", safe_divide(repeated_givenness_counter(content_text), nwords))
				indexer(header_list, index_list, "repeated_content_and_pronoun_lemmas", safe_divide((repeated_givenness_counter(content_text) + repeated_givenness_counter(givenness_prp_text) + repeated_givenness_counter(unattended_demonstratives_list)),nwords))

		###END GIVENNESS###
			if source_text != "":
				if varDict["sourceKeyOverlap"] == True: #key word overlap
					bi_list = n_grammer(lemma_text,2)
					tri_list = n_grammer(lemma_text,3)
					quad_list = n_grammer(lemma_text,4)
		
					n_list_bi = n_grammer(noun_x_text, 2)
					adj_list_bi = n_grammer(adj_x_test, 2)
					v_list_bi = n_grammer(all_verb_x_text, 2)
					v_n_list_bi = n_grammer(noun_verb_x_text, 2)
					a_n_list_bi = n_grammer(adj_noun_x_text, 2)
		
					n_list_tri = n_grammer(noun_x_text, 3)
					adj_list_tri = n_grammer(adj_x_test, 3)
					v_list_tri = n_grammer(all_verb_x_text, 3)
					v_n_list_tri = n_grammer(noun_verb_x_text, 3)
					a_n_list_tri = n_grammer(adj_noun_x_text, 3)

					n_list_quad = n_grammer(noun_x_text, 4)
					adj_list_quad = n_grammer(adj_x_test, 4)
					v_list_quad = n_grammer(all_verb_x_text, 4)
					v_n_list_quad = n_grammer(noun_verb_x_text, 4)
					a_n_list_quad = n_grammer(adj_noun_x_text, 4)
				
					simple_proportion(lemma_text,mag_news_keywords, "perc", "mag_news_uni_keywords_percentage", index_list, header_list)
					simple_proportion(noun_text,mag_news_n_keywords, "perc", "mag_news_n_uni_keywords_percentage", index_list, header_list)
					simple_proportion(all_verb_text,mag_news_v_keywords, "perc", "mag_news_v_uni_keywords_percentage", index_list, header_list)
					simple_proportion(all_verb_noun_text,mag_news_v_n_keywords, "perc", "mag_news_v_n_uni_keywords_percentage", index_list, header_list)
					simple_proportion(adj_text,mag_news_adj_keywords, "perc", "mag_news_adj_uni_keywords_percentage", index_list, header_list)

					simple_proportion(bi_list,mag_news_bi_keywords, "perc", "mag_news_bi_keywords_percentage", index_list, header_list)
					simple_proportion(tri_list,mag_news_tri_keywords, "perc", "mag_news_tri_keywords_percentage", index_list, header_list)
					simple_proportion(quad_list,mag_news_quad_keywords, "perc", "mag_news_quad_keywords_percentage", index_list, header_list)

					simple_proportion(n_list_bi,mag_news_n_bi_keywords, "perc", "mag_news_n_bi_keywords_percentage", index_list, header_list)
					simple_proportion(adj_list_bi,mag_news_adj_bi_keywords, "perc", "mag_news_adj_bi_keywords_percentage", index_list, header_list)
					simple_proportion(v_list_bi,mag_news_v_bi_keywords, "perc", "mag_news_v_bi_keywords_percentage", index_list, header_list)
					simple_proportion(v_n_list_bi,mag_news_v_n_bi_keywords, "perc", "mag_news_v_n_bi_keywords_percentage", index_list, header_list)
					simple_proportion(a_n_list_bi,mag_news_a_n_bi_keywords, "perc", "mag_news_a_n_bi_keywords_percentage", index_list, header_list)

					simple_proportion(n_list_tri,mag_news_n_tri_keywords, "perc", "mag_news_n_tri_keywords_percentage", index_list, header_list)
					simple_proportion(adj_list_tri,mag_news_adj_tri_keywords, "perc", "mag_news_adj_tri_keywords_percentage", index_list, header_list)
					simple_proportion(v_list_tri,mag_news_v_tri_keywords, "perc", "mag_news_v_tri_keywords_percentage", index_list, header_list)
					simple_proportion(v_n_list_tri,mag_news_v_n_tri_keywords, "perc", "mag_news_v_n_tri_keywords_percentage", index_list, header_list)
					simple_proportion(a_n_list_tri,mag_news_a_n_tri_keywords, "perc", "mag_news_a_n_tri_keywords_percentage", index_list, header_list)

					simple_proportion(n_list_quad,mag_news_n_quad_keywords, "perc", "mag_news_n_quad_keywords_percentage", index_list, header_list)
					simple_proportion(adj_list_quad,mag_news_adj_quad_keywords, "perc", "mag_news_adj_quad_keywords_percentage", index_list, header_list)
					simple_proportion(v_list_quad,mag_news_v_quad_keywords, "perc", "mag_news_v_quad_keywords_percentage", index_list, header_list)
					simple_proportion(v_n_list_quad,mag_news_v_n_quad_keywords, "perc", "mag_news_v_n_quad_keywords_percentage", index_list, header_list)
					simple_proportion(a_n_list_quad,mag_news_a_n_quad_keywords, "perc", "mag_news_a_n_quad_keywords_percentage", index_list, header_list)
				
				if varDict["sourceLSA"] == True: #lsa
					indexer(header_list, index_list, "source_similarity_lsa", lsa_similarity(lemma_text,source_pos_lem_dict["all"],lsa_dict))
				
				if varDict["sourceLDA"] == True: #lda
					indexer(header_list, index_list, "source_similarity_lda", lda_divergence(lemma_text,source_pos_lem_dict["all"],lda_dict))
				
				if varDict["sourceWord2vec"] == True: #word2vec
					indexer(header_list, index_list, "source_similarity_word2vec", lsa_similarity(lemma_text,source_pos_lem_dict["all"],word2vec_dict))
			
			#this prints the diagnostic file
			if varDict["outputTagged"] == True:
				for list_items in diagnostic_text:
					print_items = "\t".join(list_items) + "\n"
					try:
						diag_file.write(print_items)
					except UnicodeEncodeError:
						diag_file.write("encoding error!\n")
						 
				diag_file.flush()
				diag_file.close()
				#end diagnostic file
			
			if varDict["outputDiagnostic"] == True:
				if file_number == 0:
					diag_header_string = ",".join(diag_header_list)
					basic_diag_file.write ('{0}\n'
					.format(diag_header_string))
				
				diag_index_string_list = []
				
				for items in diag_index_list:
					diag_index_string_list.append(str(items))
				diag_string = ",".join(diag_index_string_list)
	
				basic_diag_file.write ('{0},{1}\n'
				.format(simple_filename,diag_string))

			
			index_string_list=[] 
			if file_number == 0:
				#print "header string should print"
				header_string = ",".join(header_list)
				outf.write ('{0}\n'
				.format(header_string))
			
			file_number+=1
			
			for items in index_list:
				index_string_list.append(str(items))
			string = ",".join(index_string_list)
	
			outf.write ('{0},{1}\n'
			.format(simple_filename,string))
					
		outf.flush()
		outf.close()
		
		if varDict["outputDiagnostic"] == True:
			basic_diag_file.flush()
			basic_diag_file.close()
		
		#Closing Message to let user know that the program did something: (may need to be more sophisticated)	
		
		nfiles = len(filenames)
		finishmessage = ("Processed " + str(nfiles) + " Files")
		dqMessage(gui,finishmessage)
		if system == "M" and gui == True:
			tkinter.messagebox.showinfo("Finished!", "TAACO has converted your files to numbers.\n\n Now the real work begins!")
			
class Catcher:
	def __init__(self, func, subst, widget):
		self.func = func
		self.subst = subst
		self.widget = widget

	def __call__(self, *args):
		try:
			if self.subst:
				args = apply(self.subst, args)
			return(apply(self.func, args))
		except(SystemExit, msg):
			raise(SystemExit, msg)
		except:
			import traceback
			import tkinter.messagebox
			ermessage = traceback.format_exc(1)
			ermessage = re.sub(r'.*(?=Error)', "", ermessage, flags=re.DOTALL)
			ermessage = "There was a problem processing your files:\n\n"+ermessage
			tkinter.messagebox.showerror("Error Message", ermessage)

if __name__ == '__main__':		
	root = tk.Tk()
	root.wm_title("TAACO 2.1.1")
	root.configure(background = color)
	root.geometry(geom_size)
	myapp = MyApp(root)
	root.mainloop()

# root = tk.Tk()
# root.wm_title(prog_name)
# root.configure(background = '#FFFF99')
# #sets starting size: NOTE: it doesn't appear as though Tkinter will let you make the 
# #starting size smaller than the space needed for widgets.
# root.geometry(geom_size)
# tk.CallWrapper = Catcher
# myapp = MyApp(root)
# root.mainloop()