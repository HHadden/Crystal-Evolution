import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def function_1(x, a, b):
    function = a * x**b
    return np.log10(function)

def function_2(x, a, b, c, d, f, g, i, j):
    x0 = x[:, 0] / (x[:, 2]**2)
    x1 = x[:, 1] / (x[:, 2]**2)
    function = a * x0 ** b + c * x1 * np.log10(x0 * d / ((x1 * 1e11) ** g) + f)
    function = function * (x[:, 2] ** i * j)
    #function = function * (x[:, 2] ** 1.8 * 4)
    #function = a * x[:, 0]**b / x[:, 2]**2+ c * x[:, 1] * x[:, 2]**2 * np.log10(x[:, 0]/ x[:, 2]**2*d / ((x[:, 1]/ x[:, 2]**2 * 1e9) ** g) + f)
    i = 0
    length = function.shape[0]
    while i < length:
        if function[i] > 0:
            function[i] = np.log10(function[i])
        else:
            #function[i] = function[i]-12
            #function[i] = c * x[i, 1] * x[i, 2]**2 * np.log10(x[i, 0]*d / ((x[i, 1] * 1e11) ** g) + f)-12
            function[i] = c * x1[i] * np.log10(x0[i] * d / ((x1[i] * 1e11) ** g) + f) - 14 + np.log10(x[i, 2])
        i += 1
    #return np.log10(function)
    return function

def function_2_out(x, a, b, c, d, f, g, i, j):
    x0 = x[:, 0] / (x[:, 2]**2)
    x1 = x[:, 1] / (x[:, 2]**2)
    function = a * x0 ** b + c * x1 * np.log10(x0 * d / ((x1 * 1e11) ** g) + f)
    function = function * (x[:, 2] ** i * j)
    #function = function * (x[:, 2]**1.8*4)
    #function = a * x[:, 0]**b / x[:, 2]**2+ c * x[:, 1] * x[:, 2]**2 * np.log10(x[:, 0]*d / ((x[:, 1] * 1e11) ** g) + f)
    return function

def main():
    data_1 = np.loadtxt("threshold_neu_1.txt")
    data_2 = np.loadtxt("threshold_neu_2.txt")
    data_3 = np.loadtxt("threshold_neu_3.txt")
    data_0 = np.concatenate((data_1, data_2, data_3), axis=0)
    data = data_0
    length = data.shape[0]
    n = 0
    while n < length:
        if data[n, 1] <= (1.01e-14*data[n, 3]**2):
            data = np.delete(data, n, axis=0)
            length-=1
        else:
            n+=1
    #print(data)
    #np.savetxt("Test_2.txt", data)
    inp_1, inp_2, inp_3, inp_4, inp_5 = np.hsplit(data, 5)
    inp = np.concatenate((inp_1, inp_3, inp_4), axis=1)
    #np.savetxt("Test.txt", inp)
    out = np.squeeze(inp_2)
    out = np.log10(out)


    #p = np.array(([4.94579324e-01, 9.82411759e-01, 1.76894984e+01, 1.12221611e+12, 1.11708140e-04, 9.95568252e-01, 1.8, 4]))
    p = np.array(([4.94579324e-01, 9.82411759e-01, 1.76894984e+01, 1.12221611e+12, 1.11708140e-04, 9.95568252e-01, 2, 1]))
    #p = np.array(([0.66, 0.98838684, 1.5e1, 1.5e19, 0.2, 0.5]))


    popt, pcov = curve_fit(function_2, inp, out, p0=p, maxfev=100000000, bounds=(0, [1e20, 1, 1e20, 1e20, 1, 1, 100, 100]))

    print(popt)
    #print(pcov)

    a, b, c, d, f, g, h, j = popt

    curve = np.split(data_0, 240)
    i = 79
    length = curve[i].shape[0]
    n = 0
    while n < length:
        if curve[i][n, 1] <= (1.01e-14*curve[i][n, 3]**2):
            curve[i] = np.delete(curve[i], n, axis=0)
            length -= 1
        else:
            n += 1
    inp_1, inp_2, inp_3, inp_4, inp_5 = np.hsplit(curve[i], 5)
    inp = np.concatenate((inp_1, inp_3, inp_4), axis=1)


    calc = function_2_out(inp, a, b, c, d, f, g, h, j)
    #np.savetxt("Test2.txt", calc)

    fontsize = 12

    #plt.plot(curve[i][:, 0], np.log10(curve[i][:, 1]), label="data")
    plt.plot(curve[i][:, 0], curve[i][:, 1], label="data", linewidth=3)
    plt.plot(curve[i][:, 0], calc, label="function", linewidth=3)

    plt.xlabel("A", fontsize=fontsize)
    plt.ylabel("B", fontsize=fontsize)

    plt.title("D=1e-06 Gamma=1000", fontsize=15)

    plt.xscale("log")
    plt.yscale("log")

    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.legend(fontsize=fontsize)
    plt.show()



if __name__ == '__main__':
    main()
