# SoDocu - Software Documentation

With SoDocu you can document all requirements of your software directly beside
your code. The persistence is based on text files. So you can checkin and tag 
your requirements synchronously with your code in every kind of version control 
system. You can checkout your requirements at one point in time. So you know 
exactly what features are implemented at this time.

# Requirements need to be developed
Requirements have not fallen from the sky. They need to be developed. You can not
solve problems in code which are laying in incomplete or inconsistent 
requirements. Therefor you have to:
* discover requirement sources (like stakeholder or law documents) 
* investigate the system context to identify processes, technical systems a.s.o.
* identify containing business issues
* find objectives for solving these issues
* describe scenarios to achieve the objectives (user stories)
* strip down these scenarios in atomic requirements divided in data, function, 
state an quality

SoDocu itself is documented by SoDocu. So can see your first example directly
at folder "sodocu".

# Inspiration
SoDocu is inspired by:
* http://www.arc42.de/template/template.html
* http://easyrequirement.blogspot.de/
* http://www.flonatel.de/projekte/rmtoo/

# Installation
## for running
* install [Python 2.7.x](http://www.python.org/):
  * Linux: should already be installed
  * Windows: http://www.python.org/download/
* install [pip](http://www.pip-installer.org/): 
  * Linux: sudo apt-get install python-pip
  * Windows: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip
* install [Werkzeug](http://werkzeug.pocoo.org/): 
  * Linux: sudo pip install Werkzeug
  * Windows: pip install Werkzeug
* install [Jinja2](http://jinja.pocoo.org/): 
  * Linux: sudo pip install Jinja2
  * Windows: pip install Jinja2
* install SoDocu: 
TODO

## for testing and developing
* install [nose](https://nose.readthedocs.org/en/latest/): 
  * Linux: sudo pip install nose
  * Windows: pip install nose
* install [mock](https://code.google.com/p/mock/): 
  * Linux: sudo pip install mock
  * Windows: pip install mock

# Usage
TODO

# TODOs
* ~~save current user in cookie~~
* ~~automatic saving of created/changed by/at~~ 
* ~~menu position of item type configurable~~
* ~~template for lists and single item configurable~~
* ~~dialog for confirming item delete~~
* ~~edit existing items~~
* creating further item types
* ~~make logic dynamicly depending on item type~~
* ~~use glossary entries for dynamic tooltips in web gui~~
* ~~editor for glossary entries~~
* eat your own dog food - create sodocu items
* ~~full text search over all item types~~
* ~~fill relations between items~~
* ~~create backward (from) relations automaticly~~
* dashboard shown known issues i.e.: missing relations
* graphical models:
  * BPMN for processes
  * UML for requirements
  * MindMap for objectives 
  * SysML for system context
* dependency between model and item
* ~~graphical visualization of relations~~
* i18n
* links between requirements and source code and tests
* export to pdf (srs - software requirements specification)
* ~~show number of issues for each issue type in left side menu~~
* add attachments (images, documents, ...) to items
* easy installation with pip and/or easy_install

# Known Bugs
* ~~glossary terms within glossary leads to wrong displayed original words~~
* ~~adding new item do not increase item count in left menu bar~~
* ~~OK button at delete popup do not work~~


Enjoy using SoDocu.
