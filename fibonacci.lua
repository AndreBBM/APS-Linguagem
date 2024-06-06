local n = 10
local num1 = 0
local num2 = 1
local next_number = num2  
local count = 1
 
enquanto (count < n ou count == n) {
    exibir(next_number)
    count = count + 1
    num1 = num2
    num2 = next_number
    next_number = num1 + num2
}

função Fibonacci(n){
    local num1 = 0
    local num2 = 1
    local next_number = num2  
    local count = 1
    
    enquanto (count < n ou count == n) {
        exibir(next_number)
        count = count + 1
        num1 = num2
        num2 = next_number
        next_number = num1 + num2
    }
}

local k = 20
exibir("Fibonacci de " .. k .. " números:")
Fibonacci(k)    -- Fibonacci de 20 números