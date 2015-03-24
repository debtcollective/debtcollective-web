debt.is and debtcollective.org
=======

This is a django site deployed on the heroku framework.

Please fork the repository and open pull requests when you're ready to merge.

### Step 1: Install postgresql

*Mac OSX*
http://postgresapp.com/

*Linux*
I trust you can figure it out

*Windows*
Good luck

Grab your submodule initially:
```
$ git clone ...
$ git submodule update --init --recursive
```

On the terminal:
```
$ createdb debtis
$ createuser debtis
```

### Step 2: Install Python and Virtualenv

Follow instructions for your platform.

### Step 3: Setup environment

On the terminal:
```
$ git clone </path/to/repo>
$ cd <repo>
$ virtualenv venv
$ export PYTHONPATH=$PYTHONPATH:`pwd`
$ source venv/bin/activate
$ pip install -r requirements.txt
$ cd be
$ mkdir -p staticfiles/js
$ python manage.py syncdb
```

### Step 4: Set up point data

This loads the points (world cities) into the database. This small set is just for testing. There's a larger file that has the full list to be used in production.

```
$ cat lib/points-small.sql | python manage.py dbshell
```

## Running the app

```
$ export SECRET_KEY='some-key'
$ source venv/bin/activate
(venv) $ cd be
(venv) $ python manage.py runserver
```

```
$ cd be/proj
$ grunt watch
```

## Testing the app

Create the postgresql user and databases debtis
```
$ psql
psql> CREATE DATABASE test_debtis;
psql> ALTER USER debtis createdb;
psql> ALTER DATABASE test_debtis OWNER TO debtis;
```

Running the tests:
```
$ python manage.py test
```

## Updating the map

Visit this in your browser:
```
http://localhost:8000/generate_map_json/?password=MAGIC_PASSWORD
```


## Compiling static assets

When you change the CSS/JS files, please run grunt to update the minified file so when deployed, the CDN can grab the correct one.

**Setup** **(only do once)**
```
npm install -g grunt-cli
npm install
```

**Watch**
```
grunt watch
```

**Deploy**
```
grunt
```


## Deploying to heroku
Add these to your .git/config in debtcollective-web:

```
[remote "heroku-staging"]
  url = git@heroku.com:debt-is-staging.git
  fetch = +refs/heads/*:refs/remotes/heroku-staging/*
[remote "heroku"]
  url = git@heroku.com:debt-is.git
  fetch = +refs/heads/*:refs/remotes/heroku/*
```

### To update the wizard & push:
```
cd be/proj/templates/debtcollective-wizard
git pull
cd ..
git commit -am "updating debtcollective-wizard"
git push origin master
git push heroku-staging master
git push heroku-master
```
