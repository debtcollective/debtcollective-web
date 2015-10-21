## migration path

1. push to heroku

```
git push heroku master
```

1.1 run tests

```
heroku run python be/manage.py test --app debt-is
```

1.2 make sure models are migrated
```
heroku run python be/manage.py migrate collectives --app debt-is
heroku run python be/manage.py migrate gather --app debt-is
```

2. migrate dtrs

```
heroku run python be/manage.py shell --app debt-is
import proj.arcs.dtr as dtr
dtr.send_dtr_migration_emails()
```

3. send users activation emails

- export users from sendy
- for user in users, send_activation_email
- after a couple weeks, remove the users without emails
