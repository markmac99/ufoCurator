# ufoCurator

INSTALLATION
============
Windows - download the packaged EXE and install. This will create a new entry in the Start Menu. 

Linux / MacOS - first create a python virtualenv "ufoCurator" with python 3.8.x. This is essential.

Next ppen a Terminal window and clone this repo to your hard drive using "git clone https://github.com/markmac99/ufoCurator.git".   

Finally, in the same Terminal window, activate the virtualenv, change directory into the new ufoCurator folder and run "pip install -r requirements.txt". This will install all required packages. 

USAGE
=====
Windows - run the application from the Start Menu.  
Linux / MacOS - open a Terminal window, activate the python virutalenv, cd into the ufoCurator folder and run "python curateUFO.py". 

The application GUI will start up. From the File menu, choose a folder containing a years worth of UFO data eg "c:\ufo\camera1\2021". The listbox on the left will populate with the data in the selected folder and below. You can move between captures to view the data.  

To curate the data click "Clean". This will run through every captured event and classify it. Bad data will be moved to a folder "bad". If there's lots of data this may take some time so be patient! When its finished, the list on the left will have updated to show the new location of any moved files which will have 'bad' in the path name.   

Thats it, your data is curated!  

Optional Actions
----------------
After cleaning the data you can view the moved files and move them back if you disagree with the  software. You can also move bad data that the curator missed. Neither of these is essential. 