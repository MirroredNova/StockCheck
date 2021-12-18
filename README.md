# StockCheck
StockCheck is built on a Python-based platform, and requires Python version 3.9 or newer to ensure functionality.

It also makes use of Selenium for both core functionality and testing, which requires that an appropriate ChromeDriver be provided.
This can be found at https://chromedriver.chromium.org/downloads - ensure that the ChromeDriver version matches the version of Google Chrome currently installed.
The executable file for this should be placed in the project directory's "resources/webdrivers" folder and named "chromedriver".

---

With these installed, Python's pip can be used to install the dependencies with:  
pip3 install -r requirements.txt

---

Since model data (migrations) are not included in the repository, they must be created.
If the project has previously been run on the system, all files with names other than "__init.py__" in "[folder]/migrations" should first be deleted, along with the database file, "db.sqlite3".
Then, run the following commands from the project directory:  
python manage.py makemigrations  
python manage.py migrate  

---

If you need a superuser, run the following command and fill out the text-form:  
python manage.py createsuperuser

---

Once this is done, run the following command to start the server:  
python manage.py runserver

To view the website, navigate to the following URL in your browser of choice:  
http://127.0.0.1:8000/

---

Tests can be run with:
python manage.py test
(Note that the user will need to Ctrl-C out of the tests at the end as is tries to destroy the database, as the multithreading for the webscraping service interferes with this stage)

Coverage reports with and without the (difficult to test practically) views included can be viewed from "index.html" in the appropriate folder.

