def create_package(data, package_size):
  packaged_data = []
  for i in range(0, len(data), package_size):
    packaged_data.append(data[i:i + package_size])
  return packaged_data
