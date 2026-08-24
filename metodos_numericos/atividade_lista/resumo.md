* ELIMINAÇÃO GAUSSIANA

Transformar um sistema linear Ax=bAx=b em um sistema triangular superior (equivalente) através de operações elementares, permitindo resolver por retrossubstituição.

1- Matriz aumentada [A b]
Para cada coluna k=1,2,…,n−1k=1,2,…,n−1:
Para cada linha i = k+1,..,n;
Mik=Aik/Akk
Aij = Aij-Mik*Akj para j = k,k+1,...,n
Bi=Bi-Mik*Bk

Retrossubstituição 
i​=​(bi​−∑  de j=i+1 ate n Aij​xj)/Aii

​​Fase de eliminação e retrosubstituicao separadas

Acha o fator que é o elemento a ser zerado e divide pelo pivo

depois pega elemento por elementos dessa linha menos o fator * cada elemento da linha do pivo 


Agora no processo de retrosubstituicao faca o loop inverso 

Vamos achar cada x. 

x(i) = (Aug(i, n+1) - Aug(i, i+1:n) * x(i+1:n)) / Aug(i,i);

Da para normalizar o vetor. 

* 2 Cholesky

- Importante: 

Diagonal : R(i,i) = sqrt(A(i,i) - sum(R(1:i-1,i).^2));

Fora da Diagonal : for j = i+1:n
      R(i,j) = (A(i,j) - sum(R(1:i-1,i) .* R(1:i-1,j))) / R(i,i);
    end


* 3 Decomposicao LU

A = L*U


Para cada k=1,2,…,nk=1,2,…,n:


Passo 1: Calcular linha kk de UU (elementos j=k,…,nj=k,…,n)
Ukj=Akj−∑ de p=1  ate k−1 Lkp⋅Upj
Ukj​=Akj​−p=1∑k−1​Lkp​⋅Upj​

Passo 2: Calcular coluna kk de LL (elementos i=k+1,…,ni=k+1,…,n)
Lik= (1/Ukk )*(Aik−∑ de p=1 ate k−1 Lip⋅Upk)


Se Ukk=0Ukk​=0, erro → matriz singular ou precisa pivotamento.

* 4 Decomposicao PA=LU


