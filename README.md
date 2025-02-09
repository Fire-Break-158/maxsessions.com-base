##### Minimum #####

The bare minimum to get started would be 
- Have docker installed on the base machine and ensure the current user is in the 'docker' group. If you just now added the user to the group, logout, and log back in for it to take effect, then continue with the rest below.
- Create an .env and/or DEVENV file, this of course has secrets and others so i will not provide mine but I will include an example below
	- .env is used for environment variables in a production environment
		- .env variables/example
			# For debug, only utilized in dev at the moment
			export FLASK_ENVIRONMENT=Production

			# Sets the program port 
			export BIND_ADDRESS=0.0.0.0:8500
			export MODULE_NAME=app.backbone:app

			# Allows for multiple workers to run to enable higher traffic and use
			export WORKERS=4

			# Necessary for signing and keycloak
			export SECRET_KEY=iNX6PZoa3ckNgOP4NvKmb26O
			export CLIENT_ID=website.com

			# For docker file storage/location
			export BASEDIR=/opt
			# For database connection
			export DBUSER=username
			export DBPASS=password
			export DBHOST=db.host.url
			export DBNAME=database_name
			export DBPORT=database_access_port

			# Storage location for dam
			export FILE_STORAGE_FOLDER=./files

	- DEVENV is use for environment variables in a development environment
		- DEVENV variables/example
			# For debug
			FLASK_ENVIRONMENT=Development

			# Sets the path to the application
			MODULE_NAME=app.backbone:app

			# Necessary for signing and keycloak
			SECRET_KEY=iNX6PZoa3ckNgOP4NvKmb26O
			CLIENT_ID=website.com

			# For docker file storage/location
			BASEDIR=/opt

			# For database connection
			DBUSER=username
			DBPASS=password
			DBHOST=db.host.url
			DBNAME=database_name
			DBPORT=database_access_port

			# Storage location for dam
			FILE_STORAGE_FOLDER=./files

	- The base directory for the docker files is where you would store files for each docker container is, assuming you have a parent directory for all of them to be organized in.
- A client_secrets.json file in the root directory. 
	- Eventually I do plan to make this optional but that has no immediate timeline. Below is an example of the file but missing variables:
	{
	    "web": {
	        "issuer": "",
	        "auth_uri": "",
	        "client_id": "",
	        "client_secret": "",
	        "userinfo_uri": "",
	        "token_uri": "",
	        "token_introspection_uri": "",
	        "op_logout_endpoint" : "",
	        "openid_connect_base_url" : "",
	        "redirect_uri" : ""
	    }
	}



##### Development #####

To get started with development, first complete the minimum section above:
- *Recommended but not required* create a venv to isolate your dev environment. To do this:
	- Change to the root directory for the site and run 'python3 -m venv devenv'
	- Enter the venv by running '. ./devenv/bin/activate'
	- If you choose to leave the venv you can just run 'deactivate'
- Run 'pip install --upgrade pip'
- Run 'pip install -r app/requirements.txt' to install all required libraries to run various functions
- Put your .env or DEVENV file in the root directory
- Run bash start.sh
	- Based on the env file you put in the root (as mentioned above) this will determine if it runs in dev or prod mode outside of a container

The dev environment runs in a verbose mode to make troubleshooting easier, eventually I hope to add a more in depth error handler so you won't need to use the terminal to read the stack trace but that may be a while.



##### Production #####

To get started with production, first complete the minimum section above
- In terminal, navigate to the root directory and run 'docker build -t "desiredimagename" .'
- Change the final line in the CMD file to the image name you chose in the step above 
		- After the ':' should stay the same unless you know what you are doing
- Run the command 'sudo bash CMD'



##### File Structure #####

Just so you understand, the docker directory I am referring to is a structure similar to this (best read in a text editor, git webpage doesn't display properly):

/opt
	/terraria
		/game files
		/etc
	/mysql
		/db files
		/etc
	/nginx
		/config
		/etc
	/etc



If you set a directory for each image you hope to use, as you use these tools you will select the directory you wish to work with and as you create a docker run command, you can save it to the desired directory to re-use later
without having to remember the config
