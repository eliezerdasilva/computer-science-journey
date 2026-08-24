function norma = norma_vetor(v)
	n = length(v)
	soma_quadrado =0
	for i =1:n
		soma_quadrado = soma_quadrado + v(i)^2
	end
	norma =sqrt(soma_quadrado)
end
