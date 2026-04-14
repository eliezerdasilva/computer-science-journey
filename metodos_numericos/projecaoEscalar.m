function projecao = projecao(u,v)
	if norma_vetor(v)==0
		error('Vetor nao pode ser nulo ')
	end
	s = produtoEscalar(u,v)/norma_vetor(v)
end

