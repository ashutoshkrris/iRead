<p align="center">
    <a href="https://iread.ga">
        <img src="https://github.com/ashutoshkrris/iRead/blob/master/static/images/favicon.png" width="20%">
    </a>
</p>

<h1 align="center"> 
    iRead | Where Dynamic Ideas Find You
</h1>
<div align="center">
  
<a href="https://github.com/ashutoshkrris/iRead"><img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103"></a>
<a href="https://github.com/ashutoshkrris/iRead"><img src="https://img.shields.io/badge/Built%20by-developers%20%3C%2F%3E-0059b3"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Made%20with-Python-brightgreen.svg"></a>

<a href="https://github.com/ashutoshkrris/iRead"><img src="https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=yellow"></a>
<a href="https://github.com/vigneshshettyin/"><img src="https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg?v=103"></a>
<a href="https://github.com/ashutoshkrris/iRead"><img src="https://img.shields.io/github/repo-size/ashutoshkrris/iRead.svg?label=Repo%20size&style=flat"></a>
<a href="https://github.com/ashutoshkrris/iRead"><img src="https://img.shields.io/tokei/lines/github/ashutoshkrris/iRead?color=yellow&label=Lines%20of%20Code"></a>
<a href="https://github.com/ashutoshkrris/iRead/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MPL_2.0-brightgreen.svg?v=103"></a>
<a href="https://github.com/ashutoshkrris/iRead/watchers"><img src="https://img.shields.io/github/watchers/ashutoshkrris/iRead"></a>
  
<a href="https://github.com/ashutoshkrris/iRead/graphs/contributors"><img src="https://img.shields.io/github/contributors/ashutoshkrris/iRead?color=brightgreen"></a>
<a href="https://github.com/ashutoshkrris/iRead/stargazers"><img src="https://img.shields.io/github/stars/ashutoshkrris/iRead?color=0059b3"></a>
<a href="https://github.com/ashutoshkrris/iRead/network/members"><img src="https://img.shields.io/github/forks/ashutoshkrris/iRead?color=yellow"></a>
<a href="https://github.com/ashutoshkrris/iRead/issues"><img src="https://img.shields.io/github/issues/ashutoshkrris/iRead?color=brightgreen"></a>
<a href="https://github.com/ashutoshkrris/iRead/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/ashutoshkrris/iRead?color=0059b3"></a>
<a href="https://github.com/ashutoshkrris/iRead/pulls"><img src="https://img.shields.io/github/issues-pr/ashutoshkrris/iRead?color=yellow"></a>
<a href="https://github.com/ashutoshkrris/iRead/pulls?q=is%3Apr+is%3Aclosed"><img src="https://img.shields.io/github/issues-pr-closed-raw/ashutoshkrris/iRead?color=brightgreen"></a> 
</div>
iRead is an open platform where readers find dynamic thinking, and where expert and undiscovered voices can share their writing on any topic.


## Features of iRead
 Currently we support the following features :
* Authentication and Authorization with OTP Verification
* Social Login with Google OAuth2
* CRUD on User's Profile
* CRUD on Blog Posts
* Rich Text Editor(using CKEditor) with Media Files Storage(using Cloudinary)
* Search Blogs
* Categories and Tags Filters
* Create Series of Blogs
* Like/Dislike/Comment/Reply/Share on Blog Posts
* Follow/Unfollow Users
* Show Notifications on Follow, Like and Comment
* Twitter Bot to tweet about posts published on website as well as retweet and like user's post (if they share it on Twitter)
* Bulletins(Newsletter) Subscription/Unsubscription
* Payment Integration using Paytm and Razorpay

## Technology Stack

**Frontend:** HTML, CSS(+ Bootstrap 4), JavaScript  
**Backend:** Python/Django  
**Database:** PostgreSQL  



And additional requirements are in [**requirements.txt**](https://github.com/ashutoshkrris/iRead/blob/master/requirements.txt) or [**Pipfile**](https://github.com/ashutoshkrris/iRead/blob/master/Pipfile).


## Latest Posts

<!-- BLOG-POST-LIST:START -->
- [How to Contribute to Open Source as a Beginner](http://iread.ga/posts/48/how-to-contribute-to-open-source-as-a-beginner)
- [DevIncept - Incept... Iterate... Innovate...](http://iread.ga/posts/47/devincept-incept-iterate-innovate)
- [Selection Sort](http://iread.ga/posts/46/selection-sort)
- [Bubble Sort](http://iread.ga/posts/45/bubble-sort)
- [Interview Experience || EY GDS](http://iread.ga/posts/40/interview-experience-ey-gds)
<!-- BLOG-POST-LIST:END -->

## Demo

[![Demo Video](https://i.imgur.com/n18yerL.png)](https://srty.me/iread-demo)

## Bulletin Email

<img src="https://i.imgur.com/KcsuXsw.jpg" alt="Bulletin email" height=1000>

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
    GOOGLE_OAUTH_CLIENT_ID='google-key'
    GOOGLE_OAUTH_CLIENT_SECRET='google-secret'
    TWITTER_API_KEY='twitter-api-key'
    TWITTER_API_SECRET_KEY='twitter-api-secret-key'
    TWITTER_ACCESS_TOKEN='twitter-access-token'
    TWITTER_ACCESS_TOKEN_SECRET='twitter-access-token-secret'
    PAYTM_MERCHANT_ID='paytm-merchant-id'
    PAYTM_MERCHANT_KEY='paytm-merchant-key'
    RAZORPAY_KEY_ID='rzp-key-id'
    RAZORPAY_KEY_SECRET='rzp-key-secret'
    REDIS_URL=redis://127.0.0.1:6379/1
    SHORTY_API_KEY='shorty-api-key'
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




## 💥 Our Valuable Contributors.
<a href="https://github.com/ashutoshkrris/iRead/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ashutoshkrris/iRead" />
</a>
