# to run: python ask.py article.txt n
# output: n questions about the provided article

# Useful tools which should be pre-installed
import os, sys, errno
import subprocess
import re
import itertools
import nltk
from nltk.stem import PorterStemmer
import bs4

# Import our modules from /modules
sys.path.append("modules")
import questionContentSelector
import questionFromSentence
import coref

if __name__ == '__main__':
  path_to_article = sys.argv[1]
  num_questions = int(sys.argv[2])
  # print("Generating " + str(num_questions) + " questions:")

  # Pre-process article content.
  article_content = coref.process(path_to_article)

  # Fetch sentence candidates that can be converted into questions.
  selected_content = questionContentSelector.process(article_content)

  # Use POS Tagging and Transformation rules to generate questions
  questions = questionFromSentence.process(selected_content)
  print((len(questions)))
  # Rank generated questions and return top [:num_questions]

  questions = questions[:num_questions]
  for question in questions:
    print((question + "\n"))