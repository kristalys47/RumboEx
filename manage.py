from RumboEx import app as application
from flask_script import Manager, Server


manager = Manager(application)

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host="localhost"
))

if __name__ == '__main__':
    manager.run()
