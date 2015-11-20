#Timeline

- [] Complete Data Collection and Annotation
- [] Convert all to python3
- [] Get Pickle Working

use `markov.load` and `markov.dump` for answer/ask pickle too

- [] Make Answers Verbose

Change `rep.do_tokens` to return string instead of printing...or just call it afterwards
```
import repl
rep = repl.Repl()
rep.do_train("3 --noparagraphs ./../data/candidate/personality/*")
rep.do_tokens("50")
```
Add seed to verbosity....way in the future

- [] Set up Pre-Processing
- [] Implement Question Train/Test
- [] Create UI
- [] Format Response Structure
- [] Allow Candidate Specification

change `python ask.py article.txt num_questions` to `python ask.py candidate num_questions`

- [] Gather Human Accuracy Ratings
- [] Fine Tuning Response Accuracies