from bottle import route, run, request, FormsDict, error, redirect, app
import collections, sqlite3, httplib2
from math import ceil, floor
from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets
from apiclient.errors import HttpError
from apiclient.discovery import build
from beaker.middleware import SessionMiddleware
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

#variable definitions

use_google_login = False
localhost_test = True
use_optimize = True

RESULTS_CACHE = {}

if localhost_test:
	baseURL="http://ec2-107-20-162-69.compute-1.amazonaws.com"
else:
	baseURL = "http://localhost:8080"

scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
redirect_uri = baseURL + '/search'
addedResult = """<table border = "0"><tr><th align = "left">Search Results</th></tr>"""
endTable = "</table>"
code = ""
checkLogout = 0


#import Logo from another file
with open ("Logo.txt", "r") as LogoFile:
	LogoString = LogoFile.read().replace('\n', "<br>")
	LogoString = "<html><pre>"+LogoString+ "</html>"

#Search form
searchHTML = '''
		<form action ="/search" method="post">
			Search: <input name="userinput" type="text"/>
			<input value = "Search" type="submit" />
		</form>
	'''

#logout button
logoutButton = '''<FORM METHOD="LINK" ACTION="''' + baseURL + '''/logout" ALIGN = "right">
<INPUT TYPE="submit" VALUE="Logout">
</FORM></body></html>'''

#cache
cache_opts = {
	'cache.type': 'file',
	'cache.data_dir': '/tmp/cache/data',
	'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

tmpl_cache = cache.get_cache(baseURL + '/search', type='dbm', expire = 3600)
tmpl_cache.clear()

#no browser back
disableBack = """<html><head><SCRIPT type="text/javascript">
    window.history.forward();
    function noBack() { window.history.forward(); }
</SCRIPT>
</HEAD>
<BODY onload="noBack();"
    onpageshow="if (event.persisted) noBack();" onunload="">"""


#function connecting to google API
def googleAPI():
	#google api set up
	flow = flow_from_clientsecrets("client_secrets.json", scope = scope, redirect_uri = redirect_uri)
	uri = flow.step1_get_authorize_url()
	redirect(uri)


#configure middleware
session_opts = {
	'session.type': 'file', 
	'session.cookie_expires': 300,
	'session.data_dir': './data',
	'session.auto': True,
}
wsgi_app = SessionMiddleware(app(), session_opts)


######Pages##########

#error page
@error(404)
def error404(error):
	return '''This page or file does not exist. <br><br> Please visit the <a href="''' + baseURL + '''/search"> Search page</a> for a new search.'''

#homepage - just show logo
@route('/')
def Home():
	if use_google_login:
		session = request.environ.get('beaker.session')
		session.save()
		googleAPI()
	else: 
		redirect('/search')

@route('/logout')
def logout():
	redirect("https://accounts.google.com/logout")

#search page - includes an html form with one text box for search input
@route('/search')
def search():
	if use_google_login:
		code = request.query.get("code", "")
		if(code == ""):
			redirect('/')

		flow = OAuth2WebServerFlow(client_id='470991490159.apps.googleusercontent.com', client_secret = 'Zleg_TsPX6CXU06z3XURewt8', scope = scope, redirect_uri = redirect_uri)
		credentials = flow.step2_exchange(code)
		token = credentials.id_token['sub']

		#retrieve user data with the access token
		http = httplib2.Http()
		http = credentials.authorize(http)

		#get user email
		users_service = build('oauth2', 'v2', http=http)
		user_document = users_service.userinfo().get().execute()
		user_email = user_document['email']

		#get username
		users_service = build('plus', 'v1', http=http)
		profile = users_service.people().get(userId='me').execute()
		user_name = profile['displayName']
		user_image = profile['image']['url']

	return disableBack + logoutButton + LogoString + "<br><br>" + searchHTML

@route('/search', method='POST')
def do_search():

	userinput = request.forms.get("userinput")

	#split user search into words and count the occurance of each word using collections.Counter
	words = userinput.split(" ")
	wordcounter = collections.Counter(words)
	
	#Create a new string printWordCounter which holds the text for an HTML table include all the words and the number of times they occur in the search
	printWordCounter = """<table border = "0"><tr><th align = "left">Word</th><th>Count</th></tr>"""
	for key, value in zip(wordcounter.keys(), wordcounter.values()):
		printWordCounter += ("<tr><td>" + key + """</td><td align="center">""" + str(value) + "</td></tr>")

	redirect('/search/0/'+ userinput)



def db_search(searchWord):
	conn = sqlite3.connect('table.db')
	c=conn.cursor()
	c.execute("SELECT DISTINCT DocIndex.url FROM Lexicon, DocIndex, InvertedIndex, PageRank WHERE Lexicon.word_id = InvertedIndex.word_id AND InvertedIndex.doc_id = DocIndex.doc_id AND InvertedIndex.doc_id=PageRank.doc_id AND Lexicon.word LIKE ? ORDER BY PageRank.rank", searchWord)

	return  c.fetchall()

@route('/search/<pageid>/<userinput>')
def searchpages(pageid, userinput):

	#get results from  table
	words = userinput.split(" ")
	searchWord = (words[0],)
	resultCount = 0
	page = []

	result = ""	

	if use_optimize:
		if searchWord in RESULTS_CACHE:
			result = RESULTS_CACHE[searchWord]
		else:	
			result = db_search(searchWord)
			RESULTS_CACHE[searchWord] = result
	else:
		result = db_search(searchWord)		
	
	count = 0
	for row in result:
		count+=1
		if count%20 == 1:
			page.append("")

		#split and display as url
		url = str(row).split("'")
		page[int(floor((count-1)/20))] += ('<tr><td><a href="' + url[1] + '" target="_blank">'+ url[1] + "</a></td></tr>")


	if count == 0:
		return logoutButton + LogoString + "<br><br>" + searchHTML + "<br><br>" +"Search "+  "'%s'<br><br> No results found."  %(userinput) 


	pageList = "Go to Page:<br>"+"""<table border = "0"><tr>"""
	for pagenum in range(0, len(page)):
		pageList += '<th><a href= "' + baseURL + '/search/' + str(pagenum) + '/' + userinput + '">' + str(pagenum+1) + "<a></th>"

	pageList += "</tr>"

	if int(pageid) < len(page): 
		return disableBack + logoutButton + LogoString + "<br><br>" + searchHTML + "<br><br>" +"Search "+  "'%s'<br><br>%s %s%s<br><br>%s"  %(userinput, addedResult, page[int(pageid)], endTable, pageList) 

	else:
		redirect('/err')


if localhost_test:
	run(host="localhost", port="8080", debug=True, app=wsgi_app)
else:
	run(host="0.0.0.0", port="80", debug=True, app=wsgi_app)

