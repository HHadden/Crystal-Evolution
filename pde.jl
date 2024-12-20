#u[1] = z
#u[2] = y
#u[3] = x
function olivine_loop(du, u, p, t)

    A, B, D, dx, n, N = p

    #zeitliche Ableitung von x
    du[n, 3] = A*(1-u[n, 2])

    for i in 2:n-1
        #time-derivative of z
        du[i, 1] = 1/u[n, 3]*(1/2*(dx*(i-1))*du[n,3]*((u[i+1,1]-u[i,1])/dx)+D*(((u[i-1, 1]-2u[i, 1]+u[i+1, 1])/(dx^2))+2/(dx*(i-1))*((u[i+1,1]-u[i,1])/dx)))
        
    end
    for i in n
        if (u[i, 1] > 1)
            u[i, 1] = 1
        elseif (u[i, 1] < 0)
            u[i, 1] = 0
        end        
    end
    integral = 0
    for i in 2:n-1
        integral = integral + dx * abs(((u[i-1, 1]-2u[i, 1]+u[i+1, 1])/(dx^2))-1/(dx*(i-1))*((u[i+1, 1]-u[i, 1])/dx))*(dx*(i-1))^2
        if (i == 2)
            integral = integral + dx * abs(((u[i-1, 1]-2u[i, 1]+u[i+1, 1])/(dx^2))-1/(dx*(i-1))*((u[i+1, 1]-u[i, 1])/dx))*(dx*(i-1))^2
        end
        if (i == n-1)
            integral = integral + dx * abs(((u[i-1, 1]-2u[i, 1]+u[i+1, 1])/(dx^2))-1/(dx*(i-1))*((u[i+1, 1]-u[i, 1])/dx))*(dx*(i-1))^2
        end
    end
    #time-derivative of y
    du[n, 2] = B/u[n, 3]*integral

    for i in 1:N
        #set all x and y equal
        u[i, 3] = u[n, 3]
        u[i, 2] = u[n, 2]
    end

    du[1, 1] = du[2, 1]


    if u[n, 3] <= 0
        for i in 1:n
            du[i, 1] = 0
            du[i, 2] = 0
            du[i, 3] = 0
            
            u[i, 1] = 0
            u[i, 2] = 0
            u[i, 3] = 0
        end
    end

    #time-derivative of x
    u[n, 1] = (sqrt(u[n, 3])*dx+u[n-1, 1])/(1+sqrt(u[n, 3])*dx)

end

function olivine_init(p2)
    n, γ, R0, dx = p2
    u = zeros(n, 3)
    for i in 1:n
        u[i, 3] = γ^2*R0^2
    end
    for i in 1:n
        u[i, 1] = sqrt(u[i, 3])/(2+sqrt(u[i, 3]))*(dx*(i-1))^2
        #u[i, 1] = γ*R0/(1+γ*R0/2)
    end
    return u
end

function  pde(inputs)
    A, B, D, γ, index = inputs

    tend = 1e-6
    R0 = 1e-8
    N = 40
    #N = 20
    n = N+1
    dx = 1/N

    p = A, B, D, dx, n, N
    p2 = n, γ, R0, dx
    global sol

    solver = "Tsit5"

    
    fail = false
    stable = true
    u0 = olivine_init(p2)

    i = 1

    while fail == false && tend < 1e16
        if stable == true
            tend = tend * 100
        else
            tend = tend * 10
        end
        prob_ode_olivine = ODEProblem(olivine_loop,u0,(0.,tend),p)
        println("Solve:")
        @time sol = solve(prob_ode_olivine,Tsit5())
        #@time sol = solve(prob_ode_olivine,Vern9())
        t = 0
        tstep = tend / 100
        rmax = 0
        tmax = 0
        while t < tend && fail == false
            r = sol(t)[n,3]
            if r > rmax
                rmax = r
                tmax = t
            end
            if r < rmax && stable == true
                stable = false
            end
            #if r < 1.0e-14 && fail == false
            if r < 1.0e-14 && stable == false
                fail = true
                #println("Fail: True")
            end
            t = t + tstep
        end
        println("Stable: " * string(stable))
        println("Fail: " * string(fail))
        println("Index: " * string(i))
        #=if fail == true || tend >= 1e16
            println("Plot:")
            plot_ref = plot(sol,vars=(0,3*n), lw=4, guidefontsize=14, tickfontsize = 9, legend=false)
            png(plot_ref, "Plot_" * solver * "_" * string(index) * "_" * string(i) * "_x")
            println("Plot:")
            plot_ref = plot(sol,vars=(0,2*n), ylims = (0, 5), lw=4, guidefontsize=14, tickfontsize = 9, legend=false)
            png(plot_ref, "Plot_" * solver * "_" * string(index) * "_" * string(i)* "_y")
        end=#
        i += 1
    end

    tstep = tend / 10000
    t = 0
    rmax = 0
    tmax = 0
    tfail = 0
    stable = true
    fail = false

    while t < tend && fail == false
        r = sol(t)[n,3]
        if r > rmax
            rmax = r
            tmax = t
        end
        if r < rmax && stable == true
            stable = false
        end
        #if r < 1.0e-14 && fail == false
        if r < 1.0e-14 && stable == false
            fail = true
            tfail = t
            #println("Fail: True")
        end
        t = t + tstep
    end
    if fail == false
        tfail = tend
    end
    #=t = tmax
    output = zeros(n, 2)
        for i in 1:n 
            output[i, 1] = sol(t)[i, 1]
            output[i, 2] = dx * (i-1)
        end
        println("Plot:")
        plot_ref = plot(output[:, 2], output[:, 1], lw=4, guidefontsize=14, tickfontsize = 9, legend=false)
        png(plot_ref, "Plot_" * solver * "_" * string(index) * "_z_tmax")
    t = tfail * 0.99
    output = zeros(n, 2)
        for i in 1:n 
            output[i, 1] = sol(t)[i, 1]
            output[i, 2] = dx * (i-1)
        end
        println("Plot:")
        plot_ref = plot(output[:, 2], output[:, 1], lw=4, guidefontsize=14, tickfontsize = 9, legend=false)
        png(plot_ref, "Plot_" * solver * "_" * string(index)* "_z_tfail")=#
    R_Max = sqrt(rmax/γ^2)
    return rmax, tmax, tfail, stable, R_Max
end