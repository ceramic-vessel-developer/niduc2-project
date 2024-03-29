def get_parity_bit(data):
    count = 0

    for bit in data:
        if (bit == 1):
            count += 1

    if ((count % 2) == 1):
        return 1
    else:
        return 0


def parity_encoder(packet):
    sum = 0

    for bit in packet:
        sum += bit

    if sum % 2 == 0:
        packet.append(0)
    else:
        packet.append(1)

    return packet


def parity_decoder(packet):
    sum = 0

    # we assume empty packet as an error
    if not packet:
        return 'F'

    for bit in packet[:-1]:
        sum += bit

    if sum % 2 == packet[-1]:
        return 'R'
    else:
        return 'F'
