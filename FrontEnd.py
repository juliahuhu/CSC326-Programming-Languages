from bottle import route, run, request, FormsDict, error, redirect
import collections, sqlite3
from math import ceil, floor


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

#variables
#page = []
#userinput =""
#printWordCounter = ""
addedResult = """<table border = "0"><tr><th align = "left">Search Results</th></tr>"""
#pagenum = 0
endTable = "</table>"
#pageList = ""


#error page
@error(404)
def error404(error):
	return '''This page or file does not exist. <br><br> Please visit the <a href="http://localhost:8080/search"> Search page</a> for a new search.'''

#homepage - just show logo
@route('/')
def Logo():
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

	c.execute("SELECT * FROM Lexicon WHERE word = '%s'" % testword)
	result = c.fetchall()
	print result
	c.execute("SELECT Count(word) FROM Lexicon WHERE word = '%s'" % testword)
	result2 = c.fetchall()
	print result2

	count = 0

	for row in result:
		count+=1
		if count%20 == 1:
			page.append("")

		#split and display as url
		url = str(row).split("'")
		page[int(floor(count/20))] += ('<tr><td><a href="' + url[1] + '">'+ url[1] + "</a></td></tr>")



	pageList = "Go to Page:<br>"+"""<table border = "0"><tr>"""
	print (len(page))
	for pagenum in range(0, len(page)):
		pageList += """<th><a href= "localhost:8080/search/""" + str(pagenum) + "/" + userinput + '">' + str(pagenum+1) + "<a></th>"

	pageList += "</tr>"

	if int(pageid) < len(page): 
		return LogoString + "<br><br>" + searchHTML + "<br><br>" +"Search "+  "'%s'<br><br>%s %s%s<br><br>%s"  %(userinput, addedResult, page[int(pageid)], endTable, pageList) 

	else:
		redirect('/err')



run(host="localhost", port="8080", debug=True)
