import csv
import time


def read_data(file, delimiter=','):
    with open(file) as csv_file:
        return list(csv.DictReader(csv_file))


def get_csv_fieldnames(file, delimiter=','):
    with open(file) as csv_file:
        return csv.DictReader(csv_file, delimiter=delimiter).fieldnames


def write_data(file, data: dict):
    data['submission_time'] = int(time.time())
    field_names = get_csv_fieldnames(file)
    with open(file, 'a+', ) as csv_file:
        csv.DictWriter(csv_file, fieldnames=field_names).writerow(data)
