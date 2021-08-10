## Tax Management System

> Django, Docker, Heroku, Djangorestframwork, Postgresql

## BACKEND

### Library Used

- Django
- djangorestframework
- psycopg2-binary
- djangorestframework-simplejwt
- drf-yasg

### Why choose Django and Postgresql (For Backend)?

**Django** is the one of the most popular web framework for python, Django takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. As for Postgresql it works well with Django and also preferable for the assignment as mentioned [here](./read.md).

### INSTALLATION && USAGE (DOCKER)

No need to worry about installation, if docker and docker-compose is not installed in your system please install and follow along the step(s).

- Git Clone this repo and enter into the [TaxManagementSystem](https://github.com/coderj001/TaxManagementSystem) directory.
- Create

  - a file 'django-env' with content
    ```
    debug=<>
    secret_key=<>
    postgres=<>
    DB_HOST=<>
    DB_NAME=<>
    DB_USER=<>
    DB_PASS=<>
    DB_PORT=<>
    ```
    reffer this file [here](./django-env-sample).
  - a file 'pgdb-env' with content
    ```
    POSTGRES_DB=<>
    POSTGRES_USER=<>
    POSTGRES_PASSWORD=<>
    ```
    reffer this file [here](./pgdb-env-sample).

- Run the command `docker-compose up --build`. And it should be up and running. Checkout the endpoints mentioned below. Note test case and will be run and created.
- To run test case, `docker-compose exec backend python manage.py test`. Note test case automatically run during execution of previous command `docker-compose up --build`.
- To create admin user, `docker-compose exec backend python manage.py createsuperuser`.
- Testcase is added to in docker `entrypoint.sh`. You can manually run `docker-compose exec backend python manage.py test`

### DEPLOYED (HEROKU)

Application is deployed on heroku, link of the url is [https://agile-savannah-29634.herokuapp.com/](https://agile-savannah-29634.herokuapp.com/) it will work similar to docker container. And admin config are email:admin@mail.com and password: admin required for accessing admin panel `<BASE_URL>/admin/`.

### Admin Panel

- Django provide built-in admin panel can be access from `localhost:8000/admin` url.
- If you used `docker-compose up --build` then admin user will be created by `docker-compose exec backend python manage.py createsuperuser`. Otherwise create using `python manage.py createsuperuser`
- Use django admin panel to manipulate user and tax models.

#### Preview

![image](https://i.imgur.com/G5aIJYw.png)
![image](https://i.imgur.com/2tJdQ75.png)

### Swagger UI
You can access swagger api docs from `<BASE_URL>/swagger/`. I have added custom swagger ui material.

![image](https://i.imgur.com/TukjiCE.png)

### API ENDPOINTS

#### **BASE_URL**: /api/users

### To get Login

#### Request

`POST <BASE_URL>/login/`
<br />
<br />
Body: `{'email': 'user@mail.com', 'password':'passwd123'}`

#### Response

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyODY5ODMyNywianRpIjoiN2Y2YmNiZWIwMzY4NDQ5OWIzZDE3NjNkYTVmNThkZTQiLCJ1c2VyX2lkIjoiNjIyNThlM2YtMGVmYy00N2JkLTk4ZTEtODUyNTBjMWVlZmI5In0.1zK-oOrRXTv2DnarY8ax9mldrnaQg9G67QqHTnTjJv0",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMxMjAzOTI3LCJqdGkiOiJmMWVhMmMzNzQ5ZWE0ODQ1OWIxY2ZkNzJiMjIxMDQ4NCIsInVzZXJfaWQiOiI2MjI1OGUzZi0wZWZjLTQ3YmQtOThlMS04NTI1MGMxZWVmYjkifQ.hxuesV0-Y_aq6xVWZRYLj1Dz1xnRGuAvpO5QzOyNYj4",
  "id": "62258e3f-0efc-47bd-98e1-85250c1eefb9",
  "email": "admin@mail.com",
  "username": "admin",
  "user_type": "admin",
  "state": "",
  "date_joined": "2021-08-08T21:10:46.700375+05:30",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMxMjAzOTI3LCJqdGkiOiI4MGViZjZjOTIwNzY0NmNlYTQzNDUyMzI2NWViMmYxOSIsInVzZXJfaWQiOiI2MjI1OGUzZi0wZWZjLTQ3YmQtOThlMS04NTI1MGMxZWVmYjkifQ.OGOqm1PZPCWDBM_ykwyjHicwrT4ksPN5O0BgGWKXulE"
}
```

#### Preview

![image](https://i.imgur.com/gCS5F1x.png)

### To get register tax-accountant

#### Request

`POST <BASE_URL>/register/tax-accountant/`
<br />
Body: `{ "username":"tax_accountant_1", "email":"tax_accountant_1@mail.com", "password":"tax_accountant_1" }`

#### Response

```json
{
  "id": "fca6b3b4-2645-4852-948a-7f51efd1dc87",
  "email": "tax_accountant_1@mail.com",
  "username": "tax_accountant_1",
  "user_type": "tax-accountant",
  "state": "",
  "date_joined": "2021-06-29T17:21:48.585464Z",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3NTc5MzA5LCJqdGkiOiI5ZGY4NDkzMGE3ZGI0YzZhYjg2MTVlZGM3MmY3ZmQ3YyIsInVzZXJfaWQiOiJmY2E2YjNiNC0yNjQ1LTQ4NTItOTQ4YS03ZjUxZWZkMWRjODcifQ.7cee-lCqquKTHDl0MXK0i9tFjG0FQp6oFVl8l1e5QeU"
}
```

#### Preview

![image](https://i.imgur.com/cf7WUPv.png)

### To get register customer

#### Request

`POST <BASE_URL>/register/tax-payer/`
<br />
Body: `{ "username":"tax_payer_1", "email":"tax_payer_1@mail.com", "password":"tax_payer_1" }`

#### Response

```json
{
  "id": "0d1739ea-ba36-4d1b-add5-e34045a76be5",
  "email": "tax_payer_1@mail.com",
  "username": "tax_payer_1",
  "user_type": "tax_payer_1",
  "state": "",
  "date_joined": "2021-06-29T17:24:43.532383Z",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3NTc5NDgzLCJqdGkiOiI1MTBhMzRlNjIwNTc0ZTg5YTZkYmIzOWFkYjY2MjliNCIsInVzZXJfaWQiOiIwZDE3MzllYS1iYTM2LTRkMWItYWRkNS1lMzQwNDVhNzZiZTUifQ.OwrAsVp9CuMzGOG0GMNejlYI6I-WEj5FQkjGSuhGEF4"
}
```

#### Preview

![image](https://i.imgur.com/eQmN2Gg.png)

### To get list of user

#### Request

`GET <BASE_URL>/list/`
<br />
Header: `{ 'Authorization':'Bearer <TOKEN>' }`

#### Response

Response will be different for different user base on token.

```json
[
  {
    "id": "b2bc4f19-42c2-4169-873e-9d8fe8282cda",
    "email": "sample@mail.com",
    "username": "sample",
    "first_name": null,
    "last_name": null,
    "user_type": "tax-payer",
    "state": "Bihar",
    "date_joined": "2021-08-10T19:35:42.024118+05:30"
  },
  {
    "id": "8d5bcc5c-f050-412b-9d79-41f62784bd84",
    "email": "tax-payer-3@mail.com",
    "username": "tax-payer-3",
    "first_name": null,
    "last_name": null,
    "user_type": "tax-payer",
    "state": "",
    "date_joined": "2021-08-08T21:43:00.899768+05:30"
  },
  {
    "id": "e91bad56-c4b9-42ce-ae68-c645e6b166a9",
    "email": "tax-accountant-1@mail.com",
    "username": "tax-accountant-1",
    "first_name": null,
    "last_name": null,
    "user_type": "tax-accountant",
    "state": "",
    "date_joined": "2021-08-08T21:31:03.586683+05:30"
  },
  {
    "id": "6af0da57-5806-46ed-b5f1-4089861d328e",
    "email": "tax-accountant-2@example.com",
    "username": "tax-accountant-2",
    "first_name": null,
    "last_name": null,
    "user_type": "tax-accountant",
    "state": "",
    "date_joined": "2021-08-10T22:04:58.542297+05:30"
  },
  {
    "id": "566a1d36-f6f9-4382-b4a5-61b01dd16ea8",
    "email": "tax-payer-2@mail.com",
    "username": "tax-payer-2",
    "first_name": null,
    "last_name": null,
    "user_type": "tax-payer",
    "state": "Goa",
    "date_joined": "2021-08-08T21:28:16.223335+05:30"
  },
  {
    "id": "2a370b8e-2c92-4519-ad55-14ef070b12cf",
    "email": "tax-payer-1",
    "username": "tax-payer-1",
    "first_name": "first",
    "last_name": "last",
    "user_type": "tax-payer",
    "state": "Jharkhand",
    "date_joined": "2021-08-08T21:31:11.228430+05:30"
  }
]
```

#### Preview

![image](https://i.imgur.com/mAE8u7q.png)

### To get user

#### Request

`GET <BASE_URL>/<uuid:id>/`
<br />
Header: `{ 'Authorization':'Bearer <TOKEN>' }`

#### Response

```json
{
  "id": "b2bc4f19-42c2-4169-873e-9d8fe8282cda",
  "email": "sample@mail.com",
  "username": "sample",
  "first_name": null,
  "last_name": null,
  "user_type": "tax-payer",
  "state": "Bihar",
  "date_joined": "2021-08-10T19:35:42.024118+05:30"
}
```

#### Preview

![image](https://i.imgur.com/exbuhYQ.png)

### To edit user

#### Request

`PUT <BASE_URL>/<uuid:id>/`
<br />
Body: `{ "username":"tax_payer_1", "email":"tax_payer_1@mail.com", "password":"tax_payer_1", "first_name":"tax_payer_1 update", "last_name":"tax_payer_1 last", "state": "Goa" }`
<br />
Header: `{ 'Authorization':'Bearer <TOKEN>' }`
<br />
**Note add state in user otherwire tax will not work.**

#### Response

```json
{
  "id": "2f837973-6f08-4ff0-8d18-12f791d30504",
  "email": "tax_payer_1@mail.com",
  "username": "tax_payer_1",
  "first_name": "tax_payer_1 update",
  "last_name": "tax_payer_1 last",
  "user_type": "tax_payer_1",
  "date_joined": "2021-06-27T15:26:04.635540Z"
}
```

#### Preview

![image](https://i.imgur.com/SbO1Q0T.png)

### To list of state

#### Request

`GET <BASE_URL>/state_list/`
<br />
Header: `{ 'Authorization':'Bearer <TOKEN>' }`
<br />

#### Response

```json
[
  "Andhra Pradesh",
  "Arunachal Pradesh",
  "Assam",
  "Bihar",
  "Chhattisgarh",
  "Goa",
  "Gujarat",
  "Haryana",
  "Himachal Pradesh",
  "Jharkhand",
  "Karnataka",
  "Kerala",
  "Madhya Pradesh",
  "Maharashtra",
  "Manipur",
  "Meghalaya",
  "Mizora",
  "Nagaland",
  "Odisha",
  "Punjab",
  "Rajasthan",
  "Sikkim",
  "Tamil Nadu",
  "Telangana",
  "Tripura",
  "Uttar Pradesh",
  "Uttarakhand",
  "West Bengal",
  "Andaman and Nicobar Island",
  "Chandigarh",
  "Dadra and Nagar Haveli and Daman and Diu",
  "Delhi",
  "Ladakh",
  "Lakshadweep",
  "Jammu and Kashmir",
  "Puducherry"
]
```

#### Preview

![image](https://i.imgur.com/sz1Xb1N.png)

#### **BASE_URL**: /api/tax

### To create tax

#### Request

`POST <BASE_URL>/create/`
<br />
Header: `{ 'Authorization':'Bearer <TOKEN>' }`
<br />
Body: `{ 'income': 100000, 'deadline':'2021/08/20', 'tax_accountant': 'tax_accountant_1', 'tax_payer': 'tax_payer_1'}`

#### Response

Only tax-accountant type user is allowed

```json
{
  "id": 17,
  "income": 150000,
  "status": "NEW",
  "tax_amount": 0,
  "tax_accountant": "tax_accountant_1",
  "tax_payer": "tax_payer_1",
  "created_at": "2021-08-10T22:40:10.879332+05:30",
  "updated_at": "2021-08-10T22:40:11.043337+05:30",
  "deadline": "2021-08-20T00:00:00+05:30",
  "fines": 0,
  "total_amount": 0,
  "payment_status": false,
  "payment_date": null
}
```

#### Preview

![image](https://i.imgur.com/8fnzStH.png)

### To get list of tax

#### Request

`GET <BASE_URL>/list/?status=<new|paid|delayed>&created_at='yyyy/mm/dd'&updated_at='yyyy/mm/dd'`
<br />
Header: `{ 'Authorization':'Bearer <TOKEN>' }`

#### Response

Response result different for different user.

```json
[
  {
    "id": 15,
    "income": 250001,
    "status": "NEW",
    "tax_amount": 30000.12,
    "tax_accountant": "tax-accountant-2",
    "tax_payer": "tax-payer-1",
    "created_at": "2021-08-10T20:57:24.662578+05:30",
    "updated_at": "2021-08-10T23:00:05.529047+05:30",
    "deadline": "2021-07-21T21:03:39+05:30",
    "fines": 0,
    "total_amount": 30000,
    "payment_status": false,
    "payment_date": null
  },
  {
    "id": 14,
    "income": 56000,
    "status": "NEW",
    "tax_amount": 0,
    "tax_accountant": "tax-accountant-1",
    "tax_payer": "",
    "created_at": "2021-08-09T23:04:51.759259+05:30",
    "updated_at": "2021-08-10T23:00:52.665686+05:30",
    "deadline": null,
    "fines": 0,
    "total_amount": 0,
    "payment_status": false,
    "payment_date": null
  }
]
```

#### Preview

![image](https://i.imgur.com/9bO01Lq.png)

### To edit tax

#### Request

`PUT <BASE_URL>/edit/<int:id>`
<br />
Header: `{ 'Authorization':'Bearer <TOKEN>' }`
<br />
Body: `{ "income": 60000, "deadline": "2022/10/12", "status":"delayed", "tax_payer": "tax_payer_1" }`

#### Response

Only tax-accountant type use can edit

```json
{
  "id": 17,
  "income": 60000,
  "status": "DELAYED",
  "tax_amount": 0,
  "tax_accountant": "tax_accountant_1",
  "tax_payer": "tax_payer_1",
  "created_at": "2021-08-10T22:40:10.879332+05:30",
  "updated_at": "2021-08-10T22:40:11.043337+05:30",
  "deadline": "2021-08-20T00:00:00+05:30",
  "fines": 0,
  "total_amount": 0,
  "payment_status": false,
  "payment_date": null
}
```

#### Preview

![image](https://i.imgur.com/fj4qjm8.png)

### To list of tax history

#### Request

`GET <BASE_URL>/list/<int:id>/history/`
<br />
Header: `{ 'Authorization':'Bearer <TOKEN>' }`

#### Response

admin and tax-accountant type use can edit

```json
{
  "history": [
    {
      "id": 14,
      "income": 56000,
      "status": "NEW",
      "tax_amount": 0,
      "created_at": "2021-08-09T17:34:51.759259Z",
      "updated_at": "2021-08-10T17:30:52.665686Z",
      "deadline": null,
      "fines": 0,
      "total_amount": 0,
      "payment_status": false,
      "payment_date": null,
      "tax_accountant_id": "e91bad56-c4b9-42ce-ae68-c645e6b166a9",
      "tax_payer_id": null,
      "history_id": 82,
      "history_date": "2021-08-10T17:30:52.666224Z",
      "history_change_reason": null,
      "history_type": "~",
      "history_user_id": "62258e3f-0efc-47bd-98e1-85250c1eefb9"
    },
    {
      "id": 14,
      "income": 56000,
      "status": "NEW",
      "tax_amount": 0,
      "created_at": "2021-08-09T17:34:51.759259Z",
      "updated_at": "2021-08-10T17:03:49.481736Z",
      "deadline": null,
      "fines": 0,
      "total_amount": 0,
      "payment_status": false,
      "payment_date": null,
      "tax_accountant_id": "e91bad56-c4b9-42ce-ae68-c645e6b166a9",
      "tax_payer_id": "2a370b8e-2c92-4519-ad55-14ef070b12cf",
      "history_id": 75,
      "history_date": "2021-08-10T17:03:49.482729Z",
      "history_change_reason": null,
      "history_type": "~",
      "history_user_id": "62258e3f-0efc-47bd-98e1-85250c1eefb9"
    }
  ]
}
```

#### Preview

![image](https://i.imgur.com/VqZhIl4.png)

### To payment for tax

#### Request

`GET <BASE_URL>/payment/<int:id>/`
<br />
Header: `{ 'Authorization':'Bearer <TOKEN>' }`
<br />
Body: `{'payment':'1000'}`

#### Response

Only tax-payer user type allowed

#### Preview

![image](https://i.imgur.com/ZmeWVrT.png)
