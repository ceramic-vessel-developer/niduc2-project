import random
from src import coder

def generate_data(count):
    data = []

    for i in range(count):
        data.append(random.randint(0, 1))

    return data


def run():
  packets = coder.create_packet(generate_data(256), 8)
  j = 0
  for packet in packets:
    print(f"{j}. {packet}")
    j += 1
