import bottle
from bottle_jade import JadePlugin
import requests
import json
import sys
import linecache

VIEWS_DIR=linecache.getline('id',3).rstrip()

jade=bottle.install(JadePlugin(template_folder=VIEWS_DIR))

ids = linecache.getline('id',1).rstrip()
password = linecache.getline('id',2).rstrip()

login = requests.post('https://login.misskey.xyz' ,data={'screen-name': ids, 'password': password})
cookie = {'hmsk': login.cookies['hmsk']}

updateAPIURL = 'https://himasaku.misskey.xyz/account/name/update'

def render(jadename,jadeopts={}):
	return jade.render(jadename,**jadeopts)

@bottle.get('/')
def index():


	return render("index.jade")
@bottle.post('/change')
def changename():
		changedname = bottle.request.forms.get("name")
		change = requests.post(updateAPIURL,cookies=cookie,data=changedname)
		print changedname
		print change.text
		return render("change.jade")

bottle.run(host='localhost', port=8080, debug=True, reloader=True)