# Create a Student class with attributes for name, age, and grades. Include methods to display details and calculate the average grade.


class Student:
    def __init__(self, name, age, grades):
        self.name = name
        self.age = age
        self.grades = grades

    def display_details(self):
        print(f"Name: {self.name}, Age: {self.age}, Grades: {self.grades}")

    def calculate_average(self):
        if self.grades:
            return sum(self.grades) / len(self.grades)
        return 0

    def update_details(self, name=None, age=None, grades=None):
        if name:
            self.name = name
        if age:
            self.age = age
        if grades:
            self.grades = grades
        print("Student details updated successfully.")


student = Student("Alice", 20, [85, 90, 78])
student.display_details()

print(f"Average Grade: {student.calculate_average()}")

student.update_details(name="Bob", grades=[88, 92])
student.display_details()
