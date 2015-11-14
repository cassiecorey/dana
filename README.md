#DANA
A Q&A model for the 2016 presidential candidates

##Adding a candidate/dataset
###Data folder format
Use the following tree-structure when using your own data folder:
```
/data
└── candidate1
    ├── personality
    │   └── *.txt
    └── qa
        └── *.txt	
```

###To clean a data file of some common non ASCII characters:
```
$ sed -f clean_file file.txt > clean.txt
```