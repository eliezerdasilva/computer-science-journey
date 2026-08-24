function x = gauss_elimination(A, b)
  n = length(b);
  Aug = [A b];  % matriz aumentada

  % Fase de eliminação (triangularização)
  for k = 1:n-1
    for i = k+1:n
	
      if Aug(k,k) == 0
        error('Pivô zero encontrado. Necessário pivotamento.');
      end
      fator = Aug(i,k) / Aug(k,k);
 	disp(fator);
      Aug(i, k:n+1) = Aug(i, k:n+1) - fator * Aug(k, k:n+1);
	disp(Aug);   
 end
  end

  % Retrosubstituição
  x = zeros(n,1);
  for i = n:-1:1
    x(i) = (Aug(i, n+1) - Aug(i, i+1:n) * x(i+1:n)) / Aug(i,i);
	disp(i)
	disp(x)
  end
end
