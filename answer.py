# to run: python answer.py article.txt questions.txt
# ouput: answers to the questions given after training on the article

# Useful tools which should be pre-installed
import os, sys, errno
import subprocess
import re
import itertools
import nltk
import questionClassifier
import sourceContentSelector
import coref
import pickle
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup

# To answer yes/no question, we want to just answer yes or no,
# and not return a  whole sentence. We do this by checking for
# any negatives in the sentence.
def contains_negative(sent):
  return "no" in sent or "not" in sent or "n't" in sent

# Answers a question from the information in article.
# Ranks all the sentences and then returns the top choice.
def answer(question, article):
    question = question.strip().rstrip("?").lower()
    question_type = questionClassifier.process(question)
    question = nltk.tokenize.word_tokenize(question)
    relevant = sourceContentSelector.getScoredSentences(question, article)
    top = max(relevant, key = lambda s: s[1])
    if question_type == "BOOLEAN":
      if contains_negative(top): return "No"
      else: return "Yes"
    else: return top[0]

# The main script
if __name__ == '__main__':
  article_name = sys.argv[1]
  questions = open(sys.argv[2]).read().split("\n")

  article = coref.process(article_name)
  for question in questions:
    print answer(question, article)
