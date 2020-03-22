# CV - JobPost Matcher

# About

# Getting Started

> install first [CSO-classifier](https://github.com/angelosalatino/cso-classifier)


+ *in a temporal folder*

```
git clone https://github.com/angelosalatino/cso-classifier.git
cd cso-classifier
(sudo) pip(3) install .
```

+ run the next code in a terminal or temporal file to setup the CSO-Classifier (just has to be done once)

```
import classifier.classifier as classifier
classifier.setup()
exit()
```

> install then [GMatch4py](https://github.com/Jacobe2169/GMatch4py)

+ *in a temporal folder*

```
git clone https://github.com/Jacobe2169/GMatch4py.git
cd GMatch4py
(sudo) pip(3) install .
```

> Download [GloVe](https://nlp.stanford.edu/projects/glove/) Embedding 

+ Wikipedia word2vec directly in this link: [http://nlp.stanford.edu/data/glove.6B.zip](http://nlp.stanford.edu/data/glove.6B.zip)

> Generate Culture Graph based on this paper: "[Organizational Culture & Employee Behavior](https://www.theseus.fi/bitstream/handle/10024/92815/LI_Tianya.pdf)" 

+ Just in case that it don't exist or a revision should be made. After creation, put inside the src/graphs folder

> Data science domain specific ontology is created with the help of protege (https://protege.stanford.edu/)

+ we modifed the code provided by CSO and implemented our ontology in order to create domain specific graph

> finally, download project and install our requirements:

```
git clone https://github.com/RudreshMishra/S5_CvParserMatcher.git
cd S5_CvParserMatcher
(sudo) pip(3) install r -requirements.txt
```

## Usage

> Locate the terminal in the **src** folder and type: 

*(inside **project_folder**/src/)*

```
python3 io_handler.py
```

Then, simply follow instructions :)

Example of Output: 

```
Hello!! :) 
Please, tell us what type of analysis you would like to do:
1. - OneToOneMatching (matches one CV to job posting from ids given)
2. - ManyToOneMatching (matches several CVs to a job posting from ids given)

To choose an option, simply write the number: 2

--- INPUTS ---
Now, please type inputs:
candidate_ids (write list of values comma separated) = '5e60f5895a90883323e38bbb','5e60f5895a90883323e38bbc'
job_id = 5e64cbef837ba015d90abc78

--- WEIGHTS ---
Finally, we need you to assign the weights you want to give for each of the study axes:
## Axes ## ( 1: Skills Match, 2: Domain Skills Match, 3: Culture Match, 4: Required Skills Match )

Assign a value between [0, 3] which will explain how much you're interested in each axe of study,
 => where { 0=Not interested, 1=little interested, 2=interested, 3=very interested }
* Separate the {len(axes)} values by a comma (ex: v1, v2, v3).
values (4 expected): 2,2,2,2

--- Thanks!, now, we'll start calculating ----
Computer Science Ontology loaded.
Model loaded.
Creating ontology pickle file from a copy of the CSO Ontology found in *something_adress*/cso.csv
Model loaded.

# ===================================
#   Loading word2Vec Model of 300 dimensions (it could take more than one minute)
# ===================================

- | #                                   | 553 Elapsed Time: 0:01:10
Computer Science Ontology loaded.
Model loaded.
Creating ontology pickle file from a copy of the CSO Ontology found in *something_adress*/cso.csv
Model loaded.
Computer Science Ontology loaded.
Model loaded.
Creating ontology pickle file from a copy of the CSO Ontology found in *something_adress*/cso.csv
Model loaded.

==========================

======== RESULT ==========
The next CVs were ignored completely due to Education Match considerations: 
[]
The classification of the CVs is the next one: 

1    0.832857
0    0.728012
Name: MRValues, dtype: float64
```





