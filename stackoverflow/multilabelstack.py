from os import makedirs, environ, path
import os
from os.path import expanduser, exists, join
import sys
import time
import urllib2

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from stackexchange import Sort, DESC
import stackexchange


def addQuesDirectSearch(data_home, skill): 
    
    site = stackexchange.Site(stackexchange.StackOverflow, 'CXRSlQ0gwe7r1lOU6taZ6A((')
    site.be_inclusive()
    
    mskill = skill.replace(' ', '-')
    all_questions=list()
    while True:
        try:
            all_questions = site.search(intitle=skill, tagged=mskill + ';' + skill, sorted=Sort.Views, order=DESC)   
            break
        except urllib2.HTTPError:
            print 'Error:' + str(sys.exc_info())   
            time.sleep(20)  
        except:
            print 'Error:' + str(sys.exc_info())  
            return
        
    i = 1      
    try:
        for question in all_questions:      
            #print i, str(question.title).encode('ascii', 'ignore')    
            tags = list()
            for tag in question.tags:
                tags.append(tag.encode('ascii', 'ignore'))  
            #print tags 
            if not exists(data_home + '/' + str(tags)):
                makedirs(data_home + '/' + str(tags))  
            f = open(data_home + '/' + str(tags) + '/' + str(tags) + '.txt', 'w')        
            f.write(str(question.title).encode('ascii', 'ignore') + '\n')    
            f.close()     
            i = i + 1   
            if i > 10:
                break
    except:
        pass   
        
    
    return

def addQuesTitleSearch(data_home, skill): 
    
    site = stackexchange.Site(stackexchange.StackOverflow, 'CXRSlQ0gwe7r1lOU6taZ6A((')
    site.be_inclusive()
    all_questions=list()
    while True:
        try:
            all_questions = site.search(intitle=skill, sorted=Sort.Views, order=DESC)   
            break
        except urllib2.HTTPError:
            print 'Error:' + str(sys.exc_info())   
            time.sleep(20)  
        except:
            print 'Error:' + str(sys.exc_info())  
            return
        
    i = 1      
    try:
        for question in all_questions:      
            #print i, str(question.title).encode('ascii', 'ignore')    
            tags = list()
            tags.append(skill)
            #print tags 
            if not exists(data_home + '/' + str(tags)):
                makedirs(data_home + '/' + str(tags))  
            f = open(data_home + '/' + str(tags) + '/' + str(tags) + '.txt', 'w')        
            f.write(str(question.title).encode('ascii', 'ignore') + '\n')    
            f.close()     
            i = i + 1   
            if i > 10:
                break
    except:
        pass   
        
    
    return

def addQuesBySynonyms(data_home, skill):
    site = stackexchange.Site(stackexchange.StackOverflow, 'CXRSlQ0gwe7r1lOU6taZ6A((')
    site.be_inclusive()
    
    mskill = skill.replace(' ', '-')
    all_tags=list()
    while True:
        try:
            all_tags = site.all_tags(inname=mskill)
            break
        except urllib2.HTTPError:
            time.sleep(5) 
        except:
            return
        
        tc = 1
        try:
            for tag in all_tags:
                all_questions=list()            
                while True:
                    try:
                        all_questions = site.search(intitle=skill, tagged=tag, sorted=Sort.Views, order=DESC) 
                        break
                    except urllib2.HTTPError:
                        print 'Error:' + str(sys.exc_info())   
                        time.sleep(20)  
                    except:
                        print 'Error:' + str(sys.exc_info())                 
                        return
                
                i = 1      
                try:
                    for question in all_questions:      
                        #print i, str(question.title).encode('ascii', 'ignore')                 
                        tags = list()
                        for t in question.tags:
                            tags.append(t.encode('ascii', 'ignore'))  
                        if(~tags.__contains__(skill)):     
                            tags.append(skill)
                        #print tags
                        
                        if not exists(data_home + '/' + str(tags)):
                            makedirs(data_home + '/' + str(tags))  
                        f = open(data_home + '/' + str(tags) + '/' + str(tags) + '.txt', 'w')
                        f.write(str(question.title).encode('ascii', 'ignore') + '\n')    
                        f.close()     
                        i = i + 1   
                        if i > 2:
                            break
                except:
                    pass
                tc = tc + 1
                if(tc > 10):
                    break 
        except:
            pass
            
    
    return

def addQuesByRelatedTerms(data_home, skill):
    site = stackexchange.Site(stackexchange.StackOverflow, 'CXRSlQ0gwe7r1lOU6taZ6A((')
    site.be_inclusive()
        
    mskill = skill.replace(' ', '-')
    
    empty = dict()   
    while True:
        try:
            jsonresp = site._request('/tags/' + mskill + '/related', empty)
            break
        except urllib2.HTTPError:        
            time.sleep(5) 
        except:        
            return
    try:
        items = jsonresp['items']
        tc = 1
        for item in items:
            tag = item['name']
            
            all_questions=list()
            while True:
                try:
                    all_questions = site.search(intitle=skill, tagged=tag, sorted=Sort.Views, order=DESC) 
                    break
                except urllib2.HTTPError:
                    print 'Error:' + str(sys.exc_info())   
                    time.sleep(20)  
                except:
                    print 'Error:' + str(sys.exc_info())                 
                    return
            
            i = 1      
            try:
                for question in all_questions:      
                    #print i, str(question.title).encode('ascii', 'ignore')                 
                    tags = list()
                    for tag in question.tags:
                        tags.append(tag.encode('ascii', 'ignore'))  
                         
                    if(~tags.__contains__(skill)):     
                        tags.append(skill)
                    #print tags
                    if not exists(data_home + '/' + str(tags)):
                        makedirs(data_home + '/' + str(tags))  
                    f = open(data_home + '/' + str(tags) + '/' + str(tags) + '.txt', 'w')        
                    f.write(str(question.title).encode('ascii', 'ignore') + '\n')    
                    f.close()      
                    i = i + 1   
                    if i > 2:
                        break
            except:
                pass
            tc = tc + 1
            if(tc > 10):
                break     
    except:
        pass
    
    
    return

