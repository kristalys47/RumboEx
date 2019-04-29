from flask import jsonify
from RumboEx.dao.CourseDao import CourseDAO
from RumboEx.dao.taskDao import TaskDAO
from RumboEx.handler.taskHandler import TaskHandler


class CourseHandler():

    # get a course with grades and tasks by course id
    def get_course_by_course_id(self, course_id, student_id):
        dao = CourseDAO()
        result = dao.get_course_by_course_id(course_id, student_id)
        if not result:
            return jsonify(Error='NOT FOUND'), 404

        course = self.mapToCourseDict(result)
        section_id = result[5]
        enrolled_id = result[6]
        course['time'] = []
        course['grades'] = []
        course['tasks'] = []

        # get time schedule of section
        time = dao.get_section_times_by_section_id(section_id)
        if time:
            for t in time:
                course['time'].append(self.mapToTimeDict(t))

        # get grades of course
        grades = dao.get_grades_by_enrolled_id(enrolled_id)
        if grades:
            for g in grades:
                print(g)
                course['grades'].append(self.mapToGradeDict(g))

        # get tasks of course
        dao2 = TaskDAO()
        tasks = dao2.get_study_tasks_by_user_id_and_course_id(student_id, course['course_id'])
        if tasks:
            for t in tasks:
                course['tasks'].append(self.mapToTaskDict(t))

        return jsonify(Course=course)

    # get all courses of a student
    def get_courses_by_student_id(self, student_id):
        dao = CourseDAO()
        result = dao.get_courses_by_student_id(student_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToCourseDict(r))
        return jsonify(mapped_result)

    # get all courses of a student with grades and tasks
    def get_courses_with_grades_by_student_id(self, student_id):
        dao = CourseDAO()
        courses = dao.get_courses_by_student_id(student_id)
        if not courses:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for c in courses:
            print(c)
            course = self.mapToCourseDict(c)

            section_id = c[5]
            enrolled_id = c[6]
            print(course)

            course['time'] = []
            course['grades'] = []
            course['tasks'] = []

            # get time schedule of section
            time = dao.get_section_times_by_section_id(section_id)
            if time:
                for t in time:
                    course['time'].append(self.mapToTimeDict(t))

            # get grades of course
            grades = dao.get_grades_by_enrolled_id(enrolled_id)
            if grades:
                for g in grades:
                    print(g)
                    course['grades'].append(self.mapToGradeDict(g))

            # get tasks of course
            dao2 = TaskDAO()
            tasks = dao2.get_study_tasks_by_user_id_and_course_id(student_id, course['course_id'])
            if tasks:
                for t in tasks:
                    course['tasks'].append(self.mapToTaskDict(t))

            mapped_result.append(course)
        return jsonify(mapped_result), 200

    # def get_course_by_course_id(self, course_id):
    #     dao = CourseDAO()
    #     result = dao.get_course_by_course_id(course_id)
    #     if not result:
    #         return jsonify(Error="NOT FOUND"), 404
    #     return jsonify(self.mapToIndividualCourseDict(result))

    # get all grades of a course
    def get_grades_by_course_id(self, course_id):
        dao = CourseDAO()
        result = dao.get_grades_by_enrolled_id(course_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToGradeDict(r))
        return jsonify(mapped_result)

    # POST Methods

    def insert_grade(self, user_id, form):
        if len(form) < 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            name = form['name']
            grade = form['grade']
            total = form['total']
            weight = form['weight']
            date = form['date']
            course_id = form['course_id']
            if name and course_id:
                dao = CourseDAO()
                grade_id = dao.insert_grade(name, grade, total, weight, date, user_id, course_id)
                # result = self.mapToTaskDict(task_id)
                return jsonify({'grade_id': grade_id[0]}), 200
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_course(self, user_id, form):
        codification = form['codification']
        section = form['section_num']
        name = codification
        credits = 0
        professor_id = None
        if codification and section:
            dao = CourseDAO()
            # add course to db
            course_id = dao.insert_course(name, codification, credits, professor_id)
            # add section to db
            section_id = dao.insert_section(section, course_id)
            # enroll student in section
            enrolled_id = dao.add_course_to_student(section_id, user_id)
            return jsonify({'course_id': course_id, 'section_id': section_id, 'enrolled_id': enrolled_id}), 200
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    # PUT Methods

    def changeGradeName(self, grade_id, grade_name):
        response = CourseDAO().change_grade_name(grade_id, grade_name)
        if not response:
            return jsonify(Error='GRADE NOT FOUND'), 404
        result = {'user_id': response[0], 'new_grade_name': response[1]}
        return jsonify(result=result), 200

    def changeGradeGrade(self, grade_id, grade):
        response = CourseDAO().change_grade_grade(grade_id, grade)
        if not response:
            return jsonify(Error='GRADE NOT FOUND'), 404
        result = {'user_id': response[0], 'new_grade_grade': response[1]}
        return jsonify(result=result), 200

    def changeGradeWeight(self, grade_id, grade_weight):
        response = CourseDAO().change_grade_weight(grade_id, grade_weight)
        if not response:
            return jsonify(Error='GRADE NOT FOUND'), 404
        result = {'user_id': response[0], 'new_grade_weight': response[1]}
        return jsonify(result=result), 200

    def changeGradeTotal(self, grade_id, grade_total):
        response = CourseDAO().change_grade_total(grade_id, grade_total)
        if not response:
            return jsonify(Error='GRADE NOT FOUND'), 404
        result = {'user_id': response[0], 'new_grade_total': response[1]}
        return jsonify(result=result), 200

    def changeGradeDate(self, grade_id, grade_date):
        response = CourseDAO().change_grade_date(grade_id, grade_date)
        if not response:
            return jsonify(Error='GRADE NOT FOUND'), 404
        result = {'user_id': response[0], 'new_grade_date': response[1]}
        return jsonify(result=result), 200

    # DELETE

    def deleteGrade(self, student_id, grade_id):
        response= CourseDAO().delete_grade(student_id, grade_id)
        if not response:
            return jsonify(Error='Deletion could not be completed'), 500
        result = {'grade_id': response[0]}
        return jsonify(result=result), 200

    # Map to Dictionaries

    def mapToCourseDict(self, row):
        return {
            'course_id': row[0],
            'name': row[1],
            'codification': row[2],
            'credits': row[3],
            'section_num': row[4]
        }

    # ???
    # def mapToIndividualCourseDict(self, row):
    #     return {
    #         'codification': row[0],
    #         'course_name': row[1],
    #         'professor_id': row[2],
    #         'section': row[3]
    #     }

    def mapToGradeDict(self, row):
        return {
            'grade_id': row[0],
            'name': row[1],
            'grade': row[2],
            'total': row[3],
            'weight': row[4],
            'date': row[5]
        }

    def mapToTimeDict(self, row):
        return {
            'day': row[0],
            'start': row[1],
            'end': row[2]
        }

    def mapToTaskDict(self, row):
        return {
            'task_id': row[0],
            'title': row[1],
            'description': row[2],
            'start': row[3],
            'end': row[4],
            'finished': row[5]
        }
