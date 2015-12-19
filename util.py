# Useful class for pre-processing data files, gathering stats, getting keywords etc.

import sys, os, string, re
import nltk
import collections
import numpy as np
import pickle
import repl

from nltk.stem import PorterStemmer
from collections import Counter

ps = PorterStemmer()

# Since answers that come from question-answer data are often better suited
# for response to a question, we give question-file scores a bit of a boost
# when the file is in the qa path.
qa_factor = 1.5

#####################################################
################ PROCESSING THINGS ##################
#####################################################

# Used to calculate the verbosity
# Takes: string ("trump","carson","clinton","sanders")
# Returns: int
def get_verbosity(candidate):
	# This should flip flop to give us whether we're looking at a question
	# or the candidate's answer since structure of the QA file is restricted
	# to one of each on alternating lines.
	q = True
	avg_q_len = 0
	avg_a_len = 0
	with open("data/%s/qa/QA.txt"%(candidate), 'r') as f:
		for line in f:
			if q:
				avg_q_len += len(nltk.sent_tokenize(line))
				q = False
			else:
				avg_a_len += len(nltk.sent_tokenize(line))
				q = True
	return (int)(avg_a_len/avg_q_len)

# Given a sentence string, returns a list of keywords (stemmed)
# First tokenizes the sentence, then tags POS and checks
# against our list above of what we consider "keywords"
def extract_keywords(sentence):
	# Ignore words that don't have these parts of speech when computing keywords
	# key_POS = set(["CD","FW","NN","NNS","NNP","NPS","VB","VBD","VBG","VBN","VBP","VBZ"])
	# What if the only key words were nouns....
	key_POS = set(["NN","NNS","NNP", "NNP","NNPS"])
	sentence = nltk.word_tokenize(sentence)
	tagged = nltk.tag.pos_tag(sentence)
	tagged = [pair for pair in tagged if pair[1] in key_POS]
	return {ps.stem(tag[0]) for tag in tagged}

# Processes a file to extract keyword data
# Returns Counter object with {keyword:count} for all keywords in the file
def preprocess_file(candidate, path, filename):
	# Counter used so that we can call things like "most_common"
	keyword_mapping = load_pickle(candidate, path, filename)
	# If the keyword mapping has already been done for this file, load from pickle
	if keyword_mapping != None:
		return keyword_mapping
	# Otherwise, process the file...
	keyword_mapping = Counter()
	f = open("data/%s/%s/%s"%(candidate, path, filename)).read()
	sentences = nltk.tokenize.sent_tokenize(f)
	for sentence in sentences:
		# Ignore empty sentences "..." maybe
		if sentence.strip() == "": continue
		for key in extract_keywords(sentence):
			keyword_mapping[key] += 1
	# Store this mapping for possible future use
	dump_pickle(candidate, path, filename, keyword_mapping)
	return keyword_mapping


#####################################################
############# SCORING THINGS ########################
#####################################################

# Used to find the file with the best answer in it somewhere
# Takes: a question and filename as strings
# Returns: (filename, location) both strings, location is either "qa" or "personality"
def get_top_file(question, candidate):
	question_kw = list(map(ps.stem, extract_keywords(question)))
	file_scores = Counter()
	# Score files in the personality directory
	for f in os.listdir(os.getcwd()+"/data/%s/personality/"%candidate):
		if f.endswith(".txt"):
			file_scores[(f, "personality")] = score_sent_file(question_kw, candidate, "personality", f)
	# Score files in the qa directory
	# These files should get a bit of a boost when scoring 
	# because they're better for spawning answers
	for f in os.listdir(os.getcwd()+"/data/%s/qa/"%candidate):
		if f.endswith(".txt"):
			file_scores[(f, "qa")] = score_sent_file(question_kw, candidate, "qa", f)*qa_factor
	print(file_scores)
	return file_scores.most_common(1)[0][0]

