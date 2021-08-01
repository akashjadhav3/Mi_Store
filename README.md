### Install requirements for the project:
1. Install Python3.8
2. Install Requirements file
   `sudo pip3 install -r requirements`
3. create .env file inside mac folder and add creadentials
    SECRET_KEY=xxx
    RAZORPAY_API_KEY=xxx
    RAZORPAY_API_SECRET=xxx

#### Migrate database
`python manage.py makemigrations`

```python manage.py migrate```

#### Run Project
`python manage.py runserver`

#### Admin access credentials
username: akash
password: Akash@123
