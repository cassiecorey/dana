# Useful class for pre-processing data files, gathering stats, getting keywords etc.

import sys, os, string, re
import nltk
import collections
import numpy as np
import pickle

from nltk.stem import PorterStemmer
from collections import Counter

# Ignore words that don't have these parts of speech when computing keywords
# key_POS = set(["CD","FW","NN","NNS","NNP","NPS","VB","VBD","VBG","VBN","VBP","VBZ"])
# What if the only key words were nouns....
key_POS = set(["NN","NNS","NNP", "NNP","NNPS"])

# the porter stemmer
ps = PorterStemmer()

# Used to calculate the verbosity
# Takes: a string ("trump","carson","clinton","sanders")
# Returns: an int (verbosity)
def get_verbosity(candidate):
	return avg_answer_len(candidate)/avg_question_len(candidate)

def avg_answer_len(candidate):
	return 1

def avg_question_len(candidate):
	return 1

# Given a sentence, returns a list of keywords (stemmed)
# First tokenizes the sentence, then tags POS and checks
# against our list above of what we consider "keywords"
def extract_keywords(sentence):
	sentence = nltk.word_tokenize(sentence)
	tagged = nltk.tag.pos_tag(sentence)
	tagged = [pair for pair in tagged if pair[1] in key_POS]
	return {ps.stem(tag[0]) for tag in tagged}

# Takes two sentences and returns an int representing the score
# Right now score is only calculated using proximity of the two sentences.
def score_sent_sent(s1, s2):
	return proximity(s1, s2)

# Takes two sentence strings and calculates their proximity
# Proximity is the number of matching keywords
# e.g. "The big dog" and "The small dog" returns 1
# because each has a keyword of "dog"
def proximity(s1, s2):
	# Extract the keywords from each sentence
	k1 = extract_keywords(s1)
	k2 = extract_keywords(s2)
	# Cut off any stems like "ing", "ed", etc.
	k1 = list(map(ps.stem, k1))
	k2 = list(map(ps.stem, k2))
	prox = 0
	for k in k1:
		prox += k2.count(k)
	return prox

# Processes a file to extract keyword data
# Returns Counter object with {keyword:count} for all keywords in the file
def file_preprocess(candidate, path, filename):
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

# Score a sentence against a keyword_mapping
# This is used to kind of determine topic for a file
def score_sent_km(sentence, keyword_mapping):
	score = 0
	kw = extract_keywords(sentence)
	for k in kw:
		score += keyword_mapping[k]
	return score

# Checks to see if the file pre-processing data has already been done
# If so, return the object: dict of {keyword:count}
def load_pickle(candidate, path, filename):
	with open(os.path.expanduser("data/%s/%s/%s"%(candidate, path, filename)), "rb") as f:
		try:
			return pickle.load(f)
		except:
			return None

# Dumps the keyword mapping for a file so we don't have to reprocess it
def dump_pickle(candidate, path, filename, keyword_mapping):
  with open(os.path.expanduser("data/%s/%s/%s"%(candidate, path, filename)), "wb") as f:
  	try:
  		pickle.dump(keyword_mapping, f)
  		return True
  	except:
  		print("Problem dumping.")
  		return False

