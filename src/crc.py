import numpy as np


def get_divisor(n):
    if (n == 3):
        return [1, 0, 1, 1]
    elif (n == 4):
        return [1, 1, 0, 1, 0]


def crc_encoder(packet, n):
    divisor = get_divisor(n)

    packet_length = len(packet)
    divisor_length = len(divisor)

    new_packet = list.copy(packet)
    temp_packet = list.copy(packet)

    for i in range(divisor_length - 1):
        temp_packet.append(0)

    for i in range(packet_length):
        if temp_packet[i] == 1:
            for j in range(divisor_length):
                temp_packet[i +
                            j] = int(np.logical_xor(temp_packet[i + j], divisor[j]))

    for i in range(divisor_length - 1):
        new_packet.append(temp_packet[packet_length + i])

    return new_packet


def crc_decoder(packet, n):
    divisor = get_divisor(n)

    packet_length = len(packet)
    divisor_length = len(divisor)

    new_packet = list.copy(packet)
    temp_packet = list.copy(packet)

    for i in range(packet_length - divisor_length + 1):
        if temp_packet[i] == 1:
            for j in range(divisor_length):
                temp_packet[i +
                            j] = int(np.logical_xor(temp_packet[i + j], divisor[j]))

    sum = 0

    for i in range(divisor_length):
        sum += temp_packet[packet_length - 1 - i]

    if sum == 0:
        return packet[:-(divisor_length - 1)], 'R'
    elif sum == 1:
        return packet[:-(divisor_length - 1)], 'F'
    else:
        return [], 'R'
