import numpy as np
import pandas as pd
import matplotlib as plot
from pysr import PySRRegressor
from sklearn.utils import shuffle
np.set_printoptions(threshold=np.inf)


def main():
    file = r'Daten_binaer.xlsx'

    dfin = pd.read_excel(file, sheet_name='Input_4', header=None)
    dfout = pd.read_excel(file, sheet_name='Output_Stability', header=None)

    data = dfin.values
    labels = dfout.values

    #data = np.emath.log10(data)

    mix = np.concatenate((data, labels), axis=1)
    mix = shuffle(mix)

    data_2, labels = np.hsplit(mix, np.array([4]))

    """cut = np.concatenate((data, labels), axis=1)
    i = cut.shape[0]

    while i > 0:
        i -= 1
        if cut[i, 4] > 20:
            cut = np.delete(cut, i, 0)

    print(cut.shape[0])

    data, labels = np.hsplit(cut, np.array([4]))"""

    model = PySRRegressor(
        binary_operators=["+", "*", "-", "/", "^"],
        #binary_operators=["+", "*", "-", "/"],
        unary_operators=["square", "cube", "exp", "log10", "sqrt", "tanh"],
        #unary_operators=["square", "cube"],
        constraints={'^': (-1,1)},
        niterations=40,
        populations=30,
        population_size=66,
        ncycles_per_iteration=550,
        elementwise_loss="L2MarginLoss()",
        model_selection='accuracy'
    )
    model.fit(data, labels)
    print(model)
    print(model.latex())




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
