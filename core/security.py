import ctypes
import platform
from ctypes import wintypes


class SystemSecurity:
    def __init__(self, root):
        self.root = root
        if platform.system() == "Windows":
            self.user32 = ctypes.windll.user32
            self.setup_hooks()
        else:
            self.user32 = None
            self.hook_id = None

    def setup_hooks(self):
        """Устанавливает хук клавиатуры только для системных комбинаций"""

        class KBDLLHOOKSTRUCT(ctypes.Structure):
            _fields_ = [("vkCode", wintypes.DWORD),
                        ("scanCode", wintypes.DWORD),
                        ("flags", wintypes.DWORD),
                        ("time", wintypes.DWORD),
                        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))]

        HOOKPROC = ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(KBDLLHOOKSTRUCT)
        )

        def keyboard_callback(nCode, wParam, lParam):
            if nCode >= 0 and wParam == 0x100:  # WM_KEYDOWN
                kbd = lParam.contents
                vk_code = kbd.vkCode

                # Проверяем состояние модификаторов
                alt = self.user32.GetAsyncKeyState(0x12) & 0x8000  # ALT
                ctrl = self.user32.GetAsyncKeyState(0x11) & 0x8000  # CTRL
                win = self.user32.GetAsyncKeyState(0x5B) & 0x8000  # WIN

                # Блокируем только конкретные комбинации:
                if (vk_code == 0x09 and (alt or win)):  # Alt+Tab, Win+Tab
                    return 1
                if (vk_code == 0x73 and alt):  # Alt+F4
                    return 1
                if (vk_code == 0x1B and (alt or ctrl)):  # Alt+Esc, Ctrl+Esc
                    return 1
                if vk_code in (0x5B, 0x5C):  # Win key
                    return 1

            return self.user32.CallNextHookEx(self.hook_id, nCode, wParam, ctypes.byref(lParam.contents))

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

        # Блокируем опасные комбинации через tkinter
        self.root.bind("<Alt-F4>", lambda e: "break")
        self.root.bind("<Control-Alt-Delete>", lambda e: "break")
        self.root.bind("<Escape>", lambda e: "break")
        self.root.bind("<Alt-Tab>", lambda e: "break")
        self.root.bind("<Meta-Tab>", lambda e: "break")

    def release_hooks(self):
        """Снимает все блокировки"""
        if hasattr(self, 'hook_id') and self.hook_id and self.user32:
            self.user32.UnhookWindowsHookEx(self.hook_id)