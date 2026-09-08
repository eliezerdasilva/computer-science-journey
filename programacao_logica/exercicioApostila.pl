% lista o ultimo elemento 
last([X],X).

last([_|T],X) :- last(T,X).  


efface([X|T],X,T).
% remove o elemento x da lista
efface([H|T],X,[H|L2]) :-
	H \= X,
	efface(T,X,L2).
% deleta todos
delete1([H|T],X,[H|L2]):-
	H\=X,
	delete1(T,X,L2).

fat(0,1):- !.
fat(N,F):- N1 is N -1, fat(N1,F1), F is F1*N.

% leitura
pequeno :- read(N), N <50.

% write() en ln para pular linha

processar_arquivo(Nome):-
	open(Nome,read,Stream),
	processar_stream(Stream),
	close(Stream).
processar_stream(Stream):-
	read(Stream,Termo),
	(Termo == end_of_file
	-> true
	; processar_termo(Termo),
	processar_stream(Stream)).

processar_termo(Termo) :-
	write('Lido: '), write(Termo),nl.	

estrelas(0):-!.
estrelas(N):-
	N>0,
	write('*'),
	N1 is N - 1,
	estrelas(N1).

% outra forma
estrelas(N):-
	N>=0,
	forall(between(1,N,_),write('*')).



