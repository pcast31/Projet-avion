import tkinter as tk


def dyna_ffichage(N, P):
    root = tk.Tk()

    canvas = tk.Canvas(root, width=30 * N + 10 * (N + 1), height=30 * (P + 1) + 10 * (P + 2))
    canvas.pack()

    canvas.create_rectangle(0, 0, 30 * N + 10 * (N + 1), 30 * (P + 1) + 10 * (P + 2), fill='#3C3C4B')

    root.mainloop()


if __name__ == '__main__':
    dyna_ffichage(30, 6)