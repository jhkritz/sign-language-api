# Development README.md

## Details specific to the frontend/backend application

See the README.md in  **frontend/** or **backend/**.

## Testing the staged applications

You can access the frontend application [here](https://rocky-taiga-14209.herokuapp.com/).

You can access the backend application [here](https://guarded-hamlet-40611.herokuapp.com/).

If something appears to be wrong, check the logs using the following command.

	heroku logs -a <application_name>

## Continuous deployment

Use the following commands to deploy an application to staging manually.

	git push heroku_backend `git subtree split --prefix backend <name_of_branch_to_push>`:main --force	

	git push heroku_frontend `git subtree split --prefix frontend <name_of_branch_to_push>`:main --force

You'll need to have the **heroku\_backend** and **heroku\_frontend** remotes configured. To do that,
past the following into your **.git/config** file.

	[remote "heroku_backend"]
		url = https://git.heroku.com/guarded-hamlet-40611.git
		fetch = +refs/heads/*:refs/remotes/heroku/*

	[remote "heroku_frontend"]
		url = https://git.heroku.com/rocky-taiga-14209.git
		fetch = +refs/heads/*:refs/remotes/heroku/*

## Integration testing

There's a simple test case in **backend/tests.py**. All the test cases in this file are run
everytime something is pushed to the main branch.

## Heroku CLI

- If you don't have a Heroku account, create one [here](https://www.heroku.com)

- [Install Heroku CLI and learn the basics](https://devcenter.heroku.com/articles/heroku-cli)

- _Note_: the URLs below were the output of **heroku create**, once you've created an account send
	the email address you used on the group so I can grant you access to the app.

		https://guarded-hamlet-40611.herokuapp.com/ | https://git.heroku.com/guarded-hamlet-40611.git
