from bottle import route, run, request, FormsDict, error
import collections, sqlite3


#import Logo from another file
with open ("Logo.txt", "r") as LogoFile:
	LogoString = LogoFile.read().replace('\n', "<br>")
	LogoString = "<html><pre>"+LogoString+ "</html>"

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
	return LogoString + "<br><br>" +'''
		<form action ="/search" method="post">
			Search: <input name="userinput" type="text"/>
			<input value = "Search" type="submit" />
		</form>
	'''

#search result page
@route('/search', method='POST')
def do_search():
	#read user input from form
	userinput = request.forms.get("userinput")
	
	#split user search into words and count the occurance of each word using collections.Counter
	words = userinput.split(" ")
	wordcounter = collections.Counter(words)
	
	#Create a new string printWordCounter which holds the text for an HTML table include all the words and the number of times they occur in the search
	printWordCounter = """<table border = "0"><tr><th align = "left">Word</th><th>Count</th></tr>"""
	for key, value in zip(wordcounter.keys(), wordcounter.values()):
		printWordCounter += ("<tr><td>" + key + """</td><td align="center">""" + str(value) + "</td></tr>")


	#test table
	conn = sqlite3.connect('table.db')
	c=conn.cursor()
	#c.execute('''CREATE TABLE test
	#			(date text, name text)''')
	#c.execute('INSERT INTO test VALUES ("2013-10-05", "Anmol")')
	#c.execute('INSERT INTO test VALUES ("2013-10-07", "Vincent")')
	conn.commit()
	conn.close()
	
	#get results from test table
	conn = sqlite3.connect('table.db')
	c=conn.cursor()
	addedResult = ""
	for row in c.execute('SELECT * FROM test ORDER BY date'):	
		result = c.fetchone()
		print (str(result))
		addedResult += ("<br><br>" + str(result))
		print (addedResult)

	#Display table results on page




	return LogoString + "<br><br>" + "Search "+  "'%s' <br><br> %s %s"  %(userinput, printWordCounter, addedResult) 



run(host="localhost", port="8080", debug=True)
