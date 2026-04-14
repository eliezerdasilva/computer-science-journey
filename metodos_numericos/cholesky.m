function R = cholesky(A)
  % Cholesky simplificado
  n = size(A, 1);
  R = zeros(n, n);
  
  for i = 1:n
    % Diagonal
    R(i,i) = sqrt(A(i,i) - sum(R(1:i-1,i).^2));
    disp(sum(R(1:i-1,i).^2))
    
    % Fora da diagonal
    for j = i+1:n
      R(i,j) = (A(i,j) - sum(R(1:i-1,i) .* R(1:i-1,j))) / R(i,i);
    end
  end
end

disp(R)


function x = cholesky_solve(A, b)
  R = cholesky(A);
  n = length(b);
  
  % Substituição progressiva (R' * y = b)
  y = zeros(n, 1);
  for i = 1:n
    y(i) = (b(i) - R(1:i-1,i)' * y(1:i-1)) / R(i,i);
  end
  
  % Retrosubstituição (R * x = y)
  x = zeros(n, 1);
  for i = n:-1:1
    x(i) = (y(i) - R(i,i+1:n) * x(i+1:n)) / R(i,i);
  end
end

% Teste
A = [4 1 0 0; 1 4 1 0; 0 1 4 1; 0 0 1 4];
b = A * [1; 2; 3; 4];
x = cholesky_solve(A, b);
disp(x);
