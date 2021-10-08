import tkinter as tk
import time
import random
import requests

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()
print(WORDS)

# bg='#0fcc1a'


root = tk.Tk()
root.configure(bg='#7765e3')
root.geometry("810x400")

start_time = None
end_time = None


def generate_text(word_base=WORDS):
    text_to_type = 'Type this text: '
    for i in range(40):
        if i % 4 == 0:
            text_to_type += '\n'
        text_to_type += str(random.choice(word_base)) + ' '
    return text_to_type
   


def time_start(event):
    global start_time
    start_time = time.time()
    print(start_time)



def time_end():
    global end_time
    end_time = time.time()
    print(end_time)


def start():
    root.destroy()
    new_root = tk.Tk()
    new_root.geometry("800x600")
    new_root.configure(bg='#7765e3')
    rules = tk.Label(
        new_root, 
        text="When you click the text" \
            "field program will start timer\n" \
            "When you click 'STOP' " \
            "button timer will stop",
        bg='#d6f9dd',
        fg='#3b60e4')
    rules.place(x=228.5, y=40)

    text_to_type = generate_text()

    text = tk.Label(
        new_root, 
        text=text_to_type, 
        fg='#080708', 
        font="Ubuntu 20",
        bg='#7765e3')
    text.place(x=142.5, y=90)

    typing_field = tk.Entry(new_root, width=30)
    typing_field.place(x=265.5, y=495)
    typing_field.bind("<FocusIn>", time_start)

    def show_result(entry=typing_field, text_to_type=text_to_type, results=text):
        time_end()
        written_text = typing_field.get()
        writing_time = (end_time - start_time) / 60
        wpm = (len(written_text) / 5 ) / writing_time
        spm = len(written_text) / writing_time
        mistakes = 0
        if written_text < text_to_type:
            bigger = len(written_text)
        else:
            bigger = text_to_type

        for i in range(bigger):
            if written_text[i] != text_to_type[i]:
                mistakes += 1
        
        if len(written_text) != len(text_to_type):
            mistakes += abs(len(written_text) - len(text_to_type))

        accuracy = (len(text_to_type) - mistakes / len(text_to_type)) * 100
        text.configure(
            text = f'\tYour results are\n' \
                f'\t{wpm} words per minute\n' \
                f'\t{spm} signs per minute\n' \
                f'\taccuracy {accuracy}'
        )


    
    end_button = tk.Button(
        new_root, 
        text="STOP", 
        command=show_result,
        relief='solid',
        bg='#c8adc0',
        fg='#3b60e4'
        )
    end_button.place(x=369, y=545)


header = tk.Label(
    root, 
    fg='#3b60e4', 
    text='CHECK YOUR TYPING SPEED IN MY APP FOR FREE', 
    font="Ubuntu 20",
    bg='#7765e3')
header.place(
    x=95, 
    y=40)


start_button = tk.Button(
    root, text='Start typing', 
    command=start,
    relief='solid',
    bg='#c8adc0',
    fg='#3b60e4',
    highlightthickness = 0
    )

start_button.place(x=350, y=330)



if __name__ == '__main__':
    root.mainloop()