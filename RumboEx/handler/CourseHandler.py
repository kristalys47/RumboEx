from flask import jsonify
from RumboEx.dao.CourseDao import CourseDAO
from RumboEx.dao.taskDao import TaskDAO
from RumboEx.handler.taskHandler import TaskHandler

class CourseHandler():

    def get_courses_by_student_id(self, student_id):
        dao = CourseDAO()
        result = dao.get_courses_by_student_id(student_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToCourseDict(r))
        return jsonify(mapped_result)

    def get_courses_with_grades_by_student_id(self, student_id):
        dao = CourseDAO()
        courses = dao.get_courses_by_student_id(student_id)
        if not courses:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for c in courses:
            course = self.mapToCourseDict(c)

            section_id = c[4]
            enrolled_id = c[5]

            course['time'] = []
            course['grades'] = []
            course['tasks'] = []

            # get time schedule of section
            time = dao.get_section_times_by_section_id(section_id)
            if time:
                for t in time:
                    course['time'].append(self.mapToTimeDict(t))

            # get grades of course
            grades = dao.get_grades_by_course_id(enrolled_id)
            if grades:
                for g in grades:
                    course['grades'].append(self.mapToGradeDict(g))

            # get tasks of course
            dao2 = TaskDAO()
            tasks = dao2.get_study_tasks_by_user_id_and_course_id(enrolled_id)
            # taskHandler = TaskHandler()
            # tasks = taskHandler.get_study_task_by_user_id_and_course_id(student_id, course['course_id'])
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

    def get_grades_by_course_id(self, course_id):
        dao = CourseDAO()
        result = dao.get_grades_by_course_id(course_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToGradeDict(r))
        return jsonify(mapped_result)


    def mapToCourseDict(self, row):
        return {
            'course_id': row[0],
            'name': row[1],
            'codification': row[2],
            'section_num': row[3]
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
            'name': row[0],
            'grade': row[1],
            'total': row[2],
            'weight': row[3]
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
