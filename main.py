import sys
import os
import tkinter as tk
from core.app import SchoolTestApp


def hide_console():
    """Скрывает консоль на Windows"""
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


if __name__ == "__main__":
    # Сначала скрываем консоль
    hide_console()

    # Затем создаем GUI
    root = tk.Tk()
    app = SchoolTestApp(root)

    # Запускаем главный цикл
    root.mainloop()