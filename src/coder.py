def create_packet(data, packet_size):
    packets = []

    for i in range(0, len(data), packet_size):
        packet = data[i:i + packet_size - 1]
        packet.append(get_parity_bit(packet))

        packets.append(packet)

    return packets


def get_parity_bit(data):
    count = 0

    for bit in data:
        if (bit == 1):
            count += 1

    if ((count % 2) == 1):
        return 1
    else:
        return 0
