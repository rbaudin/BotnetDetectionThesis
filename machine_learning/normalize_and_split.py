import os
import sys
sys.path.insert(0, os.environ['HOME'] + '/BotnetDetectionThesis/')

from sklearn.model_selection import train_test_split
import config as c
import csv
import pandas as pd


def normalize_data(data):
    for i in range(0, len(data[0])):
        max = 0
        for j in range(len(data)):
            if max < data[j][i]:
                max = data[j][i]
        if max != 0:
            for j in range(len(data)):
                if data[j][i] != -1:
                    data[j][i] = data[j][i] / float(max)
    return data


def write_features(filename, data, features_name):
    df = pd.DataFrame(data, columns=features_name)
    df.to_csv(c.model_folder + filename, sep=',', encoding='utf-8', index=False)


def write_targets(file_name, data_list):
    index = 0
    import csv

    with open(c.model_folder + file_name, 'wb') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n', delimiter=',')  # fieldnames=features.keys(),
        writer.writerow(data_list)
        index += 1

    print file_name, "written lines:", index


def transform_label(label):
    label_number = -1
    if 'MALWARE' in label:
        label_number = 1
    elif "NORMAL" in label:
        label_number = 0
    else:
        print "The label is incorrect"

    return label_number

if __name__ == '__main__':
    malwares = 0
    normals = 0

    X = list()
    y = list()

    LIMIT = -1 # total nb_lines, -1 = NO LIMIT

    with open(c.model_folder + "features.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile, lineterminator='\n', delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        headers = csvreader.next()
        print(headers)
        line_nb = 0

        for row in csvreader:
            target = transform_label(row[-1])
            if LIMIT != -1:
                if target == 1 and malwares < LIMIT / 2:
                    malwares += 1
                elif target == 0 and normals < LIMIT / 2:
                    normals += 1
                else:
                    continue
            else:
                malwares += target
                normals += 1 if target == 0 else 0

            X.append(row[1:-1])  # exclude key (index 0) and label (index -1 = last index)
            y.append(target)
            line_nb += 1

    features_name = headers[1:-1]

    # normalize X
    norm_X = normalize_data(X)
    print "Size of X:", len(X)
    print "Malwares:", malwares
    print "Normals:", len(X) - malwares

    # split data by sklearn library
    X_train, X_test, y_train, y_test = train_test_split(norm_X, y, test_size=.2, random_state=35)

    # Write train data
    write_features('X_train.csv', X_train, features_name)
    write_targets('y_train.csv', y_train)

    # Write test data
    write_features('X_test.csv', X_test, features_name)
    write_targets('y_test.csv', y_test)
