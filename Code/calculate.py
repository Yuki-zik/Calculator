# author：马千里
# time：2024/3/9 20:00

import re
import time
import tkinter as tk
from tkinter import ttk
import sv_ttk
from model import calculate as calc


class App(ttk.Frame):

    def INS(self, text):
        def inner(event=None):
            self.current.set(self.current.get() + str(text))
            return "break"

        return inner

    def CLEAR(self):
        if self.current.get():
            self.current.set("")
        else:
            self.result.set("")
        return "break"

    def BACKSPACE(self):
        self.current.set(self.current.get()[:-1])
        return "break"

    def RUN(self):
        self.result.set(self.current.get())
        try:
            self.current.set(calc(re.sub(r"\s+", "", self.current.get())))
        except Exception as e:
            self.current.set(f"ERR: {e}")
        return "break"

    def root_shortcuts(self, root):
        root.bind("<Control-w>", lambda e: fadeout(root))
        root.bind("<Escape>", lambda e: self.CLEAR())
        root.bind("<Return>", lambda e: self.RUN())
        root.bind("=", lambda e: self.RUN())
        root.bind("<space>", lambda e: self.RUN())

    def btn_shortcuts_on(self, root):
        root.bind("<BackSpace>", lambda e: self.BACKSPACE())
        for i in "1234567890+-()":
            root.bind(str(i), self.INS(i))
        root.bind("*", self.INS("×"))
        root.bind("/", self.INS("÷"))
        root.bind("\\", self.INS("÷"))
        root.bind("%", self.INS("%"))
        root.bind(".", self.INS("."))

    def btn_shortcuts_off(self, root):
        root.bind("<BackSpace>", "")
        for i in "1234567890+-()":
            root.bind(str(i), "")
        root.bind("*", "")
        root.bind("/", "")
        root.bind("\\", "")
        root.bind("%", "")
        root.bind(".", "")

    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.root_shortcuts(master)

        # 设置应用程序的响应式布局
        for index in range(6):
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index + 2, weight=1)

        self.result = tk.StringVar(value="")
        self.current = tk.StringVar(value="")

        # 创建标签显示计算结果
        tk.Label(
            self,
            anchor="e",
            font=("Segoe UI", 11),
            textvariable=self.result,
        ).grid(row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=(15, 0))
        self.update()

        self.text = tk.Entry(
            self,
            justify="right",
            bd=0,
            font=("Segoe UI", 20),
            textvariable=self.current,
        )
        self.text.grid(
            row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=(0, 10)
        )
        self.btn_shortcuts_on(self.text)  # 在输入框内不启用部分重叠的快捷键
        self.text.bind("<FocusIn>", lambda e: self.btn_shortcuts_off(master))
        self.text.bind("<FocusOut>", lambda e: self.btn_shortcuts_on(master))
        self.update()
        self.text.focus()

        # 创建按钮
        keys = {
            "(": "(",
            "#\ue94c": "%",
            "7": "7",
            "4": "4",
            "1": "1",
            "#\uf08c": sv_ttk.toggle_theme,  # ☀
            ")": ")",
            "x²": "²",
            "8": "8",
            "5": "5",
            "2": "2",
            "0": "0",
            "#\ue75c": self.CLEAR,  # 🗑️
            "#\ue94b": "√",
            "9": "9",
            "6": "6",
            "3": "3",
            "·": ".",
            "#\ue94f": self.BACKSPACE,  # ⌫
            "#\ue94a": "÷",
            "#\ue947": "×",
            "#\ue949": "-",
            "#\ue948": "+",
            "#\ue94e": self.RUN,  # =
        }
        for index, (text, command) in enumerate(keys.items()):
            self.update()
            if isinstance(command, str) or command is ...:
                command = self.INS(command)
            ttk.Button(
                self,
                text=text.lstrip("#"),
                width=100,
                style=("Accent.TButton" if text == "#\ue94e" else "TButton"),
                command=command,
            ).grid(row=index % 6 + 2, column=index // 6, sticky="nesw", padx=2, pady=2)


def fadein(root):
    import time

    alpha = 0.5
    while alpha <= 1:
        root.attributes("-alpha", alpha)
        alpha += 0.02
        root.update()
        time.sleep(0.01)
    root.attributes("-alpha", 1)


def fadeout(root):
    global destruction_started
    if destruction_started:
        return
    destruction_started = True
    alpha = 1
    while alpha >= 0:
        root.attributes("-alpha", alpha)
        root.update()
        x = root.winfo_x()
        y = root.winfo_y()
        root.geometry(f"+{x}+{int(y + (1-alpha)*10)}")
        alpha -= 0.3 * (1 - alpha) + 0.00001
        root.update()
        time.sleep(0.01)

    root.attributes("-alpha", 0)
    root.destroy()


def main():
    global destruction_started
    destruction_started = False

    root = tk.Tk()
    root.title("计算器")
    root.geometry("400x600")
    root.attributes("-alpha", 0.5)
    sv_ttk.set_theme("light")

    # 设置默认字体为Segoe UI
    # ttk.Style().configure("TButton", font=("Segoe UI", 13), padding=(0, 5, 0, 0))
    # ttk.Style().configure("Icon.TButton", font=("Segoe UI", 12), padding=(0, 5, 0, 0))
    # ttk.Style().configure("Accent.TButton", font=("Segoe UI", 12), padding=(0, 5, 0, 0))

    app = App(root)
    app.pack(fill="both", expand=True, padx=0, pady=0)

    # 设置窗口的最小大小
    root.update()
    width, height = root.winfo_width(), root.winfo_height()
    root.minsize(width, height)

    # 启动窗口
    root.after(0, lambda: fadein(root))
    root.protocol("WM_DELETE_WINDOW", lambda: fadeout(root))
    root.mainloop()


if __name__ == "__main__":
    main()
