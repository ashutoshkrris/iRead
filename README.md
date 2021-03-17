<p align="center">
    <a href="https://iread.ga">
        <img src="static/images/favicon.png" width="20%">
    </a>
</p>

<h1 align="center"> 
    iRead | Where Dynamic Ideas Find You
</h1>

iRead is an open platform where readers find dynamic thinking, and where expert and undiscovered voices can share their writing on any topic.


## Features of iRead
 Currently we support the following features :
* Authentication and Authorization with OTP Verification
* CRUD on User's Profile
* CRUD on Blog Posts
* Rich Text Editor(using CKEditor) with Media Files Storage(using Cloudinary)
* Search Blogs
* Categories and Tags Filters
* Like/Dislike/Comment/Reply/Share on Blog Posts
* Twitter Bot to tweet about posts published on website as well as retweet and like user's post (if they share it on Twitter)
* Bulletins(Newsletter) Subscription/Unsubscription
* Payment Integration using Paytm and Razorpay

## To Do
- [ ] Integrate Google OAuth2 

## Technology Stack

**Frontend:** HTML, CSS(+ Bootstrap 4), JavaScript  
**Backend:** Python/Django  
**Database:** PostgreSQL  

And additional requirements are in [**requirements.txt**](https://github.com/ashutoshkrris/iRead/blob/master/requirements.txt) or [**Pipfile**](https://github.com/ashutoshkrris/iRead/blob/master/Pipfile).


## Contributing

### Setting-up the project

  * Fork the Repository.
  * Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/iRead.git`
  * Change directory to iRead `$ cd iRead`
  * Add a reference to the original repository  
   `$ git remote add upstream https://github.com/ashutoshkrris/iRead.git`
  * Install venv `$ pip3 install venv`
  * Create a virtual environment `$ python -m venv env`  
  * Activate the env: `$ source env/bin/activate` (for linux) `> ./env/Scripts/activate` (for Windows PowerShell)
  * Install the requirements: `$ pip install -r requirements.txt`
  * Create a new file in the root directory of the repository (`iRead`) with name `.env` (only `.env` and not `.env.txt`) and add the following content in it:
    ```
    DEBUG=True
    SECRET_KEY=ss)143p*@)jxwzge9-i26c40_9*r%p1l0&_*nlr-_*m+op#2^w
    DB_NAME=blog
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=localhost
    DB_PORT=5432
    EMAIL_HOST_USER='email@domain.com'
    EMAIL_HOST_PASSWORD='password'
    CLOUD_NAME='cloudinary-cloud-name'
    API_KEY='cloudinary-api-key'
    API_SECRET='cloudinary-api-secret'
    TWITTER_API_KEY='twitter-api-key'
    TWITTER_API_SECRET_KEY='twitter-api-secret-key'
    TWITTER_ACCESS_TOKEN='twitter-access-token'
    TWITTER_ACCESS_TOKEN_SECRET='twitter-access-token-secret'
    PAYTM_MERCHANT_ID='paytm-merchant-id'
    PAYTM_MERCHANT_KEY='paytm-merchant-key'
    RAZORPAY_KEY_ID='rzp-key-id'
    RAZORPAY_KEY_SECRET='rzp-key-secret'
    REDIS_URL=redis://127.0.0.1:6379/1
    ```  
    or, just copy the `.env.save` file from `samples` directory to the root directory (`iRead`) and rename it to `.env` (only `.env` and not `.env.txt`)  
    
    <br>
    
    **Note** : You can also use *Pipenv* for virtual enviroment. You can find few related commands [here](https://srty.me/pipenv).
    <br>

  * Copy `sample-db.sqlite3` from `samples` directory to the root directory (`iRead`) and rename it to `db.sqlite3`.
  * Make migrations `$ python manage.py makemigrations`
  * Migrate the changes to the database `$ python manage.py migrate`
  * Create admin `$ python manage.py createsuperuser`
  * Run the server `$ python manage.py runserver`
  
#### 💡️ **Pro Tip:** 
  * Always keep your master branch in sync with the main repository (by running `$ git pull upstream master` on your local master branch). 
  * Always create a new branch before making any changes (`$ git checkout -b <new-branch-name>`), never ever make any changes directly on the master branch.

 


## 💥 How to Contribute ?
- If you wish to contribute kindly check the [CONTRIBUTING.md](https://github.com/ashutoshkrris/iRead/blob/master/CONTRIBUTING.md)🤝
- If you are completely new to Open Source, read the [Instructions](https://github.com/ashutoshkrris/iRead/blob/master/INSTRUCTIONS.md).
- Please follow the [CODE OF CONDUCT](https://github.com/ashutoshkrris/iRead/blob/master/CODE_OF_CONDUCT.md)