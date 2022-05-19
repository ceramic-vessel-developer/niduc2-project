import random
import os

from src import processor
from src import data


def generate_data(count):
  data = []

  for i in range(count):
    data.append(random.randint(0, 1))

  return data


def create_packet(data, packet_size):
  packets = []

  wild_bits_count = len(data) % (packet_size)

  # fill bits_count = packet_size - wild_bits_count - 1 (parity_bit)
  if wild_bits_count:
    fill_bits_count = packet_size - wild_bits_count
    for i in range(fill_bits_count):
      data.append(0)

  for i in range(0, len(data), packet_size):
    packet = data[i:i + packet_size]
    packets.append(packet)

  return packets


def print_packets(packets):
  i = 0

  for packet in packets:
    print(f"{i}. {packet}")
    i += 1


def print_processed_packets(packets, processed_packets, coding):
  if coding == 'crc':
    for i in range(len(processed_packets)):
      is_the_same = processed_packets[i][:-3] == packets[i]
      print(f"{i + 1}. {processed_packets[i]}   {is_the_same}")
  elif coding == 'parity_bit':
    for i in range(len(processed_packets)):
      is_the_same = processed_packets[i][:-1] == packets[i]
      print(f"{i + 1}. {processed_packets[i]}   {is_the_same}")


def print_statistics(statistics):
  print("First time good: ", statistics['first_time_good'][0])
  print("Wrong: ", statistics['wrong'][0])
  print("Not found: ", statistics['not_found'][0])

  for i in range(4):
    print(f"Repeated {i + 1} times: ", statistics['repeated'][0][i])

  print(f"Repeated more times: ", statistics['repeated'][0][4], end='\n\n')


def one_sim(packets, probability, num_bits, len_packets):
  processed_packets = []

  statistics = {
    'first_time_good': 0,
    'wrong': 0,
    'not_found': 0,
    'repeated': [0, 0, 0, 0, 0]
  }

  codings = ['crc', 'parity_bit']

  distortions = ['binary_erasure_channel', 'symmetric_binary_channel']

  for coding in codings:
    for distortion in distortions:
      filename = coding + '+' + distortion + '+' + str(probability) + '_' + str(num_bits)+'_'+str(len_packets)+".csv"
      print(f'Using algorithm: ', coding)
      print(f'Using channel: ', distortion, end='\n\n')

      processed_packets, statistics = processor.process_packets(
        packets, coding, distortion, probability)

      data.csv_writer(filename, statistics)

      print_statistics(data.csv_reader(filename))

      print("Printing processed packets:")

      print_processed_packets(packets, processed_packets, coding)

      print('')


def sims(packets,bit_num,packet_len,probability,parameter):
  if parameter=="PRO":
    for prob in probability:
      for _ in range(100):
        one_sim(packets,prob,bit_num,packet_len)
  elif parameter=="PAC":
    for packet in packet_len:
      for _ in range(100):
        one_sim(packets,probability,bit_num,packet)
  elif parameter=="BIT":
    for bit in bit_num:
      for _ in range(100):
        one_sim(packets, probability, bit, packet_len)


def analyse_data(bit_num,packet_len,probability,parameter):
  files=os.listdir()
  if parameter == "PRO":
    variations=len(probability)
    for i in range(0,len(files),variations):
      data.make_plot_from_csv(files[i:i+variations],0)
  elif parameter=="PAC":
    variations = len(packet_len)
    for i in range(0, len(files), variations):
      data.make_plot_from_csv(files[i:i + variations], 0)
  elif parameter=="BIT":
    variations = len(bit_num)
    for i in range(0, len(files), variations):
      data.make_plot_from_csv(files[i:i + variations], 0)


def run():
  parameter="PRO"
  bit_num=256
  packet_len=8
  probability=[0.05,0.1,0.15,0.2]
  os.mkdir(f'csv_{probability}_{packet_len}_{bit_num}')
  os.chdir(f'csv_{probability}_{packet_len}_{bit_num}')
  packets = create_packet(generate_data(bit_num), packet_len)
  sims(packets,bit_num,packet_len,probability,parameter)
  analyse_data(bit_num,packet_len,probability,parameter)
  print_packets(packets)
  print('')


