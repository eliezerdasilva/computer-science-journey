function p = projecaoVetorial(u,v)
	v_dot_v = produtoEscalar(v,v)
	if v_dot_v ==0
		error('Vetor nao pode ser nulo')
	end
	fator = produtoEscalar(u,v)/v_dot_v
	n =length(v)
	p = zeros(size(v))
	for i =1:n
		p(i) = fator * v(i)
	end
end


	
	
