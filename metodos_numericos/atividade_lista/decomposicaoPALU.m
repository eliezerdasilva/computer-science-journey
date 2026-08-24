function [P, L, U] = decomposicaoPA_LU(A)
  % DECOMPOSICAO PA = LU com pivotamento parcial
  %   P - matriz de permutacao (tal que P*A = L*U)
  %   L - triangular inferior com diagonal unitaria
  %   U - triangular superior
  %   A - matriz quadrada (pode ser singular)
  
  [n, m] = size(A);
  if n != m
    error('Matriz não quadrada');
  end
  
  % Inicializacao
  L = eye(n);        % diagonal unitaria
  U = zeros(n);      % sera preenchida
  P = eye(n);        % matriz de permutacao (comeca como identidade)
  
  % Copia da matriz A para trabalhar (opcional)
  M = A;             % M sera modificada durante o processo
  
  for k = 1:n
    % ========== PASSO 1: PIVOTAMENTO PARCIAL ==========
    % Encontrar o maior elemento em modulo na coluna k (linhas k..n)
    pivo_linha = k;
    max_val = abs(M(k, k));
    for i = k+1:n
      if abs(M(i, k)) > max_val
        max_val = abs(M(i, k));
        pivo_linha = i;
      end
    end
    
    % ========== PASSO 2: VERIFICAR SINGULARIDADE ==========
    if max_val < eps
      error('Matriz singular (pivo zero na coluna %d)', k);
    end
    
    % ========== PASSO 3: TROCAR LINHAS (se necessario) ==========
    if pivo_linha != k
      % Trocar linhas em M (matriz que esta sendo fatorada)
      M([k, pivo_linha], :) = M([pivo_linha, k], :);
      
      % Trocar linhas em L (apenas colunas 1..k-1, pois o resto ainda e zero)
      L([k, pivo_linha], 1:k-1) = L([pivo_linha, k], 1:k-1);
      
      % Trocar linhas em P (registrar a permutacao)
      P([k, pivo_linha], :) = P([pivo_linha, k], :);
    end
    
    % ========== PASSO 4: CALCULAR LINHA k DE U ==========
    for j = k:n
      soma = 0;
      for p = 1:k-1
        soma = soma + L(k, p) * U(p, j);
      end
      U(k, j) = M(k, j) - soma;
    end
    
    % ========== PASSO 5: VERIFICAR PIVO ATUAL ==========
    if abs(U(k, k)) < eps
      error('Pivo zero na posicao (%d,%d) apos pivotamento', k, k);
    end
    
    % ========== PASSO 6: CALCULAR COLUNA k DE L ==========
    for i = k+1:n
      soma = 0;
      for p = 1:k-1
        soma = soma + L(i, p) * U(p, k);
      end
      L(i, k) = (M(i, k) - soma) / U(k, k);
    end
  end
end