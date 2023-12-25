import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import os


class MyWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry('600x400')
        self.root.title('Ứng dụng tải lần lượt hình ảnh')

        self.image_list = []
        self.current_index = 0

        self.image_display = tk.Label(root)
        self.image_display.pack(pady=20)

        self.load_images_button = Button(root, text='Tải hình ảnh', command=self.load_images)
        self.load_images_button.pack()

        self.program_running = True
        self.auto_load_images()

    def auto_load_images(self):
        self.load_images()
        self.root.after(1000, self.auto_load_images)

    def load_images(self):
        image_dir = 'chart'  # Thay đổi đường dẫn thư mục với thư mục chứa hình ảnh của bạn
        try:
            # Tạo danh sách số từ 1 đến 600
            image_numbers = list(range(1, 601))

            # Đảm bảo không còn hơn 10 hình ảnh trong danh sách
            if len(self.image_list) >= 10:
                self.image_list.pop(0)

            image_path = os.path.join(image_dir, f"{image_numbers[self.current_index]}.png")
            image = Image.open(image_path)
            image = image.resize((400, 300), Image.ANTIALIAS)
            image_tk = ImageTk.PhotoImage(image)
            self.image_list.append(image_tk)

            # Hiển thị hình ảnh hiện tại
            self.image_display.config(image=image_tk)
            self.image_display.image = image_tk

            self.current_index = (self.current_index + 1) % len(image_numbers)

        except Exception as e:
            print(f"Lỗi khi tải hình ảnh: {e}")


def main():
    root = tk.Tk()
    window = MyWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