def load():   
    
    allskills = dict([(u'c++', 187), (u'c', 185), (u'java', 140), (u'data structures', 108), (u'sql', 104), (u'algorithms', 99), (u'javascript', 96), (u'html', 88), (u'linux', 76), (u'programming', 74), (u'python', 72), (u'matlab', 70), (u'mysql', 68), (u'microsoft office', 63), (u'php', 56), (u'software engineering', 54), (u'jsp', 50), (u'core java', 48), (u'distributed systems', 46), (u'eclipse', 43), (u'c#', 42), (u'machine learning', 41), (u'xml', 40), (u'css', 38), (u'operating systems', 37), (u'ruby on rails', 36), (u'perl', 35), (u'jquery', 34), (u'unix', 31), (u'oracle', 30), (u'ruby', 29), (u'computer architecture', 28), (u'software development', 28), (u'databases', 28), (u'agile methodologies', 27), (u'windows', 27), (u'web development', 27), (u'shell scripting', 26), (u'embedded systems', 26), (u'microsoft excel', 26), (u'verilog', 24), (u'data analysis', 24), (u'artificial intelligence', 24), (u'cloud computing', 23), (u'pl/sql', 23), (u'web services', 23), (u'microsoft sql server', 23), (u'java enterprise edition', 22), (u'requirements analysis', 21), (u'data mining', 20), (u'engineering', 20), (u'project management', 20), (u'web applications', 19), (u'management', 19), (u'analysis of algorithms', 18), (u'business intelligence', 18), (u'ajax', 18), (u'business analysis', 18), (u'spring', 18), (u'android', 18), (u'analytics', 17), (u'computer networks', 17), (u'autocad', 17), (u'unix shell scripting', 16), (u'leadership', 16), (u'photoshop', 16), (u'hadoop', 16), (u'visual studio', 15), (u'git', 15), (u'product management', 14), (u'business strategy', 14), (u'data warehousing', 14), (u'market research', 14), (u'.net', 14), (u'vhdl', 13), (u'testing', 13), (u'ansys', 13), (u'pro engineer', 13), (u'information retrieval', 13), (u'object oriented programming', 13), (u'teamwork', 13), (u'software project management', 12), (u'oop', 12), (u'android development', 12), (u'business development', 12), (u'team management', 12), (u'recruiting', 11), (u'technical recruiting', 11), (u'object oriented design', 11), (u'problem solving', 11), (u'team leadership', 11), (u'powerpoint', 11), (u'network security', 10), (u'screening', 10), (u'product development', 10), (u'manufacturing', 10), (u'computer science', 10), (u'web 2.0', 10), (u'servlets', 10), (u'rest', 10), (u'entrepreneurship', 10), (u'supply chain management', 10), (u'research', 10), (u'sdlc', 10), (u'programming and data structures', 10), (u'networking', 10), (u'natural language processing', 9), (u'tcp/ip', 9), (u'marketing', 9), (u'html 5', 9), (u'image processing', 9), (u'microsoft word', 9), (u'amazon ec2', 9), (u'solidworks', 9), (u'visual basic', 9), (u'big data', 9), (u'statistics', 9), (u'scrum', 9), (u'sourcing', 9), (u'management consulting', 9), (u'asp.net', 9), (u'ms project', 9), (u'database design', 9), (u'database management systems', 9), (u'design and analysis of algorithms', 9), (u'screening resumes', 8), (u'internet recruiting', 8), (u'netbeans', 8), (u'sas', 8), (u'soa', 8), (u'amazon web services (aws)', 8), (u'hibernate', 8), (u'business analytics', 8), (u'latex', 8), (u'digital signal processing', 8), (u'information storage and retrieval', 8), (u'interviews', 8), (u'analysis', 8), (u'software design', 8), (u'linux kernel', 8), (u'talent acquisition', 8), (u'tcl', 8), (u'embedded c', 7), (u'web design', 7), (u'benefits negotiation', 7), (u'struts', 7), (u'financial analysis', 7), (u'agile', 7), (u'opencv', 7), (u'computer vision', 7), (u'user interface design', 7), (u'start-ups', 7), (u'commissioning', 7), (u'program management', 7), (u'mapreduce', 7), (u'mobile applications', 7), (u'cadence virtuoso', 7), (u'debugging', 7), (u'finite element analysis', 7), (u'strategy', 7), (u'device drivers', 7), (u'human resources', 7), (u'project engineering', 7), (u'computer communication and networks', 7), (u'ec2', 7), (u'advanced computer architecture', 7), (u'public speaking', 7), (u'wireless networking', 7), (u'e-commerce', 6), (u'strategic planning', 6), (u'web technology', 6), (u'salesforce.com', 6), (u'consulting', 6), (u'test driven development', 6), (u'principles of compiler design', 6), (u'embedded software', 6), (u'microcontrollers', 6), (u'sql server', 6), (u'corporate finance', 6), (u'ios development', 6), (u'opengl', 6), (u'vlsi', 6), (u'vlsi design', 6), (u'catia', 6), (u'talent management', 6), (u'crm', 6), (u'executive search', 6), (u'saas', 6), (u'advanced digital signal processing', 6), (u'mongodb', 6), (u'ubuntu', 6), (u'theory of computation', 6), (u'competitive analysis', 6), (u'soap', 6), (u'operating system', 6), (u'project planning', 6), (u'event management', 6), (u'optimization', 5), (u'process improvement', 5), (u'economics', 5), (u'database management system', 5), (u'requirements gathering', 5), (u'telecommunications', 5), (u'epc', 5), (u'digital electronics', 5), (u'gis', 5), (u'wireless networks', 5), (u'advanced operating systems', 5), (u'visio', 5), (u'power plants', 5), (u'digital integrated circuit design', 5), (u'r', 5), (u'computer communication and networking', 5), (u'robotics', 5), (u'subversion', 5), (u'parallel programming', 5), (u'gnu debugger', 5), (u'data communication and computer networks', 5), (u'algorithm design', 5), (u'object oriented analysis and design', 5), (u'grid computing', 5), (u'test automation', 5), (u'social media', 5), (u'theory of computability', 5), (u'modelsim', 5), (u'json', 5), (u'lean manufacturing', 5), (u'procurement', 5), (u'socket programming', 5), (u'enterprise software', 5), (u'fmea', 5), (u'microprocessor system design', 4), (u'teaching', 4), (u'agile project management', 4), (u'user experience', 4), (u'project coordination', 4), (u'electronic circuits', 4), (u'wireless communication', 4), (u'customer service', 4), (u'codeigniter', 4), (u'computer graphics', 4), (u'contract recruitment', 4), (u'uml', 4), (u'plc', 4), (u'design patterns', 4), (u'visual c++', 4), (u'creative writing', 4), (u'scada', 4), (u'digital communication', 4), (u'functional programming', 4), (u'simulink', 4), (u'linear programming', 4), (u'j2ee application development', 4), (u'selenium', 4), (u'internal combustion engines', 4), (u'cobol', 4), (u'digital marketing', 4), (u'college recruiting', 4), (u'temporary placement', 4), (u'data structures and algorithms', 4), (u'communication', 4), (u'spice', 4), (u'rtos', 4), (u'mpi', 4), (u'remote sensing', 4), (u'django', 4), (u'unix internals', 4), (u'it strategy', 4), (u'scalability', 4), (u'operations research', 4), (u'clearcase', 4), (u'scala', 4), (u'signals and systems', 4), (u'ns2', 4), (u'labview', 4), (u'it recruitment', 4), (u'wireshark', 4), (u'openmp', 4), (u'vba', 4), (u'oracle pl/sql development', 4), (u'automotive engineering', 4), (u'instrumentation', 4), (u'pspice', 4), (u'microprocessors and microcontrollers', 4), (u'advanced computer networks', 4), (u'process control', 4), (u'english', 4), (u'power generation', 4), (u'peoplesoft', 4), (u'cross-functional team leadership', 3), (u'compilers', 3), (u'statistical modeling', 3), (u'strength of materials', 3), (u'open source', 3), (u'erp', 3), (u'oracle e-business suite', 3), (u'cryptography and security', 3), (u'solar energy', 3), (u'network programming', 3), (u'advanced logic design', 3), (u'xampp', 3), (u'asic', 3), (u'recruitments', 3), (u'cryptography', 3), (u'strategic management', 3), (u'dreamweaver', 3), (u'ip', 3), (u'oracle sql', 3), (u'internet protocols and modeling', 3), (u'fpga', 3), (u'electrical engineering', 3), (u'excel', 3), (u'civil engineering', 3), (u'personnel management', 3), (u'css javascript', 3), (u'soft computing', 3), (u'vb.net', 3), (u'software testing', 3), (u'adobe creative suite', 3), (u'cplex', 3), (u'mobile networking', 3), (u'staffing services', 3), (u'arena simulation software', 3), (u'sharepoint', 3), (u'gd&t', 3), (u'training', 3), (u'mathematical modeling', 3), (u'business information security', 3), (u'applicant tracking systems', 3), (u'performance appraisal', 3), (u'sap r/3', 3), (u'systemverilog', 3), (u'assembly language', 3), (u'd3.js', 3), (u'b2b marketing', 3), (u'manufacturing engineering', 3), (u'ipv6', 3), (u'objective-c', 3), (u'employee engagement', 3), (u'systems analysis', 3), (u'computer and network security', 3), (u'systemc', 3), (u'medical electronics', 3), (u'energy', 3), (u'fluid dynamics', 3), (u'distributed processing systems', 3), (u'permanent placement', 3), (u'marketing strategy', 3), (u'test planning', 3), (u'network engineering', 3), (u'c# 4.0', 3), (u'minitab', 3), (u'j2ee', 3), (u'p&id', 3), (u'mobile communication', 3), (u'c/c++ stl', 3), (u'signal processing', 3), (u'product design', 3), (u'informatica', 3), (u'apache pig', 3), (u'dynamic programming', 3), (u'inventory control', 3), (u'quality assurance', 3), (u'junit', 3), (u'distribution theory', 3), (u'access', 3), (u'parallel computing', 3), (u'performance management', 3), (u'semantic web', 3), (u'c++ language', 3), (u'user acceptance testing', 3), (u'marketing research', 3), (u'multithreading', 3), (u'analysis and design of algorithms', 3), (u'kaizen', 3), (u'electronics', 3), (u'xilinx ise', 3), (u'marketing management', 3), (u'pre-sales', 3), (u'db2', 3), (u'hiring', 3), (u'node.js', 3), (u'survey of optimization', 3), (u'sas programming', 3), (u'mechanical engineering', 3), (u'x86 assembly', 3), (u'six sigma', 3), (u'automation', 3), (u'market analysis', 3), (u'perl script', 3), (u'dcs', 3), (u'construction', 3), (u'oracle applications', 3), (u'materials management', 3), (u'jquery mobile', 2), (u'circuit analysis', 2), (u'database management', 2), (u'preventive maintenance', 2), (u'probabilistic graphical models', 2), (u'swing', 2), (u'omap', 2), (u'communication theory', 2), (u'process automation', 2), (u'electrical machines', 2), (u'cadence', 2), (u'ethernet', 2), (u'online advertising', 2), (u'sap erp', 2), (u'embedded system design', 2), (u'rf', 2), (u'spatial databases', 2), (u'advanced networks security', 2), (u'hypermesh', 2), (u'weka', 2), (u'contract management', 2), (u'text mining', 2), (u'resource management', 2), (u'automotive', 2), (u'ns-2', 2), (u'dbms', 2), (u'social media marketing', 2), (u'dod', 2), (u'supply chain', 2), (u'linear integrated circuits', 2), (u'graph theory', 2), (u'event planning', 2), (u'cics', 2), (u'online social networking', 2), (u'advanced database technology', 2), (u'r&d', 2), (u'5s', 2), (u'peoplecode', 2), (u'information technology', 2), (u'ccna', 2), (u'hris', 2), (u'abaqus', 2), (u'higher education', 2), (u'simulations', 2), (u'advanced system analysis and design', 2), (u'web programming languages', 2), (u'sybase', 2), (u'advanced data management', 2), (u'flash', 2), (u'wcdma', 2), (u'decision support systems', 2), (u'microprocessors', 2), (u'employer branding', 2), (u'background checks', 2), (u'ssis', 2), (u'professional services', 2), (u'image synthesis', 2), (u'apache', 2), (u'security in computing', 2), (u'account management', 2), (u'statistics in bioinformatics', 2), (u'data management', 2), (u'business process', 2), (u'employee relations', 2), (u'twitter bootstrap', 2), (u'soc', 2), (u'rational rose enterprise edition', 2), (u'arcgis server', 2), (u'content development', 2), (u'process engineering', 2), (u'control theory', 2), (u'electronic devices and circuits', 2), (u'android sdk', 2), (u'jdbc', 2), (u'power electronics', 2), (u'business objects', 2), (u'website development', 2), (u'vlsi testing', 2), (u'google app engine', 2), (u'information storage and retrieval (ongoing)', 2), (u'sap', 2), (u'plc programming', 2), (u'email marketing', 2), (u'synopsys tools', 2), (u'combinatorics and graph theory', 2), (u'data modeling', 2), (u'mfc', 2), (u'ssl', 2), (u'sales and distribution management', 2), (u'location logistics of industrial facilities', 2), (u'rural marketing', 2), (u'outsourcing', 2), (u'wireless and mobile networks', 2), (u'data visualization', 2), (u'encryption', 2), (u'arcobjects', 2), (u'refinery', 2), (u'physical design', 2), (u'engineering mechanics', 2), (u'control systems', 2), (u'environmental engineering', 2), (u'nosql', 2), (u'performance testing', 2), (u'gdb', 2), (u'data science', 2), (u'imagej', 2), (u'power systems', 2), (u'spss', 2), (u'multicore architecture & parallel programming', 2), (u'cuda', 2), (u'lean thinking and lean manufacturing', 2), (u'outlook', 2), (u'high speed networks', 2), (u'computer security', 2), (u'multicore architecture and programming', 2), (u'navy', 2), (u'mathematics', 2), (u'oracle bpel', 2), (u'staff augmentation', 2), (u'interaction design', 2), (u'integrated circuit design', 2), (u'common lisp', 2), (u'system programming', 2), (u'consumer behavior', 2), (u'search', 2), (u'google adwords', 2), (u'event driven programming', 2), (u'web analytics', 2), (u'topics in database management systems', 2), (u'advanced system software', 2), (u'lean management', 2), (u'digital electronics and system design', 2), (u'advanced algorithms', 2), (u'sales & distribution management', 2), (u'nltk', 2), (u'brand management', 2), (u'2g', 2), (u'cadence spectre', 2), (u'computers', 2), (u'rex os', 2), (u'optical communication', 2), (u'weblogic', 2), (u'global sourcing', 2), (u'game theory', 2), (u'deferred compensation', 2), (u'operations management', 2), (u'mobile wireless networks', 2), (u'business process management', 2), (u'c programming', 2), (u'oracle sql developer', 2), (u'sem', 2), (u'quality center', 2), (u'mentoring', 2), (u'solr', 2), (u'statistics for management', 2), (u'primetime', 2), (u'customer satisfaction', 2), (u'recruitment advertising', 2), (u'internet technologies', 2), (u'pattern recognition', 2), (u'random processes', 2), (u'3d modeling', 2), (u'team building', 2), (u'integration', 2), (u'neural networks', 2), (u'probability for engineering decisions', 2), (u'static timing analysis', 2), (u'jcl', 2), (u'financial modeling', 2), (u'large scale systems', 2), (u'high performance computing', 2), (u'design of machine elements', 2), (u'hive', 2), (u'predictive analytics', 2), (u'service oriented architecture', 2), (u'organizational behaviour', 2), (u'services marketing', 2), (u'phonegap', 2), (u'3g', 2), (u'distributed computing', 2), (u'compiler design', 2), (u'hudson', 2), (u'embedded linux', 2), (u'information storage & retrieval', 2), (u'oracle 9i', 2), (u'photogrammetry', 2), (u'tableau', 2), (u'application architecture', 2), (u'hr consulting', 2), (u'professional ethics', 2), (u'vendor management', 2), (u'pattern analysis', 2), (u'lte', 2), (u'retail', 2), (u'visual programming', 2), (u'accounting concepts and procedures', 2), (u'linear algebra', 2), (u'systems engineering', 2), (u'win32 api', 2), (u'calculus', 2), (u'ooad', 2), (u'computer organisation', 2), (u'linear network analysis', 2), (u'real time systems', 2), (u'sales management', 2), (u'project estimation', 2), (u'qt', 2), (u'soapui', 2), (u'etl', 2), (u'gas turbines', 2), (u'construction management', 2), (u'human computer interaction', 2), (u'http', 2), (u'verification of digital systems', 2), (u'sun certified java programmer', 2), (u'command', 2), (u'thermodynamics', 2), (u'computer organization', 2), (u'government', 2), (u'gnu octave', 2), (u'industrial engineering', 2), (u'maven', 2), (u'circuit design', 2), (u'arcgis', 2), (u'automata theory', 2), (u'new hire orientations', 2), (u'snmp', 2), (u'lidar', 2), (u'business component design and development', 2), (u'pumps', 2), (u'tomcat', 2), (u'rtl design', 2), (u'cfd', 2), (u'differential equations', 1), (u'yahoo search marketing', 1), (u'electronics and communications', 1), (u'cisco networking', 1), (u'client server system', 1), (u'computer communications and networking', 1), (u'mechatronics engineering', 1), (u'content management', 1), (u'human centered computing', 1), (u'principles of programming languages', 1), (u'real-time and embedded systems', 1), (u'cytoscape', 1), (u'simplescalar', 1), (u'openmpi', 1), (u'easytrieve', 1), (u'computer networking', 1), (u'distributed database systems', 1), (u'manufacturing systems simulation', 1), (u'mainframe testing', 1), (u'introduction to risk and uncertainity', 1), (u'unity3d', 1), (u'assembly', 1), (u'engineering management', 1), (u'financial services', 1), (u'machine learning (ongoing)', 1), (u'integrated business promotion', 1), (u'numerical analysis', 1), (u'asp.net ajax', 1), (u'yacc', 1), (u'virtualization', 1), (u'models of supply chain management', 1), (u'microprocessor & its applications', 1), (u'debuggers', 1), (u'advanced storage systems', 1), (u'designing', 1), (u'software development life cycle', 1), (u'logistics & distributions management', 1), (u'operataing systems', 1), (u'solar and thermal energy conversion', 1), (u'snooker', 1), (u'military', 1), (u'prolog', 1), (u'water quality', 1), (u'sas enterprise miner', 1), (u'diameter', 1), (u'engineering economics & financial mgmt.', 1), (u'standards compliance', 1), (u'process planning and cost estimation', 1), (u'hyperion financial reporting studio', 1), (u'army', 1), (u'channel coding for communication', 1), (u'manufacturing planning and control', 1), (u'risk management', 1), (u'campaign management', 1), (u'information technology essentials', 1), (u'location logistics for industrial facilities', 1), (u'dsp programming and applications using blackfin processsor', 1), (u'jd edwards', 1), (u'computer architecture and organization', 1), (u'dragonwave', 1), (u'release managment', 1), (u'sap2000', 1), (u'jmp', 1), (u'energy efficiency', 1), (u'artificial intelligence and machine learning for engineering design', 1), (u'supply management', 1), (u'industrial ergonomics', 1), (u'vlsi physical design and automation', 1), (u'smtp', 1), (u'portfolio management', 1), (u'google website optimizer', 1), (u'xilinx impact', 1), (u'cloud computing iaas', 1), (u'revenue analysis', 1), (u'low-power design', 1), (u'dos,windows 2000,,xp,2007', 1), (u'big data systems studio', 1), (u'special operations', 1), (u'business planning', 1), (u'business alliances', 1), (u'actionscript', 1), (u'visual paradigm', 1), (u'revenue forecasting', 1), (u'statistical computations', 1), (u'modern control theory', 1), (u'webtrends analytics', 1), (u'lan', 1), (u'programming abstraction in energy aware computing', 1), (u'ojbect oriented programming concepts', 1), (u'introduction to control theory', 1), (u'dependency injection', 1), (u'fluid mechanics', 1), (u'ovm', 1), (u'3d sensors', 1), (u'electronics devices and circuits', 1), (u'wimax', 1), (u'android application development', 1), (u'operations', 1), (u'itil v3 foundations certified', 1), (u'intellectual property', 1), (u'advanced industrial instrumentation', 1), (u'upstream', 1), (u'directed studies in software defined networking', 1), (u'cisco ios', 1), (u'market structure', 1), (u'counterterrorism', 1), (u'graduate operating systems', 1), (u'hydraulics and pneumatics', 1), (u'machine learning(ongoing)', 1), (u'deterministic methods of operations research', 1), (u'file layouts', 1), (u'semiconductor device modeling and characterization for modern applications', 1), (u'rf ic design', 1), (u'advance wireless networks', 1), (u'joint military operations', 1), (u'descriptive analytics', 1), (u'business transformation', 1), (u'personal effectiveness', 1), (u'fileaid', 1), (u'odbc', 1), (u'embedded operating systems', 1), (u'hql', 1), (u'spatial analysis and modelling', 1), (u'contemporary manufacturing management', 1), (u'cartography', 1), (u'heterogeneous parallel programming', 1), (u'engineering computation', 1), (u'cascading', 1), (u'adobe target', 1), (u'process planning & cost estimation', 1), (u'quantitative aptitude', 1), (u'sockets', 1), (u'smo', 1), (u'design and analysis of computer algorithms', 1), (u'taleo', 1), (u'direct sales', 1), (u'pathloss', 1), (u'design and analysis of experiments', 1), (u'resume', 1), (u'advanced machine dynamics', 1), (u'high performance computing (parallel computing)', 1), (u'sensors', 1), (u'microsoft visual studio 2008', 1), (u'basics of animation', 1), (u'redline', 1), (u'multimedia databases and mining', 1), (u'mobile computing advanced wireless network', 1), (u'xilinx', 1), (u'adhoc and sensor networks', 1), (u'benchmarking', 1), (u'operational planning', 1), (u'robotics and automation technology', 1), (u'customization', 1), (u'construction safety', 1), (u'grads', 1), (u'probability and random processes', 1), (u'interfacing laboratory', 1), (u'program analysis', 1), (u'introduction to instrumentation engineering', 1), (u'advertising sales', 1), (u'operation systems', 1), (u'spring integration', 1), (u'global talent acquisition', 1), (u'windbg', 1), (u'dynatrace', 1), (u'ampl', 1), (u'meteorology', 1), (u'c, java programming', 1), (u'hacking', 1), (u'mems and nanotechnology', 1), (u'bridge', 1), (u'rad', 1), (u'@risk', 1), (u'functional genomics', 1), (u'link building', 1), (u'angularjs', 1), (u'mathematical techniques in engineering', 1), (u'digital system design', 1), (u'control systems design', 1), (u'concrete', 1), (u'firmware', 1), (u'design for manufacturing', 1), (u'information security & privacy', 1), (u'perforce', 1), (u'ugs nx5', 1), (u'xilinx identify debugger', 1), (u'web-based decision support systems', 1), (u'search engine', 1), (u'vector canalyzer', 1), (u'cisco certified network programmer', 1), (u'autoit', 1), (u'system software internals', 1), (u'time management', 1), (u'node b', 1), (u'gesture recognition', 1), (u'sensors and transducers', 1), (u'co- design of embedded systems', 1), (u'ocr', 1), (u'systems analysis, modelling and design', 1), (u'structural engineering', 1), (u'vehicle body engineering', 1), (u'data mining and warehousing', 1), (u'cloud environments', 1), (u'j2ee web services', 1), (u'high availability', 1), (u'iraf. programming languages : c', 1), (u'active directory', 1), (u'energy management', 1), (u'advanced network analysis', 1), (u'combustion', 1), (u'non traditional manufacturing processes', 1), (u'programming fundamentals', 1), (u'space systems', 1), (u'architecting software systems', 1), (u'numerical computing', 1), (u'sociology & global issues', 1), (u'intelligent user interface', 1), (u'omx', 1), (u'search advertising', 1), (u'media relations', 1), (u'affiliate marketing', 1), (u'security clearance', 1), (u'logic', 1), (u'com', 1), (u'sustainable operations', 1), (u'systems design', 1), (u'smart gwt', 1), (u'stakeholder management', 1), (u'oceanography', 1), (u'introduction to computer systems', 1), (u'environmental impact assessment', 1), (u'high computer architecture i', 1), (u'moral and political philosophy', 1), (u'programmable systems-on-a-chip', 1), (u'java programming', 1), (u'design and analysis of parallel algorithms', 1), (u'robolectric', 1), (u'website administration', 1), (u'reconnaissance', 1), (u'advanced database technologies', 1), (u'geospatial data analysis', 1), (u'models of software systems', 1), (u'ic', 1), (u'control logic', 1), (u'oracle reports', 1), (u'ccnp', 1), (u'methods of software systems', 1), (u'data interpretation', 1), (u'qgis', 1), (u'business intelligence and data mining', 1), (u'medical devices', 1), (u'reliability, maintenance and safety engineering', 1), (u'javascriptmvc', 1), (u'digital image processing', 1), (u'quantitative techniques in management', 1), (u'chip multiprocessor architecture', 1), (u'image analysis', 1), (u'testng', 1), (u'environmental science and engineering', 1), (u'materials', 1), (u'multimedia computing', 1), (u'netezza', 1), (u'sales channel', 1), (u'website promotion', 1), (u'psychometrics', 1), (u'product strategy', 1), (u'artificial intelligence and expert systems', 1), (u'metrology and quality assurance', 1), (u'resilient hardware systems', 1), (u'code generation', 1), (u'megastat', 1), (u'leed accredited', 1), (u'digital communication systems', 1), (u'rnc', 1), (u'logic design', 1), (u'mobile marketing', 1), (u'mip', 1), (u'search engine submission', 1), (u'social networking', 1), (u'ibm mainframe', 1), (u'high speed computer arithmetic', 1), (u'probability and statistics', 1), (u'responsive design', 1), (u'web content management', 1), (u'online marketing', 1), (u'windows 7', 1), (u'networking and communication', 1), (u'system virtualization', 1), (u'neural networks for machine learning', 1), (u'theory of database systems', 1), (u'embedded software development', 1), (u'introduction to optimization', 1), (u'trace32', 1), (u'reverse osmosis', 1), (u'graduate seminar', 1), (u'database managements systems', 1), (u'it transformation', 1), (u'pli', 1), (u'technology start-up', 1), (u'system-on-a-chip design', 1), (u'graduate computer architecture', 1), (u'joomla', 1), (u'principles of communication', 1), (u'microsoft office,open office', 1), (u'introduction to numerical analysis', 1), (u'e-business', 1), (u'dlp products  symantec  ,mcafee, trendmicro , checkpoint.......', 1), (u'intelligence analysis', 1), (u'entrepreneur', 1), (u'ppp', 1), (u'introduction to manufacturing', 1), (u'advanced database management', 1), (u'automotive aerodynamics', 1), (u'pro/engineer', 1), (u'wordpress', 1), (u'advance heat transfer', 1), (u'tcpdump', 1), (u'mining massive data sets', 1), (u'responsive web design', 1), (u'value engineering', 1), (u'foundations of advanced networking', 1), (u'aircraft engines', 1), (u'information systems project & program management', 1), (u'point cloud library', 1), (u'human factors', 1), (u'design for manufacturing and assembly', 1), (u'consumer package goods', 1), (u'cosmos', 1), (u'applied combustion and air pollution control', 1), (u'corporate information planning', 1), (u'jax-rs', 1), (u'rational rose', 1), (u'file systems', 1), (u'accounting', 1), (u'rf system design', 1), (u'management of information technology', 1), (u'3gpp', 1), (u'webos', 1), (u'hp service manager', 1), (u'jms', 1), (u'executive reporting', 1), (u'algorithms to architectures', 1), (u'sqr', 1), (u'dynamics of machinery', 1), (u'sociology', 1), (u'growth strategies', 1), (u'tivoli', 1), (u'corporate financial reporting and analysis', 1), (u'power plant engineering', 1), (u'backend development', 1), (u'mechanical analysis', 1), (u'mobile interaction design', 1), (u'saucelabs', 1), (u'optimization issues in vlsi cad', 1), (u'integrated materials management', 1), (u'cryptography and network security', 1), (u'operating-systems', 1), (u'switches', 1), (u'complier design', 1), (u'netbsd', 1), (u'flask', 1), (u'jvm', 1), (u'computer architechture', 1), (u'pharmaceutical sales', 1), (u'crystal xcelsius', 1), (u'fundamentals of computing', 1), (u'robotium', 1), (u'air quality engineering', 1), (u'big data computing', 1), (u'tanks', 1), (u'water treatment', 1), (u'dsp course on programming and applications conducted by analog devices and iit madras', 1), (u'fx derivatives', 1), (u'life cycle assessment', 1), (u'tcp/ip protocols', 1), (u'teradata', 1), (u'microwave systems', 1), (u'contemporary challenges to macro-financial policies', 1), (u'beautifulsoup', 1), (u'client billing', 1), (u'site planning', 1), (u'pivots', 1), (u'mobile phone apps', 1), (u'neural and fuzzy systems', 1), (u'water', 1), (u'safety management systems', 1), (u'financial management', 1), (u'application packaging', 1), (u'principles of manufacturing systems engineering', 1), (u'nanometer scale ic design', 1), (u'data mining and data warehousing', 1), (u'navigation', 1), (u'numerical methods', 1), (u'tms320c55x (dsp processor)', 1), (u'filezilla', 1), (u'angular js', 1), (u'traceability matrix', 1), (u'backup products symantec backup exec, netbackup, comvault ..............', 1), (u'stress analysis', 1), (u'cucumber framework', 1), (u'pervasive computing', 1), (u'testing tools', 1), (u'business case', 1), (u'hazop', 1), (u'passive microwave components', 1), (u'student placement coordinator at imt-nagpur', 1), (u'introduction to financial accounting', 1), (u'siebel', 1), (u'probability and stochastic processes', 1), (u'dhtml', 1), (u'windows phone app development', 1), (u'capsmill', 1), (u'cae', 1), (u'cad', 1), (u'onboarding', 1), (u'certified scrum master csm', 1), (u'stored procedures', 1), (u'digital vlsi', 1), (u'advanced logic design(audit)', 1), (u'c#.net', 1), (u'intelligence community', 1), (u'computer aided manufacturing', 1), (u'introductory java programming', 1), (u'loyalty programs', 1), (u'chef', 1), (u'code composer studio', 1), (u'capistrano', 1), (u'automotive petrol engines', 1), (u'heat and mass transfer', 1), (u'vlsi for dsp systems', 1), (u'ppc', 1), (u'candidate generation', 1), (u'embedded systems design and modeling', 1), (u'heat transfer', 1), (u'jit', 1), (u'microstrategy', 1), (u'optimization and verification of vlsi systems', 1), (u'computer simulation concepts', 1), (u'swishmax', 1), (u'finance', 1), (u'icetool', 1), (u'refineries', 1), (u'microcontrollers and applications', 1), (u'code design', 1), (u'power distribution', 1), (u'ip multimedia subsystem', 1), (u'design and analysis of algorithm', 1), (u'win32', 1), (u'defence sector', 1), (u'well testing', 1), (u'system analysis and project management', 1), (u'parallel processing', 1), (u'analysis of algorithm', 1), (u'advanced natural language processing', 1), (u'facebook marketing', 1), (u'automotive diesel engines', 1), (u'logical reasoning', 1), (u'gis for real estate', 1), (u'factory', 1), (u'inofrmation retrieval', 1), (u'internet', 1), (u'hci', 1), (u'computer programming for gis', 1), (u'xml application', 1), (u'talent scouting', 1), (u'arcsde', 1), (u'digitization', 1), (u'test and diagnosis of igital systems', 1), (u'energy policy and economics', 1), (u'market modeling', 1), (u'cognos', 1), (u'mobile device programming', 1), (u'electron devices', 1), (u'advanced data structures', 1), (u'altera quartus', 1), (u'supply chain operations', 1), (u'hr transformation', 1), (u'qtp', 1), (u'ncfm', 1), (u'machine learning (advanced)', 1), (u'github', 1), (u'meshing', 1), (u'ms office', 1), (u'organizational leadership', 1), (u'open source software, osum', 1), (u'allen bradley', 1), (u'ant', 1), (u'rapid product development', 1), (u'mechanize', 1), (u'wcs', 1), (u'micro economics', 1), (u'modelling tools', 1), (u'erdas imagine', 1), (u'biomedical instrumentation', 1), (u'probabilistic graphical models : theory', 1), (u'ansi c', 1), (u'digital mapping', 1), (u'business modeling', 1), (u'introduction to algorithms', 1), (u'adaptability', 1), (u'test management', 1), (u'robotics programming laboratory', 1), (u'system testing', 1), (u'ceragon', 1), (u'mrp', 1), (u'advanced computer security', 1), (u'air compressors', 1), (u'over-sampled data converters', 1), (u'nlp', 1), (u'sas certified base programmer', 1), (u'digital principles and system design', 1), (u'programming projects in java', 1), (u'air pollution control', 1), (u'algorithms and data structure', 1), (u'gap analysis', 1), (u'biometrics', 1), (u'big data analytics', 1), (u'amazon cloudfront', 1), (u'microwave communication', 1), (u'microwave circuit design', 1), (u'robo', 1), (u'patran', 1), (u'web2.0', 1), (u'accounting for managers', 1), (u'bridgewave', 1), (u'offshore oil & gas', 1), (u'boilers', 1), (u'javaservlets', 1), (u'subcontracts management', 1), (u'abinitio etl tool', 1), (u'leadership hiring', 1), (u'basic xcode', 1), (u'hydrogen fuel cells', 1), (u'global networking', 1), (u'socket.io', 1), (u'work design and facilities planning', 1), (u'dependable computing', 1), (u'lng', 1), (u'gnu make', 1), (u'backbone.js', 1), (u'objective c', 1), (u'wireless communications', 1), (u'jboss application server', 1), (u'computer integrated and flexible manufacture', 1), (u'online reputation management', 1), (u'websphere', 1), (u'oracle discoverer', 1), (u'multicore architectures and programming', 1), (u'international marketing', 1), (u'organizational change & leadership', 1), (u'firewalls', 1), (u'generic programming', 1), (u'jquery ui', 1), (u'microsoft visual studio c++', 1), (u'gwt', 1), (u'management of information systems', 1), (u'phpmyadmin', 1), (u'software defined network', 1), (u'kinematics of machines', 1), (u'university teaching', 1), (u'communication protocols', 1), (u'wireless and mobile communication', 1), (u'vehicle maintenance', 1), (u'statistical data analysis', 1), (u'fmcg', 1), (u'vlsi 1', 1), (u'computer and communication networks', 1), (u'agilent ads', 1), (u'automotive transmission', 1), (u'basic management courses covering supply chain, cost management, accounting, marketing, strategy, etc.', 1), (u'editorial', 1), (u'social bookmarking', 1), (u'security management', 1), (u'iso 14040', 1), (u'channel coding of communication', 1), (u'website analysis', 1), (u'power engineering from national power training institute(npti),ministry of power,india', 1), (u'distributed operating system', 1), (u'circuit thoery', 1), (u'publishing technical papers', 1), (u'network architecture', 1), (u'advance database management advance database management', 1), (u'measurement and quality control', 1), (u'control engineering', 1), (u'information retreival', 1), (u'e-band', 1), (u'events', 1), (u'unigraphics', 1), (u'network simulator', 1), (u'eucalyptus', 1), (u'introduction to parallel programming', 1), (u'vlsi system design', 1), (u'consumer behaviour', 1), (u'web caching', 1), (u'microwave and radio frequency wave propagation', 1), (u'algorithms in genetics', 1), (u'applied probability', 1), (u'analog and digital communications', 1), (u'technical documentation', 1), (u'java2d', 1), (u'microprocessors and microcontrollers lab', 1), (u'change management', 1), (u'cs 6604: fall 2013 data mining large networks and time-series', 1), (u'rfx process', 1), (u'omniture', 1), (u'talent mining', 1), (u'adsense', 1), (u'microsoft expression', 1), (u'automation and computer integrated manufacturing', 1), (u'cmos vlsi design', 1), (u'amazon s3', 1), (u'computer organization and architecture', 1), (u'information visualization', 1), (u'military experience', 1), (u'geoprocessing', 1), (u'managing operations', 1), (u'electronic circuit design', 1), (u'customer experience', 1), (u'snort', 1), (u'statistical inference', 1), (u'information storage and retreival', 1), (u'interactive system design', 1), (u'military operations', 1), (u'market risk', 1), (u'redis', 1), (u'mathcad', 1), (u'energy supply and conversion', 1), (u'piping', 1), (u'introduction to optimization: linear and non-linear programming', 1), (u'web de', 1), (u'employee referral programs', 1), (u'optimi', 1), (u'qnx', 1), (u'visual basic programming', 1), (u'tdd', 1), (u'e business', 1), (u'biomedical engineering', 1), (u'rdbms', 1), (u'methods for time series analysis', 1), (u'ospf', 1), (u'idcams', 1), (u'ideas, texts and contexts: thinkers of modern india', 1), (u'computational mechanics', 1), (u'computer integrated manufacturing', 1), (u'php4/5', 1), (u'basic unity 3d', 1), (u'strategic consulting', 1), (u'atnd', 1), (u'ipv4', 1), (u'electronic warfare', 1), (u'service oriented architecture design', 1), (u'advance computer architecture', 1), (u'apis', 1), (u'analog circuit design', 1), (u'relational database management systems', 1), (u'rotating equipment', 1), (u'ibm rational clearquest', 1), (u'ms vc++', 1), (u'illustrator', 1), (u'sap netweaver', 1), (u'component interface', 1), (u'step 5 plc', 1), (u'mobile wireless networking', 1), (u'mobile computing', 1), (u'sales', 1), (u'ssrs', 1), (u'automata and theory of formal languages', 1), (u'uix', 1), (u'direct marketing', 1), (u'mathematica', 1), (u'capstone in security', 1), (u'computer aided design', 1), (u'heat exchangers', 1), (u'combustion and heat transfer', 1), (u'parallel computer architecture', 1), (u'enterprise it architecture', 1), (u'arm cortex-m3 (lm3s9b92)', 1), (u'sap implementation', 1), (u'evaluating networked systems', 1), (u'multimedia framework', 1), (u'dynamics of machines', 1), (u'training delivery', 1), (u'internet protocols and modelling', 1), (u'advanced operating systems and distributed systems', 1), (u'independent study', 1), (u'scalaz', 1), (u'fundamentals of embedded systems', 1), (u'asic design lab', 1), (u'large-scale advanced data analysis', 1), (u'theory of algorithms', 1), (u'goal oriented', 1), (u'materials science', 1), (u'computer hardware and system maintenance', 1), (u'automobile engineering', 1), (u'puzzles', 1), (u'government contracting', 1), (u'global mapper', 1), (u'arts', 1), (u'proclarity', 1), (u'japanese language proficiency test', 1), (u'google earth', 1), (u'intro to database management systems', 1), (u'onshore', 1), (u'geospatial application development', 1), (u'top secret', 1), (u'information systems audit & control', 1), (u'machine vision', 1), (u'hardware software co-design of embedded systems', 1), (u'ui/ux design', 1), (u'oracle 10g', 1), (u'threads', 1), (u'ollydbg', 1), (u'computational neuroscience', 1), (u'linear integrated circuit design', 1), (u'qualnet', 1), (u'advertising', 1), (u'conversion optimization', 1), (u'mobile ipv6', 1), (u'organising', 1), (u'vim', 1), (u'computer aided drafting and cost esitmation', 1), (u'information security and privacy', 1), (u'esri', 1), (u'software engineering & management', 1), (u'game development', 1), (u'communication theory and systems', 1), (u'petroleum', 1), (u'governance', 1), (u'brazilian portuguese', 1), (u'automata', 1), (u'sap crm technical', 1), (u'cloud computing and storage', 1), (u'subsea engineering', 1), (u'apache - mod wsgi', 1), (u'industrial management', 1), (u'introduction to hadoop and mapreduce', 1), (u'marketing management - i and ii', 1), (u'probability, statistics and queuing theory', 1), (u'introduction to distributed systems', 1), (u'principles of management', 1), (u'budgets', 1), (u'turbo c++', 1), (u'rehabilitation engineering', 1), (u'unix and shell programming', 1), (u'low power design', 1), (u'equest', 1), (u'weblogic administration', 1), (u'hrsg', 1), (u'technology', 1), (u'advanced cloud computing', 1), (u'human information processing', 1), (u'pre silicon verification', 1), (u'managing international operations', 1), (u'bioinformatics', 1), (u'rtl coding', 1), (u'maintenance management', 1), (u'space operations', 1), (u'mutual funds', 1), (u'systemve', 1), (u'strategic partnerships', 1), (u'desktop security products symantec, trendmicro, mcafee................', 1), (u'oil & gas industry', 1), (u'mobile application development using ios and android', 1), (u'pcl', 1), (u'mapinfo', 1), (u'ibm rational tools', 1), (u'full-life cycle recruiting', 1), (u'antennae and wave propagation', 1), (u'communication skills', 1), (u'gradle', 1), (u'root cause analysis', 1), (u'probability in engineering decisions', 1), (u'is research seminar', 1), (u'decision support', 1), (u'gas processing', 1), (u'ms excel pivot tables', 1), (u'environmental awareness', 1), (u'job fairs', 1), (u'siemens s7-200', 1), (u'research for marketing decisions', 1), (u'interagency coordination', 1), (u'ftp', 1), (u'p', 1), (u'process safety', 1), (u'business requirements', 1), (u'network design', 1), (u'asp', 1), (u'sbt', 1), (u'diesel engine', 1), (u'graduate database systems', 1), (u'ibm data stage', 1), (u'internet protocol modeling', 1), (u'bash', 1), (u'operational cost analysis', 1), (u'estimating software development and maintenance projects', 1), (u'mobile devices', 1), (u'dft', 1), (u'arcmap', 1), (u'principles of data management', 1), (u'feed', 1), (u'hacmp', 1), (u'antenna and wave propagation', 1), (u'data reconciliation', 1), (u'thermal power plant', 1), (u'automobile', 1), (u'gpg', 1), (u'backhaul', 1), (u'landing page optimization', 1), (u'applied consulting', 1), (u'full-cycle recruiting', 1), (u'bi publisher', 1), (u'logical thinker', 1), (u'pipelines', 1), (u'omap soc', 1), (u'application engine', 1), (u'quantitative analytics', 1), (u'solution architecture', 1), (u'discrete mathematics', 1), (u'automation cnc & robotics', 1), (u'information theory', 1), (u'wan optimisation', 1), (u'corporate communications', 1), (u'amazon web services', 1), (u'air quality', 1), (u'predictive modeling', 1), (u'presentation preparation', 1), (u'computer programming', 1), (u'test automation framework', 1), (u'agile testing', 1), (u'total quality management', 1), (u'database and information systems', 1), (u'jsf', 1), (u'information processing - from data to solutions', 1), (u'advanced software engineering', 1), (u'content management system', 1), (u'zynq -7000', 1), (u'gis applications', 1), (u'mechatronics', 1), (u'physics', 1), (u'jboss eap', 1), (u'gis theories, models & issues', 1), (u'biztalk', 1), (u'managing projects', 1), (u'xcode', 1), (u'weapons', 1), (u'video and image processing using fpgas', 1), (u'networks', 1), (u'geomatics', 1), (u'completion', 1), (u'sales enablement', 1), (u'offshore operations', 1), (u'personnel supervision', 1), (u'stereo vision', 1), (u'fpso', 1), (u'cuda c', 1), (u'event tracing for windows', 1), (u'electronic instrumentation', 1), (u'database implementation', 1), (u'digital marketing experience', 1), (u'iphone development', 1), (u'algorithm design techniques', 1), (u'combined cycle', 1), (u'transmission lines', 1), (u'insight generation', 1), (u'computers and new media(ongoing)', 1), (u'ubiquitous computing', 1), (u'basic circuit theory', 1), (u'youth entrepreneurship', 1), (u'hyperion hfm', 1), (u'computational fluid dynamics', 1), (u'advance network and security', 1), (u'intelligence', 1), (u'telecom bss', 1), (u'proposal writing', 1), (u'defense', 1), (u'systems programming', 1), (u'energy demand and utilization', 1), (u'seo', 1), (u'arm', 1), (u'analog', 1), (u'automotive chassis', 1), (u'data communications and networking', 1), (u'social recruiting', 1), (u'design for manufacture and assembly', 1), (u'xslt', 1), (u'benefits administration', 1), (u'discrete time system', 1), (u'solid state devices', 1), (u'substation', 1), (u'high-volume recruiting', 1), (u'cloud computing and big data', 1), (u'plc ladder logic', 1), (u'homeland security', 1), (u'network coding', 1), (u'speech writing', 1), (u'publishing', 1), (u'aspen hysys', 1), (u'system analysis', 1), (u'it strategy and management', 1), (u'amazon mechanical turk', 1), (u'channel coding for communications', 1), (u'scalable architecture', 1), (u'gas', 1), (u'computer architecture - undergraduate level', 1), (u'spatial data management', 1), (u'experimental physics', 1), (u'digital systems', 1), (u'networking and security products, fortigate, checkpoint, sonicwall, cyberoam, ..', 1), (u'mainframe', 1), (u'vlsi digital conversion circuits', 1), (u'system center', 1), (u'uppaal', 1), (u'rip', 1), (u'adobe photoshop', 1), (u'electromagnetic fields and waves', 1), (u'integer programming', 1), (u'iar embedded workbench', 1), (u'statistical distribution theory', 1), (u'coffeescript', 1), (u'events organizer', 1), (u'x86', 1), (u'distribution strategies', 1), (u'statistics and linear programming', 1), (u'cucumber', 1), (u'mips', 1), (u'guice', 1), (u'clean air act', 1), (u'minilink e', 1), (u'discovery process', 1), (u'oops,java software development,c programming', 1), (u'synopsis', 1), (u'market entry', 1), (u'chemistry', 1), (u'gsm', 1), (u'wiimote for pc', 1), (u'ldv', 1), (u'webmaster services', 1), (u'openstack', 1), (u'advanced analog electronics', 1), (u'introduction to robotics', 1), (u'tcl-tk', 1), (u'essentials of organizational behavior, subjective well being of happiness, training and development, performance management, labor law, psychometrics,', 1), (u'ext js', 1), (u'force protection', 1), (u'compensation', 1), (u'advanced database systems', 1), (u'jstl', 1), (u'semantic html', 1), (u'tcp/ip stack', 1), (u'gem5', 1), (u'hpc for applications in engineering', 1), (u'job descriptions', 1), (u'mis project management and implementation', 1), (u'business process mapping', 1), (u'managerial finance', 1), (u'introduction to databases (stanford online)', 1), (u'statistic theory', 1), (u'control systems lab', 1), (u'innovation', 1), (u'ptc pro/engineer', 1), (u'organic search', 1), (u'micro processors and micro controllers', 1), (u'boolean searching', 1), (u'mathematical foundations of computer science', 1), (u'it project management', 1), (u'processing', 1), (u'web technologies', 1), (u'rapidminer', 1), (u'applications software development', 1), (u'private cloud', 1), (u'bgp', 1), (u'idl', 1), (u'energy transport and storage', 1), (u'graphics and multimedia', 1), (u'messaging', 1), (u'l2/l3 protocols', 1), (u'microprocessers and microcontrollers', 1), (u'robotics and intelligent sensors', 1), (u'xpressmp', 1), (u'lingo', 1), (u'spam', 1), (u'vbscript', 1), (u'demand forecasting', 1), (u'heroku', 1), (u'ppap', 1), (u'bsc', 1), (u'object oriented modeling', 1), (u'functional testing', 1), (u'cmos design', 1), (u'xpath', 1), (u'sales process', 1), (u'sas e-miner', 1), (u'websphere application server', 1), (u'fundamentals of digital image processing', 1), (u'oracle spatial', 1), (u'spatial concepts and organisation', 1), (u'desalination', 1), (u'is planning and strategy', 1), (u'surveying', 1), (u'design and analysis of communication networks', 1), (u'goal-oriented individual with strong leadership capabilities', 1), (u'c# and .net technology', 1), (u'webadf', 1), (u'nat', 1), (u'llvm', 1), (u'c/c++', 1), (u'coding in c, c++, java', 1), (u'ladder logic', 1), (u'intoduction to vlsi design automation', 1), (u'pivot tables', 1), (u'sudoku', 1), (u'vehicles', 1), (u'foundry', 1), (u'organizational development', 1), (u'information assurance', 1), (u'servers (jsdk 2.0,apache tomcat 5.5,6.0,7.0)', 1), (u'valves', 1), (u'natural gas', 1), (u'implementation of programming languages', 1), (u'bioconductor', 1), (u'treasury management', 1), (u'go', 1), (u'energy industry', 1), (u'manufacturing processes', 1), (u'software lab', 1), (u'computer control systems', 1), (u'infopath forms', 1), (u'salesforce api', 1), (u'databases( oracle,mysql,microsoft access )', 1), (u'asynchronous systems', 1), (u'xml publisher', 1), (u'undergrad operating systems', 1), (u'magik', 1), (u'wastewater treatment', 1), (u'inspection', 1), (u'cmos analog deisgn', 1), (u'sas base', 1), (u'investment analysis', 1), (u'primavera software training', 1), (u'lean thinking and lean engineering', 1), (u'verilog-a', 1), (u'cnc programming', 1), (u'energy systems analysis', 1), (u'online lead generation', 1), (u'bdd', 1), (u'salary negotiation', 1), (u'advance compiler', 1), (u'industrial instrumentation-1', 1), (u'mobile technology', 1), (u'octave', 1), (u'lex', 1), (u'partner management', 1), (u'corporate strategy', 1), (u'talend open studio', 1), (u'pdsn', 1), (u'human resource management', 1), (u'atm networks', 1), (u'iphone application development', 1), (u'rolls royce', 1), (u'structural analysis', 1), (u'production support', 1), (u'computer communication and network', 1), (u'formal topics in databases', 1), (u'enterprise application development', 1), (u'sensors and transducers lab', 1), (u'api', 1), (u'web marketing', 1), (u'purchasing processes', 1), (u'production and inventory control', 1), (u'microprocessor and interfacing', 1), (u'search engine technology', 1), (u'winfiol', 1), (u'digital signal processing lab', 1), (u'openmax', 1), (u'mobile and pervasive computing', 1), (u'applied probability methods in engineering', 1), (u'reporting & analysis', 1), (u'engineering mathematics', 1), (u'advanced computer architecture ii', 1), (u'advanced vlsi design', 1), (u'hazard identification', 1), (u'circuits lab', 1), (u'performance evaluation of computer systems', 1), (u'leadership development', 1), (u'release management', 1), (u'netcat', 1), (u'metasploit', 1), (u'readiness', 1), (u'communication systems', 1), (u'grails', 1), (u'ferret', 1), (u'steel design', 1), (u'ites strategy and policy, analysis,modelling and design,information assurance, business intelligence, software project management, service quality management,,', 1), (u'healthcare', 1), (u'jira', 1), (u'advanced process control', 1), (u'digital control systems', 1), (u'laser physics', 1), (u'strategic leadership', 1), (u'wireless and sensor networks', 1), (u'digital signal processing systems', 1), (u'satellite communication', 1), (u'pressure vessels', 1), (u'talent mapping', 1), (u'eclipse, net-beans, my-eclipse', 1), (u'blogging', 1), (u'software testing, validation and verification', 1), (u'lp', 1), (u'legacy conversion', 1), (u'flex', 1), (u'resource management techniques', 1), (u'statistics 101', 1), (u'staad', 1), (u'computer network operations', 1), (u'rexx', 1), (u'spatial analysis', 1), (u'c4isr', 1), (u'primavera p6', 1), (u'compilers design', 1), (u'reactive systems engineering', 1), (u'digital integrated ic design', 1), (u'data analytics', 1), (u'front-end', 1), (u'algorithm design and analysis', 1), (u'openni', 1), (u'html scripting', 1), (u'vlsi ii', 1), (u'rex', 1), (u'usability design', 1), (u'verilog-ams', 1), (u'dhcp', 1), (u'design using c++', 1), (u'rf engineering', 1), (u'ipod', 1), (u'cad/cam', 1), (u'customer oriented', 1), (u'customer relations', 1), (u'temporary staffing', 1), (u'network laboratory', 1), (u'tortoise svn', 1), (u'security in e-commerce', 1), (u'energy conservation', 1), (u'oil/gas', 1), (u'terracotta', 1), (u'digital design', 1), (u'digital system design & synthesis', 1), (u'measurement systems', 1), (u'udp', 1), (u'vlsi systems', 1), (u'advanced vlsi logic synthesis', 1), (u'automotive electrical and electronics', 1), (u'engineering materials and metallurgy', 1), (u'minilink tn', 1), (u'data bases and systems', 1), (u'food industry', 1), (u'linear integrated ciruits', 1), (u'new business development', 1), (u'simulation modelling for decision making', 1), (u'human operator in complex systems', 1), (u'national engineering college', 1), (u'minilink hc', 1), (u'simulation methods & applications', 1), (u'design of experiments', 1), (u'google analytics', 1), (u'database system', 1), (u'soa testing', 1), (u'industrial psychology and work ethics', 1), (u'mis', 1), (u'ieee 802.11', 1), (u'micrium os-iii', 1), (u'distributed algos and systems (ongoing)', 1), (u'intelligent user interfaces', 1), (u'energy audits', 1), (u'application tracking', 1), (u'fundamentals of the design and analysis of algorithms', 1), (u'offshore drilling', 1), (u'estimation and detection', 1), (u'simultaneous localization and mapping (online, prof. cyrill stachniss, university of freiburg)', 1), (u'sap abap', 1), (u'painting', 1), (u'loadrunner', 1), (u'routing', 1), (u'xlminer', 1), (u'controls', 1), (u'envi', 1), (u'introduction to analog cmos design', 1), (u'optimization techniques', 1), (u'ksh', 1), (u'ms office suite', 1), (u'advanced computing models and architectures', 1), (u'photography', 1), (u'simulation and modeling', 1), (u'capsturn', 1), (u'arc objects', 1), (u'project management fundamentals', 1), (u'total quality managemant', 1), (u'bio-image informatics', 1), (u'linux virtual memory manager', 1), (u'management information systems', 1), (u'testing and diagnosis of digital systems', 1), (u'database applications', 1), (u'j2me development', 1), (u'system administration', 1), (u'racket', 1), (u'erp implementations', 1), (u'distirubted systems', 1), (u'rosa 8.0.3', 1), (u'microsoft summer school on security & privacy 2011', 1), (u'appengine', 1), (u'advanced java programming', 1), (u'lua', 1), (u'analog integrated circuit design', 1), (u'vlsi i', 1), (u'social graph', 1), (u'internet protocols', 1), (u'technical presentations', 1), (u'ansa tool', 1), (u'moodle', 1), (u'html/xml', 1), (u'c, c++, html, javascript, basics of xml and php, got training in core java, jsp.', 1), (u'programming in c', 1), (u'qfd', 1), (u'manufacturing systems planning and analysis', 1), (u'industrial economics', 1), (u'active top secret security clearance', 1), (u'analysis of software artifacts (grad software engg.)', 1), (u'rpo', 1), (u'options futures and derivatives', 1), (u'building relationships', 1), (u'business process improvement', 1), (u'ciena', 1), (u'behavioural sciences i and ii', 1), (u'asp.net mvc', 1), (u'supervisory skills', 1), (u'system software', 1), (u'windows phone', 1), (u'marketing communications', 1), (u'sas/sql', 1), (u'independent research study on wireless networks and android permissions', 1), (u'micro processors and applications', 1), (u'software quality assurance', 1), (u'online marketing analysis', 1), (u'constraint programming', 1), (u'cvs', 1), (u'corporate restructuring: human dimensions', 1), (u'downstream oil & gas', 1), (u'squid', 1), (u'digital techniques', 1), (u'software testing and quality assurance', 1), (u'benefit cost analysis', 1), (u'embedded operating systems- linux', 1), (u'bayesian data analysis', 1), (u'introduction to transport materials', 1), (u'artificial inteligence', 1), (u'nyquist-rate data converters', 1), (u'quality management', 1), (u'ios', 1), (u'architectures', 1), (u'artificial neural networks', 1), (u'ni labview', 1), (u'drawing', 1), (u'books', 1), (u'web intelligence and big data', 1), (u'coordination', 1), (u'statistical methods', 1), (u'microsoft project', 1), (u'non-linear & dynamic programming', 1), (u'search analysis', 1), (u'nato', 1), (u'css3', 1), (u'petrochemical', 1), (u'computational methods in biological modeling and simulation', 1), (u'digital rf', 1), (u'site catalyst', 1), (u'energy policy', 1), (u'computer communications and networks', 1), (u'motorola', 1), (u'oracle service bus', 1), (u'google webmaster tools', 1), (u'feasibility studies', 1), (u'analog electronic circuits', 1), (u'global client management', 1), (u'thermal engineering', 1), (u'regression testing', 1), (u'objectarx', 1), (u'geospatial data', 1), (u'strategic sourcing', 1), (u'innovation for energy and the environment', 1), (u'head hunting, persuasive communication, search and networking', 1), (u'lead generation', 1), (u'sketching', 1), (u'information security', 1), (u'honeywell dcs', 1), (u'automotive pollution and control', 1), (u'web services api', 1), (u'internet protocol & modelling', 1), (u'pressure', 1), (u'msn adcenter', 1), (u'kernel programming', 1), (u'national security', 1), (u'low noise electric design', 1), (u'glade', 1), (u'keyword research', 1), (u'database systems', 1), (u'linux kernel and driver development', 1), (u'cocoa', 1), (u'mechanical engineering standards', 1), (u'corporate governance', 1), (u'steam boilers', 1), (u'site execution', 1), (u'b.e- mechanical engineering', 1), (u'retail management', 1), (u'energy system modeling', 1), (u'renewable energy', 1), (u'board bring-up', 1), (u'molecular cell biology', 1), (u'emergency management', 1), (u'military training', 1), (u'analog and cmos design', 1), (u'production engineering', 1), (u'gis application', 1), (u'tactics', 1), (u'wcf services', 1), (u'analytical instrumentation', 1), (u'engineering economics and financial accounting', 1), (u'depth imaging', 1), (u'sun certified web component developer', 1), (u'computational genomics', 1), (u'spufi', 1), (u'digital communication techniques', 1), (u'command & control', 1), (u'restful webservices', 1), (u'pig', 1), (u'soql', 1), (u'javase', 1), (u'cmos', 1), (u'introduction to soft computing', 1), (u'fuels and lubricants', 1), (u'hydrogen storage', 1), (u'machine learning on coursera', 1), (u'manufacturing technology', 1), (u'ibm websphere commerce', 1), (u'rspec', 1), (u'federated proxy servers (wsgi)', 1), (u'basic objective-c', 1), (u'sphinx', 1), (u'statistical software for business applications', 1), (u'microelectronics', 1), (u'balanced scorecard', 1), (u'business interlligence , software and techniques', 1)])
        
    data_home = environ.get('SCIKIT_LEARN_DATA', join('../', 'scikit_learn_data'))
    data_home = expanduser(data_home) + '/multilabeldata'
    if not exists(data_home):
        makedirs(data_home)        
    
    
    for skill in allskills.iterkeys():        
        skill = skill.encode('ascii', 'ignore')          
            
        addQuesDirectSearch(data_home, skill)
        addQuesTitleSearch(data_home, skill)
        addQuesBySynonyms(data_home, skill)
        addQuesByRelatedTerms(data_home, skill)        

