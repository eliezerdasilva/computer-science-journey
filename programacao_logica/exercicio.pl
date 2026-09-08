% Exercicio familia do João

pai(joao,maria).
pai(joao,marcos).
pai(joao,joana).
pai(joao,pedro).
pai(pedro,ricardo).
pai(pedro,bruno).
pai(bruno,victor).

sexo(joao,masculino).
sexo(maria,feminino).
sexo(pedro,masculino).
sexo(marcos,masculino).
sexo(joana,feminino).
sexo(ricardo,masculino).
sexo(bruno,masculino).
sexo(victor,masculino).

avo(X,Y) :- pai(X,Z),pai(Z,Y).
irmao(X,Y) :- 
	pai(P,X),
	pai(P,Y),
	X\= Y,
	sexo(X,masculino).

irma(X,Y) :-
	pai(P,X),
	pai(P,Y),
	X\=Y,
	sexo(X,feminino).

neto(X,Y) :- 
	pai(Y,Z),
	pai(Z,X),
	sexo(X,masculino).
neta(X,Y) :-
	pai(Y,Z),
	pai(Z,X),
	sexo(X,feminino).

bisneto(X,Y) :-
	pai(Y,Z),
	pai(Z,W),
	pai(W,X),
	sexo(X,masculino).

% Exercicio alunos
aluno(maria).
aluno(joao).
aluno(felipe).
aluno(bruno).

nota(maria,8.5).
nota(joao,6.0).
nota(felipe,9.0).
nota(bruno,7.0).

passou(X) :-
	nota(X,N),
	N>= 7.

frequencia(maria,80).
frequencia(joao,90).
frequencia(felipe,70).
frequencia(bruno,60).

passou2(X) :-
	nota(X,N),
	N >=7,
	frequencia(X,F),
	F>= 75.


reprovado(X) :-
	aluno(X),
	nota(X,N),
	N >= 0, N =< 10,
	frequencia(X,F),
	F>=75 , F=< 100,
	\+ passou2(X).


% potencia
pot(_,0,1):- !.
pot(B,1,B):- !.
pot(B,E,R) :-
	E > 1,
	E1 is E - 1,
	pot(B,E1,R1),
	R is R1 * B.  
 
