#final_test.py
import datetime
import pickle
import argparse



class Task:
    """Representation of a task
    Attributes:
    - name string
    - unique id number
    - priority int value of 1, 2, or 3; 1 is default
    - due date - date, this is optional
    """

    # static member to store a unique id
    id_count = 0


    def __init__(self, name, due_date=None, priority=1):
        """Initialize a task with a name and optional priority and due date"""
        self.name = name

        self.id_count += 1
        self.unique_id = self.id_count

        self.priority = priority
        self.due_date = due_date
        self.created_date = datetime.datetime.now()
        self.completed_date = None

    def __str__(self):
        """Return a string representation of a task"""
        # return f"{self.unique_id} {self.name} {self.priority} {self.due_date}"
        due_date = "-"
        created_date = "-"
        completed_date = "-"

        if( self.due_date is not None ):
            due_date = str(self.due_date)

        if( self.created_date is not None ):
            created_date = str(self.created_date)

        if( self.completed_date is not None ):
            completed_date = str(self.completed_date)

        now = datetime.datetime.now()
        age_days = now-self.created_date
        #return ("%-5s%-5s%-11s%-11s%s-11s%s-11s%s" % (self.unique_id, f"{age_days.days}d", due_date,self.priority,self.name))
        #adding created time and completed time for str return
        return ("%-5s%-5s%-11s%-11s%-21s%-33s%s" % (self.unique_id, f"{age_days.days}d", due_date,self.priority,self.name,created_date,completed_date))

    def is_overdue(self):
        """Return True if a task is overdue"""
        if self.due_date:
            return self.due_date < datetime.datetime.now()
        return False

    def is_complete(self):
        """Return True if a task is complete"""
        return self.completed_date is not None

    def mark_complete(self):
        """Mark a task as complete"""
        self.completed_date = datetime.datetime.now()

    def __eq__(self, other):
        """Return True if two tasks are equal"""
        return self.name == other.name and self.priority == other.priority and self.due_date == other.due_date

    def __lt__(self, other):
        if self.due_date is None and other.due_date is None:
            if self.priority <= other.priority:
                return True
            else:
                return False
        elif self.due_date is not None and other.due_date is None:
            return True
        elif self.due_date is not None and other.due_date is not None:
            if self.due_date < other.due_date:
                return True
            elif self.due_date > other.due_date:
                return False 
            else:
                if self.priority <= other.priority:
                    return True
                else:
                    return False


class Tasks:
#"""A list of Task objects."""
    def __init__(self):
    #"""Read pickled tasks file into a list if it's avaialble  """
        try:
            with open(".tasks.pickle", "rb") as f:
                self.tasks = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.tasks = []

    def pickle_tasks(self):
        """Picle your task list to a file"""
        with open(".tasks.pickle", "wb") as f:
            pickle.dump(self.tasks, f)

    # Complete the rest of the methods, change the method definitions as needed
    def list(self):
        """Return a list of all tasks, should only return incomplete tasks"""
        return self.tasks

    def report(self):
        """Return a report of all tasks, including completed and overdue"""
        report = []
        for task in self.tasks:
            report.append(str(task))
        return "\n".join(report)

    def done(self, id):
        """Mark a task as done by id"""
        for task in self.tasks:
            #task.completed_date = datetime.datetime.now()
            if task.unique_id == id:
                task.mark_complete()
                print(f"Completed task {id}")
                break

    def query(self, query):
        """Return all tasks that match a search word"""
        #query: making everything in same case to make sure search both upper and lower case, -i /i match case
        results = []
        for word in query:
            for task in self.tasks:
                if word.lower() in task.name.lower():
                    results.append(task)
        return results

    def add(self, task):
        """Add a new task"""
        if( len(self.tasks) > 0 ):
            id_count = self.tasks[len(self.tasks) - 1].unique_id
            task.unique_id = id_count + 1
        self.tasks.append(task)
        print("Created Task",task.unique_id)
        #unique id 
    
    def delete (self,task_id):
        """delete task with unique id"""
        for task in self.tasks:
            if task.unique_id == task_id:
                self.tasks.remove(task)
                print(f"Deleted task {task_id}")
                return

    def get_incomplete_tasks(self):
        incomplete_tasks = []
        for task in self.tasks:
            if not task.is_complete():
                incomplete_tasks.append(task)
        return incomplete_tasks
       

    def get_all_tasks(self):
        return self.tasks

    def __str__(self):
        s = ""
        print(f"{len(self.tasks)} tasks")
        for task in self.tasks:
            s += str(task)
        return s

def print_tasks(tasks):
    
    sorted_tasks = sorted(tasks)
    print("%-5s%-5s%-11s%-11s%-21s%-33s%s" % ("ID", "Age", "Due Date","Priority","Task","Created","Completed"))
    print("--   ---  --------   --------   ----                 ---------------------------      -------------------------")
    for task in sorted_tasks:
        print(str(task))

def print_report(tasks):
    sorted_tasks = sorted(tasks)
    print("%-5s%-5s%-11s%-11s%-21s%-33s%s" % ("ID", "Age", "Due Date","Priority","Task","Created","Completed"))
    print("--   ---  --------   --------   ----                 ----------------------------      -------------------------")
    for task in sorted_tasks:
        print(str(task))

def main():
    '''all the real work  that drives the program'''
    parser=argparse.ArgumentParser(description="Update your Todo list.")
    # set the arguments for add 
    parser.add_argument('--add',type=str,required=False,help='a task string to add to your list')
    parser.add_argument('--priority',type=int,required=False,default=1,help='Priority of task; default value is 1')
    parser.add_argument('--due',type=str,required=False,help='Due date is in dd/mm/yyyy format')
    
    # set the arguments for list
    parser.add_argument('--list',required=False,action="store_true",help='list all tasks that have not been completed')

    # set the arguments for delete
    parser.add_argument('--delete',type=int,required=False,help='a task to be deleted')

    # set the arguments for report
    parser.add_argument('--report',required=False,action="store_true",help='list all tasks')

    # set arguments for query
    parser.add_argument('--query', type=str, required=False, nargs="+", help="priority of task; default value is 1")

    # set arguments for don
    parser.add_argument('--done',type=int,required=False,help='a task to be completed')

    #parse the argument
    args = parser.parse_args()

    #create instance of tasks, load previous data (current data on the pickle)
    task_list = Tasks()

    # Read out arguments (note the types)
    if args.add: #to add task into the tasks 
        priority = 1
        if args.priority:
            priority = args.priority
        due = None
        if args.due:
            due = args.due
        task_list.add(Task(args.add, due, priority))
    elif args.delete:
        task_list.delete(args.delete) 
    elif args.list:
         
        print_tasks(task_list.get_incomplete_tasks())
    elif args.report:
        print_report(task_list.get_all_tasks())
    elif args.query:
        print_tasks(task_list.query(args.query))
    elif args.done:
        task_list.done(args.done)

    
    #save current list into pickle
    task_list.pickle_tasks()
    exit()


if __name__ == "__main__":
    main()