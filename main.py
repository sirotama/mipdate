import bottle
from bottle_jade import JadePlugin
import requests
import json
import linecache

VIEWS_DIR=linecache.getline('id',3).rstrip()

jade=bottle.install(JadePlugin(template_folder=VIEWS_DIR))
def render(jadename,jadeopts={}):
	return jade.render(jadename,**jadeopts)

@bottle.get('/')
def index():

	ids = linecache.getline('id',1).rstrip()
	password = linecache.getline('id',2).rstrip()

	login = requests.post('https://login.misskey.xyz' ,data={'screen-name': ids, 'password': password})
	cookie = {'hmsk': login.cookies['hmsk']}

	return render("index.jade")
@bottle.post('/change')
def changename():
	return render("change.jade")
bottle.run(host='localhost', port=8080, debug=True, reloader=True)