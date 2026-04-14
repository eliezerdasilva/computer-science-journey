% Exercício 14: Matriz A com números inteiros
A = [4 1 0 0;
     1 4 1 0;
     0 1 4 1;
     0 0 1 4];

fprintf('=== EXERCÍCIO 14 ===\n');
fprintf('Matriz A (inteiros):\n');
disp(A);

% Verificações
fprintf('Determinante: %d\n', det(A));
fprintf('Número de condição: %.2f\n', cond(A));
fprintf('Diagonal: %d %d %d %d\n', diag(A));

% Exercício 15: Vetor x e b
x = [1; 2; 3; 4];
b = A * x;

fprintf('\n=== EXERCÍCIO 15 ===\n');
fprintf('Vetor x:\n');
disp(x);
fprintf('Vetor b = A*x:\n');
disp(b);

% Exercício 16: Decomposição LU (implementação manual)
function [L, U] = lu_decomposition_int(A)
  n = size(A, 1);
  L = eye(n);
  U = A;
  
  for k = 1:n-1
    for i = k+1:n
      if U(k,k) == 0
        error('Pivô zero. Necessário pivotamento.');
      end
      L(i,k) = U(i,k) / U(k,k);
      for j = k:n
        U(i,j) = U(i,j) - L(i,k) * U(k,j);
      end
    end
  end
end

fprintf('\n=== EXERCÍCIO 16 ===\n');
[L, U] = lu_decomposition_int(A);

fprintf('Matriz L (triangular inferior):\n');
disp(L);

fprintf('Matriz U (triangular superior):\n');
disp(U);

% Verificar A = L*U
fprintf('\nVerificação - L*U:\n');
disp(L * U);

fprintf('Erro máximo: %e\n', max(max(abs(A - L*U))));

% Resolver sistema usando LU
function x = lu_solve(L, U, b)
  n = length(b);
  % Substituição progressiva: L*y = b
  y = zeros(n,1);
  for i = 1:n
    y(i) = b(i);
    for j = 1:i-1
      y(i) = y(i) - L(i,j) * y(j);
    end
  end
  
  % Retrosubstituição: U*x = y
  x = zeros(n,1);
  for i = n:-1:1
    x(i) = y(i);
    for j = i+1:n
      x(i) = x(i) - U(i,j) * x(j);
    end
    x(i) = x(i) / U(i,i);
  end
end

% Resolver o sistema
x_calc = lu_solve(L, U, b);

fprintf('\n--- Solução do sistema ---\n');
fprintf('x calculado:\n');
disp(x_calc);
fprintf('Solução esperada:\n');
disp(x);
fprintf('Erro: %e\n', norm(x_calc - x));

% Método alternativo usando \ do Octave
fprintf('\n--- Usando operador \\ do Octave ---\n');
x_octave = A \ b;
disp(x_octave);
