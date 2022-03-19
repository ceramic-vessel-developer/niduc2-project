def create_packet(data, packet_size):
    packets = []

    wild_bits_count = len(data) % (packet_size - 1)

    # fill bits_count = packet_size - wild_bits_count - 1 (parity_bit)
    fill_bits_count = packet_size - wild_bits_count - 1

    for i in range(fill_bits_count):
        data.append(0)

    for i in range(0, len(data), packet_size - 1):
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
