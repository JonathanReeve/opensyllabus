import json
import os
import json
raw_data = open('categorized-syllabi.json').read()
data = json.loads(raw_data)

subjectList = ['english', 'mathematics', 'chemistry', 'psychology', 'sociology', 'biology', 'physics', 'religion', 'philosophy', 'journalism', 'french', 'literature', 'astronomy', 'pe ', 'music', 'art', 'anthropology', 'spanish', 'political science', 'microeconomics', 'macroeconomics', 'computer science', 'economics', 'math ', 'latin', 'geology', 'history', 'physical education', 'film studies', 'mythology', 'public relations', 'greek', 'hist '] 

bySubject={}
for item in data: 
    subj = item['subject'] 
    if item['text'] is not None: 
        if subj not in bySubject: 
            bySubject[subj] = item['text'] 
        else: 
            bySubject[subj] += item['text'] 

print bySubject.keys()
print bySubject['art'][:100]

import nltk

tokens={} 
for subject in bySubject: 
    tokens[subject] = nltk.word_tokenize(bySubject[subject]) 

texts = {} 
for subject in tokens: 
    try: 
        texts[subject] = nltk.Text(tokens[subject])
    except:
        print "Error!" 

collocations = {} 
for subject in texts: 
    print "Subject: "+subject
    collocations[subject] = texts[subject].collocations()
    print collocations[subject] 

