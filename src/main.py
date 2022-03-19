import random


def generate_data(count):
    data = []

    for i in range(count):
        data.append(random.randint(0, 1))

    return data


def run():
    print('hello world')
