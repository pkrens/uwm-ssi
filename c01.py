import math
import glob
import os
from enum import Enum

class Atrybut:
    class AttributeType(Enum):
        s = 1
        n = 2

    def __init__(self, name, attribute_type, data):
        self.name = name
        self.data = data
        self.unique_values = set(data)
        self.attribute_type = Atrybut.AttributeType.s
        if attribute_type == 's':
            self.attribute_type = Atrybut.AttributeType.s
        elif attribute_type == 'n':
            self.attribute_type = Atrybut.AttributeType.n
            try:
                self.data = list(map(float, data))
            except ValueError:
                self.attribute_type = Atrybut.AttributeType.s

    def is_symbolic(self):
        if self.attribute_type == Atrybut.AttributeType.s:
            return True
        return False

    def min(self):
        if self.is_symbolic():
            raise TypeError("Atrybut jest typu symbolicznego!")
        return min(self.data)
        
    def max(self):
        if self.is_symbolic():
            raise TypeError("Atrybut jest typu symbolicznego!")
        return max(self.data)

    def stdev(self):
        if self.is_symbolic():
            raise TypeError("Atrybut jest typu symbolicznego!")
        data_sum = sum(self.data)
        data_avg = data_sum / len(self.data)
        stdev_sum = 0
        for val in self.data:
            stdev_sum += (val - data_avg) ** 2
        stdev_sum /= len(self.data)
        stdev_sum = math.sqrt(stdev_sum)
        return stdev_sum

class KlasaDecyzyjna:
    def __init__(self, wartosc):
        self.wartosc = wartosc
        self.atrybuty = []

class SystemDecyzyjny:
    def __init__(self, data_file_name, attributes_file_name):
        self._data_file_name = data_file_name
        self._attributes_file_name = attributes_file_name
        self.klasy_decyzyjne = []
        self.atrybuty = []
        self._get_attributes()
        self._fill_decision_classes()

    def _fill_decision_classes(self):
        decision_classes = self.get_decision_classes()
        for decision_class in decision_classes:
            klasa_decyzyjna = KlasaDecyzyjna(decision_class)
            klasa_decyzyjna.atrybuty = self._get_attributes_from_class(decision_class)
            self.klasy_decyzyjne.append(klasa_decyzyjna)

    def _get_attributes(self):
        data = open(self._attributes_file_name)
        i = 0
        for line in data.readlines():
            column_data = self._get_column(i)
            nazwa = line.split(' ')[0]
            typ = line.split(' ')[1]
            typ = typ.strip()
            self.atrybuty.append(Atrybut(nazwa, typ, column_data))
            i = i + 1

    def _get_attributes_from_class(self, decision_class):
        data = open(self._attributes_file_name)
        attributes = []
        i = 0
        for line in data.readlines():
            column_data = self._get_column_from_class(i, decision_class)
            nazwa = line.split(' ')[0]
            typ = line.split(' ')[1]
            typ = typ.strip()
            attributes.append(Atrybut(nazwa, typ, column_data))
            i = i + 1
        return attributes

    def _get_column(self, column_number):
        data = open(self._data_file_name)
        column_data = []
        for single_line in data.readlines():
            column_data.append(single_line.split()[column_number])
        return column_data

    def _get_column_from_class(self, column_number, decision_class):
        data = open(self._data_file_name)
        column_data = []
        for single_line in data.readlines():
            column_value = single_line.split()[column_number]
            column_class = single_line.split()[-1]
            if column_class != decision_class:
                continue
            column_data.append(column_value)
        return column_data
    
    def _get_column_data(self, column_number):
        data = open(self._data_file_name)
        column_data = {}
        for single_line in data.readlines():
            column_value = single_line.split()[column_number]
            if column_value in column_data:
                column_data[column_value] += 1
            else:
                column_data[column_value] = 1
        return column_data

    def _get_column_data_from_class(self, column_number, decision_class):
        data = open(self._data_file_name)
        column_data = {}
        for single_line in data.readlines():
            column_value = single_line.split()[column_number]
            column_class = single_line.split()[-1]
            if column_class != decision_class:
                continue
            if column_value in column_data:
                column_data[column_value] += 1
            else:
                column_data[column_value] = 1
        return column_data

    def get_decision_classes(self):
        decision_classes = self._get_column_data(-1)
        return decision_classes.keys()

    def get_decision_classes_data(self):
        decision_classes = self._get_column_data(-1)
        return decision_classes

def wypisz_dane_o_systemie_decyzyjnym(system_decyzyjny):
    print("Klasy decyzyjne:")
    print(system_decyzyjny.get_decision_classes())
    print("Liczebnosc klas decyzyjnych:")
    print(system_decyzyjny.get_decision_classes_data())
    print("Atrybuty systemu decyzyjnego:")
    for atrybut in system_decyzyjny.atrybuty:
        print("Atrybut:")
        print(atrybut.name)
        if atrybut.attribute_type == Atrybut.AttributeType.n:
            print("Atrybut numeryczny")
            print("Min:")
            print(atrybut.min())
            print("Max:")
            print(atrybut.max())
            print("Odchylenie standardowe:")
            print(atrybut.stdev())
        else:
            print("Atrybut symboliczny")
            print("Wartości unikalne:")
            for wartosc in atrybut.unique_values:
                print(wartosc)

    print("Atrybuty poszczególnych klas decyzyjnych:")
    for klasa_decyzyjna in system_decyzyjny.klasy_decyzyjne:
        print("Klasa decyzyjna:")
        print(klasa_decyzyjna.wartosc)
        for atrybut in klasa_decyzyjna.atrybuty:
            print("Atrybut:")
            print(atrybut.name)
            if atrybut.attribute_type == Atrybut.AttributeType.n:
                print("Atrybut numeryczny")
                print("Min:")
                print(atrybut.min())
                print("Max:")
                print(atrybut.max())
                print("Odchylenie standardowe:")
                print(atrybut.stdev())
            else:
                print("Atrybut symboliczny")
                print("Wartości unikalne:")
                for wartosc in atrybut.unique_values:
                    print(wartosc)

#main

type_files = glob.glob("data/*-type.txt")
for type_file in type_files:
    data_filename = type_file.replace("-type", "")
    if os.path.exists(data_filename) == False:
        continue
    type_filename = os.path.basename(type_file)
    try:
        system_decyzyjny = SystemDecyzyjny(data_filename, type_file)
        print("Plik:")
        print(data_filename)
        wypisz_dane_o_systemie_decyzyjnym(system_decyzyjny)
    except:
        print("Błąd w systemie:")
        print(data_filename)