from bottle import route, run, request, FormsDict, error, redirect, app
from pyswip import Prolog

#variable definitions
sudokuFormH = ''' <form action ="/solve" method="post">'''
sudokuFromEnd = '''<input value = "Solve!" type="submit" /> </form> '''

######Pages##########
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
	sudokuStrings = []
	sudokuStrings2 = []
	sudokuString = "["
	for i in range (1,82):
		digit = request.forms.get(str(i))
		if digit.isdigit():
			sudoku.append(digit)
		else:
			sudoku.append("_")

	sudokuStrings.append(sudoku[0:9])
	sudokuStrings.append(sudoku[9:18])
	sudokuStrings.append(sudoku[18:27])
	sudokuStrings.append(sudoku[27:36])
	sudokuStrings.append(sudoku[36:45])
	sudokuStrings.append(sudoku[45:54])
	sudokuStrings.append(sudoku[54:63])
	sudokuStrings.append(sudoku[63:72])
	sudokuStrings.append(sudoku[72:81])
	for row in sudokuStrings:
		sudokuStrings2.append("["+ ",".join(row) + "]")

	sudokuString = ",".join(sudokuStrings2)
	redirect('/solve/'+sudokuString)
 
queryS="""Puzzle=[[8,_,_,_,_,_,_,_,_],[_,_,3,6,_,_,_,_,_],[_,7,_,_,9,_,2,_,_],[_,5,_,_,_,7,_,_,_],[_,_,_,_,4,5,7,_,_],[_,_,_,1,_,_,_,3,_],[_,_,1,_,_,_,_,6,8],[_,_,8,5,_,_,_,1,_],[_,9,_,_,_,_,4,_,2]],Puzzle=[A,B,C,D,E,F,G,H,I],sudoku([A,B,C,D,E,F,G,H,I]).  """

@route('/solve/<sudokuString>')
def solveSudoku(sudokuString):
	print "in solve"
	answerString = ""
	prolog = Prolog()
	prolog.consult('sudokusolver.pl')
	queryString = "Puzzle = [" + sudokuString + "],  Puzzle = [A,B,C,D,E,F,G,H,I],  sudoku([A,B,C,D,E,F,G,H,I]).  "
	queryString = queryS
	res =  list(prolog.query(queryString, maxresult=1))	
	print res
	if not res:
		#results is empty
		return "Invalid Sudoku"
	else:	
		final = []
		cols = ["A","B","C","D","E","F","G","H","I"]
		for col in cols:
			final.append(" ".join(map( str,res[0][col])))
			
		return "<br>".join(final)

run(host="localhost", port="8080", debug=True)

