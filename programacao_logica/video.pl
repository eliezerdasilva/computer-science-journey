main :- read(X),(X== end_on_file -> true; verificaSinal(X),main).

verificaSinal(X) :- (X>0 -> write("Valor positivo."),nl;(X =:= 0-> write("Valor nulo."),nl;write("Valor negativo."),nl)).

:- initialization(main).
