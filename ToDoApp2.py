
import datetime
from Tkinter import *
import tkMessageBox
import tkFileDialog

DATE_FORMAT = '%d/%m/%Y'
TODAY = datetime.datetime.today()

# Used for displaying an item in the GUI
DISPLAY_FORMAT = "{0:<30}{1}"

# Used for encoding items to be saved to a file
SAVE_FORMAT = "{0},{1}\n"


def as_datetime(date_string):
    """Convert a date string in 'dd/mm/yyyy' format into a datetime object.

    as_datetime(str) -> datetime

    Returns None if date_string is invalid.
    """
    try:
        return datetime.datetime.strptime(date_string, DATE_FORMAT)
    except ValueError as e:
        return None


def as_date_string(date):
    """Convert a datetime object into a date string in 'dd/mm/yyyy' format.

    as_datetime(datetime) -> str
    """
    return date.strftime(DATE_FORMAT)



MODIFIED_TODO=[]

import os


class ToDoError(Exception):

    ''' raises an exeption '''
    def __init__(self,message):
        Exception.__init__(self,message)
    
class ToDoItem (object):
    ''' ToDoItem class that takes two strings a task and a date to create a ToDoItem object'''
    def __init__ (self, name, date):
        '''constructor '''
            
        self._name = name
        self._date = date
        if as_datetime(date) == None:
            raise ToDoError ('Invalid date: '+"'{}'".format(date)) #raises an error if the date is invalid
        else : True
        
        
    def get_name(self):
        '''return a string of the task name'''
        return self._name
    
    def get_date(self):
        '''returns a string of the date'''
        return self._date
    
    def is_overdue(self):
        '''checks if the item is overdue '''
        if as_datetime(self._date)< TODAY :
            return True
        elif as_datetime(self._date) > TODAY:
            return False
        
    def __str__(self):
        ''' Displays  the todoitem in DISPLAY_FORMAT'''
        return DISPLAY_FORMAT.format(self._name, self._date)
        
    def __repr__(self):
        ''' Re^resents the Todoitem in represent Format'''
        return 'ToDoItem ({0}, {1})'.format(self._name, self._date)
        
    def save_string(self):
        return(','.join([self.get_name(), self.get_date()]) + '\n')

    def __lt__(self,other):
        ''' returns boolean value to aid in sort and sorted'''
        if as_datetime(self._date) < as_datetime(other._date):
            return True
        else: 
            return False
        
    
class ToDoList (object):
    ''' ToDoList that takes no item and creates a List '''
    
    def __init__(self):
        '''constructor creates an empty todo list'''
        self.TODO =[]
       
    def needs_saving(self):
        '''Checks if lists needs saving by comparing them '''
        
        if sorted(self.TODO)== sorted(MODIFIED_TODO):
            return False
        else:
            return True
        
    def load_file(self, filename):
        ''' Loads file by putting it into a list'''
        if filename:
            with open(filename, 'r')as f:
                try:
                    for line in f:
                        name, date = line.strip().rsplit(',', 1)#strips spaces and split at last comma
                        MODIFIED_TODO.append(ToDoItem(name, date))
                        self.TODO.append(ToDoItem(name, date))
                except Exception as exeption:
                    tkMessageBox.showerror(title='INVALID FILE',message=exeption)#error message for invalid file
            
        
        
    def clear_todo(self):
        ''' empty todo list'''
        self.TODO=[]
        

    def save_file(self, filename):
        '''used to save file'''
        f = open(filename, 'w')
        for item in sorted(self.TODO):
            f.write(item.save_string())
        f.close()

    def get_all(self):
        '''returns todo list in time order'''
        
        return sorted(self.TODO)
    

    def get_todo(self,index):
        ''' get item from todo list at specific index'''
        return sorted(self.TODO)[index]

    def remove_todo(self, index):
        ''' removes item from list at specific index'''
        self.TODO.remove(sorted(self.TODO)[index])

    def set_todo(self, index, item):
        ''' checks for index and removes item and replaces it with new task'''
        if index == None :
            self.TODO.append(item)
        else:
            self.TODO.remove(sorted(self.TODO)[index])
            self.TODO.append(item)

    

