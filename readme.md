## Làm việc với Input, Request, Search, Data

***1. Working with Input Form***

***2. Working with Input Form and Request***
>[Search Form/Search.py](Search%20Form/Search.py)

***3. Search Form***
>[Search Form/SearchWithData.py](Search%20Form/SearchWithData.py)

***4. Working with Session***
>[Session Login/app.py](Session%20Login/app.py)

***5. Registration Form***
>[Registration Form/app.py](Registration%20Form/app.py)

## Làm việc với cơ sở dữ liệu SQLite 
***1. Working with SQLite database***
> [SQLite/app.py](SQLite/app.py)

***2. Flask-SQLAlchemy***
> [SQLite/main_2_SQLAlchemy.py](SQLite/main_2_SQLAlchemy.py)

## Làm việc với cơ sở dữ liệu - Search Form
***3. Search Form***
>[Search Form with DB/app.py](Search%20Form%20with%20DB/app.py)

## Làm việc với cơ sở dữ liệu - Login Form Session
***5. Working with Session - Check User***
>[Login Form with DB/app_login_db.py](Login%20Form%20with%20DB/app_login_db.py)

## Làm việc với cơ sở dữ liệu - New Registration Form
***2.2. New Registration Form***
>[Registration Form with DB/app_registration.py](Registration%20Form%20with%20DB/app_registration.py)

## Làm việc với cơ sở dữ liệu - Shopping Cart
>[Shopping Cart/app.py](Shopping%20Cart/app.py)



# Một số lỗi thường gặp
1. Port conflict
> netstat -ano | findstr :5000
> taskkill /PID <PID> /F
2. Run ra template cũ chứ không ra cái đang làm, không render được template 
> restart 
3. OperationalError (sqlite3.OperationalError: unable to open database file)
> check database's path 
4. Bad Request
> check value in request.form[]
5. Method Not Allowed
> add 'GET' or 'POST' (or both) to @app.route
6. Internal Server Error 
> just pray for yourself ;<
