from bottle import route, run, request, FormsDict
import collections


#import Logo from another file
with open ("Logo.txt", "r") as LogoFile:
	LogoString = LogoFile.read().replace('\n', "<br>")
	LogoString = "<html><pre>"+LogoString+ "</html>"


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


	return LogoString + "<br><br>" + "Search "+  "'%s' <br><br> %s"  %(userinput, printWordCounter) 


run(host="localhost", port="8080", debug=True)
