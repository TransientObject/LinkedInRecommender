from flask import Flask, jsonify, render_template, request
from linkedin import linkedin
import webbrowser
from flask_bootstrap import Bootstrap
import sys
import unicodedata
import json
sys.path.insert(0, 'stackoverflow')
sys.path.insert(0, 'github')
import multilabelstack
import git_crawler
import time

app = Flask(__name__)
Bootstrap(app)

API_KEY = '75v25tzfq15ygo'
API_SECRET = 'Sjn97PD59ihFTjuQ'
RETURN_URL = 'http://localhost:5000/redir.html'


@app.route('/')
def home():
	return render_template('login.html')

@app.route('/_login')
def login():
	authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
	webbrowser.open(authentication.authorization_url)  #open this URL on your browser
	return

def get_skills(profile):
	return [skill['skill']['name'].lower() for skill in profile['skills']['values']]

def get_courses(profile):
	return [course['name'].lower() for course in profile['courses']['values']]

def dump_json(fields, filename):
	with open(filename,'w') as f:
		f.write(json.dumps(fields))
	f.close()

@app.route('/stack.html')
def stack():
	f = open('linkedin/stackoverflow_qns.json', 'r')
	line = f.readline()
	stackoverflow_qns = json.loads(line)
	# print [value for value in stackoverflow_qns.values()]
	# print "jello"
	# for key in stackoverflow_qns.keys():
	# 	tags = stackoverflow_qns[key]['tags']
	# 	tags = [unicodedata.normalize('NFKD', tag).encode('ascii','ignore') for tag in tags]
	# 	stackoverflow_qns[key]['tags'] = tags
	print [value for value in stackoverflow_qns.values()]
	return render_template('stack.html', questions=stackoverflow_qns)

@app.route('/github.html')
def github():
	f = open('linkedin/git_repos.json', 'r')
	line = f.readline()
	github_repos = json.loads(line)
	# print [value for value in stackoverflow_qns.values()]
	# print "jello"
	# for key in stackoverflow_qns.keys():
	# 	tags = stackoverflow_qns[key]['tags']
	# 	tags = [unicodedata.normalize('NFKD', tag).encode('ascii','ignore') for tag in tags]
	# 	stackoverflow_qns[key]['tags'] = tags
	return render_template('github.html', repos=github_repos["items"])

@app.route('/redir.html')
def redir():
	authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
	application = linkedin.LinkedInApplication(authentication)

	if request.args.get('code', '') != '':
		authentication.authorization_code = request.args.get('code', '')
		authentication.get_access_token()
		profile = application.get_profile(selectors=['id', 'first-name', 'last-name', 'location', 'distance', 'num-connections', 'skills', 'educations', 'interests', 'courses', 'following', 'related-profile-views', 'job-bookmarks', 'certifications'])
		skills = get_skills(profile)
		courses = get_courses(profile)
		input_values = list(set(skills + courses))
		# print input_values
		github_input_values = ['c', 'c++', 'java', 'data structures', 'algorithms']
		github_input_values = input_values[:10]
		stack_qn_recommendations = multilabelstack.query(input_values)
		github_recommendations = git_crawler.query(github_input_values)
		dump_json(stack_qn_recommendations, "linkedin/stackoverflow_qns.json")
		dump_json(github_recommendations, "linkedin/git_repos.json")
		return render_template('redir.html')
	else:
		print "No Auth Code\n"
		return render_template('redir.html')

if __name__ == '__main__':
	app.debug = True
	app.run()