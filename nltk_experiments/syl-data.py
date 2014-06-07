import os
import json
raw_data = open('1000.json').read()
data = json.loads(raw_data)['results'] 

#add subject field to data
for item in data: 
    item['subject'] = ''

subjectList = ['english', 'mathematics', 'chemistry', 'psychology', 'sociology', 'biology', 'physics', 'religion', 'philosophy', 'journalism', 'french', 'literature', 'astronomy', 'pe ', 'music', 'anthropology', 'spanish', 'political science', 'microeconomics', 'macroeconomics', 'computer science', 'economics', 'math ', 'latin', 'geology', 'history', 'physical education', 'film studies', 'mythology', 'public relations', 'greek', 'hist '] 

for item in data: 
    if item['text'] is not None: 
#        print item['text'][:30]
        item['text'] = item['text'].strip() 
        for subject in subjectList: 
            if subject in item['text'][:140].lower(): 
#                print('adding '+subject+' to item!')
                item['subject'] = subject
            else: 
                if 'eng' in item['filename'].lower(): 
                    item['subject'] = 'english'
                if 'math' in item['filename'].lower(): 
                    item['subject'] = 'mathematics'

unknowns = [] 
for item in data: 
    #handle aliases
    if item['subject'] == 'literature': 
        item['subject'] = 'english'
    if item['subject'] == 'math ': 
        item['subject'] = 'mathematics'
    if item['subject'] == 'pe ': 
        item['subject'] = 'physical education' 
    if item['subject'] == 'hist ': 
        item['subject'] = 'history'
    if item['subject'] == 'macroeconomics' or item['subject'] == 'microeconomics': 
        item['subject'] = 'economics'

    if item['subject'] == '': 
        unknowns.append(item) 
        data.remove(item) #remove all unknowns

#for unknown in unknowns[:100]: 
    #if unknown['text'] is not None: 
        #print unknown['text'][:60]

print "number of unknowns: "+str(len(unknowns)) 

def get_all_subfolder_names(foldername):
    subfolderList = [ x[1] for x in os.walk(foldername) ][0]
    return subfolderList

def get_all_filenames_in_folder(folderName):
    """ walk the folder contents and get the names of the individual file names """
    fileList = []
    w = os.walk(folderName)
    try:
        loc = w.next()
        while w:
            fileList.append(loc)
            loc = w.next()
    except Exception, E:
        print E
    return fileList[0][2]

folderName = 'text-files' 
newdata = [] 
## get all of the file names in the folder
subjects = get_all_subfolder_names(folderName)
for subj in subjects:
    fullFolderName = folderName + "/" + subj
    fileNames = get_all_filenames_in_folder(fullFolderName)
    ## some of the files are hidden and not what we want
    ## filter so that we only use .txt files
    txtFiles = filter(lambda x: ".txt" in x, fileNames)
    #print txtFiles
    ## now, move to that folder
    currentFilePath = os.path.abspath(".")
    os.chdir(currentFilePath + "/" + fullFolderName)
    #standardize subjects
    if subj == 'physical-education': 
        subj = 'physical education'
    if subj == 'political-science': 
        subj = 'policial science'
    if subj == 'math': 
        subj = 'mathematics' 
    for myFile in txtFiles:
        f = open(myFile, 'r')
        theText = "".join(f.readlines())
        data.append({'subject':subj, 'filename':myFile, 'text':theText})
    os.chdir(currentFilePath)
    #print data[-5:]

subjects = [] 
for item in data: 
    if item['subject'] not in subjects: 
        subjects.append(item['subject'])

print "Subjects: "
print subjects
print "Number of syllabi: "
print str(len(data))

with open('categorized-syllabi.json', 'w') as outfile: 
 json.dump(data, outfile)

