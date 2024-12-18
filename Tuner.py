import numpy as np
import pandas as pd
import tensorflow as tf
import keras
import keras_tuner
import math
from keras import layers
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle

def build_model(hp):
    model = keras.Sequential()
    model.add(keras.Input(shape=(4,)))
    for i in range(hp.Int("num_layers", 1, 5)):
        model.add(layers.Dense(units=hp.Int("units_" + str(i + 1), min_value=8, max_value=1024, step=8),
                               activation=hp.Choice("activation_" + str(i + 1),
                                                    values=["relu", "tanh", "selu", "elu", "exponential", "linear"])))
    model.add(layers.Dense(1, activation='sigmoid'))
    #model.add(layers.Dense(1, activation=hp.Choice("activation_final", values=["relu", "tanh", "selu", "elu", "exponential", "linear"])))
    model.compile(optimizer=hp.Choice("optimizer", values=["SGD", "RMSprop", "Adam", "Adadelta", "Adagrad", "Adamax", "Nadam", "Ftrl"]), loss="mean_squared_error",
                  metrics=["mean_absolute_percentage_error", "mean_absolute_error"])
    return model

def main():
    file = r'Daten7/Daten_binaer.xlsx'
    dfin = pd.read_excel(file, sheet_name='Input_4', header=None)
    dfout = pd.read_excel(file, sheet_name='Output_Stability', header=None)

    data = dfin.values
    labels = dfout.values

    data = np.emath.log10(data)

    datascaler = StandardScaler()
    datascaler.fit(data)
    data = datascaler.transform(data)

    mix = np.concatenate((data, labels), axis=1)
    mix = shuffle(mix)

    data_2, labels = np.hsplit(mix, np.array([4]))

    print(data_2)
    print(labels)

    epochs_search = 200
    epochs_fit = 200

    tuner = keras_tuner.Hyperband(
        build_model,
        objective="loss",
        max_epochs=epochs_search,
        executions_per_trial=1,
        hyperband_iterations=1,
        overwrite=True,
        directory="my_dir",
        project_name="Tuner_R_Max",
    )

    tuner.search_space_summary()
    results_tuner = tuner.search(data_2, labels, epochs=epochs_search, validation_split=0.2)

    models = tuner.get_best_models(num_models=3)
    tuner.results_summary()
    results = open("results.txt", "w+")
    results.write(str(results_tuner))
    i = 0

    while (i < 3):
        j = str(i)
        models[i].fit(data_2, labels, epochs=epochs_fit, validation_split=0.1)
        models[i].save('Tuner_Stablility_neu_' + j + '.h5')

        dot_img_file = 'Tuner_IE_AE_normalized2_valloss' + j + '.png'
        tf.keras.utils.plot_model(
            models[i],
            to_file=dot_img_file,
            show_shapes=True,
            show_dtype=False,
            show_layer_names=False,
            rankdir="TB",
            expand_nested=False,
            dpi=96,
            layer_range=None,
        )
        i+=1

if __name__ == '__main__':
    main()