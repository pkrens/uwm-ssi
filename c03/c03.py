import random
import sys
import math
sys.path.append('./c02/')
from c02 import KlasyfikatorBayesa

def divide_data(data, folds):
    data_manipulated = data[:]
    divided_data = []
    for i in range(0, folds, 1):
        divided_data.append([])
    random.shuffle(data_manipulated)
    counter = 0
    for i in data_manipulated:
        divided_data[counter].append(i)
        counter = counter + 1
        counter = counter % folds
    return divided_data

def losuj_bez_zwracania(data, ilosc):
    data_manipulated = data[:]
    elements_to_return = []
    for _ in range(ilosc):
        data_length = len(data_manipulated)
        random_index = random.randint(0, data_length - 1)
        elements_to_return.append(data_manipulated.pop(random_index))
    return elements_to_return, data_manipulated

def losuj_ze_zwracaniem(data, ilosc):
    data_manipulated = data[:]
    data_length = len(data_manipulated)
    elements_to_return = []
    indexes = []
    data_to_return = []
    for _ in range(ilosc):
        random_index = random.randint(0, data_length - 1)
        indexes.append(random_index)
    for index in indexes:
        elements_to_return.append(data_manipulated[index])
    for i in range(data_length):
        if i not in indexes:
            data_to_return.append(data_manipulated[index])
    return elements_to_return, data_to_return

def train_and_test(data, test_size):
    results_matrix = {}
    possible_classes = []
    for i in data:
        possible_classes.append(i.strip().split(' ')[-1])
    possible_classes = set(possible_classes)
    for current_class in possible_classes:
        results_matrix[current_class] = {}
        for inside_class in possible_classes:
            results_matrix[current_class][inside_class] = 0
    test_amount = math.floor(test_size * len(data))
    trn, tst = losuj_bez_zwracania(data, test_amount)
    classifier = KlasyfikatorBayesa(trn)
    for tst_obj in tst:
        tst_obj_splitted = tst_obj.strip().split(' ')
        classification_result = classifier.klasyfikuj(tst_obj_splitted[:-1])
        real_result = tst_obj_splitted[-1]
        results_matrix[real_result][classification_result] += 1
    return results_matrix

def test_with_passed_data(trn, tst):
    results_matrix = {}
    possible_classes = []
    for i in trn:
        possible_classes.append(i.strip().split(' ')[-1])
    for i in tst:
        possible_classes.append(i.strip().split(' ')[-1])
    possible_classes = set(possible_classes)
    for current_class in possible_classes:
        results_matrix[current_class] = {}
        for inside_class in possible_classes:
            results_matrix[current_class][inside_class] = 0
    classifier = KlasyfikatorBayesa(trn)
    for tst_obj in tst:
        tst_obj_splitted = tst_obj.strip().split(' ')
        classification_result = classifier.klasyfikuj(tst_obj_splitted[:-1])
        real_result = tst_obj_splitted[-1]
        results_matrix[real_result][classification_result] += 1
    return results_matrix

def mccv(data, folds, test_size):
    results_array = []
    for _ in range(folds):
        results_array.append(train_and_test(data, test_size))
    return results_array

def cv(data, folds):
    divided_data = divide_data(data, folds)
    results_array = []
    for fold in range(len(divided_data)):
        temp_folded_data = divided_data[:]
        temp_tst = temp_folded_data.pop(fold)
        temp_trn = []
        for i in range(len(temp_folded_data)):
            for item in temp_folded_data[i]:
                temp_trn.append(item)
        results_array.append(test_with_passed_data(temp_trn, temp_tst))
    return results_array

def bootstrap(data):
    results_matrix = {}
    possible_classes = []
    for i in data:
        possible_classes.append(i.strip().split(' ')[-1])
    possible_classes = set(possible_classes)
    for current_class in possible_classes:
        results_matrix[current_class] = {}
        for inside_class in possible_classes:
            results_matrix[current_class][inside_class] = 0
    test_amount = len(data)
    trn, tst = losuj_ze_zwracaniem(data, test_amount)
    classifier = KlasyfikatorBayesa(trn)
    for tst_obj in tst:
        tst_obj_splitted = tst_obj.strip().split(' ')
        classification_result = classifier.klasyfikuj(tst_obj_splitted[:-1])
        real_result = tst_obj_splitted[-1]
        results_matrix[real_result][classification_result] += 1
    return results_matrix

def bagging(data, folds):
    results_array = []
    for _ in range(folds):
        results_array.append(bootstrap(data))
    return results_array

def get_accuraties_single(matrix):
    correctness_arr = []
    correct_objects = 0
    all_objects = 0
    for current_class in matrix:
        objects_in_class_count = 0
        for result_class in matrix[current_class]:
            objects_in_class_count += matrix[current_class][result_class]
        correctness = 1
        try:
            correctness = matrix[current_class][current_class] / objects_in_class_count
        except:
            pass
        correct_objects += matrix[current_class][current_class]
        all_objects += objects_in_class_count
        correctness_arr.append(correctness)
    acc_glob = correct_objects / all_objects
    acc_bal = sum(correctness_arr) / len(matrix)
    return acc_glob, acc_bal

def get_accuraties_multiples(matrix):
    acc_glob_sum = 0
    acc_bal_sum = 0
    for one_result in matrix:
        acc_glob, acc_bal = get_accuraties_single(one_result)
        acc_glob_sum += acc_glob
        acc_bal_sum += acc_bal
    return acc_glob_sum / len(matrix), acc_bal_sum / len(matrix)

# main
if __name__ == "__main__":
    system_handle = open("./c03/australian.txt")
    system_data_raw = system_handle.readlines()

    system_data = system_data_raw[:]
    t_and_t_results = train_and_test(system_data, 0.5)
    print('t&t = ', t_and_t_results)
    print('accs t&t = ', get_accuraties_single(t_and_t_results))

    system_data = system_data_raw[:]
    mccv5_results = mccv(system_data, 5, 0.5)
    print('mccv5 = ', mccv5_results)
    print('accs mccv5 = ', get_accuraties_multiples(mccv5_results))

    system_data = system_data_raw[:]
    cv_results = cv(system_data, 5)
    print('cv5 = ', cv_results)
    print('accs cv5 = ', get_accuraties_multiples(cv_results))

    system_data = system_data_raw[:]
    loo_results = cv(system_data, len(system_data))
    print('loo = ', cv_results)
    print('accs loo = ', get_accuraties_multiples(loo_results))

    system_data = system_data_raw[:]
    bagging_results = bagging(system_data, 5)
    print('bagging = ', bagging_results)
    print('accs bagging = ', get_accuraties_multiples(bagging_results))