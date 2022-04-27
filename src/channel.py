import random


def symetric_binary_channel(packet, p):
  for i in range(len(packet)):
    if random.uniform(0, 1) <= p:
      if packet[i]:
        packet[i] = 0
      else:
        packet[i] = 1
  return packet
