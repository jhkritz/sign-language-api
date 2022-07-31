# Development README.md

## Route testing

Theres a small shell script that runs a few curl commands. They should all succeed if you edit the
path for the image in one of the requests (as noted in a comment in test\_requests.sh). You should
also export the **DATABASE\_URL** environment variable so the database contains the expected data.

		sh backend/application/test_requests.sh

## API Documentation

*Swagger.io* recommends using Flask-RESTplus [here](https://swagger.io/blog/api-development/swagger-annotation-libraries/). 
However, this library is outdated and has been replaced by Flask-RESTX. This is the 
[link](https://flask-restx.readthedocs.io/en/latest/quickstart.html#) to it's the documentation.

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

		flask run

## Setting up your local PostgreSQL server

- Install Postgres if you don't already have it

		sudo apt-get install postgresql

- Login to psql
			
		sudo -u postgres psql

- Create the user with the appropriate password. Use the ones below:

		CREATE DATABASE sign_language_api;
		CREATE USER sign_language_api WITH ENCRYPTED PASSWORD 'flask123';
		GRANT ALL PRIVILEGES ON DATABASE sign_language_api TO sign_language_api;

## Heroku CLI

- If you don't have a Heroku account, create one [here](https://www.heroku.com)

- [Install Heroku CLI and learn the basics](https://devcenter.heroku.com/articles/heroku-cli)

- _Note_: the URLs below were the output of **heroku create**, once you've created an account send
	the email address you used on the group so I can grant you access to the app.

		https://guarded-hamlet-40611.herokuapp.com/ | https://git.heroku.com/guarded-hamlet-40611.git

## Heroku Postgres

- To connect the application to the remote database (run this before **flask run**)

		heroku config -a guarded-hamlet-40611 # To get the database url
		export DATABASE_URL='url_from_previous_command' # To allow our app to access the url.

	If you get tired of doing that, add that last command to your ~/.bashrc (if you're using bash) 
	or your ~/.zshrc (if you're using zsh)
	

- To interact with the remote database with psql

		heroku pg:psql -a guarded-hamlet-40611
		
# frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```
	