def query(userskillset):

    dpath = expanduser(environ.get('SCIKIT_LEARN_DATA', join('../', 'scikit_learn_data') + '/multilabeldata'))
            
    if(path.isdir(dpath) == False):    
        load()
        
    file_paths = []  
    data = dict()
    for root, directories, files in os.walk(dpath):   
        for filename in files:          
            filepath = os.path.join(root, filename)     
            file_paths.append(filepath)       
            labeltext = filename.split('.txt')[0].translate(None, "['] ")            
            labels = list(labeltext.split(','))
            
            f = open(filepath, 'r')          
            txt = f.read()
            f.close()
            data[txt] = labels
          
    X_train = data.keys()
            
    all_labels = set()
    for labels in data.itervalues():
        for label in labels:
            all_labels.add(label)
            
    target_names = list(all_labels)
    
    y_train = list()
            
    for txt, labels in data.iteritems():
        targets = list()
       
        for label in labels:
            index = target_names.index(label)            
            targets.append(index)
        
        y_train.append(targets)
        
    classifier = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', OneVsRestClassifier(LinearSVC()))])
    classifier.fit(X_train, y_train)
    
    
    docs_new = dict()
    site = stackexchange.Site(stackexchange.StackOverflow, 'CXRSlQ0gwe7r1lOU6taZ6A((')
    site.be_inclusive()
    all_questions=list()    
    while True:
        try:
            all_questions = site.recent_questions(sort='hot', order=DESC) 
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
            docs_new[str(q.title).encode('ascii', 'ignore').lower()] = q            
            i = i + 1           
            if(i > 1000):                
                break
            
    except:
        pass 
    
    X_test = docs_new.keys()
    
    predicted = classifier.predict(X_test)
    dict1 = dict()
    
    i = 0
    
    for doc, labels in zip(X_test, predicted):
        
        labelnames = list()
        for label in labels:
            labelnames.append(target_names[label])
        
        q = docs_new[doc]
        
        if(len(labels) == 0):  
                
            tagmatch = set(userskillset) & set(q.tags) 
            if(tagmatch):
                #print 't:', i, doc, q.tags          
                #print ''                    
                
                innerdict = dict()                 
                innerdict['title'] = q.title 
                innerdict['labels'] = labelnames        
                innerdict['score'] = q.score
                innerdict['view_count'] = q.view_count
                innerdict['url'] = q.url  
                innerdict['tags'] = q.tags
                i = i + 1
                dict1[i] = innerdict
                
            
        else:        
            labelmatch = set(userskillset) & set(labelnames)      
            tagmatch = set(userskillset) & set(q.tags) 
            if(labelmatch or tagmatch):            
                #print 'l:', i, doc, q.tags, labelnames
                #print ''                    
                    
                
                innerdict = dict()                 
                innerdict['title'] = q.title 
                innerdict['labels'] = labelnames        
                innerdict['score'] = q.score
                innerdict['view_count'] = q.view_count
                innerdict['url'] = q.url  
                innerdict['tags'] = q.tags
                i = i + 1
                dict1[i] = innerdict
            
        
        
    return dict1    



# userskillset = [u'distributed systems', u'software engineering', u'computer architecture', u'requirements analysis', u'test driven development', u'information storage and retrieval (ongoing)', u'grid computing', u'soql', u'common lisp', u'problem solving', u'mysql', u'xml', u'distributed algos and systems (ongoing)', u'git', u'amazon cloudfront', u'capistrano', u'bdd', u'hudson', u'technical recruiting', u'c#', u'heroku', u'computer communication and networks', u'operating systems', u'principles of compiler design', u'artificial intelligence', u'web services', u'design and analysis of algorithms', u'python', u'programming and data structures', u'team leadership', u'rspec', u'amazon s3', u'agile project management', u'data structures', u'cucumber', u'unix internals', u'machine learning (ongoing)', u'code design', u'ruby', u'release management', u'jquery', u'chef', u'sphinx', u'database management systems', u'amazon ec2', u'amazon web services (aws)', u'programming', u'ruby on rails', u'c++', u'algorithms', u'object oriented analysis and design', u'object oriented programming', u'multicore architecture and programming']
# q = query(userskillset)
# print len(q)