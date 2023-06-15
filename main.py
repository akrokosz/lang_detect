import math
import random
import os
import codecs
import re


class Neuron:
    training_speed = 0.1
    wagi = []

    def __init__(self, liczba_wejsc):
        self.liczba_wejsc = liczba_wejsc
        self.wagi = []
        for i in range(self.liczba_wejsc):
            x = random.random()
            while x == 0:
                x = random.random()
            self.wagi.append(x)

    def calc_net(self, wejscia):
        suma = 0
        for x in range(self.liczba_wejsc):
            suma += float(wejscia[x]) * float(self.wagi[x])
        return suma

    def normalize(self):
        leng = 0
        for i in range(0, len(self.wagi)):
            leng += math.pow(self.wagi[i], 2)

        leng = math.sqrt(leng)

        for i in range(0, len(self.wagi)):
            self.wagi[i] /= leng

    def train(self, training_line, numer_neuronu):
        answer = 1 if int(training_line[-1]) == numer_neuronu else -1
        result = self.calc_net(training_line[:-1])
        for x in range(len(self.wagi)):
            self.wagi[x] += (answer - result) * self.training_speed * float(training_line[x])
        result = self.calc_net(training_line[:-1])

        return abs(answer - result)


class Network:
    lista_neuronow = []
    training = []
    testing = []

    def __init__(self, sizes: list):
        for size in sizes:
            n = Neuron(size)
            self.lista_neuronow.append(n)

    def train(self, training_tab):

        for numer_neuronu in range(0, len(self.lista_neuronow)):
            neuron = self.lista_neuronow[numer_neuronu]
            print("Trening " + str(numer_neuronu) + ":")

            error = 0.0
            for line in training_tab:
                error += neuron.train(line, numer_neuronu)
                print("Error: " + str(error))
            error = error/len(self.lista_neuronow)

            while error > 1.6:
                error = 0
                for line in training_tab:
                    error += neuron.train(line, numer_neuronu)
                error = error/len(self.lista_neuronow)
                print("Error: " + str(error))
            neuron.normalize()

    def test(self, testing_tab):

        predictions = []
        out = {}

        for numer_neuronu in range(0, len(self.lista_neuronow)):
            neuron = self.lista_neuronow[numer_neuronu]
            for linia in testing_tab:
                result = neuron.calc_net(linia)
                answer = 1 if linia[-1] == numer_neuronu else -1
                print("predykcja: " + str(result) + ", rzeczywistosc: " + str(answer))
                predictions.append(result)

                out[numer_neuronu] = predictions
            predictions = []
            print("------------------------------------")

        for i in range(0, len(testing_tab)):
            activates_most = max(out[0][i], out[1][i], out[2][i])
            for key, value in out.items():
                if value[i] == activates_most:
                    matching_key = key
                    print("wynik to = " + str(matching_key))

    def input_test(self, inp):
        dicti = {}
        langs = {}
        for numer_neuronu in range(0, len(self.lista_neuronow)):
            obecny_neuron = self.lista_neuronow[numer_neuronu]
            result = obecny_neuron.calc_net(inp)
            print("predykcja: " + str(result))
            dicti[result] = numer_neuronu
        output = dicti[max(dicti)]
        for i in range(len(self.lista_neuronow)):
            langs[i] = os.listdir('data_train')[i]

        print("-----------------WYNIK TO: " + str(langs[output]))

    def work(self):
        while True:
            input_string = str(input("podaj zdanie po niemiecku, angielsku lub polsku: "))
            row = []
            for i in "abcdefghijklmnopqrstuvwxyzL":
                row.append(input_string.count(i) / len(input_string.replace("[\\W|\\d]", "")))
            self.input_test(row)


def dir_to_data(catalog):
    list_of_rows = []
    row = []
    text = ""
    list_of_directories = os.listdir(catalog)

    for g, dirname in enumerate(list_of_directories):
        d = os.listdir(catalog + '/' + dirname)
        for file in d:
            with codecs.open(catalog + '/' + dirname + "/" + file, encoding='utf-8') as f:
                for line in f:
                    text += replacements(line)
            text = re.sub("[\\W|\\d]", "", text)
            for i in "abcdefghijklmnopqrstuvwxyz":
                row.append(text.count(i) / len(text))
            row.append(g)
            list_of_rows.append(row)
            text = ""
            row = []
    return list_of_rows


def replacements(x):
    x = x.lower()
    special_characters = {ord('ą'): 'a', ord('ę'): 'e', ord('ó'): 'u', ord('ł'): 'l',
                          ord('ń'): 'n', ord('ż'): 'z', ord('ź'): 'z',
                          ord('ä'): 'a', ord('ö'): 'o', ord('ü'): 'u', ord('ß'): 's'}
    x = x.translate(special_characters)
    return x


def main():
    lang_train = dir_to_data('data_train')
    lang_test = dir_to_data('data_test')

    li = [26, 26, 26]
    nn = Network(li)
    nn.train(lang_train)
    nn.test(lang_test)
    nn.work()


if __name__ == "__main__":
    main()
