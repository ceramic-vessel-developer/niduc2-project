def create_packet(data, package_size):
    packet_data = []

    for i in range(0, len(data), package_size):
        packet_data.append(data[i:i + package_size])

    return packet_data
