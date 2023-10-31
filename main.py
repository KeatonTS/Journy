import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from ttkthemes import ThemedStyle
import dbOperations
from db import *
import connection

# Connect to note database
ndb, conn = connection.start()

# Window configs
root = Tk()
root.resizable(width=False, height=False)
root.title("Journy")
style = ThemedStyle(root)
style.set_theme("scidblue")

# Constant fonts
TITLE_LABEL_FONT = ("calibri", 18, "bold")
STARTER_LABEL_FONT = ("calibri", 12, "bold")
STATIC_LABEL_FONT = ("calibri", 18, "bold")
BUTTON_TEXT_FONT_BOLD = ('calibri', 14, 'bold')
BUTTON_TEXT_FONT = ('calibri', 12)
TEXT_BOX_FONT = ('calibri', 12)
NOTE_MESSAGE_FONT = ('calibri', 12, 'italic')
DATE_FONT = ('calibri', 10, 'underline')

# Button Images
new_note_img = PhotoImage(file='assets/new_note_button.png')
new_note_v2_img = PhotoImage(file='assets/new_note_button_V2.png')
note_bttn_img = PhotoImage(file='assets/note_button.png')
save_bttn_img = PhotoImage(file='assets/save_button.png')
edit_bttn_img = PhotoImage(file='assets/edit_button.png')
delete_bttn_img = PhotoImage(file='assets/delete_button.png')
cancel_bttn_img = PhotoImage(file='assets/cancel_button.png')
back_buttn_img = PhotoImage(file='assets/back_bttn.png')


note_in_progress = False  # Affects UI depending on if a note is being worked on


def clear_widgets(*widget_name: str):
    """
    Removes overlapping widgets when selecting different options in the window.
    *args passed are widget names using the "name=" argument and are processed whenever a change happens. Pass *args
    that you wish to destroy to adjust the window appropriately. Each dynamic widget has a name assigned to it.
    """
    for name in widget_name:

        try:
            widget = root.nametowidget(name)
            widget.destroy()
        except KeyError:  # Ignores any error if the widget doesn't exist. The process should continue no matter what
            pass


def delete_and_refresh(_id):
    """Removes item from db, then refreshes/updates the list of notes"""
    global note_in_progress
    if messagebox.askyesno(title='Confirm', message="Are you sure you want to delete this note?\nThis cannot be undone."):
        dbOperations.deleteNote(noteId=_id, connection=conn, notes=ndb)
        clear_widgets('current_note', 'current_title', 'note_date', 'edit_bttn', 'del_bttn', 'title_label',
                      'note_bttn_2', 'back_bttn', 'note_bttn')
        refresh()
        note_in_progress = False

    return


def get_all_notes():
    """
    Called whenever the main function is run. checks the database for notes. if there are no notes, a message letting
    the user know they have no notes will be generated. Otherwise, a list comprehension is run, creating buttons for the
    total number of notes in "all_notes".
    """
    all_notes = dbOperations.getAllNotes(conn, ndb)
    if not all_notes:
        # no notes add one string
        label = tk.Label(root, text="No notes. Add one!", font=NOTE_MESSAGE_FONT)
        label.place(x=75, y=75)
        separator = ttk.Separator(root, orient='vertical', name='separate')
        separator.place(relx=.34, rely=.11, relwidth=0.002, relheight=0.75)
    else:
        button_box = Text(root, name='bttn_box',  width=25, height=20, state='disabled',
                          background='#F0F0F0', bd=0, cursor='arrow')
        button_box.place(x=65, y=80)
        scroll = ttk.Scrollbar(root, command=button_box.yview, orient='vertical', name='scroll')
        scroll.place(x=270, y=55, relheight=0.75, relwidth=0.010)
        button_box.config(yscrollcommand=scroll.set)

        button_list = [Button(button_box,
                              name=f'note_bttn{all_notes.index(item)}',
                              cursor='hand2',
                              image=note_bttn_img,
                              compound='center',
                              text=f'{item.title}\n{item.date}',
                              bd=0,
                              font=BUTTON_TEXT_FONT,
                              command=lambda i=item: display_note(root, i),
                              justify='left') for item in all_notes
                       ]

        button_list.reverse()
        for buttons in button_list:
            button_box.window_create('end', window=buttons, pady=5)
        clear_widgets('separate')

        return all_notes


