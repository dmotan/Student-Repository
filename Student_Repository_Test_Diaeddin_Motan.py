""" Automated tests for HW09_Student_Repository.py """


import unittest
import os
from Student_Repository_Diaeddin_Motan import Repository, Student, Instructor
from utilities import file_reader


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.test_path = '/Users/dmotan/Desktop/Master/SSW-810/week9/stevens'
        self.repo = Repository(self.test_path, False)

    def test_Student_attributes(self):
        """ Verify that a specific student is set up properly """
        expected = {
            '10103': ('10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']),
            '10115': ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']),
            '10172': ('10172', 'Forbes, I', ['SSW 555', 'SSW 567']),
            '10175': ('10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']),
            '10183': ('10183', 'Chapman, O', ['SSW 689']),
            '11399': ('11399', 'Cordova, I', ['SSW 540']),
            '11461': ('11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']),
            '11658': ('11658', 'Kelly, P', ['SSW 540']),
            '11714': ('11714', 'Morton, A', ['SYS 611', 'SYS 645']),
            '11788': ('11788', 'Fuller, E', ['SSW 540'])
        }

        calculated = {cwid: student.pt_row()
                      for cwid, student in self.repo._students.items()}

        self.assertEqual(expected, calculated)

    def test_Instructor_attributes(self):
        """ Verify that a specific instructor is set up properly """
        expected = {
            ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
            ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
            ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
            ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
            ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
            ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
            ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
            ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
            ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
            ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
            ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
            ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)
        }

        calculated = {tuple(detail) for instructor in self.repo._instructors.values(
        ) for detail in instructor.pt_row()}

        self.assertEqual(expected, calculated)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
