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

    def get_all_tasks_by_user_id(self, user_id):
        dao = TaskDAO()
        mapped_result = []

        # get course tasks
        course = dao.get_course_tasks_by_user_id(user_id)
        if course:
            for t in course:
                task = self.mapToTaskDict(t)
                task['type'] = 'course'
                mapped_result.append(task)

        # get study tasks
        study = dao.get_study_tasks_by_user_id(user_id)
        if study:
            for t in study:
                task = self.mapToTaskDict(t)
                task['type'] = 'study'
                mapped_result.append(task)

        # get personal tasks
        personal = dao.get_personal_tasks_by_user_id(user_id)
        if personal:
            for t in personal:
                task = self.mapToTaskDict(t)
                task['type'] = 'personal'
                mapped_result.append(task)

        # get appointment tasks
        appointment = dao.get_appointment_tasks_by_user_id(user_id)
        if appointment:
            for t in appointment:
                task = self.mapToTaskDict(t)
                task['type'] = 'appointment'
                mapped_result.append(task)

        if not mapped_result:
            return jsonify(Error='NOT FOUND'), 404

        return jsonify(mapped_result), 200

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

    def insert_study_task(self, user_id, form):
        print('form', form)
        print(form['task_name'])
        if len(form) != 5:
            return jsonify(Error="Malformed post request"), 400
        else:
            task_name = form['task_name']
            task_description = form['task_description']
            start_time = form['start_time']
            end_time = form['end_time']
            course_id = form['course_id']
            finished = False
            if task_name and start_time and end_time and course_id and finished:
                dao = TaskDAO()
                task_id = dao.add_study_task(task_name, task_description, start_time, end_time, finished, course_id)
                dao.add_task_to_user(user_id, task_id)
                result = self.mapToTaskDict([task_id, task_name, task_description, start_time, end_time, finished])
                return jsonify(result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insert_personal_task(self, user_id, form):
        print('form', form)
        print(len(form))
        if len(form) is not (4 or 3):
            return jsonify(Error="Malformed post request"), 400
        else:
            print('form', form)
            task_name = form['task_name']
            task_description = form['task_description']
            start_time = form['start_time']
            end_time = form['end_time']
            finished = False
            if task_name and start_time and end_time:
                dao = TaskDAO()
                task_id = dao.add_personal_task(task_name, task_description, start_time, end_time, finished)
                dao.add_task_to_user(user_id, task_id)
                # result = self.mapToTaskDict(task_id)
                return jsonify({'task_id': task_id[0]}), 200
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def mapToTaskDict(self, row):
        # Verificar orden de atributos en la tabla
        return {
            'task_id': row[0],
            'title': row[1],
            'description': row[2],
            'start': row[3],
            'end': row[4],
            'finished': row[5]
            }

    def mapCourseName(selfself, row):
        return{'name': row[0], 'codification': row[1], 'section': row[2]}
