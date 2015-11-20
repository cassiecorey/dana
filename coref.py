# coref.py

# Useful tools which should be pre-installed
import os, sys, errno
import subprocess
import re
import itertools
import nltk
from nltk.stem import PorterStemmer
import bs4

# the set of pronouns, used for anaphora resolution
pronouns = set(["he", "she", "it", "its", "it's", "him", "her", "his","they",
                "their","we", "our","i","you","your","my","mine","yours","ours"])

resolved_articles = {}

# Runs coreference resolution on the article using arkref.
def process(path_to_article):
  original_path = path_to_article
  try:
    if path_to_article in resolved_articles:
      return resolved_articles[path_to_article]
    # arkref_out = open("arkref_out.txt", "w")
    fh = open("NUL","w")
    subprocess.call(["./arkref.sh", "-input", path_to_article], stdout = fh, stderr = fh)
    fh.close()

    tagged_article = open(path_to_article.replace("txt", "tagged")).read()
    tagged_article = "<root>"+tagged_article+"</root>" # trick arkref into doing entire doc
    soup = bs4.BeautifulSoup(tagged_article, "html.parser").root
    for entity in soup.find_all(True):
      if entity.string != None and entity.string.strip().lower() in pronouns:
        antecedent_id = entity["entityid"].split("_")[0]
        antecedent = soup.find(mentionid=antecedent_id)
        antecedent = str(antecedent).split(">", 1)[1].split("<", 1)[0]
        #string = re.sub('<.*?>',' ',str(antecedent))
        #tok = nltk.word_tokenize(string)
        #ants = [(x,y) for x,y in nltk.pos_tag(tok) if y in {'NNP','NN'}]
        entity.string.replace_with(antecedent)
    resolved = re.sub("<.*?>", "", str(soup))
  except:
    resolved = open(original_path).read()

  resolved_articles[path_to_article] = resolved
  return resolved