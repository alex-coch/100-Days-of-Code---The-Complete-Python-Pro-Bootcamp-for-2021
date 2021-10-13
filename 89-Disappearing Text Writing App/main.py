from tkinter import *

root = Tk()
root.geometry(('700x600'))
root.config(pady=40, padx=40)
txt = '' 

# image= PhotoImage(file='logo1.png')
# label= Label(root, image=image, justify='center')
label= Label(root, justify='center')
label.pack()

def delete_txt():
    global label
    label1.destroy()
    tx = 'Kapooooooooom, text is gone!'
    bye = Label(root, text=tx, font=('Helvetica', 30, 'bold'), justify='center', fg='red')
    bye.pack()
    ex = Button(root, command=root.destroy, relief=RAISED, text='Exit', padx=20, pady=20)
    ex.pack()


label1 = Label(root, text=txt)
label1.pack()
des = ''

info = Label(root, text="Start typing after you press 'Start typing' \n text will disappear after 6 seconds of "
                        "inactivity ", font=('Helvetica', 20, 'bold'), justify='center', fg='red')
info.pack()

def start():
    global des
    info.destroy()
    btn.destroy()
    des = root.after(6000, delete_txt)


btn = Button(root, command=start, relief=RAISED, padx=20, pady=20, text='Start typing')
btn.pack(pady=20)

def writing(event=None):
    global txt, label1, des
    root.after_cancel(des)
    txt += event.char
    label1.config(text=txt, font=('Helvetica', 20, 'bold'), justify='center', wraplength=600)
    des = root.after(6000, delete_txt)



root.bind('<Key>', writing)

def backspace(event):
    global txt, label1
    txt = txt[:-1]
    label1.config(text=txt)

root.bind('<BackSpace>', backspace)


root.mainloop()