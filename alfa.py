import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def open_file(filename):
    try:

        with open(filename, mode='r') as file:
            content: str = file.read().splitlines()

    except PermissionError:
        print('Permission denied')

    return content


def list_files(directory):
    r = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.txt':
                r.append(os.path.join(subdir, file))
    return r


folder = '/home/kacper/Dokumenty/alfaHPM/2018-09-24'

filelist = list_files(folder)

n = 0
while n < len(filelist):

    currentfile: list = open_file(filelist[n])
    output = []

    for element in currentfile[3:]:
        freq = element.split()[0]
        freq = float(freq)
        epsRe = element.split()[1]
        epsRe = float(epsRe)
        epsIm = element.split()[2]
        epsIm = float(epsIm)
        muRe = element.split()[3]
        muRe = float(muRe)
        muIm = element.split()[4]
        muIm = float(muIm)

        stalaeps = 8.854187818E-12 * 2 * np.pi * freq * 10E9
        stalami = 1.256637061E-6 * 2 * np.pi * freq * 10E9

        epsilon: complex = np.complex(0, 1) * np.complex(epsRe, -epsIm) * stalaeps
        mi: complex = np.complex(0, 1) * stalami * np.complex(muRe, -muIm)

        gama = np.sqrt(mi * epsilon)
        alfa = np.real(gama)
        alfadB = 8.686 * alfa

        output.append((freq, stalaeps, stalami, epsRe, epsIm, muRe, muIm, epsilon, mi, gama, alfa, alfadB))

    outputpd = pd.DataFrame(data=output,
                            columns=['freq[GHz]', 'stalaeps', 'stalami', 'epsRe', 'epsIm', 'muRe', 'muIm', 'epsilon',
                                     'mi',
                                     'gama', 'alfa', 'alfa[dB/m]'])

    csvfilename = filelist[n].replace('.txt', '.csv')
    outputpd.to_csv(csvfilename, sep='\t', encoding='utf-8')

    try:
        plotfilename = filelist[n].replace('.txt', '')
        outputpd.plot(x='freq[GHz]', y='alfa[dB/m]')
        plt.savefig(plotfilename)
        plt.close()

    except TypeError:
        print(f'coś nie tak z plikiem {filelist[n]}')

    n += 1
