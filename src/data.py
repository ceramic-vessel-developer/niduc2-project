import csv, ast
import numpy as np
import matplotlib.pyplot as plt

def csv_writer(filename,results):
  with open(filename,'a') as file:
    writer=csv.DictWriter(file,results.keys())
    writer.writerow(results)


def csv_reader(filename):
  results={
    'first_time_good': [],
    'wrong': [],
    'not_found': [],
    'repeated': []
  }
  with open(filename, 'r') as file:
    reader = csv.DictReader(file, fieldnames=results.keys())
    for row in reader:
      results['first_time_good'].append(int(row['first_time_good']))
      results['wrong'].append(int(row['wrong']))
      results['not_found'].append(int(row['not_found']))
      results['repeated'].append(ast.literal_eval(row['repeated']))
  return results


def make_plot_from_csv(files,parameter):
  data=[]
  name=files[0].split('+')[0]+files[0].split('+')[1]
  for file in files:
    record={
    'first_time_good':0,
    'wrong':0,
    'not_found':0
  }
    n=float(file.split('+')[2].split('_')[parameter])
    open_file=csv_reader(file)
    open_file.pop('repeated')
    for key,value in open_file.items():
      record[key]=np.average(value)
    data.append((n,record))
  data.sort()
  x_axis = [x[0] for x in data]
  y_axis_ftg=[x[1]['first_time_good'] for x in data]
  y_axis_w=[x[1]['wrong'] for x in data]
  y_axis_nf=[x[1]['not_found'] for x in data]
  plt.plot(x_axis,y_axis_ftg,label="First time good", marker='o')
  plt.plot(x_axis,y_axis_w,label="Wrong", marker='o')
  plt.plot(x_axis,y_axis_nf,label="Falsely marked as good", marker='o')
  if parameter==0:
    plt.xlabel('Probability of distortion')
  elif parameter==1:
    plt.xlabel('Packet length')
  elif parameter == 1:
    plt.xlabel('Amount of data')
  plt.ylabel('Average number')
  plt.title(name)
  plt.legend()
  plt.show()

