import sys

def read_coordinates(file_path):
    print("Koordinatları dosyadan okuma...")
    x_coordinates = []
    y_coordinates = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            x, y = map(float, line.strip().split(','))
            if 2754 < x < 2757:
                x, y = 0.0, 0.0
            x_coordinates.append(x)
            y_coordinates.append(y)
    print("Koordinatlar başarıyla okundu.")
    return x_coordinates, y_coordinates

def write_coordinates_to_file(x_values, y_values, file_path):
    print("Düzeltilmiş koordinatları dosyaya yazma...")
    if len(x_values) != len(y_values):
        raise ValueError("X ve Y listelerinin uzunlukları eşit olmalıdır.")
    with open(file_path, 'w') as file:
        for x, y in zip(x_values, y_values):
            file.write(f"{x},{y}\n")
    print(f"Koordinatlar '{file_path}' dosyasına yazıldı.")

def find_next_non_zero(values, start_index):
    for i in range(start_index, len(values)):
        if values[i] != 0.0:
            return i
    return None

def correct_zeros(values, start_index=0):
    while True:
        zero_index = find_next_non_zero(values, start_index)
        if zero_index is None:
            break

        first_non_zero_index = find_next_non_zero(values, zero_index + 1)
        if first_non_zero_index is None:
            break

        zero_count = first_non_zero_index - zero_index - 1
        if zero_count > 0:
            increase_rate = (values[first_non_zero_index] - values[zero_index]) / (zero_count + 1)
            for i in range(zero_index + 1, first_non_zero_index):
                values[i] = values[zero_index] + (i - zero_index) * increase_rate

        start_index = first_non_zero_index + 1
    return values

def correct_backwards(values):
    zero_index = find_next_non_zero(values, 0)
    if zero_index is None:
        return values
    first_non_zero_index = find_next_non_zero(values, zero_index + 1)
    if first_non_zero_index is None:
        return values
    difference = values[first_non_zero_index] - values[zero_index]
    for i in range(zero_index - 1, -1, -1):
        values[i] = values[i + 1] - difference
    return values


# Ana kod
input_file = 'outputs/txt_outputs/ball_coordinates_first.txt'
x_coordinates, y_coordinates = read_coordinates(input_file)

print("X koordinatları için 0.0 değerlerini düzeltme başlıyor...")
corrected_valuesX = correct_zeros(x_coordinates)
print("Y koordinatları için 0.0 değerlerini düzeltme başlıyor...")
corrected_valuesY = correct_zeros(y_coordinates)

temp_file_path = 'outputs/txt_outputs/ball_coordinates_temp.txt'
write_coordinates_to_file(corrected_valuesX, corrected_valuesY, temp_file_path)

corrected_valuesX, corrected_valuesY = read_coordinates(temp_file_path)

print("X koordinatları için geriye doğru tamamlama başlıyor...")
final_valuesX = correct_backwards(corrected_valuesX)
print("Y koordinatları için geriye doğru tamamlama başlıyor...")
final_valuesY = correct_backwards(corrected_valuesY)

output_file_path = 'outputs/txt_outputs/ball_coordinates_final.txt'
write_coordinates_to_file(final_valuesX, final_valuesY, output_file_path)