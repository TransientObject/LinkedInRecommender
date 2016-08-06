#Refer multilabelstack for working code

import stackexchange
import urllib2
import sys
import time
from stackexchange import Sort, DESC
from os.path import expanduser, exists, join
from os import makedirs, environ, path
import tarfile
import pprint

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

def addQuesDirectSearch(tar, skill): 
    
    site = stackexchange.Site(stackexchange.StackOverflow, 'CXRSlQ0gwe7r1lOU6taZ6A((')
    site.be_inclusive()
    
    if not exists('20news-bydate-train' + '\\' + skill + '$1'):
        makedirs('20news-bydate-train' + '\\' + skill + '$1')
    if not exists('20news-bydate-test' + '\\' + skill + '$1'):
        makedirs('20news-bydate-test' + '\\' + skill + '$1') 

    f = open('20news-bydate-train' + '\\' + skill + '$1\\' + skill + '.txt', 'w')         
    f.truncate()    
    f2 = open('20news-bydate-test' + '\\' + skill + '$1\\' + skill + '.txt', 'w')         
    f2.truncate()   
    
    while True:
        try:
            all_questions = site.search(intitle=skill, tagged=skill, sorted=Sort.Views, order=DESC)                  
            all_questionstitle = site.search(intitle=skill, sorted=Sort.Views, order=DESC) 
            break
        except urllib2.HTTPError:
            print 'Error:' + str(sys.exc_info())   
            time.sleep(20)  
        except:
            print 'Error:' + str(sys.exc_info())                 
            f.close()  
            f2.close()            
            return
        
    i = 1      
    try:
        for question in all_questions:      
            print i, str(question.title).encode('ascii', 'ignore')                 
            f.write(str(question.title).encode('ascii', 'ignore') + '\n')    
            f2.write(str(question.title).encode('ascii', 'ignore') + '\n')       
            i = i + 1   
            if i > 1000:
                break
    except:
        pass   
        
    i = 1      
    try:
        for question in all_questionstitle:      
            print i, str(question.title).encode('ascii', 'ignore')                 
            f.write(str(question.title).encode('ascii', 'ignore') + '\n')    
            f2.write(str(question.title).encode('ascii', 'ignore') + '\n')       
            i = i + 1   
            if i > 2000:
                break
    except:
        pass 
    
    f.close()
    f2.close()
    tar.add(f.name)   
    tar.add(f2.name) 
    return

def addQuesBySynonyms(tar, skill):
    site = stackexchange.Site(stackexchange.StackOverflow, 'CXRSlQ0gwe7r1lOU6taZ6A((')
    site.be_inclusive()
    
    if not exists('20news-bydate-train' + '\\' + skill + '$2'):
        makedirs('20news-bydate-train' + '\\' + skill + '$2')
    if not exists('20news-bydate-test' + '\\' + skill + '$2'):
        makedirs('20news-bydate-test' + '\\' + skill + '$2') 

    f = open('20news-bydate-train' + '\\' + skill + '$2\\' + skill + '.txt', 'w')         
    f.truncate()    
    f2 = open('20news-bydate-test' + '\\' + skill + '$2\\' + skill + '.txt', 'w')         
    f2.truncate() 
    
    while True:
        try:
            tags = site.all_tags(inname=skill)
            break
        except urllib2.HTTPError:
            time.sleep(5) 
        except:
            break
        
        tc = 1
        for tag in tags:
                        
            while True:
                try:
                    all_questions = site.search(intitle=skill, tagged=tag, sorted=Sort.Views, order=DESC) 
                    break
                except urllib2.HTTPError:
                    print 'Error:' + str(sys.exc_info())   
                    time.sleep(20)  
                except:
                    print 'Error:' + str(sys.exc_info())                 
                    break
            
            i = 1      
            try:
                for question in all_questions:      
                    print i, str(question.title).encode('ascii', 'ignore')                 
                    f.write(str(question.title).encode('ascii', 'ignore') + '\n')    
                    f2.write(str(question.title).encode('ascii', 'ignore') + '\n')       
                    i = i + 1   
                    if i > 20:
                        break
            except:
                pass
            tc = tc + 1
            if(tc > 20):
                break 
            
    tar.add(f.name)   
    tar.add(f2.name) 
    f.close()
    f2.close()
    return

