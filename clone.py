import requests
import json
import os, sys
import subprocess
import getpass

def clone():
	if len(sys.argv)<2:
		print 'Usage : python clone.py USERNAME'
		sys.exit()

	username = sys.argv[1]
	response = requests.get('https://api.github.com/users/'+ username) 
	content = response.json()
	if content['name']:
		print 'Hello %s' % content['name']
	else:
		print 'Wrong Username. Exiting!'
	parameters = { 'per_page' : '200'}
	repoUrl = 	requests.get('https://api.github.com/users/'+ username +'/repos', params=parameters)
	content = repoUrl.json()

	path = '/home/'+getpass.getuser()+'/developer/github/'+username
	print 'Path: '+path
	try:
		os.chdir(path)
	except OSError:
		os.makedirs(path)
		os.chdir(path)

	with open('data.json', 'w') as datafile:
		json.dump(content, datafile)

	with open('repoName.txt', 'w') as repoName, open('cloneUrl.txt', 'w') as cloneUrl:
		for item in content:
			repoName.write(item['name']+'\n')
			cloneUrl.write(item['clone_url']+'\n')
	with open('cloneUrl.txt', 'r') as cloneUrl:
		urls = cloneUrl.readlines()
	for url in urls:
		subprocess.call(["git", "clone", url[:-1]])

	print 'Done! Enjoy!'


if __name__ == '__main__':
	clone()