class View (Listbox):
    ''' View class used to display items on the GUI'''
    def __init__(self, todolist,master):
        #constructor
        self.master = master
        self.todolist = ToDoList()
        self.controller = Controller
        self.mylistbox=Listbox(master,width=100,height=20,font=('Courier',10))
        self.mylistbox.pack()
      
    def display_dates(self, todolist):
        ''' Used to display dates in red is overdue and blue if not'''
        for item in todolist :
             
            if item.is_overdue()== True:
                self.mylistbox.insert(END, str(item))
                self.mylistbox.pack()
                self.mylistbox.itemconfig(END, fg = 'red')
            else :
                self.mylistbox.insert(END, str(item))
                self.mylistbox.pack()
                self.mylistbox.itemconfig(END, fg = 'blue')
        
    def delete(self):
        '''clears the listbox'''
        self.mylistbox.delete(0,END)
    def remove (self):
        '''removing item from todo according to the index'''
        index = self.mylistbox.curselection()
        self.mylistbox.delete(index)
        self.todolist.remove_todo(1)

    def addtask(self):
        AddToDo()

    def edit (self):
        index = self.mylistbox.curselection()[0]
        self.addtodo()
        self.mylistbox.set_todo(index, item)
        
class AddToDo(Toplevel):
    ''' Top Level class used to open input window as a top level window'''
    def __init__(self, master=None):
        #construct GUI
        popupwindow = Toplevel(height = 10, width = 30)
        popupwindow.title('top level box')
        popupwindow.geometry("450x100")
        Label(popupwindow, text='Enter Task: ').pack(side=LEFT)
        Task = Entry(popupwindow, width=20).pack(side = LEFT)
        Label(popupwindow, text='Enter Date: ').pack(side=LEFT)
        Date = Entry(popupwindow, width=20).pack(side = LEFT)
        Button(popupwindow,text= 'OK', command = self.add_task).pack(side= LEFT)
       
        
    def add_task (self):
        ''' add the task and date entered in the entry box to the todo list'''
        
        self.TODO.append(ToDoItem(Task.get(),Date.get()))


class OpenFile(Frame):
    '''opens file by browsing computer'''
    
    def askopenfile(self):

        filename = tkFileDialog.askopenfilename(filetypes=[("Text files","*.txt")])
        return filename
        


class Controller (object):
    '''used to interact with user'''
    
    def __init__(self, master):
        #constructor GUI
        self.master = master
        self.todolist = ToDoList()
        self.openfile = OpenFile(master)
        self.view = View(self, master)
        
        

                           
        self.add_button = Button(master,text= 'add todo', command = self.add_task)
        self.add_button.pack(side=LEFT)

        self.remove_button = Button(master,text= 'remove todo', command=self.remove)
        self.remove_button.pack(side=LEFT)

        self.edit_button = Button(master,text= 'edit todo', command = self.edit)
        self.edit_button.pack(side=LEFT)
        
        
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open ToDo File", command=self.open_file)
        filemenu.add_command(label="Save File", command=self.save_file)
        filemenu.add_command(label="Exit", command=self.close)
        menubar.add_cascade(label="File", menu=filemenu)
        # display the menu
        master.config(menu=menubar)
        
    
    def add_task(self):
        self.view.addtask()
        
    def remove(self):
        self.view.remove()
            
    def edit (self):
        self.view.edit()
        
    def save_file(self):
        filename = tkFileDialog.asksaveasfilename()
        if filename:
            self.todolist.save_file(filename)
            
       
     
        
    #open file         
    def open_file (self):
        self.todolist.clear_todo()
        self.view.delete()
        filename = self.openfile.askopenfile()
        self.todolist.load_file(filename)
        task_list = self.todolist.get_all()
        self.view.display_dates(task_list)

    def close(self):
        """
        End app
        """
        self.master.destroy()

    
                
      

class ToDoApp(object):
    def __init__(self, master=None):
        master.title("TODOs")
        self.controller = Controller(master)


def main():
    root = Tk()
    app = ToDoApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
