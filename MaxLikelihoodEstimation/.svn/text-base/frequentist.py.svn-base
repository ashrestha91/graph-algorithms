from math import log
import sys
import string

def predict(ham, mad, filename):
    print "loglikelihood for hamilton:",logLikelihood(ham,filename), "\nloglikelihood for madison:",logLikelihood(mad, filename)
    if(logLikelihood(ham, filename) > logLikelihood(mad, filename)):
        return "hamilton"
    else:
        return "madison"

def logLikelihood(logclassifier, filename):
    wordcount,_ = getWordCounts([filename])
    return sum( [wordcount[word] * logclassifier(word) for word in wordcount.iterkeys()] )

def getWordCounts(lst, gamma = 0):
    wordcounts = dict()
    totalwords = 0
    for filename in lst:
        f = open(filename, 'r')
        for ln in f.readlines():
            ln = ln.translate(string.maketrans("",""), string.punctuation).lower()
            for word in ln.split():
                word = stem(word)
                if(word in wordcounts):
                    wordcounts[word]+=1
                    totalwords+=1
                else:
                    wordcounts[word]=gamma+1
                    totalwords+=gamma+1
        f.close()
    return wordcounts, totalwords

dictionary = set()
def initializeDictionary():
    f=open('/usr/share/dict/words','r')
    for ln in f.readlines():
        dictionary.add(ln.strip())
    f.close()

def isword(word):  
    return ("".join( ["\n",word,"\n"]) in dictionary)

#remove 's' if appropriate
def stem(word):
    if word[-1] == 's' and isword(word[:-1]):
        return word[:-1]
    return word

#returns log classifier
def filesToLogClassifier(lst, gamma, remove_words=0):
    wordcounts, totalwords = getWordCounts(lst, gamma)
     #get rid of words that are very common
    if remove_words > 0:
        for word in sorted(wordcounts.iterkeys(),key = (lambda word: wordcounts[word]))[-remove_words:]:
            totalwords -= wordcounts[word]-gamma
            wordcounts[word] = gamma 
    for word in wordcounts.iterkeys():
        wordcounts[word] = log(wordcounts[word]) - log(totalwords)
    return (lambda x: wordcounts[x] if x in wordcounts else log(gamma) - log(totalwords))

def test(mclassifier, hclassifier):
    testdata =   [ "".join( ["./federalist/unknown" ,str(i),".txt"] )
                                        for i in range(1,12) ]
    for filename in testdata:
        print filename,":\n",predict(hclassifier, mclassifier, filename),"\n"

def cross_validation(mad, ham, gamma, remove_words = 0):
    count = 0
    fullham = filesToLogClassifier(ham, gamma, remove_words)
    for filename in mad:
        print "excluding",filename,": "
        curmad = filesToLogClassifier( [fname for fname in mad if fname != filename ] , gamma, remove_words)
        prediction = predict(fullham, curmad, filename)         
        print prediction,":",prediction == "madison","\n"
        if(prediction == "madison"):
            count+=1

    fullmad = filesToLogClassifier(mad, gamma, remove_words)
    for filename in ham:
        print "excluding",filename,": "
        curham = filesToLogClassifier( [fname for fname in ham if fname != filename ] , gamma, remove_words)
        prediction = predict(curham, fullmad, filename)
        print prediction,":",prediction == "hamilton","\n"
        if(prediction == "hamilton"):
            count+=1
        
    return count/float(30)
    

def main():
    madison_training =   [ "".join( ["./federalist/madison" ,str(i),".txt" ] )
                                        for i in range(1,16) ]
    hamilton_training =  [ "".join( ["./federalist/hamilton",str(i),".txt" ] )
                                        for i in range(1,16) ] 
    initializeDictionary()

    gamma = 2
    remove_words = 6
    mc = filesToLogClassifier(madison_training, gamma, remove_words)
    hc = filesToLogClassifier(hamilton_training, gamma, remove_words)
    test(mc,hc)#run classifiers on test data
    
    """
    #test number of words to remove
    for i in range(0,20):
        print i,": ", cross_validation(madison_training, hamilton_training, gamma, remove_words = i)
    """
   
    """
    #tested gamma values via cross-validation for 1-100, and got highest value, which was 2. 
    #Since this got perfect accuracy during training, no other methods were tested
    gamma = float(sys.argv[1])
    cv_list = []
    f = open('cv-'+str(gamma), 'w')    
    cv_list.append(cross_validation(madison_training, hamilton_training, gamma,remove_words))
    f.close()
    """

    #cvgamma = sorted([ (cross_validation(madison_training, hamilton_training, gamma,remove_words),gamma*.25) 
    #                                                                                     for gamma in range(1,40) ], reverse=True)[0]
    #print cvgamma                    

if __name__ == "__main__":
    main()

