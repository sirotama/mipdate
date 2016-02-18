# -*- coding: utf-8 -*-

import bottle
from bottle_jade import JadePlugin
import requests,re
import json
import sys
import linecache
import os

VIEWS_DIR=os.environ.get("VIEWS_DIR",linecache.getline('id',3).rstrip())

jade=bottle.install(JadePlugin(template_folder=VIEWS_DIR))

ids = os.environ.get("MISSKEY_SCREEN_NAME",linecache.getline('id',1).rstrip())
password = os.environ.get("MISSKEY_PASSWORD",linecache.getline('id',2).rstrip())

updateAPIURL = 'https://himasaku.misskey.xyz/account/name/update'
postAPIURL= "https://himasaku.misskey.xyz/posts/create"
res = requests.get("https://misskey.xyz/")
res.raise_for_status()
cookie = {"hmsk":res.cookies["hmsk"]}
csrf = re.search('<meta name="csrf-token" content="([A-Za-z0-9\\-_]+)">',res.text).group(1)
res = requests.post("https://login.misskey.xyz/",headers={'csrf-token':csrf},data={"screen-name":ids,"password":password},cookies = cookie)
res.raise_for_status()

def render(jadename,jadeopts={}):
	return jade.render(jadename,**jadeopts)

@bottle.get('/')
def index():


	return render("index.jade")
@bottle.post('/change')
def changename():
		changedname = {'name': bottle.request.forms.get("name")}
		change = requests.post(updateAPIURL,cookies=cookie,data=changedname,headers={"csrf-token":csrf} )

		post = requests.post(postAPIURL,cookies=cookie,data={'text' : '' + bottle.request.forms.get("name") + 'に改名させられました。' },headers={"csrf-token":csrf})
		return render("change.jade")

bottle.run(host='0.0.0.0', port=int(os.environ.get("PORT",8080)), reloader=True)
