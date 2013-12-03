from bottle import route, run, request, FormsDict, error, redirect, app
from pyswip import Prolog

#variable definitions

localhost_test = True

if localhost_test:
	baseURL="http://ec2-107-20-162-69.compute-1.amazonaws.com"
else:
	baseURL = "http://localhost:8080"

redirect_uri = baseURL + '/search'


sudokuFormH = ''' <form action ="/solve" method="post">'''
sudokuFromEnd = '''<input value = "Search" type="submit" /> </form> '''

######Pages##########

#error page
@error(404)
def error404(error):
	return '''This page or file does not exist. <br><br> Please visit the <a href="''' + baseURL + '''/search"> Search page</a> for a new search.'''

#homepage - just show logo
@route('/')
def Home():
	sudokuform = ""
	for i in range( 1,82):
		name = str(i)
		sudokuform = sudokuform + ' <input type="text" name="'+ name+'" size="1" maxlength="1" class="box-10" value=""/>'
		if i%9 == 0:
			sudokuform += "<br>"
		
	sudokuform += "<br>"
	return sudokuFormH + sudokuform + sudokuFromEnd


@route('/solve', method='POST')
def solve():
	sudoku = []
	sudokuString = "["
	for i in range(1,82):
		digit = request.forms.get(str(i))
		if digit.isdigit():
			sudoku.append(digit)
		else:
			sudoku.append("0")
	sudokuString +=  ",".join(sudoku)
	print sudokuString
	sudokuString += "]"
	redirect('/solve/'+sudokuString)
	
	return sudoku
 

@route('/search', method='POST')
def do_search():
	userinput = request.forms.get("userinput")
	#split user search into words and count the occurance of each word using collections.Counter
	return s1
	#redirect('/search/0/'+ userinput)

@route('/solve/<sudokuString>')
def solveSudoku(sudokuString):
	print "In solve, got string" + sudokuString

	answerString = ""
	prolog = Prolog()
	prolog.consult('sudoku.pl')
	for result in prolog.query("sudoku(" + sudokuString + ")."):
		r = result["X"]
		for i, letter in enumerate(letters):
			print letter, "=", r[i]

	print "That's all..."
	return sudokuString


@route('/search/<pageid>/<userinput>')
def searchpages(pageid, userinput):
	#get results from  table
	words = userinput.split(" ")
	searchWord = (words[0],)
	resultCount = 0
	page = []

	result = ""	

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
	run(host="localhost", port="8080", debug=True)
else:
	run(host="0.0.0.0", port="80", debug=True, app=wsgi_app)

