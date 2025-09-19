from functools import total_ordering


class Mentor:
    """
    Класс для всех наставников
    """

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering # Декоратор @total_ordering автоматически создает все методы сравнения
class Lecturer(Mentor):
    """
    Класс лекторов курсов, наследуемый от родительского класса Mentor
    """

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        average_grade = self.get_average_grade()
        return f"Имя: {self.name}\n" \
               f"Фамилия: {self.surname}\n" \
               f"Средняя оценка за лекции: {average_grade:.1f}"

    def get_average_grade(self):
        """
        Возвращает среднюю оценку лектора за все лекции
        """
        if not self.grades:
            return 0
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_grade() == other.get_average_grade()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_grade() < other.get_average_grade()


class Reviewer(Mentor):
    """
    Класс ревьюеров курсов, наследуемый от класса Mentor
    """
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return f"Имя: {self.name}\n" \
               f"Фамилия: {self.surname}"

    def rate_hw(self, student_obj, course, grade):
        """
        Выставляет оценку за домашнее задание студенту.
        """
        if (isinstance(student_obj, Student) and
            course in self.courses_attached and
            course in student_obj.courses_in_progress):
            if course in student_obj.grades:
                student_obj.grades[course] += [grade]
            else:
                student_obj.grades[course] = [grade]
        else:
            return 'Ошибка'


@total_ordering # Декоратор @total_ordering автоматически создает все методы сравнения
class Student:
    """
    Класс студентов курсов
    """
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecture(self, lecturer_obj, course, grade):
        """
        Выставляет оценку за лекцию лектору.
        """
        if (isinstance(lecturer_obj, Lecturer) and
            course in self.courses_in_progress and
            course in lecturer_obj.courses_attached and
            1 <= grade <= 10):
            if course in lecturer_obj.grades:
                lecturer_obj.grades[course] += [grade]
            else:
                lecturer_obj.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        average_grade = self.get_average_grade()
        return f"Имя: {self.name}\n" \
               f"Фамилия: {self.surname}\n" \
               f"Средняя оценка за домашние задания: {average_grade:.1f}\n" \
               f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n" \
               f"Завершенные курсы: {', '.join(self.finished_courses)}"

    def get_average_grade(self):
        """
        Возвращает среднюю оценку студента за все домашние задания
        """
        if not self.grades:
            return 0
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_grade() == other.get_average_grade()

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_grade() < other.get_average_grade()


def get_average_student_hw_grade(students, course):
    """
    Подсчитывает среднюю оценку за домашние задания по всем студентам на указанном курсе
    """
    total_grades = []

    for student in students:
        if course in student.grades:
            total_grades.extend(student.grades[course])
    return sum(total_grades) / len(total_grades) if total_grades else 0


def get_average_lecturer_grade(lecturers, course):
    """
    Подсчитывает среднюю оценку за лекции по всем лекторам на указанном курсе
    """
    total_grades = []

    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades.extend(lecturer.grades[course])
    return sum(total_grades) / len(total_grades) if total_grades else 0


lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Круглов', 'Вячеслав')
lecturer3 = Lecturer('Пятницкий', 'Олег')

reviewer1 = Reviewer('Круглова', 'Мария')
reviewer2 = Reviewer('Самойлов', 'Роман')

student1 = Student('Алёхина', 'Ольга', 'Ж')
student2 = Student('Петров', 'Григорий', 'М')
student3 = Student('Немов', 'Сава', 'М')

student1.courses_in_progress = ['Python', 'Git']
student1.finished_courses = ['Введение в программирование']
student2.courses_in_progress = ['C++', 'Java']
student2.finished_courses = ['Введение в программирование']
student3.courses_in_progress = ['Python', 'Java']
student3.finished_courses = ['Введение в программирование']

reviewer1.courses_attached = ['Python', 'Git']
reviewer2.courses_attached = ['C++', 'Java']

lecturer1.courses_attached = ['Python', 'Git']
lecturer2.courses_attached = ['C++', 'Java']
lecturer3.courses_attached = ['Python', 'Java', 'C++']

student1.rate_lecture(lecturer1, 'Python', 9 )
student1.rate_lecture(lecturer1, 'Git', 7 )
student1.rate_lecture(lecturer3, 'Python', 5 )

student2.rate_lecture(lecturer2, 'C++', 8 )
student2.rate_lecture(lecturer2, 'Java', 7 )
student2.rate_lecture(lecturer3, 'Java', 5 )
student2.rate_lecture(lecturer3, 'C++', 7 )

student3.rate_lecture(lecturer1, 'Python', 8 )
student3.rate_lecture(lecturer2, 'Java', 7 )
student3.rate_lecture(lecturer3, 'Java', 5 )

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Git', 9)

reviewer2.rate_hw(student2, 'C++', 8)
reviewer2.rate_hw(student2, 'Java', 9)

reviewer1.rate_hw(student3, 'Python', 8)
reviewer2.rate_hw(student3, 'Java', 9)

students_list = [student1, student2, student3]
lecturers_list = [lecturer1, lecturer2, lecturer3]

course_name = 'Python'

average_hw = get_average_student_hw_grade(students_list, course_name)
average_lect = get_average_lecturer_grade(lecturers_list, course_name)

print(lecturer1, '\n')
print(lecturer2, '\n')
print(student1, '\n')
print(student2, '\n')
print(reviewer1, '\n')
print(reviewer2, '\n')

print(f"Средняя оценка студентов по курсу {course_name}: {average_hw:.1f}")
print(f"Средняя оценка лекторов по курсу {course_name}: {average_lect:.1f}")


