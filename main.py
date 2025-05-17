import sys
import ctypes
import tkinter as tk
from core.app import SchoolTestApp


def is_admin():
    """Проверяет права администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    # На Windows требуем права администратора
    if sys.platform == "win32" and not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

    # Создаем и запускаем приложение
    root = tk.Tk()
    app = SchoolTestApp(root)
    root.mainloop()