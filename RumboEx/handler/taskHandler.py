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
            print(r)
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


    def insert_personal_task(self, form):
        print(form)
        if len(form) != 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            task_name = form['task_name']
            task_description = form['task_description']
            start_time = form['start_time']
            end_time = form['end_time']
            finished = form['finished']
            if task_name and start_time and end_time and finished:
                dao = TaskDAO()
                task_id = dao.add_personal_task(task_name, task_description, start_time, end_time, finished)
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
