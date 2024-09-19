from PIL import Image, ImageTk
import tkinter as tk


root = tk.Tk()
root.geometry("1000x1000")
root.title("Splash Screen")

try:
    image = Image.open("logo.png")
    image = image.resize((900, 600), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
except FileNotFoundError:
    print("Error")
    root.destroy()
    exit()
except Exception as e:
    print("IDK WHAT HAPPEND")
    root.destroy()
    exit()
label = tk.Label(root, image=photo, bg="black")
label.place(x=0, y=0, relwidth=1, relheight=1)
label.pack(pady=50)  


def close_window():
    root.destroy()

root.after(3000, close_window)

root.mainloop()
