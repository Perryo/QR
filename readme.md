## QR.io - A proof of concept app for process Paypal and Stripe payments from QR codes.
![Preview](/resources/qr-code-preview.png)


## [Read about the concept](https://docs.google.com/presentation/d/1jcgRLmKWfdXqevXLpTVdEw5ZXjX_mKXW0xb6DaJSWRg/edit?usp=sharing)

Features:
- Stripe integration including ApplePay
- Paypal integration
- Gathers analytics and customer reviews
- Prototyped on Django to provide database access to editing outstanding payments and creating new orders.
- Credential management with git-secret


## How to use:
0) Highly suggested to be familiar with [Django](https://docs.djangoproject.com/en/3.1/), especially how settings, models, and urls function.
1) Setup [git-secret](https://git-secret.io/)
2) Get credentials for Stripe and Paypal:
  - [Stripe](https://stripe.com/docs)
  - [Paypal](https://developer.paypal.com/docs/checkout/)
3) Create a credentials.json in the resources folder, the default structure for this project is as follows:
  ```
  {
    "secret": "", // This is the csrf key django uses
    "db_engine": "django.db.backends.mysql", // Use whatever engine your database instance will be
    "db_name": "",
    "db_user": "",
    "db_password": "",
    "db_host": "",
    "db_port": "",
    "stripe": {
      "api_key": "" //API Key for Stripe
    },
    "paypal": {
      "client_id": "",  // Credentials for Paypal
      "client_secret": ""
    }
  }
  ```
4) Locally, it is acceptable to use the sqlite3 database. This is used when the `setting.py` config is used for environment setup. For deployment see `settings_server.py`.
5) Start server with Django's `runserver` command.
