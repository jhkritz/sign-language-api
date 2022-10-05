# Backend README.md

## Dataset

You can download an ASL dataset [here](https://www.kaggle.com/datasets/grassknoted/asl-alphabet?resource=download)

## Setting up Flask

- Get into the correct directory:

		cd backend

- Create a virtual environment:

		python3 -m venv venv

- Activate the virtual environment:

		source venv/bin/activate

- Install all requirements:

		pip install -r requirements.txt

- Run the Flask server:
	
		python3 app.py


## API Documentation

*Swagger.io* recommends using Flask-RESTplus [here](https://swagger.io/blog/api-development/swagger-annotation-libraries/). 
However, this library is outdated and has been replaced by Flask-RESTX. This is the 
[link](https://flask-restx.readthedocs.io/en/latest/quickstart.html#) to it's the documentation.

## Setting up your local PostgreSQL server

- Install Postgres if you don't already have it

		sudo apt-get install postgresql

- Login to psql
			
		sudo -u postgres psql

- Create the user with the appropriate password. Use the ones below:

		CREATE DATABASE sign_language_api;
		CREATE USER sign_language_api WITH ENCRYPTED PASSWORD 'flask123';
		GRANT ALL PRIVILEGES ON DATABASE sign_language_api TO sign_language_api;

## Heroku Postgres

- To connect the application to the remote database (run this before **flask run**)

		heroku config -a guarded-hamlet-40611 # To get the database url
		export DATABASE_URL='url_from_previous_command' # To allow our app to access the url.

	If you get tired of doing that, add that last command to your ~/.bashrc (if you're using bash) 
	or your ~/.zshrc (if you're using zsh)
	

- To interact with the remote database with psql

		heroku pg:psql -a guarded-hamlet-40611
