

função soma_n_primeiros(n){ -- Função que soma os n primeiros números
    local soma = 0  -- Variável que armazena a soma
    local contador = 1
    enquanto contador < n  ou contador == n{    -- equivalente a <=
        soma = soma + contador
        contador = contador + 1
    }        
    retorna soma
}

local variável
variável = 10
local resultado = soma_n_primeiros(variável)
exibir(resultado)
-- exibir(soma) esse comando não funcionaria pois a variável soma é local a função soma_n_primeiros


local Aáàãâ = 10
exibir(Aáàãâ) -- 10