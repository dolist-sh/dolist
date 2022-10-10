## DoList
DoList is a web app that finds and reports the TODO comments in the repositories. It's currently under construction. 

- Check out the DoList in action at the [dev env](http://15.188.137.121/signin)


### Run test locally
Tests for database access module is run against the postgres instance. 

Run the following commands before running tests locally.
- export POSTGRES_USER=[your_db_user] POSTGRES_DB=[your_db_name]
- ./scripts/init-db.sh