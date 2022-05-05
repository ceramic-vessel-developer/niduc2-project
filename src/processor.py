import copy

from src import parity_bits, channel


def process_packets(packets):
    # Simulating process of sending packets in stop and wait ARQ

    processed_packets = []

    statistics = {'first_time_good': 0,
                  'wrong': 0, 'repeated': [0, 0, 0, 0, 0], 'not_found': 0}

    for packet in packets:
        error = False
        repeated = 0

        while True:
            encoded_packet = parity_bits.parity_encoder(copy.copy(packet))
            sent_packet = channel.binary_erasure_channel(encoded_packet, 0.05)
            response = parity_bits.parity_decoder(sent_packet)

            if response == 'R':
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

    return processed_packets, statistics
