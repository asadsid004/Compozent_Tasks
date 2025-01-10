# Write a program that stores student data (name, age, grades) in a dictionary and performs CRUD operations.


def student_data_crud():
    students = {}

    while True:
        print("\nMenu:")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Add student
            roll_no = input("Enter roll number: ")
            if roll_no in students:
                print("Student with this roll number already exists.")
            else:
                name = input("Enter name: ")
                age = int(input("Enter age: "))
                grades = input("Enter grades (comma-separated): ").split(",")
                students[roll_no] = {"name": name, "age": age, "grades": grades}
                print("Student added successfully.")

        elif choice == "2":
            # View students
            if not students:
                print("No students found.")
            else:
                for roll_no, data in students.items():
                    print(
                        f"Roll No: {roll_no}, Name: {data['name']}, Age: {data['age']}, Grades: {', '.join(data['grades'])}"
                    )

        elif choice == "3":
            # Update student
            roll_no = input("Enter roll number of the student to update: ")
            if roll_no in students:
                name = (
                    input("Enter new name (leave blank to keep current): ")
                    or students[roll_no]["name"]
                )
                age = (
                    input("Enter new age (leave blank to keep current): ")
                    or students[roll_no]["age"]
                )
                grades = (
                    input(
                        "Enter new grades (comma-separated, leave blank to keep current): "
                    ).split(",")
                    or students[roll_no]["grades"]
                )
                students[roll_no] = {"name": name, "age": int(age), "grades": grades}
                print("Student updated successfully.")
            else:
                print("Student not found.")

        elif choice == "4":
            # Delete student
            roll_no = input("Enter roll number of the student to delete: ")
            if roll_no in students:
                del students[roll_no]
                print("Student deleted successfully.")
            else:
                print("Student not found.")

        elif choice == "5":
            # Exit
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")


student_data_crud()
