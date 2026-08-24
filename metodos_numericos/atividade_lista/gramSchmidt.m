function [Q, R] = gram_schmidt(A, normalizar)
  
  
  if nargin < 2
    normalizar = false;
  end

  [m, n] = size(A);
  if m < n
    error('Número de linhas deve ser >= número de colunas.');
  end

  Q = zeros(m, n);
  R = zeros(n, n);

  for j = 1:n
    % Inicia com a coluna j de A
    v = A(:, j);
    
    % Subtrai as projeções sobre os vetores já ortogonalizados
    for i = 1:j-1
      
      dot_v_qi = 0;
      % 0 a primeira fez	
      for k = 1:m
        dot_v_qi = dot_v_qi + v(k) * Q(k, i);
      end
      % 0 primeira fez
      dot_qi_qi = 0;
      for k = 1:m
        dot_qi_qi = dot_qi_qi + Q(k, i) * Q(k, i);
      end
      if dot_qi_qi > eps
        coef = dot_v_qi / dot_qi_qi;
      else
        coef = 0;   % Q(:,i) é zero (dependência linear)
      end
      R(i, j) = coef;
      % Subtrai a projeção
      for k = 1:m
        v(k) = v(k) - coef * Q(k, i);
      end
    end

    % Calcula a norma do vetor resultante
    norm_v = 0;
    for k = 1:m
      norm_v = norm_v + v(k)^2;
    end
    norm_v = sqrt(norm_v);

    if norm_v < eps
      warning('Coluna %d é combinação linear das anteriores. Vetor nulo em Q.', j);
      Q(:, j) = zeros(m, 1);
      if normalizar
        R(j, j) = 0;
      else
        R(j, j) = 1;   % valor arbitrário para manter triangularidade
      end
    else
      if normalizar
        % Normaliza o vetor
        for k = 1:m
          Q(k, j) = v(k) / norm_v;
        end
        R(j, j) = norm_v;
      else
        % Mantém o vetor ortogonal (não normalizado)
        Q(:, j) = v;
        R(j, j) = 1;
      end
    end
  end

  % Se normalizou, recalcula R = Q' * A (garante consistência)
  if normalizar
    R2 = zeros(n, n);
    for i = 1:n
      for j = 1:n
        dot = 0;
        for k = 1:m
          dot = dot + Q(k, i) * A(k, j);
        end
        R2(i, j) = dot;
      end
    end
    R = R2;
  end
end
