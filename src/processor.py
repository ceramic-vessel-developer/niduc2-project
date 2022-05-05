import copy

from src import parity_bits, channel


def process_packets(packets, distortion, probability):
    # Simulating process of sending packets in stop and wait ARQ

    processed_packets = []

    statistics = {
        'first_time_good': 0,
        'wrong': 0,
        'not_found': 0,
        'repeated': [0, 0, 0, 0, 0]
    }

    for packet in packets:
        error = False
        not_found = False
        repeated = 0

        while True:
            encoded_packet = parity_bits.parity_encoder(copy.copy(packet))

            if distortion == 'binary_erasure_channel':
                sent_packet = channel.binary_erasure_channel(
                    encoded_packet, probability)
            elif distortion == 'symetric_binary_channel':
                sent_packet = channel.symetric_binary_channel(
                    encoded_packet, probability)

            response = parity_bits.parity_decoder(sent_packet)

            if response == 'R':
                print('response R, ', encoded_packet, sent_packet)
                if encoded_packet != sent_packet:
                    print('something found')
                    not_found = True

                break
            else:
                error = True
                repeated += 1

        processed_packets.append(sent_packet)

        if (repeated > 0) and (repeated <= 5):
            statistics['repeated'][repeated - 1] += 1

        if error:
            statistics['wrong'] += 1
        else:
            statistics['first_time_good'] += 1

        if not_found:
            statistics['not_found'] += 1

    return processed_packets, statistics
