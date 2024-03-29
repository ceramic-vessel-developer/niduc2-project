import copy

from src import channel, crc, parity_bits


def process_packets(packets, coding, distortion, probability):
    # Simulating process of sending packets in stop and wait ARQ

    processed_packets = []

    statistics = {
        'first_time_good': 0,
        'wrong': 0,
        'not_found': 0,
        'corrected': 0,
        'repeated': [0, 0, 0, 0, 0]
    }

    for packet in packets:
        error = False
        not_found = False
        corrected = False
        repeated = 0

        encoded_packet = []
        sent_packet = []
        response = ''

        while True:
            if coding == 'crc':
                encoded_packet = crc.crc_encoder(copy.copy(packet), 4)
            elif coding == 'parity_bit':
                encoded_packet = parity_bits.parity_encoder(copy.copy(packet))

            if distortion == 'binary_erasure_channel':
                sent_packet = channel.binary_erasure_channel(
                    copy.copy(encoded_packet), probability)
            elif distortion == 'symmetric_binary_channel':
                sent_packet = channel.symetric_binary_channel(
                    copy.copy(encoded_packet), probability)

            if coding == 'crc':
                decoded_packet, response = crc.crc_decoder(sent_packet, 4)
            elif coding == 'parity_bit':
                response = parity_bits.parity_decoder(sent_packet)

            if response == 'R':
                if encoded_packet != sent_packet:
                    not_found = True
                elif error:
                  corrected = True
                break
            else:
                error = True
                repeated += 1

        processed_packets.append(sent_packet)

        if (repeated > 0) and (repeated <= 5):
            statistics['repeated'][repeated - 1] += 1

        if corrected:
            statistics['corrected'] += 1
        if error:
            statistics['wrong'] += 1
        elif not not_found:
            statistics['first_time_good'] += 1

        if not_found:
            statistics['not_found'] += 1

    return processed_packets, statistics

