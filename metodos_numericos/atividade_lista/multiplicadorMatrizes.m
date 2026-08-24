function C = multiplicadorMatrizes(A,B)
	[m,n] = size(A)
	[p,q] = size(B)
	if n!=p
 		error('Numero de colunas de A deve ser igual ao numero de linhas de b')
	end
	C = zeros(m,p);
	for i = 1:m
		for j=1:p
			soma = 0 
				for k=1:n
				soma = soma + A(i,k) * B(k,j);
				end
			C(i,j)=soma
		end
	end
end
