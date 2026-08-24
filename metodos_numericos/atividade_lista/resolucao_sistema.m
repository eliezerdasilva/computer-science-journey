function x = resolucao_sistema(A,b)
    Aug = [A b];
    U = gauss_sem_pivot(Aug);
    % U esta escalonada
    [m,n_total] = size(U);
    n = n_total - 1;  % número de incógnitas

    % Extrair b_mod ANTES de modificar U
    b_mod = U(:, n_total);  % última coluna da matriz modificada

    % Agora sim, remove a última coluna
    U = U(:, 1:n);

    disp('Matriz U triangular:');
    disp(U);
    disp('Vetor b modificado:');
    disp(b_mod);

    % Substituição reversa
    x = zeros(n,1);

    for i = n:-1:1
        soma = 0;
        for j = i+1:n
            soma = soma + U(i,j) * x(j);
        end
        x(i) = (b_mod(i) - soma) / U(i,i);
    end
end
