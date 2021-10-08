from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont

FONT = ("Georgia", 18, "bold")


# TODO. Functions


def add_img():
    global img, tk_img
    x = filedialog.askopenfilename(title="open")
    img = Image.open(x)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img = img.resize((600, 600), Image.ANTIALIAS)
    tk_img = ImageTk.PhotoImage(img)
    panel.config(image=tk_img)
    panel.image = tk_img
    # canvas.itemconfig(sample_img, image = img)


def display_img():
    img = ImageTk.PhotoImage(Image.open("./images/w.jpg"))
    panel.config(image=img)
    panel.image = img


def watermark_img_text():
    global width, height
    draw = ImageDraw.Draw(img)

    text = watermark_entry.get()
    font = ImageFont.load_default()
    textwidth, textheight = draw.textsize(text)

    width, height = img.size
    margin = 10
    x = width - textwidth - margin
    y = height - textheight - margin

    colors = img.getpixel((textwidth,textheight))
    print(colors)

    draw.text((x, y), text=text, font=font)
    img.save("./images/w.jpg")
    display_img()


# TODO. UI Design

window = Tk()
window.title("Watermark Your Images")
window.config(padx=40, pady=40)

add_img_btn = Button(text="Add Image",
                     highlightthickness=0,
                     relief="solid",
                     bd=1,
                     command=add_img,
                     padx=5,
                     pady=50,
                     font=FONT)
add_img_btn.grid(row=0, column=0)


watermark_entry = Entry(width=30,
                        relief="solid")

watermark_entry.grid(row=1, column=0)
watermark_entry.focus()

add_watermark = Button(text="Watermark It!",
                       highlightthickness=0,
                       relief="solid",
                       bd=1,
                       command=watermark_img_text,
                       padx=5,
                       pady=50,
                       font=FONT)
add_watermark.grid(row=2, column=0)

img = Image.open("./images/o-o.jpeg")
img = img.resize((1000, 600), Image.ANTIALIAS)
width, height = img.size
tk_img = ImageTk.PhotoImage(img)
panel = Label(image=tk_img)
panel.image = tk_img
panel.grid(row=0, column=1, rowspan=4, padx=25)

window.mainloop()