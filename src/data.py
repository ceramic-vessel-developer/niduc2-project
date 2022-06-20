import ast
import csv

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def csv_writer(filename, results):
    with open(filename, 'a') as file:
        writer = csv.DictWriter(file, results.keys())
        writer.writerow(results)


def csv_reader(filename):
    results = {
        'first_time_good': [],
        'wrong': [],
        'not_found': [],
        'corrected': [],
        'repeated': []
    }

    with open(filename, 'r') as file:
        reader = csv.DictReader(file, fieldnames=results.keys())

        for row in reader:
            results['first_time_good'].append(int(row['first_time_good']))
            results['wrong'].append(int(row['wrong']))
            results['not_found'].append(int(row['not_found']))
            results['corrected'].append(int(row['corrected']))
            results['repeated'].append(ast.literal_eval(row['repeated']))

    return results


def make_plot_from_csv(files, parameter):
    data = []
    name = files[0].split('+')[0]+files[0].split('+')[1]

    if name == "crcbinary_erasure_channel":
      name = "CRC in binary erasure channel"
    elif name == "crcsymmetric_binary_channel":
      name = "CRC in binary symmetric channel"
    elif name == "parity_bitsymmetric_binary_channel":
      name = "Parity bit in symmetric binary channel"
    elif name == "parity_bitbinary_erasure_channel":
      name = "Parity bit in binary erasure channel"

    for file in files:
        record = {
            'first_time_good': 0,
            'wrong': 0,
            'corrected': 0,
            'not_found': 0
        }
        if(parameter==2):
          n = float(file.split('+')[2].split('_')[parameter][:-4])
        else:
          n = float(file.split('+')[2].split('_')[parameter])

        open_file = csv_reader(file)
        open_file.pop('repeated')

        for key, value in open_file.items():
            record[key] = np.average(value)

        data.append((n, record))

    data.sort()

    x_axis = [x[0] for x in data]
    y_axis_ftg = [x[1]['first_time_good'] for x in data]
    y_axis_w = [x[1]['wrong'] for x in data]
    y_axis_nf = [x[1]['not_found'] for x in data]
    y_axis_cor = [x[1]['corrected'] for x in data]

    plt.plot(x_axis, y_axis_ftg, label="First time good", marker='o',color='g')
    plt.plot(x_axis, y_axis_w, label="Wrong", marker='o',color='y')
    plt.plot(x_axis, y_axis_nf, label="Falsely marked as good", marker='o',color='r')
    plt.plot(x_axis, y_axis_cor, label="Corrected", marker='o', color='b')

    if parameter == 0:
        plt.xlabel('Probability of distortion')
    elif parameter == 1:
        plt.xlabel('Amount of data')
    elif parameter == 2:
        plt.xlabel('Packet length')

    plt.ylabel('Average number')
    plt.title(name)
    plt.legend()
    plt.show()


# def make_histogram(files, parameter):
#     data = []
#     name = files[0].split('+')[0]+files[0].split('+')[1]
#
#     for file in files:
#         # record = {
#         #     'repeated': [],
#         # }
#         #
#         # if (parameter == 2):
#         #   n = float(file.split('+')[2].split('_')[parameter][:-4])
#         # else:
#         #   n = float(file.split('+')[2].split('_')[parameter])
#
#         open_file = csv_reader(file)
#
#         repeated = open_file.pop('repeated')
#
#         # transpose data matrix from format repeats for i-element in sublist
#         # [[a, b, c], [d, e, f]]
#         # to format repeats set for i-element (repeat) in list
#         # [[a, d], [b, e], [c, f]]
#         #repeated_transposed = list(map(list, zip(*repeated)))
#         for repeat in repeated:
#           for j in range(5):
#             if(repeat[j]):
#               for k in range(repeat[j]):
#                 data.append(j+1)
#
#         # more repeats
#         # for repeats in repeated_transposed:
#         #     record['repeated'].append(repeats)
#         #
#         # data.append((n, record))
#
#
#     sns.set()
#     h = sns.histplot(data, bins=[1, 2, 3, 4, 5])
#     plt.xlabel('repetitions')
#     plt.ylabel('occurences')
#     plt.title('histogram title')
#
#     h.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5])
#     h.set_xticklabels(["1", "2", "3", "4", "5+"])
#
#     plt.show()
#     # data.sort()
#     #
#     # # print(data)
#     #
#     # # list index == i-repeat because first time good was added and this is 0-repeat
#     # max_repeats = data[0][1]['repeated'].__len__()
#     #
#     # big_data = []
#     # y_axis = []
#     #
#     # # big_data.append(data[0][1]['repeated'])
#     #
#     # # for i in range(1, max_repeats - 1):
#     # #     for j in range(0, max_repeats - 1):
#     # #         big_data[j].append(data[i][1]['repeated'][j])
#     # # print(data)
#     #
#     # for i in range(data.__len__()):
#     #     count = 0
#     #
#     #     for j in range(max_repeats):
#     #         print(data[i][1]['repeated'][j])
#     #
#     #         for k in range(data[i][1]['repeated'][j].__len__()):
#     #             count += data[i][1]['repeated'][j][k]
#     #
#     #     big_data.append(count)
#     #
#     # # print('#############################3', big_data)
#     #
#     # # for dataset in data:
#     # #     for i in range(1, max_repeats):
#     # #         big_data.append(dataset[1]['repeated'][i])
#     # #         print('--------------------------------', dataset)
#     #
#     # # for dataset in big_data:
#     # #     count = 0
#     #
#     # #     for value in dataset:
#     # #         count += value
#     #
#     # #     y_axis.append(count)
#     #
#     # x_axis = [x for x in range(0, max_repeats)]
#     # y_axis = big_data
#     #
#     # n, bins, patches = plt.hist(y_axis, max_repeats, density=True)
#     #
#     # plt.subplots_adjust(left=0.15)
#     #
#     # # print(n)
#     # # print(bins)
#     #
#     # plt.xlabel('Repeats number')
#     # plt.ylabel('Occurences')
#     # plt.title(name)
#     # plt.grid(True)
#     # plt.legend()
#     # plt.show()
