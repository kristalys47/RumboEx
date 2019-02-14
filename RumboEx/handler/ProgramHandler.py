from flask import jsonify
from RumboEx.dao.ProgramDao import ProgramDAO


class ProgramHandler:

    def get_faculties_and_programs(self):
        dao = ProgramDAO()
        faculties = dao.get_faculties()
        if not faculties:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for f in faculties:
            faculty_num = f[0]
            programs = dao.get_programs(faculty_num)
            programs_arr = []
            if programs:
                for p in programs:
                    programs_arr.append(self.mapToProgramDict(p))
            mapped_result.append(self.mapToFacultyDict([f[0], f[1], programs_arr]))
        return jsonify(Faculties=mapped_result)

    def mapToFacultyDict(self, row):
        return {'faculty_num': row[0], 'faculty_name': row[1], 'programs': row[2]}

    def mapToProgramDict(self, row):
        return {'program_name': row[0], 'program_num': row[1]}
