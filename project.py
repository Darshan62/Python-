import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font

class Student:
    def __init__(self, student_id, name, marks):
        self.student_id = student_id
        self.name = name
        self.marks = marks

    def __repr__(self):
        return f"Student(ID: {self.student_id}, Name: {self.name}, Marks: {self.marks})"

def binary_search(student_records, target_id):
    low = 0
    high = len(student_records) - 1
    while low <= high:
        mid = (low + high) // 2
        if student_records[mid].student_id == target_id:
            return mid
        elif student_records[mid].student_id < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def selection_sort(student_records, key='student_id', reverse=False):
    n = len(student_records)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if (reverse and getattr(student_records[j], key) > getattr(student_records[min_idx], key)) or (
                    not reverse and getattr(student_records[j], key) < getattr(student_records[min_idx], key)):
                min_idx = j
        student_records[i], student_records[min_idx] = student_records[min_idx], student_records[i]

def add_sample_records(student_records):
    sample_records = [
        (106, "Frank", 78),
        (107, "Grace", 92),
        (108, "Henry", 85),
        (109, "Ivy", 79),
        (110, "Jack", 88)
    ]
    for student_id, name, marks in sample_records:
        student_records.append(Student(student_id, name, marks))
    print("Sample records added successfully.")

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x600")

        self.students = []

        # Add sample records
        add_sample_records(self.students)

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Set custom styles
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
        style.configure("TButton", font=("Helvetica", 12), background="#0052cc", foreground="white")
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("Treeview", font=("Helvetica", 12), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))

        title_font = Font(family="Helvetica", size=20, weight="bold")

        title = tk.Label(self.root, text="Student Management System", font=title_font, background="#0052cc", foreground="white")
        title.pack(pady=10, fill=tk.X)

        frame = tk.Frame(self.root, background="#f0f0f0")
        frame.pack(pady=20)

        tk.Label(frame, text="Student ID").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(frame, text="Student Name").grid(row=0, column=1, padx=10, pady=5)
        tk.Label(frame, text="Marks").grid(row=0, column=2, padx=10, pady=5)

        self.id_entry = ttk.Entry(frame)
        self.id_entry.grid(row=1, column=0, padx=10, pady=5)

        self.name_entry = ttk.Entry(frame)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.marks_entry = ttk.Entry(frame)
        self.marks_entry.grid(row=1, column=2, padx=10, pady=5)

        add_button = ttk.Button(frame, text="Add Student", command=self.add_student)
        add_button.grid(row=1, column=3, padx=10, pady=5)

        update_button = ttk.Button(frame, text="Update Marks", command=self.update_marks)
        update_button.grid(row=1, column=4, padx=10, pady=5)

        search_frame = tk.Frame(self.root, background="#f0f0f0")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search Student by ID").grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_student)
        search_button.grid(row=0, column=2, padx=10, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Marks"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Marks", text="Marks")
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        delete_button = ttk.Button(self.root, text="Delete Student", command=self.delete_student)
        delete_button.pack(pady=10)

        sort_id_button = ttk.Button(self.root, text="Sort by ID", command=self.sort_by_id)
        sort_id_button.pack(pady=10)

        sort_marks_button = ttk.Button(self.root, text="Sort by Marks", command=self.sort_by_marks)
        sort_marks_button.pack(pady=10)

        self.load_data()

    def load_data(self):
        for student in self.students:
            self.tree.insert('', 'end', values=(student.student_id, student.name, student.marks))

    def add_student(self):
        try:
            student_id = int(self.id_entry.get())
            name = self.name_entry.get()
            marks = int(self.marks_entry.get())

            new_student = Student(student_id, name, marks)
            self.students.append(new_student)
            self.tree.insert('', 'end', values=(student_id, name, marks))
            self.clear_entries()
            messagebox.showinfo("Success", "Student record added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data")

    def update_marks(self):
        try:
            student_id = int(self.id_entry.get())
            new_marks = int(self.marks_entry.get())
            index = binary_search(self.students, student_id)
            if index != -1:
                self.students[index].marks = new_marks
                self.refresh_tree()
                messagebox.showinfo("Success", "Marks updated successfully.")
            else:
                messagebox.showerror("Error", "Student not found")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data")

    def delete_student(self):
        try:
            student_id = int(self.id_entry.get())
            index = binary_search(self.students, student_id)
            if index != -1:
                del self.students[index]
                self.refresh_tree()
                messagebox.showinfo("Success", "Student record deleted successfully.")
            else:
                messagebox.showerror("Error", "Student not found")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data")

    def search_student(self):
        try:
            search_id = int(self.search_entry.get())
            index = binary_search(self.students, search_id)
            if index != -1:
                student = self.students[index]
                messagebox.showinfo("Result", f"Student found: {student}")
            else:
                messagebox.showinfo("Result", "Student not found")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid student ID")

    def sort_by_id(self):
        selection_sort(self.students, key='student_id')
        self.refresh_tree()

    def sort_by_marks(self):
        selection_sort(self.students, key='marks', reverse=True)
        self.refresh_tree()

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.load_data()

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()
