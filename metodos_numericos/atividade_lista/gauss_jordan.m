function x = gauss_jordan(A, b)
  n = length(b);
  Aug = [A b];  % matriz aumentada

  % Gauss–Jordan
  for k = 1:n
    % Verifica pivô
    if Aug(k,k) == 0
      error('Pivô zero encontrado. Necessário pivotamento.');
    end

    % Normaliza a linha do pivô
    Aug(k, k:n+1) = Aug(k, k:n+1) / Aug(k, k);

    % Elimina os elementos acima e abaixo do pivô
    for i = 1:n
      if i != k
        fator = Aug(i, k);
        Aug(i, k:n+1) = Aug(i, k:n+1) - fator * Aug(k, k:n+1);
      end
    end
  end

  % A solução está na última coluna
  x = Aug(:, n+1);
disp( Aug(:, n+1) );	
end

