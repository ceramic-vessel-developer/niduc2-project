import copy
import random

from src import parity_bits, channel


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


def run():
    packets = create_packet(generate_data(256), 8)

    j = 0

    for packet in packets:
        print(f"{j}. {packet}")
        j += 1

    processed_packets = []
    statistics = {'first_time_good': 0, 'wrong': 0, 'repeated': 0}

    # Simulating process of sending packets in stop and wait ARQ
    for packet in packets:
        error = False

        while True:
            encoded_packet = parity_bits.parity_encoder(copy.copy(packet))
            sent_packet = channel.binary_erasure_channel(encoded_packet, 0.05)
            response = parity_bits.parity_decoder(sent_packet)

            if response == 'R':
                break
            else:
                error = True
                statistics['repeated'] += 1

        processed_packets.append(sent_packet)

        if error:
            statistics['wrong'] += 1
        else:
            statistics['first_time_good'] += 1

    print("First time good: ", statistics['first_time_good'])
    print("Wrong: ", statistics['wrong'])
    print("Repeated: ", statistics['repeated'])
    print("Printing processed packets:")

    for i in range(len(processed_packets)):
        is_the_same = processed_packets[i][:-1] == packets[i]
        print(f"{i + 1}. {processed_packets[i]}   {is_the_same}")
