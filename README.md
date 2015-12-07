#DANA
A Q&A model for the 2016 presidential candidates

##About
###Sources
This model combines code from these other GitHub repos:

[arkref](https://github.com/brendano/arkref)

[markov](https://github.com/barrucadu/markov)

[NLP-Project](https://github.com/ryhan/NLP-project)

The goal is to create a program that can be used to ask questions directed at one of four presidential candidates – Donald Trump, Ben Carson, Hillary Clinton, or Bernie Sanders – and respond in a way that shares some resemblance with how the candidate would realistically respond.

##Using DANA
###Install
You can clone this repo or download the zip and unpack it.

###Run
####Answer
```
$ python answer.py candidate questions.txt
```


##Data
###Directory Structure
Data folders should be formatted using the structure below:
```
/data
└── candidate
    ├── personality
    │   └── *.txt
    └── qa
        └── *.txt	
```

###File Format
QA files should be formated with questions and answers each on separate lines and not spanning more than one line (no '\n' except between question and answer). They should also not have any unneccessary '\n' anywhere (at the end for example) as this might skew the results of ```data_stats```.

###To clean a file of some common non ASCII characters:
```
$ sed -i.bak -f clean_file file.txt
```
The original file will be saved as file.txt.bak. If cleaning was successful you can call
```
$ rm file.txt.bak
```
to delete the original. 

If you're still encountering non-ASCII errors after running the above command, you might want to open your data file in Sublime (or some other text editor) and search for non-ASCII characters using find with the following regex:
```
[^\x00-\x7F]
```
If you find non-ASCII characters that aren't already in `clean_file` feel free to add them using the format:
```
s/\char/\replacement/g
```
If you encounter
```
sed: RE error: illegal byte sequence
```
try running
```
$ unset LANG
```

###Gathering Statistics
```
$ data_stats /path/to/data
```
Will create or update a file named data_stats.txt containing:
```
candidate
personality files: n
word count: n
question count: n
average question length: n
average answer length: n
```
for each candidate in your data folder.