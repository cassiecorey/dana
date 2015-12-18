# to run: python answer.py article.txt questions.txt
# ouput: answers to the questions given after training on the article

# Useful tools which should be pre-installed
import os, sys, errno
import subprocess
import itertools
import nltk
import questionClassifier
import sourceContentSelector
import repl

# To answer yes/no question, we want to just answer yes or no,
# and not return a  whole sentence. We do this by checking for
# any negatives in the sentence.
def contains_negative(sent):
  return "no" in sent or "not" in sent or "n't" in sent

# Answers a question from the information in article.
# Ranks all the sentences and then returns the top choice.
def answer(question, article, candidate):
  question = question.strip().rstrip("?").lower()
  
  print("1: Classify the question")
  question_type = questionClassifier.process(question)
  
  print("2: Tokenize the question")
  question = nltk.tokenize.word_tokenize(question)
  
  print("3: Score the data sentences against the question")
  relevant = sourceContentSelector.getScoredSentences(question, article, candidate)
  
  print("4: Return the most likely answer:")
  top = max(relevant, key = lambda s: s[1])
  print(top)
  if question_type == "BOOLEAN":
    if contains_negative(top): return "No"
    else: return "Yes"
  else: return top[0]

def verbosify(question, candidate, verbosity, answer):
  print("5: Making the answer verbose")
  rep = repl.Repl()
  rep.do_train("6 --noparagraphs data/%s/personality/all.txt"%candidate)
  responses = []
  
  for i in range(0,10):
    response = rep.do_sentences([int(verbosity),tuple(answer.split())])
    # re-train because this makes it generate a new response
    rep.do_train("6 --noparagraphs data/%s/personality/all.txt"%candidate)
    responses.append(response)
  
  print("6: Scoring the markov generated responses")
  question = nltk.tokenize.word_tokenize(question)
  scored_responses = sourceContentSelector.getScoredVResponses(question, responses, candidate)
  top = max(scored_responses, key = lambda s: s[1])
  return top[0]


# The main script
if __name__ == '__main__':
  candidate = sys.argv[1]
  questions = open(sys.argv[2]).read().split("\n")
  verbosity = sys.argv[3]
  rep = repl.Repl()

  article = open("data/%s/personality/all.txt"%candidate).read()
  for question in questions:
    ans = answer(question, article, candidate)
    verbose = verbosify(question, candidate, verbosity, ans)
    print("7: And our final answer from %s is:"%candidate)
    print(ans+ " " + verbose)



