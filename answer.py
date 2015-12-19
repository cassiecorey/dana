# to run: python answer.py article.txt questions.txt
# ouput: answers to the questions given after training on the article

# Useful tools which should be pre-installed
import os, sys, errno
import subprocess
import itertools
import nltk
import questionClassifier
import util

# To answer yes/no question, we want to just answer yes or no,
# and not return a  whole sentence. We do this by checking for
# any negatives in the sentence.
def contains_negative(sent):
  return "no" in sent or "not" in sent or "n't" in sent

# Answers a question from the information in article.
# Ranks all the sentences and then returns the top choice.
def answer(question, candidate):
  question = question.strip().rstrip("?").lower()
  
  print("1: Classify the question")
  question_type = questionClassifier.process(question)

  print("2: Locate a top-scoring file")
  top_file, path = util.get_top_file(question, candidate)
  
  if path=="qa":
    return util.get_qa_answer(question, candidate, top_file)

  print("3: Locate a top-scoring sentence within the file")
  top_sentence = util.get_top_sentence(question, candidate, path, top_file)
  # top_sentence = "This campaign is about the needs of the American people. "

  print("4: Calculate candidate verbosity")
  verbosity = util.get_verbosity(candidate)

  print("5: Make the answer verbose")
  answer = top_sentence + " " + util.verbosify(question, candidate, verbosity, top_sentence)

  return answer



# The main script
if __name__ == '__main__':
  candidate = sys.argv[1]
  question = open(sys.argv[2]).read()

  ans = answer(question, candidate)
  print("--------And our final answer from %s is...---------"%candidate)
  print(ans)



