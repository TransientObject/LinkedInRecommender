from github3 import login
from github3 import search_repositories
import sys
import codecs
import itertools
import requests
import json
import time
import collections
import copy

class GitSearchResult():
	repoName = ""
	repoDesc = ""
	starCount = ""
	repoURL = ""
	queryTermResult = ""
	
	def __init__(self,repoName = None,repoDesc = None,starCount = None,repoURL = None,queryTermResult = None):
		self.repoName = repoName
		self.repoDesc = repoDesc
		self.starCount = starCount
		self.repoURL = repoURL
		self.queryTermResult = queryTermResult

def dd():
	return list(collections.defaultdict())
	
data = collections.defaultdict(dd)

resultData = collections.defaultdict(dd)
	
def login_git():
	gh = login('SattyS', password='qzpm123Tamu', token='d2a4d66b7825ca378c5f')
	return gh
	
def search_repo(query,limit,gh,classQuery):
	result = gh.search_repositories(query,sort="forks")
	gsrList = []
	for repository_search_result in result:
		gsrList.append(GitSearchResult(repository_search_result.repository.name,
		repository_search_result.repository.description,repository_search_result.repository.watchers,repository_search_result.repository.html_url,classQuery))
		if limit == len(gsrList):
			break
	return gsrList
	
def getRelatedQueryTerms(query,limit):
	related_query_list = [query]
	url = 'http://api.stackexchange.com/2.2/tags/', query ,  '/related?site=stackoverflow'
	url_string = ''.join(url) 
	r = requests.get(url_string)
	_limit = 0
	if(r.ok):
		repoItem = json.loads(r.text or r.content)
		itemsList = repoItem['items']
		if(len(itemsList) < limit):
			_limit = len(itemsList)
		else:
			_limit = limit
		for i in range(0,_limit):
			related_query_list.append(str(itemsList[i]['name']))
	return related_query_list
	
def getSkills(query_list):
	#Pase linkedin call here
	# main_query_list = ['c++', 'ruby', 'python', 'machine learning']
	main_query_list = query_list
	ret_list = []
	for q in main_query_list:
		q = q.replace(" ", "-")
		ret_list.append(q)
	return ret_list
	
def getJSONresult(gh, query_list):
	#relatedQueryDict = defaultdict(list)
	main_query_list = getSkills(query_list)
	related_query_list = []
	fullQueryList = []
	gsrList = []
	for query in main_query_list:
		related_query_list.append(getRelatedQueryTerms(query,1))
	#temp - stackexchange ratelimit
	#related_query_list.append(['c++','c','qt','template'])
	#related_query_list.append(['ruby','rails','python','perl'])
	k = 0
	for query in main_query_list:
		for ele in related_query_list[k]:
			if ele in fullQueryList:
				related_query_list[k].remove(ele)
			else:
				fullQueryList.append(ele)
		for related_query in related_query_list[k]:
			gsrList.append(search_repo(related_query,2,gh,query))
		k += 1
	
	cnt = 0
	resultRepoList = []
	for skillset in gsrList[:]:
		for skill in skillset[:]:
			if not resultRepoList:
				resultRepoList.append(skill)
			else:
				flag = 0
				for ele in resultRepoList:
					if skill.repoName == ele.repoName:
						flag = 1
						gsrList[cnt].remove(skill)
						break
				if flag == 0:
					resultRepoList.append(skill)
		cnt += 1
		
	#jsonOutput = collections.OrderedDict()
	gsrList = list(itertools.chain.from_iterable(gsrList))
	gsrLength = len(gsrList)
	gsrList.sort(key=lambda x: x.starCount, reverse=True)
	for i in gsrList:
		tempdict = collections.defaultdict()
		#if i.queryTermResult == 'machine-learning':
		tempdict['repoName'] = i.repoName
		tempdict['repoDesc'] = i.repoDesc
		tempdict['starCount'] = i.starCount
		tempdict['repoURL'] = i.repoURL
		tempdict['queryTermResult'] = i.queryTermResult
		data[i.queryTermResult].append(tempdict)
	globalCount = 0
	flag = 0
	resDataCount = 0
	while True:
		for q in main_query_list:
			if gsrLength == resDataCount:
				flag = 1
				break
			if len(data[q]) < globalCount+1:
				continue
			resultData['items'].append(data[q][globalCount])
			resDataCount += 1
		globalCount += 1
		if flag == 1:
			break
	# jsonData = json.dumps(resultData)
	return resultData

def query(query_list):
	if sys.stdout.encoding != 'UTF-8':
		sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
	gh = login_git()
	jsonData = getJSONresult(gh, query_list)
	return jsonData

# query(['c', 'c++', 'java', 'data structures', 'algorithms'])

# if __name__ == "__main__":
# 	main()