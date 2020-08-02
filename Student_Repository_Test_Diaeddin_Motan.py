""" Automated tests for HW09_Student_Repository.py """


import unittest
import os
from Student_Repository_Diaeddin_Motan import Repository, Student, Instructor, Major
from utilities import file_reader
import sqlite3


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.test_path = '/Users/dmotan/Desktop/Master/SSW-810/week11'
        self.repo = Repository(self.test_path, False)

    # def test_Student_attributes(self):
    #     """ Verify that a specific student is set up properly """
    #     expected = {
    #         '10103': ('10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], 3.44),
    #         '10115': ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], 3.81),
    #         '10172': ('10172', 'Forbes, I', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], ['CS 501', 'CS 513', 'CS 545'], 3.88),
    #         '10175': ('10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 513', 'CS 545'], 3.58),
    #         '10183': ('10183', 'Chapman, O', ['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545'], 4.0),
    #         '11399': ('11399', 'Cordova, I', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], 3.0),
    #         '11461': ('11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671'], ['SSW 540', 'SSW 565', 'SSW 810'], 3.92),
    #         '11658': ('11658', 'Kelly, P', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], 0.0),
    #         '11714': ('11714', 'Morton, A', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], 3.0),
    #         '11788': ('11788', 'Fuller, E', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], 4.0)
    #     }

    #     calculated = {cwid: student.pt_row()
    #                   for cwid, student in self.repo._students.items()}

    #     self.assertEqual(expected, calculated)

    # def test_Instructor_attributes(self):
    #     """ Verify that a specific instructor is set up properly """
    #     expected = {
    #         ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
    #         ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
    #         ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
    #         ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
    #         ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
    #         ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
    #         ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
    #         ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
    #         ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
    #         ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
    #         ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
    #         ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)
    #     }

    #     calculated = {tuple(detail) for instructor in self.repo._instructors.values(
    #     ) for detail in instructor.pt_row()}

    #     self.assertEqual(expected, calculated)

    # def test_Major_attributes(self):
    #     """ Verify that a specific major is set up properly """
    #     expected = {
    #         'SFEN': ('SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']),
    #         'SYEN': ('SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']),
    #     }

    #     calculated = {name: major.pt_row()
    #                   for name, major in self.repo._majors.items()}

    #     self.assertEqual(expected, calculated)

    def test_student_grade_summary(self):
        """ Verify that a specific major is set up properly """
        DB_FILE: str = "/Users/dmotan/Desktop/Master/SSW-810/week11/810_student_repo.db"
        db: sqlite3.Connection = sqlite3.connect(DB_FILE)

        expected = {
            ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
            ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
            ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
            ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
            ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
            ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
            ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
            ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
            ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')
        }

        calculated = {row
                      for row in db.execute("select s.Name, s.CWID, g.Course, g.Grade, i.Name from grades g join students s on s.CWID=g.StudentCWID join instructors i on g.InstructorCWID=i.CWID order by s.Name asc")}

        self.assertEqual(expected, calculated)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
