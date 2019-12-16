import glob
import os
import math
import random

class ObiektSystemuDecyzyjnego:
    def __init__(self, data):
        self.data = data
        self.atrybuty = self._get_attributes()
        self.klasa_decyzyjna = self._get_decision_class()

    def _get_attributes(self):
        return self.data[:-1]

    def _get_decision_class(self):
        return self.data[-1]

class KlasaDecyzyjna:
    def __init__(self, data, nazwa_klasy):
        self.nazwa_klasy = nazwa_klasy
        self.obiekty = self._get_objects_from_data(data)

    def _get_objects_from_data(self, data):
        lista_obiektow = []
        for obj in data:
            lista_obiektow.append(ObiektSystemuDecyzyjnego(obj))
        return lista_obiektow

class KlasyfikatorBayesa:
    def __init__(self, baza_wiedzy):
        self.baza_wiedzy = baza_wiedzy
        self.system_objects = self._get_system_objects()
        self.klasy_decyzyjne = self._get_decision_classes()

    def _get_system_objects(self):
        system_objects = []
        for dec_obj in self.baza_wiedzy:
            system_objects.append(ObiektSystemuDecyzyjnego(dec_obj))
        return system_objects

    def _get_column_data(self, column_number):
        column_data = {}
        for single_line in self.baza_wiedzy:
            column_value = single_line.split()[column_number]
            if column_value in column_data:
                column_data[column_value] += 1
            else:
                column_data[column_value] = 1
        return column_data

    def get_decision_classes(self):
        decision_classes = self._get_column_data(-1)
        return decision_classes.keys()

    def _get_decision_classes(self):
        decision_classes = self._get_column_data(-1)
        results = {}
        for decision_class in decision_classes:
            results[decision_class] = []
        for decision_object in self.baza_wiedzy:
            decision_object_splitted = decision_object.strip().split(' ')
            results[decision_object_splitted[-1]].append(ObiektSystemuDecyzyjnego(decision_object_splitted))            
        return results

    def _get_classes_probability(self):
        all_objects_count = 0
        prawdopodobienstwa_klas = {}     
        for obj in self.klasy_decyzyjne:
            all_objects_count = all_objects_count + len(self.klasy_decyzyjne[obj])  
        for klasa_decyzyjna in self.klasy_decyzyjne:
            prawdopodobienstwa_klas[klasa_decyzyjna] = len(self.klasy_decyzyjne[klasa_decyzyjna]) / all_objects_count 
        return prawdopodobienstwa_klas
    
    def klasyfikuj(self, obiekt_do_klasyfikacji):
        lista_prawdopodobienstw = {}
        prawdopodobienstwa_klas = self._get_classes_probability()
        for klasa, obiekty in self.klasy_decyzyjne.items():
            ilosc_obiektow_w_klasie = len(obiekty)
            ilosc_pasujacych_obiektow = [0] * len(obiekt_do_klasyfikacji)
            for obiekt in obiekty:
                index = 0
                for attr in obiekt_do_klasyfikacji:
                    if attr == obiekt.atrybuty[index]:
                        ilosc_pasujacych_obiektow[index] = ilosc_pasujacych_obiektow[index] + 1
                    index = index + 1
            lista_prawdopodobienstw[klasa] = prawdopodobienstwa_klas[klasa]
            p_czesciowe = 0
            index = 0
            for attr in obiekt_do_klasyfikacji:
                p_czesciowe = p_czesciowe + ilosc_pasujacych_obiektow[index] / ilosc_obiektow_w_klasie
                index = index + 1
            lista_prawdopodobienstw[klasa] = p_czesciowe
            lista_prawdopodobienstw[klasa] = lista_prawdopodobienstw[klasa] * prawdopodobienstwa_klas[klasa]
        highest_probabilities_classes = []
        highest_probability_value = max(lista_prawdopodobienstw.values())
        for prawdopodobienstwo_klasy in lista_prawdopodobienstw:
            if lista_prawdopodobienstw[prawdopodobienstwo_klasy] == highest_probability_value:
                highest_probabilities_classes.append(prawdopodobienstwo_klasy)
        return random.choice(highest_probabilities_classes)

# main
if __name__ == "__main__":
    system_TRN_handle = open("./c02/australian_TRN.txt")
    system_TST_handle = open("./c02/australian_TST.txt")
    system_TRN = system_TRN_handle.readlines()
    system_TST = system_TST_handle.readlines()
    klasyfikator = KlasyfikatorBayesa(system_TRN)

    correct_amount = {}
    overall_amount = {}
    wyniki = []

    for obiekt_do_klasyfikacji in system_TST:
        wynik = klasyfikator.klasyfikuj(obiekt_do_klasyfikacji.strip().split(' ')[:-1])
        prawidlowa_klasa = obiekt_do_klasyfikacji.strip()[-1]
        if prawidlowa_klasa not in overall_amount:
            correct_amount[prawidlowa_klasa] = 0
            overall_amount[prawidlowa_klasa] = 0
        overall_amount[prawidlowa_klasa] += 1
        if wynik == prawidlowa_klasa:
            correct_amount[prawidlowa_klasa] += 1
        wyniki.append(wynik)

    liczba_klas = len(overall_amount)
    suma_licznika_bal_acc = 0
    suma_licznika_glob_acc = 0
    wszystkie_obiekty = 0
    for klasa in correct_amount:
        suma_licznika_bal_acc += correct_amount[klasa] / overall_amount[klasa]
        suma_licznika_glob_acc += correct_amount[klasa]
        wszystkie_obiekty += overall_amount[klasa]
    balanced_accuraty = suma_licznika_bal_acc / liczba_klas
    global_accuraty = suma_licznika_glob_acc / wszystkie_obiekty
    print('Balanced Acc = ', balanced_accuraty)
    print('Global Acc = ', global_accuraty)

    file = open('dec_bayes.txt', 'w')
    for wynik in wyniki:
        file.write(wynik)
        file.write('\n')
    file.close()

    file = open('acc_bayes.txt', 'w')
    file.write('Global Acc = ')
    file.write(str(global_accuraty))
    file.write('\n')
    file.write('Balanced Acc = ')
    file.write(str(balanced_accuraty))
    file.close()