# Returns a top-scoring sentence from a file
# Takes: string, string
# Returns: string
def get_top_sentence(question, candidate, path, filename):
	# Stemmed keywords of the question
	question_kw = list(map(ps.stem, extract_keywords(question)))
	sentence_scores = Counter()
	article = open("data/%s/%s/%s"%(candidate,path,filename)).read()
	file_sentences = nltk.sent_tokenize(article)
	for sentence in file_sentences:
		sentence_kw = list(map(ps.stem, extract_keywords(sentence)))
		sentence_scores[sentence] = score_kw_kw(question_kw, sentence_kw)
	return sentence_scores.most_common(1)[0][0]

# Returns the answer associated with a related question from QA data
def get_qa_answer(question, candidate, filename):
	question_kw = list(map(ps.stem, extract_keywords(question)))
	scores = Counter()
	article = open("data/%s/qa/%s"%(candidate, filename)).read()
	qa_pairs = article.split("\n")
	for i in range(0,(int)(len(qa_pairs)/2),2):
		ask_kw = list(map(ps.stem, extract_keywords(qa_pairs[i])))
		answer_kw = list(map(ps.stem, extract_keywords(qa_pairs[i+1])))
		scores[i] = score_kw_kw(question_kw, ask_kw) + score_kw_kw(question_kw, answer_kw)
	print(scores)
	index = scores.most_common(1)[0][0]
	return qa_pairs[index+1]



# Scores two sentences
# Right now score is only calculated using proximity of the two sentences.
# Takes: keyword list, keyword list
# Returns: int
def score_kw_kw(kw1, kw2):
	score = proximity(kw1, kw2)
	return score

# Score a sentence against a file
# This is used to kind of determine topic for a file
# Takes: keyword list, string, string, string
# Returns: int
def score_sent_file(sentence_kw, candidate, path, filename):
	score = 1
	keymap = preprocess_file(candidate, path, filename)
	for key_word in sentence_kw:
		score += keymap[key_word]

	# If the file had none of the keywords in it return 0
	if score == 1:
		return 0

	# Otherwise normalize the score a bit compared to the length of the file
	# This is necessary to give the QA guys a shot at answering some questions...
	f = open("data/%s/%s/%s"%(candidate, path, filename)).read()
	num_s = len(nltk.sent_tokenize(f))
	score = (int)(num_s/score)
	return score

# Scores a sentence against a verbose response generated by the Markov Chain
# Takes: string, string
# Returns: int
def score_sent_vb(sentence, vb_response):
	score = 0
	vb_sentences = nltk.sent_tokenize(vb_response.lower())
	for vb_sentence in vb_sentences:
		score += proximity(sentence, vb_sentence)
	return score

# Calculates the proximity of two sentences
# Proximity is the number of matching keywords
# e.g. "The big dog" and "The small dog" returns 1
# because each has a keyword of "dog"
# Takes: key_map, key_map
# Returns: int
def proximity(kw1, kw2):
	prox = 0
	for k in kw1:
		if k in kw2:
			prox += 1
	return prox


#####################################################
############### VERBOSIFYING THINGS #################
#####################################################

# Generates a high-proximity verbose response
# Takes: string, string, int, string
# Returns: string
def verbosify(question, candidate, verbosity, answer):
	rep = repl.Repl()
	rep.do_train("6 --noparagraphs data/%s/personality/*"%candidate)
	responses = Counter()
	for i in range(0,10):
		response = rep.do_sentences([int(verbosity),tuple(answer.split())])
		# re-train because this makes it generate a new response
		rep.do_train("6 --noparagraphs data/%s/personality/*"%candidate)
		responses[response] = score_sent_vb(question, response)
	return responses.most_common(1)[0][0]

#####################################################
############### PICKLING THINGS #####################
#####################################################

# Checks to see if the file pre-processing data has already been done
# If so, return the object: dict of {keyword:count}
def load_pickle(candidate, path, filename):
		try:
			with open(os.path.expanduser("picklejar/%s_%s_%s"%(candidate, path, filename)), "rb") as f:
				return pickle.load(f)
		except:
			return None

# Dumps the keyword mapping for a file so we don't have to reprocess it
def dump_pickle(candidate, path, filename, keyword_mapping):
  with open(os.path.expanduser("picklejar/%s_%s_%s"%(candidate, path, filename)), "wb+") as f:
  	try:
  		pickle.dump(keyword_mapping, f)
  		return True
  	except:
  		print("Problem dumping.")
  		return False
