import os
import numpy as np
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt


def open_file(filename):
    try:

        with open(filename, mode='r') as file:
            content: str = file.read().splitlines()

    except PermissionError:
        print('Permission denied')

    return content


def close_file(filename, content):
    try:

        with open(filename, mode='w') as file:
            file.write(content)

    except PermissionError:
        print('Permission denied')


def list_files(directory):
    r = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.txt':
                r.append(os.path.join(subdir, file))
    return r


def merge_dicts(*dict_args):
    result = {}

    return result


folder = '/home/kacper/Dokumenty/alfaHPM/testy'

filelist = list_files(folder)
pprint(filelist[0])

currentfile = []
currentfile = open_file(filelist[0])
csvfilename = filelist[0].replace('.txt', '.csv')

output = []

for element in currentfile[3:]:
    freq = element.replace(',', '.').split()[0]
    freq = float(freq)
    epsRe = element.replace(',', '.').split()[1]
    epsRe = float(epsRe)
    epsIm = element.replace(',', '.').split()[2]
    epsIm = float(epsIm)
    muRe = element.replace(',', '.').split()[3]
    muRe = float(muRe)
    muIm = element.replace(',', '.').split()[4]
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
                        columns=['freq[GHz]', 'stalaeps', 'stalami', 'epsRe', 'epsIm', 'muRe', 'muIm', 'epsilon', 'mi',
                                 'gama', 'alfa', 'alfa[dB/m]'])

csvfilename = filelist[0].replace('.txt', '.csv')
outputpd.to_csv(csvfilename, sep='\t', encoding='utf-8')

plotfilename = filelist[0].replace('.txt', '')
outputpd.plot(x='freq[GHz]', y='alfa[dB/m]')
plt.savefig(plotfilename)