def addQuesByRelatedTerms(tar, skill):
    site = stackexchange.Site(stackexchange.StackOverflow, 'CXRSlQ0gwe7r1lOU6taZ6A((')
    site.be_inclusive()
    
    if not exists('20news-bydate-train' + '\\' + skill + '$3'):
        makedirs('20news-bydate-train' + '\\' + skill + '$3')
    if not exists('20news-bydate-test' + '\\' + skill + '$3'):
        makedirs('20news-bydate-test' + '\\' + skill + '$3')  

    f = open('20news-bydate-train' + '\\' + skill + '$3\\' + skill + '.txt', 'w')         
    f.truncate()    
    f2 = open('20news-bydate-test' + '\\' + skill + '$3\\' + skill + '.txt', 'w')         
    f2.truncate() 
    
    empty = dict()   
    while True:
        try:
            jsonresp = site._request('/tags/' + skill + '/related', empty)
            break
        except urllib2.HTTPError:        
            time.sleep(5) 
        except:        
            break
    try:
        items = jsonresp['items']
        tc = 1
        for item in items:
            tag = item['name']
            
            while True:
                try:
                    all_questions = site.search(intitle=skill, tagged=tag, sorted=Sort.Views, order=DESC) 
                    break
                except urllib2.HTTPError:
                    print 'Error:' + str(sys.exc_info())   
                    time.sleep(20)  
                except:
                    print 'Error:' + str(sys.exc_info())                 
                    break
            
            i = 1      
            try:
                for question in all_questions:      
                    print i, str(question.title).encode('ascii', 'ignore')                 
                    f.write(str(question.title).encode('ascii', 'ignore') + '\n')    
                    f2.write(str(question.title).encode('ascii', 'ignore') + '\n')       
                    i = i + 1   
                    if i > 20:
                        break
            except:
                pass
            tc = tc + 1
            if(tc > 20):
                break     
    except:
        pass
    
    tar.add(f.name)   
    tar.add(f2.name) 
    f.close()
    f2.close()
    return

def load():   
    
    skillsdict = dict([(u'data structures', 107), (u'algorithms', 98), (u'programming', 73), (u'microsoft office', 63), (u'software engineering', 52), (u'core java', 48), (u'distributed systems', 44), (u'machine learning', 41), (u'operating systems', 36), (u'ruby on rails', 35), (u'linux', 76), (u'xml', 39), (u'mysql', 67), (u'unix', 31), (u'perl', 35), (u'html', 88), (u'python', 71), (u'java', 140), (u'c#', 41), (u'matlab', 70), (u'jquery', 33), (u'eclipse', 43), (u'c', 185), (u'eclipse', 43), (u'javascript', 96), (u'c++', 186), (u'css', 38), (u'sql', 104), (u'oracle', 30), (u'jsp', 50), (u'php', 56)])
    
    data_home = environ.get('SCIKIT_LEARN_DATA', join('~', 'scikit_learn_data'))
    data_home = expanduser(data_home) + '\\20news_home'
    if not exists(data_home):
        makedirs(data_home)        
    
    tar = tarfile.open(data_home + '\\20news-bydate.tar.gz', "w:gz")
    for skill in skillsdict.iterkeys():        
        skill = skill.encode('ascii', 'ignore')          
            
        addQuesDirectSearch(tar, skill)
        addQuesBySynonyms(tar, skill)
        addQuesByRelatedTerms(tar, skill)        
            
    tar.close()
 
