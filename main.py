from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

BG_COLOR = "#C0D8C0"


# ---------------------------- SEARCH ------------------------------- #
def search():
    website_input = website_entry.get()
    if len(website_input) == 0:
        messagebox.showwarning(title="Empty Input detected", message="Type in the website that you are looking for.")
    else:
        try:
            with open(file="saved_passwords.json", mode="r") as save_file:
                data = json.load(save_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            messagebox.showwarning(title="No Entries", message="You have no saved passwords yet. "
                                                               "Try adding them first.")
        else:
            if website_input in data:
                messagebox.showinfo(title=f"{website_input}",
                                    message=f"Email: {data[website_input]['email']} \n"
                                            f"Password: {data[website_input]['password']}")
            else:
                messagebox.showinfo(title="Website not found", message="No entry for this website found!")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for x in range(randint(8, 10))]
    password_symbols = [choice(symbols) for x in range(randint(2, 4))]
    password_numbers = [choice(numbers) for x in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    print(password)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_input = website_entry.get()
    email_input = email_entry.get()
    password_input = password_entry.get()
    new_data = {website_input: {
        "email": email_input,
        "password": password_input
    }}

    if len(website_input) == 0 or len(password_input) == 0:
        messagebox.showwarning(title="Empty Input detected", message="Empty entries are not accepted! Try again.")
    else:
        messagebox.showinfo(title="", message="Password saved!")

        website_entry.delete(0, "end")
        password_entry.delete(0, "end")

        website_entry.focus()

        try:
            with open(file="saved_passwords.json", mode="r") as save_file:
                # Reading old data
                data = json.load(save_file)
                # Updating old data with new data
                data.update(new_data)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = new_data
        finally:
            with open(file="saved_passwords.json", mode="w") as save_file:
                # Saving updated data
                json.dump(data, save_file, indent=4)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("MyPass")
window.config(padx=40, pady=40, bg=BG_COLOR)

canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
canvas_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=canvas_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", bg=BG_COLOR)
website_label.grid(row=1, column=0)

website_entry = Entry()
website_entry.grid(row=1, column=1, sticky="EW")
website_entry.focus()

website_search_button = Button(text="Search", command=search)
website_search_button.grid(row=1, column=2, sticky="EW")

email_label = Label(text="Email/Username:", bg=BG_COLOR)
email_label.grid(row=2, column=0)

email_entry = Entry()
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, "dummymail@test.org")

password_label = Label(text="Password:", bg=BG_COLOR)
password_label.grid(row=3, column=0)

password_entry = Entry()
password_entry.grid(row=3, column=1, sticky="EW")

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2, sticky="EW")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
