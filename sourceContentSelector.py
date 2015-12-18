#!/usr/bin/python

# sourceContentSelector.py
# Given a question, returns relevant parts of an article

import sys, os, string, re
import nltk
from nltk.stem import PorterStemmer
import collections
import numpy as np
import pickle

# Ignore words that don't have these parts of speech when computing keywords
# key_POS = set(["CD","FW","NN","NNS","NNP","NPS","VB","VBD","VBG","VBN","VBP","VBZ"])
# What if the only key words were nouns....
key_POS = set(["NN","NNS","NNP", "NNP","NNPS"])
# auxiliary verbs we should ignore
aux = set(["is", "was", "did", "does", "do", "were", "are"])

# the porter stemmer
ps = PorterStemmer()

# Given a question, returns a list of keywords
def getKeywords(question):
  tagged = nltk.tag.pos_tag(question)
  tagged = [pair for pair in tagged if pair[1] in key_POS and pair[0].lower() not in aux]
  return {ps.stem(tag[0]) for tag in tagged}

# Given a question, return a list of each sentence in the article
# with a score attached to it
def getScoredSentences(question, article, candidate):
  print(question)
  # Try saving time by loading from pickle
  scored_sentences = load(candidate)
  if scored_sentences != None:
    return scored_sentences

  # If it wasn't in pickle...
  scored_sentences = []
  sentences = nltk.tokenize.sent_tokenize(article)
  for sentence in sentences:
      if sentence.strip() == "": continue
      tokenized = nltk.word_tokenize(sentence.lower())
      s = score(question, tokenized)
      scored_sentences.append((sentence, s))
  dump(candidate, scored_sentences)
  return scored_sentences

# Takes an array of candidate verbosity responses and scores them
def getScoredVResponses(question, responses, candidate):
  scored_responses = []
  for response in responses:
    if response.strip() == "": continue
    tokenized = nltk.word_tokenize(response.lower())
    s = score(question, tokenized)
    scored_responses.append((response, s))
  return scored_responses

# Scores a sentence based on how well we think it answers the question
def score(question, sentence):
    score = 0
    sentence = list(map(ps.stem, sentence))
    keywords = getKeywords(question)
    question = list(map(ps.stem, question))
    score += proximity(keywords, sentence)
    return score

def proximity(keywords, sentence):
  score = 0
  for key in keywords:
    score += sentence.count(key)
  return score

def load(candidate):
  with open(os.path.expanduser("data/%s/personality/pickles.txt"%candidate), "rb") as f:
    try:
      return pickle.load(f)
    except:
      return None

def dump(candidate, scored_sentences):
  with open(os.path.expanduser("data/%s/personality/pickles.txt"%candidate), "wb") as f:
    try:
      pickle.dump(scored_sentences, f)
      return True
    except:
      print("Problem dumping scored sentences into pickle.txt")
      return False

