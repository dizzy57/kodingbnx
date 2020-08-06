# kodingbnx

This is a simple web-app that may be used by any group of people to organize and run their daily study/practice routine.

It serves two main purposes: task management/scheduling and solutions submission.

### Solution submission

Every user has access to a submissions page where they can publish their solution for the current day's problem.

### Task management and scheduling

An admin can prepare a list of tasks for students. One task per day :)

## How to build and run

`docker-compose up --build`

When running for the first time you will need to create a Django super user:

`docker-compose exec web /venv/bin/python /app/manage.py createsuperuser`

Access the site on http://localhost:8000/, log in using the super user credentials created earlier.

### Note for Docker Toolbox users on Windows

You might need to setup port forwarding, see https://stackoverflow.com/a/45822356/76176.

Also, mounting might not work if the project is outside of Users folder. Move it there or try https://headsigned.com/posts/mounting-docker-volumes-with-docker-toolbox-for-windows/.
