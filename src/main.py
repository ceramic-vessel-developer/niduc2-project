import random

from src import processor


def generate_data(count):
    data = []

    for i in range(count):
        data.append(random.randint(0, 1))

    return data


def create_packet(data, packet_size):
    packets = []

    wild_bits_count = len(data) % (packet_size)

    # fill bits_count = packet_size - wild_bits_count - 1 (parity_bit)
    if wild_bits_count:
        fill_bits_count = packet_size - wild_bits_count
        for i in range(fill_bits_count):
            data.append(0)

    for i in range(0, len(data), packet_size):
        packet = data[i:i + packet_size]
        packets.append(packet)

    return packets


def print_packets(packets):
    i = 0

    for packet in packets:
        print(f"{i}. {packet}")
        i += 1


def print_processed_packets(packets, processed_packets):
    for i in range(len(processed_packets)):
        is_the_same = processed_packets[i][:-1] == packets[i]
        print(f"{i + 1}. {processed_packets[i]}   {is_the_same}")


def print_statistics(statistics):
    print("First time good: ", statistics['first_time_good'])
    print("Wrong: ", statistics['wrong'])
    print("Not found: ", statistics['not_found'])

    for i in range(4):
        print(f"Repeated {i + 1} times: ", statistics['repeated'][i])

    print(f"Repeated more times: ", statistics['repeated'][4], end='\n\n')


def run():
    packets = create_packet(generate_data(256), 8)

    print_packets(packets)

    processed_packets = []

    statistics = {
        'first_time_good': 0,
        'wrong': 0,
        'not_found': 0,
        'repeated': [0, 0, 0, 0, 0]
    }

    distortions = ['binary_erasure_channel', 'symetric_binary_channel']

    probability = 0.05

    for distortion in distortions:
        print(f'Using channel: ', distortion, end='\n\n')

        processed_packets, statistics = processor.process_packets(
            packets, distortion, probability)

        print_statistics(statistics)

        print("Printing processed packets:")

        print_processed_packets(packets, processed_packets)

        print('')
