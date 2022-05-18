import csv, ast

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

