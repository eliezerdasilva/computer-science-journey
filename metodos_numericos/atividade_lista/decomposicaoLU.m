function [L,U]= decomposicaoLU(A)
	[n,m]=size(A)
	if n!=m
		error('Matriz não quadrada')
	end
	L = eye(n)
	U = zeros(n)
	
	for k=1:n
		for j = k :n
			soma = 0
			for p = 1:k-1
				
				soma = soma + L(k,p)* U(p,j);
			end
			U(k,j) = A(k,j) - soma
			disp(U)
		end
		
		if abs(U(k,k))<eps
			error('Pivo zero')
		end
		for i = k+1:n
			soma =0 
			for p=1:k-1
				soma = soma +L(i,p)*U(p,k)
			end
			disp(L)
			L(i,k) = (A(i,k)-soma)/U(k,k);
			disp(L)
		end
end
