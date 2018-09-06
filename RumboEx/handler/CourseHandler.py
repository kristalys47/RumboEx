from flask import jsonify
from RumboEx.dao.CourseDao import CourseDAO

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

    def get_course_by_course_id(self, course_id):
        dao = CourseDAO()
        result = dao.get_course_by_course_id(course_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        return jsonify(self.mapToIndividualCourseDict(result))


    def mapToCourseDict(self, row):
        # check how the order is returned
        return {
            'user_id': row[4],
            'codification': row[0],
            'course_name': row[1],
            'professor_id': row[2],
            'section': row[3]
        }

    def mapToIndividualCourseDict(self, row):
        return {
            'codification': row[0],
            'course_name': row[1],
            'professor_id': row[2],
            'section': row[3]
        }
