import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ tệp Excel
file_path = 'results.xlsx'
df = pd.read_excel(file_path)

# Chọn cột cần vẽ biểu đồ
column_name = 'Accuracy'
values = df[column_name][:100]

# Tạo biểu đồ đường
plt.plot(values, marker='o', linestyle='-', color='b')
plt.title(f'Biểu đồ độ chính xác của thuật toán')
plt.xlabel('')  # or customize with your own x-axis label
plt.ylabel(column_name)
plt.grid(True)
plt.show()
