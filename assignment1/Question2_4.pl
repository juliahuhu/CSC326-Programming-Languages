%Question 2
all_diff([]).
all_diff([H|T]):-
    \+member(H,T),
    all_diff(T).

%Question 3
no_dup( H, Y):-
	sort(H,Y).

%Question 4
verify(Sudoku, X):-
Sudoku = [
S00, S01, S02, S03, S04, S05, S06, S07, S08,
S10, S11, S12, S13, S14, S15, S16, S17, S18,
S20, S21, S22, S23, S24, S25, S26, S27, S28,
S30, S31, S32, S33, S34, S35, S36, S37, S38,
S40, S41, S42, S43, S44, S45, S46, S47, S48,
S50, S51, S52, S53, S54, S55, S56, S57, S58,
S60, S61, S62, S63, S64, S65, S66, S67, S68,
S70, S71, S72, S73, S74, S75, S76, S77, S78,
S80, S81, S82, S83, S84, S85, S86, S87, S88],

Row0 = [S00, S01, S02, S03, S04, S05, S06, S07, S08],
Row1 = [S10, S11, S12, S13, S14, S15, S16, S17, S18],
Row2 = [S20, S21, S22, S23, S24, S25, S26, S27, S28],
Row3 = [S30, S31, S32, S33, S34, S35, S36, S37, S38],
Row4 = [S40, S41, S42, S43, S44, S45, S46, S47, S48],
Row5 = [S50, S51, S52, S53, S54, S55, S56, S57, S58],
Row6 = [S60, S61, S62, S63, S64, S65, S66, S67, S68],
Row7 = [S70, S71, S72, S73, S74, S75, S76, S77, S78],
Row8 = [S80, S81, S82, S83, S84, S85, S86, S87, S88],

Col0 = [S00, S10, S20, S30, S40, S50, S60, S70, S80],
Col1 = [S01, S11, S21, S31, S41, S51, S61, S71, S81],
Col2 = [S02, S12, S22, S32, S42, S52, S62, S72, S82],
Col3 = [S03, S13, S23, S33, S43, S53, S63, S73, S83],
Col4 = [S04, S14, S24, S34, S44, S54, S64, S74, S84],
Col5 = [S05, S15, S25, S35, S45, S55, S65, S75, S85],
Col6 = [S06, S16, S26, S36, S46, S56, S66, S76, S86],
Col7 = [S07, S17, S27, S37, S47, S57, S67, S77, S87],
Col8 = [S08, S18, S28, S38, S48, S58, S68, S78, S88],

Squ0 = [S00, S01, S02, S10, S11, S12, S20, S21, S22],
Squ1 = [S03, S04, S05, S13, S14, S15, S23, S24, S25],
Squ2 = [S06, S07, S08, S16, S17, S18, S26, S27, S28],
Squ3 = [S30, S31, S32, S40, S41, S42, S50, S51, S52],
Squ4 = [S33, S34, S35, S43, S44, S45, S53, S54, S55],
Squ5 = [S36, S37, S38, S46, S47, S48, S56, S57, S58],
Squ6 = [S60, s61, s62, S70, S71, S72, S80, S81, S82],
Squ7 = [S63, S64, S65, S73, S74, S75, S83, S84, S85],
Squ8 = [S66, S67, S68, S76, S77, S78, S86, S87, S88],

all_diff(Row0),
all_diff(Row1),
all_diff(Row2),
all_diff(Row3),
all_diff(Row4),
all_diff(Row5),
all_diff(Row6),
all_diff(Row7),
all_diff(Row8),

all_diff(Col0),
all_diff(Col1),
all_diff(Col2),
all_diff(Col3),
all_diff(Col4),
all_diff(Col5),
all_diff(Col6),
all_diff(Col7),
all_diff(Col8),

all_diff(Squ0),
all_diff(Squ1),
all_diff(Squ2),
all_diff(Squ3),
all_diff(Squ4),
all_diff(Squ5),
all_diff(Squ6),
all_diff(Squ7),
all_diff(Squ8).


