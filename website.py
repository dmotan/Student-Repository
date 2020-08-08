from flask import Flask, render_template
import sqlite3
from typing import Dict

DB_FILE: str = "/Users/dmotan/Desktop/Master/SSW-810/week12/810_student_repo.db"

app: Flask = Flask(__name__)


@app.route('/students')
def students() -> str:
    query = """ select s.Name, s.CWID, g.Course, g.Grade, i.Name
              from grades g
              join students s on s.CWID=g.StudentCWID
              join instructors i on g.InstructorCWID=i.CWID
              order by s.Name asc
          """

    db: sqlite3.Connection = sqlite3.connect(DB_FILE)

    data: Dict[str, str] = [{'name': name, 'cwid': cwid, 'course': course, 'grade': grade, 'instructor': inst}
                            for name, cwid, course, grade, inst in db.execute(query)]
    db.close()
    print(data)
    return render_template('students.html',
                           title='Stevens Repository',
                           table_title='Student, Course, Grade, and Instructor',
                           students=data)


app.run(debug=True)
