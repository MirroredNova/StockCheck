# StockCheck
To run our application on MAC, you first need to install the dependencies with:  
pip3 install -r requirements.txt

---

Since model data (migrations) are not included in the repo, they must be created.
Navigate to the base StockCheck project folder in terminal/PS and run the following commands:  
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