def refresh():
    main(root)


def newNote(editing_note=False, item=None):
    """
    Has functions for both saving and editing a note depending on which button a user clicks. Default args are flags
    that only change based on certain conditions.
    """
    global note_in_progress

    note_in_progress = True

    clear_widgets("new_note_button", 'note_bttn_2', 'current_title', 'note_date', 'current_note',
                  'edit_bttn', 'del_bttn', 'back_bttn')

    note_title = Label(root, text="New Note Title:", name='title_label', font=TITLE_LABEL_FONT)
    note_title.place(x=340, y=25)

    note_title_entry = Entry(root, font=STARTER_LABEL_FONT, name='title_entry', width=24, borderwidth=0)
    note_title_entry.place(x=535, y=33)

    today_i_label = Label(root, text="Today, I...", name='today_label', font=STARTER_LABEL_FONT)
    today_i_label.place(x=340, y=80)
    today_input = Text(root, name='today_entry', height=1.5, width=50, font=TEXT_BOX_FONT, wrap='word', borderwidth=0)
    today_input.place(x=350, y=110)

    tmrrw_i_label = Label(root, text="Tomorrow, I...", name='tmrrw_label', font=STARTER_LABEL_FONT)
    tmrrw_i_label.place(x=340, y=180)
    tmrrw_input = Text(root, name='tmrrw_entry', height=1.5, width=50, font=TEXT_BOX_FONT, wrap='word', borderwidth=0)
    tmrrw_input.place(x=350, y=215)

    general_label = Label(root, text="Anything else?", name='general_label', font=STARTER_LABEL_FONT)
    general_label.place(x=340, y=285)
    general_input = Text(root, name='general_entry', height=5, width=50, font=TEXT_BOX_FONT, wrap='word', borderwidth=0)
    general_input.place(x=350, y=315)

    def save(editing):
        """
        Doubles for saving new notes and edited notes, the condition of if a note is being edited is triggered when
        the edit button is pressed. Becomes false again when note is saved or deleted.
        """
        global note_in_progress
        title_answer = note_title_entry.get()
        today_answer = today_input.get("1.0", END).strip()
        tmrrw_answer = tmrrw_input.get("1.0", END).strip()
        general_answer = general_input.get("1.0", END).strip()

        if editing:  # a flag catching if a note is being edited to use the update method rather than create
            if not len(title_answer) > 20:
                dbOperations.updateNote(conn, ndb, item.id, title_answer, today_answer, tmrrw_answer, general_answer)
                note_in_progress = False
                clear_widgets('title_label', 'title_entry', 'today_label', 'today_entry', 'tmrrw_label',
                              'tmrrw_entry', 'general_label', 'general_entry', 'cancel_bttn', 'save_bttn')
                refresh()
                return
            else:
                messagebox.showwarning(message='Title must be less than 20 characters.', title='Error')

        else:
            if not len(title_answer) > 20:
                dbOperations.createNote(conn, ndb,  title_answer, today_answer, tmrrw_answer, general_answer)
                clear_widgets('title_label', 'title_entry', 'today_label', 'today_entry', 'tmrrw_label',
                              'tmrrw_entry', 'general_label', 'general_entry', 'cancel_bttn', 'save_bttn')
                note_in_progress = False
                refresh()
                return

            messagebox.showwarning(message='Title must be less than 20 characters.', title='Error')

    def cancel():
        clear_widgets('title_label', 'title_entry', 'today_label', 'today_entry', 'tmrrw_label', 'tmrrw_entry',
                      'general_label', 'general_entry', 'cancel_bttn', 'save_bttn', 'current_title', 'back_bttn',)
        main(root)

    if editing_note:  # Prefill Entry and Text widgets with text of the note being edited
        clear_widgets('current_note', 'note_date', 'edit_bttn', 'del_bttn', 'back_bttn')
        note_title_entry.insert('end', f'{item.title}')
        today_input.insert('end', item.today)
        tmrrw_input.insert('end', item.tomorrow)
        general_input.insert('end', item.general)

    save_button = Button(root, image=save_bttn_img, bd=0, name='save_bttn', command=lambda: save(editing_note))
    save_button.place(x=654, y=425)
    cancel_button = Button(root, image=cancel_bttn_img, bd=0, name='cancel_bttn', command=cancel)
    cancel_button.place(x=545, y=425)


