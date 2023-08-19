from tkinter import *
from tkinter import messagebox
import pyperclip  # Used to copy words to clipboard
import json
from json.decoder import JSONDecodeError


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
    password_list += [random.choice(letters) for i in range(nr_letters)]
    password_list += [random.choice(symbols) for i in range(nr_symbols)]
    password_list += [random.choice(numbers) for i in range(nr_numbers)]
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    # Nested dictionary
    new_data = {website: {
        "email": email,
        "password": password
    }}
    if len(email) == 0 or len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="OPPS!!", message="Please dont leave any field empty.")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"Email/Username:{email}\nPassword:{password}\nIs this ok?")
        if is_ok:
            try:
                with open("password.json", 'r') as file:
                    # Reading the old data
                    data = json.load(file)
                    # Updating the new data
                    data.update(new_data)
            except FileNotFoundError:
                with open("password.json", 'w') as file:
                    # Writing in the file
                    json.dump(new_data, file, indent=4)  # indent helps us read
            else:
                with open("password.json", 'w') as file:
                    # Saving in the file
                    json.dump(data, file, indent=4)  # indent helps us read

        password_entry.delete(0, END)
        website_entry.delete(0, END)
        email_entry.delete(0, END)
        website_entry.focus()


# ---------------------------- SEARCH ------------------------------- #
def search():
    try:
        with open("password.json", "r") as file:
            data = json.load(file)
            try:
                website = website_entry.get().title()
                messagebox.showinfo(title=website,
                                    message=f"Email:{data[website]['email']}\nPassword:{data[website]['password']}")
            except KeyError:

                messagebox.showwarning(title="Opps!", message=f"No data named {website} found in file")
    except JSONDecodeError:  # Empty file error
        messagebox.showwarning(title="Opps!!", message="File is empty")
    except FileNotFoundError:
        messagebox.showwarning(title="Opps!!", message="File not found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(pady=50, padx=50, bg="#FFFFFF")
window.title("Password Manager")

# Canvas
canvas = Canvas(width=200, height=200, highlightthickness=0, bg="#FFFFFF")
tomato = PhotoImage(file="logo.png")  # TO read thorough the file and get the image
canvas.create_image(100, 100, image=tomato)
canvas.grid(row=1, column=2)

# Website_label
website_label = Label(text="Website:", bg="#FFFFFF")
website_label.grid(row=2, column=1)

# Website_Entry
website_entry = Entry(width=37, bg="#FFFFFF")
website_entry.focus()  # focus or start cursor in that entry
website_entry.grid(row=2, column=2)

# Search btn
search_btn = Button(text="Search", bg="#FFFFFF", width=17, command=search)
search_btn.grid(row=2, column=3)

# email_label
email_label = Label(text="Email/Username:", bg="#FFFFFF")
email_label.grid(row=3, column=1)

# email_Entry
email_entry = Entry(width=59, bg="#FFFFFF")
email_entry.grid(row=3, column=2, columnspan=2)

# password_label
password_label = Label(text="Password:", bg="#FFFFFF")
password_label.grid(row=4, column=1)

# password_Entry
password_entry = Entry(width=37, bg="#FFFFFF")
password_entry.grid(row=4, column=2)

# generate_button
generate_btn = Button(text="Generate Password", bg="#FFFFFF", width=17, command=generate_password)
generate_btn.grid(row=4, column=3)

# Add_button
add_btn = Button(text="Add", bg="#FFFFFF", width=50, command=save_data)
add_btn.grid(row=5, column=2, columnspan=2)

window.mainloop()