def query(userskillset):

    fpath = expanduser(environ.get('SCIKIT_LEARN_DATA', join('~', 'scikit_learn_data') + '\\20news-bydate.pkz'))
    
    if(path.isfile(fpath) == False):    
        load()
    
    categories = ['programming$1', 'linux$1', 'unix$1', 'mysql$1', 'distributed systems$1', 'xml$1', 'java$1', 'perl$1', 'python$1', 'html$1', 'matlab$1', 'operating systems$1', 'c#$1', 'javascript$1', 'data structures$1', 'jsp$1', 'sql$1', 'php$1', 'jquery$1', 'c$1', 'software engineering$1', 'eclipse$1', 'ruby on rails$1', 'c++$1', 'machine learning$1', 'algorithms$1', 'css$1', 'core java$1', 'oracle$1', 'microsoft office$1',
                  'programming$2', 'linux$2', 'unix$2', 'mysql$2', 'distributed systems$2', 'xml$2', 'java$2', 'perl$2', 'python$2', 'html$2', 'matlab$2', 'operating systems$2', 'c#$2', 'javascript$2', 'data structures$2', 'jsp$2', 'sql$2', 'php$2', 'jquery$2', 'c$2', 'software engineering$2', 'eclipse$2', 'ruby on rails$2', 'c++$2', 'machine learning$2', 'algorithms$2', 'css$2', 'core java$2', 'oracle$2', 'microsoft office$2',
                  'programming$3', 'linux$3', 'unix$3', 'mysql$3', 'distributed systems$3', 'xml$3', 'java$3', 'perl$3', 'python$3', 'html$3', 'matlab$3', 'operating systems$3', 'c#$3', 'javascript$3', 'data structures$3', 'jsp$3', 'sql$3', 'php$3', 'jquery$3', 'c$3', 'software engineering$3', 'eclipse$3', 'ruby on rails$3', 'c++$3', 'machine learning$3', 'algorithms$3', 'css$3', 'core java$3', 'oracle$3', 'microsoft office$3']
    
    twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
      
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(twenty_train.data)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    
    clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
    
    site = stackexchange.Site(stackexchange.StackOverflow, 'CXRSlQ0gwe7r1lOU6taZ6A((')
    site.be_inclusive()
    
    docs_new = dict()  
    
    
    while True:
        try:
            all_questions = site.recent_questions(sorted=Sort.Votes, order=DESC)              
            break
        except urllib2.HTTPError:
            print 'Error:' + str(sys.exc_info())   
            time.sleep(20)  
        except:
            print 'Error:' + str(sys.exc_info())  
            return
          
    
    
    try:
        i = 1
        for q in all_questions:         
            docs_new[str(q.title).encode('ascii', 'ignore')] = q            
            i = i + 1           
            if(i > 1000):                
                break
            
    except:
        pass 
    
    
    
    
    
    X_new_counts = count_vect.transform(docs_new.keys())
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    
    predicted = clf.predict(X_new_tfidf)
    
    dict1 = dict()
    dict2 = dict()
    dict3 = dict()
    
    
    i = 0
    j = 0
    k = 0
    ic = 0
    jc = 0
    kc = 0
    for doc, category in zip(docs_new.keys(), predicted):
        
        q = docs_new[doc]
        skill = twenty_train.target_names[category].translate(None, '$123')   
        category = twenty_train.target_names[category].split('$')[-1] 
        
        innerdict = dict()
        
        
        if(userskillset.__contains__(skill) and category == '1'):
             
            innerdict['title'] = q.title 
            innerdict['skill'] = skill
            innerdict['type'] = 'direct'
            innerdict['score'] = q.score
            innerdict['view_count'] = q.view_count
            innerdict['url'] = q.url  
            innerdict['tags'] = str(q.tags)
            i = i + 1
            dict1[i] = innerdict
            if(q.tags.__contains__(skill)):
                ic = ic + 1
        
            
            
        if(userskillset.__contains__(skill) and category == '2'):
             
            innerdict['title'] = q.title 
            innerdict['skill'] = skill
            innerdict['type'] = 'synonym'
            innerdict['score'] = q.score
            innerdict['view_count'] = q.view_count
            innerdict['url'] = q.url 
            innerdict['tags'] = str(q.tags)
            j = j + 1 
            dict2[j] = innerdict
            if(q.tags.__contains__(skill)):
                jc = jc + 1
            
            
        if(userskillset.__contains__(skill) and category == '3'):
             
            innerdict['title'] = q.title 
            innerdict['skill'] = skill
            innerdict['type'] = 'related'
            innerdict['score'] = q.score
            innerdict['view_count'] = q.view_count
            innerdict['url'] = q.url 
            innerdict['tags'] = str(q.tags)
            k = k + 1 
            dict3[k] = innerdict
            if(q.tags.__contains__(skill)):
                kc = kc + 1
                
    jsondict = dict(dict1.items() + dict2.items()+dict3.items())    
    return jsondict
  
skills = ['c', 'c++', 'java', 'data structures', 'algorithms']
pprint.pprint(query(skills))
