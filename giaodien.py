import tkinter as tk
from tkinter import Label, Listbox, Button
import openpyxl
import threading
import os
from PIL import Image, ImageTk

class MyWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x600')
        self.root.title('Ứng dụng thông báo nhu cầu thức ăn cho tôm')

        self.result_list = []
        self.image_list = []
        self.current_index = 0
        self.need_to_feed = False
        self.processing_paused = False

        self.result_listbox = Listbox(root, width=40, height=10)
        self.result_listbox.pack(pady=20)

        self.label = Label(root, text='', font=('Helvetica', 16))
        self.label.pack()

        self.image_display = tk.Label(root)
        self.image_display.pack()

        self.start_button = Button(root, text='Bắt đầu xử lý', command=self.start_processing)
        self.start_button.pack()

        self.accept_button = Button(root, text='Chấp nhận', command=self.accept_input, state=tk.DISABLED)
        self.accept_button.pack()

        self.program_running = True
        self.load_results_thread = threading.Thread(target=self.load_results_from_excel, daemon=True)

    def start_processing(self):
        self.accept_button.config(state=tk.DISABLED)
        self.result_listbox.delete(0, tk.END)
        self.need_to_feed = False
        self.processing_paused = False
        self.current_index = 0

        if not self.load_results_thread.is_alive():
            self.load_results_thread = threading.Thread(target=self.load_results_from_excel, daemon=True)
            self.load_results_thread.start()

        # Bắt đầu tự động tải hình ảnh sau mỗi giây
        self.auto_load_images()

    def auto_load_images(self):
        self.load_images()
        self.root.after(1000, self.auto_load_images)

    def load_results_from_excel(self):
        try:
            workbook = openpyxl.load_workbook('results.xlsx')
            sheet = workbook.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                result = row[1]
                self.result_list.append(result)
                self.result_listbox.insert(tk.END, result)

                if len(self.result_list) > 10:
                    self.result_list.pop(0)
                    self.result_listbox.delete(0)

                if len(self.result_list) == 10 and self.result_list.count("Eating") >= 7:
                    self.label.config(text='Cần cho ăn')
                    self.need_to_feed = True
                    self.accept_button.config(state=tk.NORMAL)
                    self.processing_paused = True

                elif 4 < self.result_list.count("Eating") < 7:
                    self.label.config(text='Đang ăn chậm')
                    self.need_to_feed = True
                    self.accept_button.config(state=tk.NORMAL)
                    self.processing_paused = True

                else:
                    self.label.config(text='Không cần cho ăn')
                    self.need_to_feed = False
                    self.accept_button.config(state=tk.DISABLED)

                self.root.update()
                self.root.after(1000)

            workbook.close()

        except Exception as e:
            print(f"Lỗi khi tải kết quả từ Excel: {e}")

    def load_images(self):
        try:
            # Tạo danh sách số từ 1 đến 600
            image_numbers = list(range(1, 601))

            image_name = f"{image_numbers[self.current_index]}.png"
            image_path = os.path.join('chart', image_name)
            image = Image.open(image_path)
            image = image.resize((400, 300), Image.ANTIALIAS)
            image_tk = ImageTk.PhotoImage(image)
            self.image_list.append(image_tk)
            self.display_current_image(image_tk, image_name)

            self.current_index = (self.current_index + 1) % len(image_numbers)

        except Exception as e:
            print(f"Lỗi khi tải hình ảnh: {e}")

    def check_image_list_length(self):
        if len(self.image_list) >= 10:
            self.image_list.pop(0)

    def display_current_image(self, image_tk, image_name):
        self.image_display.config(image=image_tk)
        self.image_display.image = image_tk
        print(f"Đã hiển thị hình ảnh: {image_name}")

    def accept_input(self):
        self.accept_button.config(state=tk.DISABLED)
        self.processing_paused = False

    def reset_status(self):
        self.label.config(text='Đang xử lý')
        self.need_to_feed = False
        self.accept_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    window = MyWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
