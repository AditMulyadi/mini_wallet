## Mini Wallet Application

### Requiremets:
- Python 3.9
- Django 4.1
- Database SQLite (default)

### Installation:
1. Clone this project to your local machine
2. Create new python virtualenv by executing this command:
   ```
   virtualenv env -p python3.9
   ```
3. Activate the newly created env by executing this command:
   ```
   source env/bin/activate
   ```
4. Change directory to be inside the project folder
   ```
   cd mini_wallet
   ```
5. Install all required packages by executing this command:
   ```
   pip install -r requirements.txt
   ```
6. Migrate database
   ```
   ./manage.py migrate
   ```
7. Run server!
   ```
   ./manage.py runserver 8000
   ```
   
Your mini_wallet project is now ready!


### Postman

You can import this [Postman Collection](https://github.com/AditMulyadi/mini_wallet/blob/master/postman-collection.json) inside the project folder as a collection to help you access the API. Making sure that you include the token inside the header after getting the token authentication from the _INIT_ API.
