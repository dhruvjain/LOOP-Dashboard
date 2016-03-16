# loop_dashboard
Run the django server:
- `cd loop_server`
- `python manage.py runserver 0:8000`
Visit the dashboard http://127.0.0.1:8000/dashboard/home/

### Local Database Setup
- `cd loop_server`
- Enter mysql shell with `mysql -u dg -p` and type the password
- `set foreign_key_checks=0`
- Exit mysql shell `exit`
- `python manage.py sqlclear dashboard | python manage.py dbshell` This clears the existing tables
- Again enter mysql shell
- `set foreign_key_checks=1`
- Exit mysql shell `exit`
- `python manage.py syncdb` Creates the tables corresponding to the models.py file
- `python populate_tables.py` This populates tables with the data

### Project Design
`/loop_server/dashboard/models.py` - Has the database models used in this project
`/loop_server/dashboard/api/resources.py` - Has the definitions of TastyPie Resource Classes correponding the models' classes in `models.py`
`/loop_server/static/js/dashboard.js` - Data manipulation functions and classes are present here
`/loop_server/dashboard/templates/base.html` - Base template file made using django templating language
`/loop_server/dashboard/templates/home.html` - Dashboard Home page. Contains the UI and corresponding javascript helper functions

### Dependencies
- [django](https://www.djangoproject.com/)
- [TastyPie](https://django-tastypie.readthedocs.org/en/latest/) - Python library that helps making your django project RESTful with less code
- [Highcharts](http://www.highcharts.com/) - Fast and efficient charting library used for making elegant charts
- [Materialize](http://materializecss.com/) - A modern responsive front-end framework based on Material Design

### Bugs
- Page doesn't show properly on mobile in portrait. In landscape it works fine
- Highcharts make blunders if a chart is initialized in a `div` which in hidden. Therefore, show the `div` first and then initialize the chart

### Sample Screenshots
![showcase1](https://github.com/dhruvjain/LOOP-Dashboard/blob/master/images/pic1.png)
![showcase2](https://github.com/dhruvjain/LOOP-Dashboard/blob/master/images/pic2.png)
![showcase3](https://github.com/dhruvjain/LOOP-Dashboard/blob/master/images/pic3.png)