def display_note(root, item):
    """
    Structures the right view of the root window to display the selected note. Creates all buttons appropriate to
    the selected note.
    """
    global note_in_progress

    # Clear the previous note from displaying overtop
    if note_in_progress:
        clear_widgets('title_label', 'title_entry', 'today_label', 'today_entry', 'tmrrw_label', 'tmrrw_entry',
                          'general_label', 'general_entry', 'cancel_bttn', 'save_bttn')
        note_in_progress = False

    try:
        clear_widgets('current_note')
    except KeyError:
        pass

    note_title_label = Label(text=f'{item.title}', font=STATIC_LABEL_FONT, name='current_title')
    note_title_label.place(x=350, y=25)
    date_label = Label(text=f'Created on: {item.date}', name='note_date', font=DATE_FONT)
    date_label.place(x=350, y=70)

    note_box = Text(width=48, height=16, font=BUTTON_TEXT_FONT, name='current_note', background='#F0F0F0',
                    bd=0, cursor='arrow', wrap='word')
    note_box.place(x=360, y=100)

    note_box.insert(
        END,
        f'\n\nToday, I {item.today}\n\n'
        f'Tomorrow, I {item.tomorrow}\n\n'
        f'Other than that, {item.general}\n\n'

    )
    note_box.config(state='disabled')
    edit_button = Button(root, name='edit_bttn', image=edit_bttn_img, bd=0, command=lambda current_note=item: newNote(
        editing_note=True, item=current_note))
    edit_button.place(x=545, y=415)

    delete_button = Button(root, name='del_bttn', image=delete_bttn_img, bd=0,
                           command=lambda current_note=item.id: delete_and_refresh(current_note))
    delete_button.place(x=654, y=415)

    new_note_v2_bttn = Button(root, name='note_bttn_2', image=new_note_v2_img, bd=0, command=newNote)
    new_note_v2_bttn.place(x=355, y=415)

    back_button = Button(root, image=back_buttn_img, name='back_bttn', bd=0, command=lambda: clear_widgets(
        'back_bttn',
        'edit_bttn',
        'del_bttn',
        'current_title',
        'current_note',
        'note_date',
        'note_bttn_2'
    ))
    back_button.place(x=312, y=30)


def main(root):
    """
    Main window, shows notes and can add note. root window changes depending on available notes and is
    called to refresh the window when deleting or adding a note to update the UI with remaining notes or messages.
    """
    #page dimensions and title
    root.geometry("800x500")

    # Your notes string
    title = tk.Label(root, text="Your Notes", font=STATIC_LABEL_FONT)
    title.pack(padx=0, pady=50)
    title.place(x=50, y=25)

    # Left Pane - list of notes
    if not get_all_notes():
        # clears notes and buttons if all notes are deleted
        clear_widgets('bttn_box', 'note_bttn', 'scroll')

    # new note button
    new_note_button = Button(root, image=new_note_img, name='new_note_button', command=newNote, bd=0)
    new_note_button.place(x=465, y=200)

    root.mainloop()


if __name__ == "__main__":
    main(root)
