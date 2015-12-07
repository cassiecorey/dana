#Timeline

- [ ] **Complete Data Collection and Annotation**
- [x] **Convert all to python3**

    used `2to3 -w file.py` on everything

    created an anaconda deprecation warning that can be ignored: 
    
    `DeprecationWarning: inspect.getargspec() is deprecated, use inspect.signature() instead`

- [x] **Get Pickle Working**

    sourceContentSelector.getScoredSentences() was taking the longest so this uses pickle to save scored sentences.    

- [x] **Make Answers Verbose**

    Change `rep.do_tokens` to return string instead of printing...or just call it afterwards
    ```
    import repl
    rep = repl.Repl()
    rep.do_train("3 --noparagraphs ./../data/candidate/personality/*")
    rep.do_tokens("50")
    ```
    Take 100 ```do_sentences(verbosity + prefix)```, score them on proximity and return the most likely match.

- [ ] **Set up Pre-Processing**
- [ ] **Implement Question Train/Test**
- [ ] **Create UI**
- [ ] **Format Response Structure**
- [x] **Allow Candidate Specification**

    change `python ask.py article.txt num_questions` to `python ask.py candidate num_questions`

- [ ] **Gather Human Accuracy Ratings**
- [ ] **Fine Tuning Response Accuracies**
