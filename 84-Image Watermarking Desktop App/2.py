from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()

path = filedialog.askopenfilename()
watermatk_path = filedialog.askopenfilename()

img = Image.open(path)

watermark = Image.open(watermatk_path).convert("RGBA")
watermark = watermark.resize((100, 100))

new_img = Image.new('RGBA', (img.size[0], img.size[1]), (255,255,255))
new_img.paste(img, (0, 0))
new_img.paste(watermark, (img.size[0]-100, img.size[1]-100), watermark)
new_img.save("watermarked_img.png", format='png')

watermarked_image = Image.open("watermarked_img.png")


photoimg = ImageTk.PhotoImage(watermarked_image)
panelA = tk.Label(image=photoimg)
# panelA.image = photoimg
panelA.pack(side="left", padx=10, pady=10)

root.mainloop()