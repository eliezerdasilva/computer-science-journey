function produto = produtoEscalar(u,v)
	n = length(u)
	produto = 0 
	for i =1:n
		produto=produto+u(i)*v(i)
	end
end

