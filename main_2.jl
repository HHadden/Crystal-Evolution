using DifferentialEquations, Plots, Printf, Random
include("pde.jl")

function loop()

    #println(rand())
    #println(bitrand(1)[1])

    index = 1

    io_1 = open("results_stable_5.txt", "w")
    io_2 = open("results_unstable_5.txt", "w")

    while index <= 2000

        #=rng_γ = rand()
        γ = 10 + 990 * rng_γ

        
        rng_A = rand()
        A = (7e-18 + 9.3e-17 * rng_A) * γ^2
        rng_B = rand()
        B = (1e-18 + 9e-18 * rng_B) * γ^2
        rng_D = rand()
        D = (1e-13 + 9e-13 * rng_D) * γ^2=#

        rng_γ = rand()
        exp_γ = 1 + 2 * rng_γ
        γ = 10^exp_γ

        rng_A = rand()
        exp_A = -15 + 9 * rng_A
        A = 10^exp_A * γ^2

        rng_B = rand()
        exp_B = -15 + 9 * rng_B
        B = 10^exp_B * γ^2

        rng_D = rand()
        exp_D = -20 + 8 * rng_D
        D = 10^exp_D * γ^2


    
        inputs = A, B, D, γ, index
        try
            rmax, tmax, tfail, stable = pde(inputs)
            println("Index:")
            println(index)

            str_A = @sprintf("%.6e",A)
            str_B = @sprintf("%.6e",B)
            str_D = @sprintf("%.6e",D)
            str_γ = @sprintf("%.6e",γ)
            str_rmax = @sprintf("%.6e",rmax)
            str_tmax = @sprintf("%.6e",tmax)
            str_tfail = @sprintf("%.6e",tfail)

            if stable == true
                write(io_1, "A:" * str_A * " B:" * str_B * " D:" * str_D * " γ:" * str_γ * " R_Max:" * str_rmax * " T_Max:" * str_tmax * " T_Fail:" * str_tfail * " Index:" * string(index) * "\n")
            end
            if stable == false
                write(io_2, "A:" * str_A * " B:" * str_B * " D:" * str_D * " γ:" * str_γ * " R_Max:" * str_rmax * " T_Max:" * str_tmax * " T_Fail:" * str_tfail * " Index:" * string(index) * "\n")
            end
        catch
        end
                    
        index = index + 1
    end
    close(io_1)
    close(io_2)
end


loop()