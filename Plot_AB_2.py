import numpy as np
import pandas as pd
import keras
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def main():
    #Use this model to plot the stability"
    model = keras.models.load_model("Tuner_Stablility_neu_0.h5")

    #Use this model to plot the logarothm of the maximum radius"
    #model = keras.models.load_model("Tuner_R_Max_neu_1.h5")

    file = r'Daten_binaer.xlsx'
    file = r'Daten_unstable.xlsx'
    dfin = pd.read_excel(file, sheet_name='Input_4', header=None)
    data = dfin.values
    data = np.log10(data)
    datascaler = StandardScaler()
    datascaler.fit(data)

    a = 2000
    b = 2000

    A = np.logspace(-9, -0, a)
    B = np.logspace(-9, -0, b)
    D = 1e-6
    gamma = 1000
    XD = np.full((a*b, 1), D)
    XG = np.full((a*b, 1), gamma)
    #Z = np.zeros((a, b))

    A1, A2 = np.meshgrid(A, B)

    X1 = np.reshape(A1, (a * b, 1))
    X2 = np.reshape(A2, (a * b, 1))

    X3 = np.concatenate((X1, X2), axis=1)
    X3 = np.concatenate((X3, XD), axis=1)
    X3 = np.concatenate((X3, XG), axis=1)

    print(X3)

    inputs_log = np.log10(X3)

    inputs_scaled = datascaler.transform(inputs_log)

    results = model.predict(inputs_scaled)

    Z = np.reshape(results, (a, b))

    fig, ax = plt.subplots()

    pc = ax.pcolormesh(A1, A2, Z, vmin=0, vmax=1, cmap='Greys')

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