import ctypes
import platform
from ctypes import wintypes


class SystemSecurity:
    def __init__(self, root):
        self.root = root
        self.user32 = ctypes.windll.user32 if platform.system() == "Windows" else None
        self.hook_id = None
        if platform.system() == "Windows":
            self.setup_hooks()

    def setup_hooks(self):
        """Устанавливает системные хуки для блокировки клавиш"""
        HOOKPROC = ctypes.WINFUNCTYPE(
            wintypes.HHOOK,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM
        )

        def keyboard_callback(nCode, wParam, lParam):
            if nCode >= 0:
                kbd = ctypes.cast(lParam, ctypes.POINTER(ctypes.c_ulong)).contents
                vk_code = kbd.vkCode

                alt_pressed = self.user32.GetAsyncKeyState(0x12) & 0x8000
                ctrl_pressed = self.user32.GetAsyncKeyState(0x11) & 0x8000
                win_pressed = self.user32.GetAsyncKeyState(0x5B) & 0x8000

                # Блокируем только системные комбинации
                if (vk_code == 0x09 and (alt_pressed or win_pressed)):  # Alt+Tab, Win+Tab
                    return 1
                if (vk_code == 0x73 and alt_pressed):  # Alt+F4
                    return 1
                if (vk_code == 0x1B and (alt_pressed or ctrl_pressed)):  # Alt+Esc, Ctrl+Esc
                    return 1
                if vk_code in (0x5B, 0x5C):  # Win key
                    return 1

            return self.user32.CallNextHookEx(self.hook_id, nCode, wParam, lParam)

        self.hook_proc = HOOKPROC(keyboard_callback)
        self.hook_id = self.user32.SetWindowsHookExA(
            13,  # WH_KEYBOARD_LL
            self.hook_proc,
            None,
            0
        )

    def disable_window_controls(self):
        """Отключает стандартные элементы управления окном"""
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")

        # Дополнительная блокировка через tkinter
        self.root.bind("<Alt-F4>", lambda e: "break")
        self.root.bind("<Control-Alt-Delete>", lambda e: "break")
        self.root.bind("<Escape>", lambda e: "break")
        self.root.bind("<Alt-Tab>", lambda e: "break")
        self.root.bind("<Meta-Tab>", lambda e: "break")

    def release_hooks(self):
        """Освобождает системные хуки"""
        if self.hook_id and self.user32:
            self.user32.UnhookWindowsHookEx(self.hook_id)