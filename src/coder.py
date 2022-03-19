def create_packet(data, packet_size):
    packet_data = []

    for i in range(0, len(data), packet_size):
        packet_data.append(data[i:i + packet_size])

    return packet_data
