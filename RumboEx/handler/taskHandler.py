from flask import jsonify, request
from RumboEx.dao.taskDao import TaskDAO

class TaskHandler():


    def get_all_tasks(self):
        dao = TaskDAO()
        result = dao.get_all_tasks()
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToTaskDict(r))
        return jsonify(mapped_result)


    def get_personal_task_by_user_id(self, user_id):
        dao = TaskDAO()
        result = dao.get_personal_tasks_by_user_id(user_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToTaskDict(r))
        return jsonify(mapped_result)


    def get_study_task_by_user_id(self, user_id):
        dao = TaskDAO()
        result = dao.get_study_tasks_by_user_id(user_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToTaskDict(r))
        return jsonify(mapped_result)


    def get_course_task_by_user_id(self, user_id):
        dao = TaskDAO()
        result = dao.get_course_tasks_by_user_id(user_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToTaskDict(r))
        return jsonify(mapped_result)


    def get_appointment_tasks_by_user_id(self, user_id):
        dao = TaskDAO()
        result = dao.get_appointment_tasks_by_user_id(user_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToTaskDict(r))
        return jsonify(mapped_result)

    def get_study_task_by_user_id_and_course_id(self, user_id, course_id):
        dao = TaskDAO()
        result = dao.get_study_tasks_by_user_id_and_course_id(user_id, course_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToTaskDict(r))
        return jsonify(mapped_result)

    def get_courses(self, user_id):
        dao = TaskDAO()
        #just trying it make it work pero se que esta mal
        result = dao.get_all_courses()
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapCourseName(r))

        print(mapped_result)
        return jsonify(mapped_result)

    def get_study_task_count_by_user_id(self,user_id):
        dao = TaskDAO()
        result = dao.get_study_task_count_by_user_id(user_id)
        if not result:
            return jsonify(Error= "NOT FOUND"),404
        print(result)
        return jsonify(result)

    def get_personal_task_count_by_user_id(self,user_id):
        dao = TaskDAO()
        result = dao.get_personal_task_count_by_user_id(user_id)
        if not result:
            return jsonify(Error="NOT FOUND"), 404
        print(result)
        return jsonify(result)

    def get_appointment_task_count_by_user_id(self,user_id):
        dao=TaskDAO()
        result = dao.get_appointment_task_count_by_user_id(user_id)
        if not result:
            return jsonify(Error = "NOT FOUND"),404
        print(result)
        return jsonify(result)

    def get_course_task_count_by_user_id(self,user_id):
        dao = TaskDAO()
        result = dao.get_course_task_count_by_user_id(user_id)
        if not result:
            return jsonify(Error = "NOT FOUND"),404
        print(result)
        return jsonify(result)

    def insert_personal_task(self, user_id, form):
        print('form', form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            print('form', form)
            task_name = form['task_name']
            task_description = form['task_description']
            start_time = form['start_time']
            end_time = form['end_time']
            finished = False
            if task_name and start_time and end_time and finished:
                dao = TaskDAO()
                task_id = dao.add_personal_task(task_name, task_description, start_time, end_time, finished)
                dao.add_task_to_user(user_id, task_id)
                result = self.mapToTaskDict([task_id, task_name, task_description, start_time, end_time, finished])
                return jsonify(result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def mapToTaskDict(self, row):
        # Verificar orden de atributos en la tabla
        return {
            'task_id': row[0],
            'title': row[2],
            'description': row[3],
            'start': row[1],
            'end': row[4],
            'finished': row[5]
            }

    def mapCourseName(selfself, row):
        return{'name': row[0], 'codification': row[1], 'section': row[2]}
