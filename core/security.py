import ctypes
import platform


class SystemSecurity:
    def __init__(self, root_window):
        self.root = root_window
        self.hook_id = None

        if platform.system() == "Windows":
            self.user32 = ctypes.WinDLL('user32')
            self._setup_windows_security()

    def _setup_windows_security(self):
        """Windows-специфичные настройки безопасности"""
        # Блокируем Alt+Tab через низкоуровневый хук
        HOOKPROC = ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_void_p))

        def keyboard_hook(nCode, wParam, lParam):
            # Разрешаем все клавиши кроме системных комбинаций
            return 0

        self.keyboard_hook = HOOKPROC(keyboard_hook)
        self.hook_id = self.user32.SetWindowsHookExA(
            13,  # WH_KEYBOARD_LL
            self.keyboard_hook,
            None,
            0
        )

    def disable_window_controls(self):
        """Отключает элементы управления окном"""
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")

        # Блокируем опасные комбинации
        self.root.bind("<Alt-F4>", lambda e: "break")
        self.root.bind("<Control-Alt-Delete>", lambda e: "break")
        self.root.bind("<Escape>", lambda e: "break")
        self.root.bind("<Alt-Tab>", lambda e: "break")
        self.root.bind("<Meta-Tab>", lambda e: "break")

    def unblock_system(self):
        """Снимает все блокировки"""
        if hasattr(self, 'hook_id') and self.hook_id:
            self.user32.UnhookWindowsHookEx(self.hook_id)