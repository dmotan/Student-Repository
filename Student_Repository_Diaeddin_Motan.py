import os
from collections import defaultdict
from prettytable import PrettyTable
from utilities import file_reader
from typing import List, Tuple, Dict, DefaultDict, Iterator, Any, Set


class Major:
    """ Represents a major """
    pt_hdr: List[str] = ['Major', 'Required Courses', 'Electives']

    def __init__(self, name: str) -> None:
        self._name = name
        self._major: Dict[str, Dict[str, Set[str]]] = {
            name: {'R': set(), 'E': set()}}

    def _add_course(self, flag: str, course: str) -> None:
        self._major[self._name][flag].add(course)

    def _remaining_required(self, courses: Set[str]) -> Set[str]:
        for m_courses in self._major.values():
            return m_courses['R'] - set(courses)

    def _remaining_electives(self, courses: Set[str]) -> Set[str]:
        for m_courses in self._major.values():
            c = m_courses['E'].intersection(set(courses))
            if len(c) > 0:
                return []
            return m_courses['E']

    def pt_row(self) -> Tuple[str, List[str], List[str]]:
        """ A major data to be added to the Majors prettytable
        """
        for courses in self._major.values():
            return self._name, sorted(courses['R']), sorted(courses['E'])


class Student:
    """ Represent a single student """
    pt_hdr: Tuple[str, str, str] = ['CWID', 'Name', 'Completed Courses',
                                    'Remaining Required', 'Remaining Electives', 'GPA']

    def __init__(self, cwid: str, name: str, major: Major):
        self._cwid: str = cwid
        self._name: str = name
        self._major: Major = major
        # key: course value: str with grade
        self._courses: Dict[str, str] = dict()

    def add_course(self, course: str, grade: str) -> None:
        """ Note that the student took a course """
        self._courses[course] = grade

    def pt_row(self) -> Tuple[str, str, List[str]]:
        """ return a list of values to populate the prettytable for this student """
        return self._cwid, self._name, sorted(self._courses.keys()), sorted(
            self._major._remaining_required(self._courses.keys())), sorted(
            self._major._remaining_electives(self._courses.keys())), self._get_gpa()

    def _get_gpa(self) -> float:
        sum: float = 0
        total: int = len(self._courses.keys())
        for grade in self._courses.values():
            if grade == 'A':
                sum += 4.0
            if grade == 'A-':
                sum += 3.75
            if grade == 'B+':
                sum += 3.25
            if grade == 'B':
                sum += 3.0
            if grade == 'B-':
                sum += 2.75
            if grade == 'C+':
                sum += 2.25
            if grade == 'C':
                sum += 2.0
            else:
                sum += 0
        if total != 0:
            return round(sum/total, 2)
        return 0


class Instructor:
    """ Represent a single student """
    pt_hdr: List[str] = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid: int, name: str, dept: str) -> None:
        self._cwid: int = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(
            int)  # key: course value: number of students

    def _add_student(self, course: str) -> None:
        """ Note that another student took a course with this instructor """
        self._courses[course] += 1

    def pt_row(self) -> Tuple[str, str, List[str]]:
        """ A generator returning rows to be added to the Instructor prettytable
            The prettytable includes only those instructors who have taught at least one course
        """
        for course, count in self._courses.items():
            yield self._cwid, self._name, self._dept, course, count


class Repository:
    """ Store all information abut students and instructors """

    def __init__(self, wdir: str, ptables: bool = True) -> None:
        self._wdir: str = wdir  # directory with the all files
        # key:cwid, value: instance of student class
        self._students: Dict[str, Student] = dict()
        # key:cwid, value: instance of instructor class
        self._instructors: Dict[str, Instructor] = dict()
        self._majors: Dict[str, Major] = dict()

        try:
            self._get_major_data(os.path.join(wdir, 'majors.txt'))
            self._get_students(os.path.join(wdir, 'students.txt'))
            self._get_instructors(os.path.join(wdir, 'instructors.txt'))
            self._get_grades(os.path.join(wdir, 'grades.txt'))

        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print(fnfe)

        if ptables:
            print('\nMajor Summary')
            self.major_table()

            print('\nStudent Summary')
            self.student_table()

            print('\nInstructor Summary')
            self.instructor_table()

    def _get_major_data(self, path: str) -> None:
        """ read majors file and store required and elective data.
            Allow exceptions from reading the file to flow back to the caller
        """
        for major_name, flag, course in file_reader(path, 3, sep='\t', header=True):
            if major_name in self._majors:
                self._majors[major_name]._add_course(flag, course)
            else:
                self._majors[major_name] = Major(major_name)
                self._majors[major_name]._add_course(flag, course)

    def _get_students(self, path: str) -> None:
        """ read students from path and add to the self.students.
            Allow exceptions from reading the file to flow back to the caller
        """
        for cwid, name, major in file_reader(path, 3, sep=';', header=True):
            self._students[cwid] = Student(cwid, name, self._majors[major])

    def _get_instructors(self, path: str) -> None:
        """ read instructors from path and add to the self.instructors.
            Allow exceptions from reading the file to flow back to the caller
        """
        for cwid, name, dept in file_reader(path, 3, sep='|', header=True):
            self._instructors[cwid] = Instructor(cwid, name, dept)

    def _get_grades(self, path: str) -> None:
        """ read grades file and attreibute the grade to the appropriate student and instructor.
            Allow exceptions from reading the file to flow back to the caller
        """
        for student_cwid, course, grade, instructor_cwid in file_reader(path, 4, sep='|', header=True):
            if student_cwid in self._students:
                self._students[student_cwid].add_course(course, grade)
            else:
                print(f"Found grade for unknown student '{student_cwid}'")

            if instructor_cwid in self._instructors:
                self._instructors[instructor_cwid]._add_student(course)
            else:
                print(f"Found grade for unknown student '{instructor_cwid}'")

    def major_table(self) -> None:
        """ print a PrettyTable with a summary of all majors """
        pt: PrettyTable = PrettyTable(field_names=Major.pt_hdr)
        for major in self._majors.values():
            pt.add_row(major.pt_row())

        print(pt)

    def student_table(self) -> None:
        """ print a PrettyTable with a summary of all students """
        pt: PrettyTable = PrettyTable(field_names=Student.pt_hdr)
        for student in self._students.values():
            pt.add_row(student.pt_row())

        print(pt)

    def instructor_table(self) -> None:
        """ print a PrettyTable with a summary of all instructors """
        pt: PrettyTable = PrettyTable(field_names=Instructor.pt_hdr)
        for instructor in self._instructors.values():
            # each instructor may teach many classes
            for row in instructor.pt_row():
                pt.add_row(row)

        print(pt)


def main():
    wdir09 = '/Users/dmotan/Desktop/Master/SSW-810/week10'
    wdir10 = '/Users/dmotan/Desktop/Master/SSW-810/week10/test'
    wdir_bad_data = '/Users/dmotan/Desktop/Master/SSW-810/week10/bad'

    try:
        print("Good data")
        _ = Repository(wdir09)

        print("\nBad Data")
        print("should report unkown student instructor")
        _ = Repository(wdir10)

        print("\nBad Fields\n")
        print("should report bad student, grade, instructor feeds")
        _ = Repository(wdir_bad_data)
    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"Exception in main: {e}")


if __name__ == '__main__':
    main()
