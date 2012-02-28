Simple Django application to view current beers at the Flying Saucer Houston location.  The application depends on my custom saucer api for getting the beers, etc.  Message me if you would like to see it and/or use it.

Required packages:

    - Django 1.0.4 final
    - Python 2.5

Nice to have packages:

    - Pylint 0.19.0

This project uses the pylint python package for code analysis and to ensure
the code follows certain standards.  View the standards.rc file for more
information on coding standards for this project (mostly the default pylint
settings).

You can analyze the source for yourself using pylint by doing the following:
    - Install pylint 0.19.0 (read pylint docs for more info)
    - Specify the standards.rc file with the --rcfile option to pylint
      or if you are on a UNIX box put rename the included standards.rc file
      to ~/.pylintrc (make sure you don't already have one first!)
