# Django-meme-site

Example of site where you can post your images with titles and like or comment them. These images is added automaticly to separate site called 'waiting room'. Only accounts with admin permission can add images to main site.

To run this web app you need to follow these steps:

1: In empty folder open console and copy project there `git clone https://github.com/Sierakos/Django-meme-site.git`  
2: Create virtual environment `py -m venv env`  
3: install all needed librares `pip install -r requirements.txt`  
4: go to memeplz folder `cd memeplz`  
5: make migration for creating database `py manage.py migrate`  
6: OPTIONAL create superuser `py manage.py createsuperuser`
7: run server `py manage.py runserver`  
