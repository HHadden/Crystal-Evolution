import numpy as np
import pandas as pd
import keras
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def main():
    model = keras.models.load_model("Tuner_Stablility_neu_0.h5")
    #model = keras.models.load_model("Tuner_R_Max_neu_1.h5")
    #model_2 = keras.models.load_model("Model_Stability.h5")

    file = r'Daten7/Daten_binaer.xlsx'
    dfin = pd.read_excel(file, sheet_name='Input_4', header=None)
    data = dfin.values
    data = np.log10(data)
    datascaler = StandardScaler()
    datascaler.fit(data)

    """file_2 = r'Daten5/Daten_B.xlsx'
    dfin_2 = pd.read_excel(file_2, sheet_name='Input_4', header=None)
    data_2 = dfin_2.values
    data_2 = np.log10(data_2)
    datascaler_2 = StandardScaler()
    datascaler_2.fit(data_2)"""

    a = 2000
    b = 2000

    #A = np.logspace(-7, -4, a)
    #B = np.logspace(-7, -5, b)

    A = np.logspace(-9, -0, a)

    B = np.logspace(-9, -0, b)
    D = 1e-6
    gamma = 1000
    XD = np.full((a*b, 1), D)
    XG = np.full((a*b, 1), gamma)
    #Z = np.zeros((a, b))

    A1, A2 = np.meshgrid(A, B)

    #np.savetxt("meshgrid_1.txt", A1)
    #np.savetxt("meshgrid_2.txt", A2)

    X1 = np.reshape(A1, (a * b, 1))
    X2 = np.reshape(A2, (a * b, 1))

    X3 = np.concatenate((X1, X2), axis=1)
    X3 = np.concatenate((X3, XD), axis=1)
    X3 = np.concatenate((X3, XG), axis=1)

    print(X3)

    inputs_log = np.log10(X3)

    #print(inputs_log)
    inputs_scaled = datascaler.transform(inputs_log)
    #inputs_scaled_2 = datascaler_2.transform(inputs_log)

    #print(inputs_scaled)

    #inputs_scaled = datascaler.transform(X3)

    results = model.predict(inputs_scaled)
    #results_2 = model_2.predict(inputs_scaled_2)
    #results = np.power(10, results)
    #print(results)

    Z = np.reshape(results, (a, b))
    #Z_2 = np.reshape(results_2, (a, b))

    """i1 = 0
    while i1 < a:
        i2 = 0
        while i2 < b:
            if Z_2[i1, i2] > 0.5:
                Z[i1, i2] = np.nan
            i2 += 1
        i1 += 1"""

    """i1 = 0
    while i1 < a:
        i2 = 0
        while i2 < b:
            if Z[i1, i2] < -3 or Z[i1, i2] > -1.3:
                Z[i1, i2] = np.nan
            i2 += 1
        i1 += 1"""



    fig, ax = plt.subplots()

    #ax.contourf(A, B, Z, levels=levels)
    #pc = ax.pcolormesh(A1, A2, Z)

    #pc=ax.pcolormesh(A1, A2, Z, vmin=-4, vmax=-0)
    pc = ax.pcolormesh(A1, A2, Z, vmin=0, vmax=1, cmap='Greys')
    #pc = ax.contourf(A1, A2, Z, 20, cmap='Greys')
    #fig.colorbar(pc)

    fontsize = 12

    fig.colorbar(pc).ax.tick_params(labelsize=fontsize)

    plt.xlabel("A", fontsize=fontsize)
    plt.ylabel("B", fontsize=fontsize)
    plt.xscale("log")
    plt.yscale("log")
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    #plt.title("log(R_Max), D="+str(D)+", Gamma="+str(gamma), fontsize=15)
    plt.title("D=" + str(D) + ", Gamma=" + str(gamma), fontsize=15)

    plt.show()



if __name__ == '__main__':
    main()