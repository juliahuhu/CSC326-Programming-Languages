from bottle import route, run, request, FormsDict, error, redirect
import collections, sqlite3, httplib2
from math import ceil, floor
from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets
from apiclient.errors import HttpError
from apiclient.discovery import build


scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
redirect_uri = 'http://localhost:8080/searchRedirect'
addedResult = """<table border = "0"><tr><th align = "left">Search Results</th></tr>"""
endTable = "</table>"

#import Logo from another file
with open ("Logo.txt", "r") as LogoFile:
	LogoString = LogoFile.read().replace('\n', "<br>")
	LogoString = "<html><pre>"+LogoString+ "</html>"

searchHTML = '''
		<form action ="/search" method="post">
			Search: <input name="userinput" type="text"/>
			<input value = "Search" type="submit" />
		</form>
	'''

def googleAPI():
	#google api set up
	flow = flow_from_clientsecrets("client_secrets.json", scope = scope, redirect_uri = redirect_uri)
	uri = flow.step1_get_authorize_url()
	redirect(uri)


@route('/searchRedirect')
def searchRedirect():
	#exchange one time code for access token
	print("gettting code now")
	code = request.query.get("code", "")
	print("code ==========" + code)
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

	redirect('/search')


#error page
@error(404)
def error404(error):
	return '''This page or file does not exist. <br><br> Please visit the <a href="http://localhost:8080/search"> Search page</a> for a new search.'''

#homepage - just show logo
@route('/')
def Logo():
	googleAPI()
	return LogoString


#search page - includes an html form with one text box for search input
@route('/search')
def search():	
	return LogoString + "<br><br>" + searchHTML

#search result page
#@route('/search/<pageid>', method = 'POST')
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

@route('/search/<pageid>/<userinput>')
def searchpages(pageid, userinput):

	conn = sqlite3.connect('table.db')
	c=conn.cursor()
		
	#get results from  table
	words = userinput.split(" ")
	searchWord = (words[0],)
	testword = ('draper',)
	resultCount = 0
	page = []
	#for row in c.execute("SELECT * FROM Lexicon WHERE word = '%s'" % searchWord):	
	#for row in c.execute('SELECT * FROM Lexicon, DocIndex, Links WHERE Lexicon.id = DocIndex.id AND Lexicon.id = Links.id'):	
	#for row in c.execute('SELECT url FROM Lexicon, DocIndex, Links WHERE Lexicon.id = DocIndex.id AND Lexicon.id = Links.id AND url = ?', testword2):	
	#for row in c.execute('SELECT * FROM Lexicon, DocIndex, Links WHERE Lexicon.id = DocIndex.id AND Lexicon.id = Links.id AND Lexicon.word LIKE ?', [words[0]]):	
		#add ORDER BY Page Rank
		#print row
		#resultCount +=1
		#temp = (str(row)).split("'")
		#print temp
		#addedResult += ("<br><br>" + temp[1])

	c.execute("SELECT DocIndex.url FROM Lexicon, DocIndex, InvertedIndex, PageRank WHERE Lexicon.word_id = InvertedIndex.word_id AND InvertedIndex.doc_id = DocIndex.doc_id AND InvertedIndex.doc_id=PageRank.doc_id AND Lexicon.word LIKE ? ORDER BY PageRank.rank", searchWord)
	#c.execute("SELECT * FROM Lexicon WHERE word = '%s'" % testword)
	result = c.fetchall()
	print result
	#c.execute("SELECT Count(word) FROM Lexicon WHERE word = '%s'" % testword)
	#result2 = c.fetchall()
	#print result2

	count = 0

	for row in result:
		count+=1
		if count%20 == 1:
			page.append("")

		#split and display as url
		url = str(row).split("'")
		print url
		print count
		print int(floor(count/20))
		page[int(floor((count-1)/20))] += ('<tr><td><a href="' + url[1] + '" target="_blank">'+ url[1] + "</a></td></tr>")


	if count == 0:
		return LogoString + "<br><br>" + searchHTML + "<br><br>" +"Search "+  "'%s'<br><br> No results found."  %(userinput) 


	pageList = "Go to Page:<br>"+"""<table border = "0"><tr>"""
	print (len(page))
	for pagenum in range(0, len(page)):
		pageList += '<th><a href= "http://localhost:8080/search/' + str(pagenum) + '/' + userinput + '">' + str(pagenum+1) + "<a></th>"

	pageList += "</tr>"

	if int(pageid) < len(page): 
		return LogoString + "<br><br>" + searchHTML + "<br><br>" +"Search "+  "'%s'<br><br>%s %s%s<br><br>%s"  %(userinput, addedResult, page[int(pageid)], endTable, pageList) 

	else:
		redirect('/err')



run(host="localhost", port="8080", debug=True)
