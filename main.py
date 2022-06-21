from tkinter import *
from tkinter import messagebox
import random
import json
# import pyperclip

WINDOW_TITLE_TEXT = "Password Manager"
WEBSITE_LABEL_TEXT = "Website:"
EMAIL_USER_NAME_LABEL_TEXT = "Email/User name:"
PASSWORD_LABEL_TEXT = "Password:"
data = {}

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    password = ''.join(password_list)
    password_entry.insert(0, password)

    # pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    global data
    website = (website_entry.get()).title()
    password = password_entry.get()
    email = email_user_name_entry.get()
    data_dic = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Ops!", message="Don't let any blank field")
    else:
        ask_if_wanna_save = messagebox.askokcancel(title="Attention!", message="Do you wanna save this information?")

        if ask_if_wanna_save:
            try:
                read_json()
            except FileNotFoundError:
                with open("C:/Users/Lucas/Documents/passwords.json", mode="w") as data_file:
                    json.dump(data_dic, data_file, indent=4)
            else:
                data.update(data_dic)
                with open("C:/Users/Lucas/Documents/passwords.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


def read_json():
    global data
    with open("C:/Users/Lucas/Documents/passwords.json", mode="r") as data_file:
        data = json.load(data_file)


def search():
    global data
    read_json()
    website_to_search = (website_entry.get()).title()
    try:
        searched_website = data[website_to_search]
    except KeyError:
        messagebox.showerror(title="ERROR", message="Item not found")
    else:
        searched_email = searched_website['email']
        searched_password = searched_website['password']
        messagebox.showinfo(title=f"{website_to_search}", message=f"email: {searched_email}"
                                  f"\npassword: {searched_password}")

        email_user_name_entry.delete(0, END)
        email_user_name_entry.insert(END, searched_email)
        password_entry.delete(0, END)
        password_entry.insert(END, searched_password)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title(WINDOW_TITLE_TEXT)
window.config(padx=50, pady=50)

bg_padlock_image = PhotoImage(file="C:/Users/Lucas/Documents/Projects/password_manager/logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=bg_padlock_image)
canvas.grid(column=1, row=0)

website_label = Label(text=WEBSITE_LABEL_TEXT)
website_label.grid(column=0, row=1, sticky="e")
email_user_name_label = Label(text=EMAIL_USER_NAME_LABEL_TEXT)
email_user_name_label.grid(column=0, row=2)
password_label = Label(text=PASSWORD_LABEL_TEXT)
password_label.grid(column=0, row=3, sticky="e")

website_entry = Entry(width=34)
website_entry.grid(column=1, row=1, sticky="w")
website_entry.focus()
email_user_name_entry = Entry(width=53)
email_user_name_entry.grid(column=1, row=2, columnspan=2, sticky="w")
email_user_name_entry.insert(0, "example@gmail.com")
password_entry = Entry(width=34)
password_entry.grid(row=3, column=1, sticky="w")

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
add_button = Button(text="Add", width=45, command=save_data)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", command=search, width=14)
search_button.grid(column=2, row=1)

window.mainloop()
