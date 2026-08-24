function U = gauss_sem_pivot(A)
	[m,n]=size(A)
	U = A;
	% A funcao min ela pega o menor valor, é necessario para escalonar
	for i =1:min(m,n)
		% abs é o modulo
		if abs(U(i,i)) < eps
			error('Pivo zero encontrado. Necessario pivoteamento')
		end
		%eliminar abaixo do pivo		
		% m comeca tipo na linha 2 e coluna 1 
		for j = i+1:m 
			if U(j,i)!=0
				fator = U(j,i)/U(i,i);
				% aqui é a parte das operacoes as linhas
				for k =i:n
					U(j,k) = U(j,k)- fator * U(i,k);
				end
			end
		end
	end
end
			
		
