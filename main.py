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


lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Круглов', 'Вячеслав')

reviewer1 = Reviewer('Круглова', 'Мария')
reviewer2 = Reviewer('Самойлов', 'Роман')

student1 = Student('Алёхина', 'Ольга', 'Ж')
student2 = Student('Петров', 'Григорий', 'М')

student1.courses_in_progress = ['Python', 'Git']
student1.finished_courses = ['Введение в программирование']
student2.courses_in_progress = ['C++', 'Java']
student2.finished_courses = ['Введение в программирование']

reviewer1.courses_attached = ['Python', 'Git']
reviewer2.courses_attached = ['C++', 'Java']

lecturer1.courses_attached = ['Python', 'Git']
lecturer2.courses_attached = ['C++', 'Java']

student1.rate_lecture(lecturer1, 'Python', 9 )
student1.rate_lecture(lecturer1, 'Git', 7 )
student2.rate_lecture(lecturer2, 'C++', 8 )
student2.rate_lecture(lecturer2, 'Java', 7 )

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Git', 9)
reviewer2.rate_hw(student2, 'C++', 8)
reviewer2.rate_hw(student2, 'Java', 9)


print(lecturer1, '\n')
print(lecturer2, '\n')
print(student1, '\n')
print(student2, '\n')
print(reviewer1, '\n')
print(reviewer2, '\n')

print(f"Средняя оценка студента Алехиной О. больше чем Петрова Г. : {student1 > student2}")
print(f"Средняя оценка лектора Иванова И. равна оценке Круглова В. : {student1 == student2}")


