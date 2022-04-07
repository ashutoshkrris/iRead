<p align="center">
    <a href="https://ireadblog.com">
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

- Authentication and Authorization with OTP Verification
- Social Login with Google OAuth2
- CRUD on User's Profile
- CRUD on Blog Posts
- Rich Text Editor(using CKEditor) with Media Files Storage(using Cloudinary)
- Search Blogs
- Categories and Tags Filters
- Create Series of Blogs
- Like/Dislike/Comment/Reply/Share on Blog Posts
- Follow/Unfollow Users
- Show Notifications on Follow, Like and Comment
- Twitter Bot to tweet about posts published on website as well as retweet and like user's post (if they share it on Twitter)
- Digests(Newsletter) Subscription/Unsubscription
- Public API and RSS Feed Support

## Technology Stack

**Frontend:** HTML, CSS(+ Bootstrap 4), JavaScript  
**Backend:** Python/Django  
**Database:** PostgreSQL

And additional requirements are in [**requirements.txt**](https://github.com/ashutoshkrris/iRead/blob/master/requirements.txt) or [**Pipfile**](https://github.com/ashutoshkrris/iRead/blob/master/Pipfile).

## Latest Posts

<!-- BLOG-POST-LIST:START -->
- [Introduction to Data Structures and Algorithms](http://ireadblog.com/posts/162/introduction-to-data-structures-and-algorithms)
- [How to unpack Python list or tuple the better way?](http://ireadblog.com/posts/161/how-to-unpack-python-list-or-tuple-the-better-way)
- [Python Rich is getting richer](http://ireadblog.com/posts/160/python-rich-is-getting-richer)
- [Getting Started With PysonDB](http://ireadblog.com/posts/159/getting-started-with-pysondb)
- [bool&lpar;&rpar; function in Python](http://ireadblog.com/posts/158/bool-function-in-python)
<!-- BLOG-POST-LIST:END -->

## API Documentation

- Base URL: `https://ireadblog.com/api/v1`
- `pk` refers to the Post ID.
- Base URL for `thumbnail` is: `https://res.cloudinary.com/dlomjljb6/image/upload/v1/`
- Post URL can be built as: `https://ireadblog.com/posts/<post_id>/<post_slug>`

#### Endpoints

- Endpoint for all posts: `/posts`

  - Accepts GET Request
  - Returns JSON Response as:
    ```json
    [
      {
        "model": "core.post",
        "pk": 92,
        "fields": {
          "title": "Your title here",
          "seo_overview": "Your post overview here",
          "slug": "post-slug-here",
          "content": "Your post content here",
          "timestamp": "2022-02-22T02:43:40.770Z",
          "author": "Ashutosh Krishna",
          "thumbnail": "media/blog/thumbnails/R_xjlzdd",
          "categories": "CategoryName",
          "tags": ["tag1", "tag2"]
        }
      }
    ]
    ```
  - To limit the number of posts, use `?limit=x` in the URL. <br> e.g. `https://ireadblog.com/api/v1/posts?limit=3` returns the latest 3 posts on iRead.

- Endpoint for posts for specific category: `/posts?category=<category-slug>`
  - Accepts GET Request
  - Replace `<category-slug>` with correct category slug
  -  Category Slug can be found on any category page. For example, when you visit the **Web Development** category page, the URL of the page is: `https://ireadblog.com/categories/web-development`. So the `<category-slug>` is `web-development`. 
  - JSON response looks same as above.
  - To limit the number of posts for a category, use `?category=<category-slug>&limit=x` in the URL. <br> e.g. `https://ireadblog.com/api/v1/posts?category=web-development&limit=3` returns the latest 3 Web Development posts on iRead.

- Endpoint for posts for specific tag: `/posts?tag=<tag-name>`
  - Accepts GET Request
  - Replace `<tag-slug>` with correct tag name
  -  Tag Name can be found on any Tag page. For example, when you visit the **DevInceptCommunity** tag page, the URL of the page is: `https://ireadblog.com/tags/DevInceptCommunity`. So the `<tag-name>` is `DevInceptCommunity`. 
  - JSON response looks same as above.
  - To limit the number of posts for a tag, use `?tag=<tag-name>&limit=x` in the URL. <br> e.g. `https://ireadblog.com/api/v1/posts?tag=DevInceptCommunity&limit=3` returns the latest 3 posts on iRead with the tag #DevInceptCommunity.

- Endpoint for posts for a user: `/<username>/posts`

  - Accepts GET Request
  - Replace `<username>` with your username.
  - JSON response looks same as above.
  - To limit the number of posts by user, use `?limit=x` in the URL. <br> e.g. `https://ireadblog.com/api/v1/posts?limit=3` returns the latest 3 posts by that user on iRead.

- Endpoint for a single post: `/post/<post_id>/<slug>`
  - Accepts GET request
  - Replace `<post_id>` with the Post ID and `<slug>` with the slug of the post.
  - JSON response looks same as above.

## RSS Feed

- iRead Posts RSS Feed URL: `https://ireadblog.com/feed`
- User Posts RSS Feed URL: `https://ireadblog.com/feed/<username>`
- You can also find the RSS Feed in your profile if you're logged in.

## Demo

[![Demo Video](https://img.youtube.com/vi/hbbN8ZX4EFc/0.jpg)](https://youtu.be/hbbN8ZX4EFc)

## Bulletin Email

<img src="https://i.imgur.com/KcsuXsw.jpg" alt="Bulletin email" height=1000>

## Contributing

### Setting-up the project

- Fork the Repository.
- Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/iRead.git`
- Change directory to iRead `$ cd iRead`
- Add a reference to the original repository  
  `$ git remote add upstream https://github.com/ashutoshkrris/iRead.git`
- Install venv `$ pip3 install venv`
- Create a virtual environment `$ python -m venv env`
- Activate the env: `$ source env/bin/activate` (for linux) `> ./env/Scripts/activate` (for Windows PowerShell)
- Install the requirements: `$ pip install -r requirements.txt`
- Create a new file in the root directory of the repository (`iRead`) with name `.env` (only `.env` and not `.env.txt`) and add the following content in it:

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
  REDIS_URL=redis://127.0.0.1:6379/1
  REVUE_API_KEY='revue-api-here'
  ```

  or, just copy the `.env.save` file from `samples` directory to the root directory (`iRead`) and rename it to `.env` (only `.env` and not `.env.txt`)

  <br>

  **Note** : You can also use _Pipenv_ for virtual enviroment. You can find few related commands [here](https://srty.me/pipenv).
  <br>

- Copy `sample-db.sqlite3` from `samples` directory to the root directory (`iRead`) and rename it to `db.sqlite3`.
- Make migrations `$ python manage.py makemigrations`
- Migrate the changes to the database `$ python manage.py migrate`
- Create admin `$ python manage.py createsuperuser`
- Run the server `$ python manage.py runserver`

#### 💡️ **Pro Tip:**

- Always keep your master branch in sync with the main repository (by running `$ git pull upstream master` on your local master branch).
- Always create a new branch before making any changes (`$ git checkout -b <new-branch-name>`), never ever make any changes directly on the master branch.

## 💥 How to Contribute ?

- If you wish to contribute kindly check the [CONTRIBUTING.md](https://github.com/ashutoshkrris/iRead/blob/master/CONTRIBUTING.md)🤝
- If you are completely new to Open Source, read the [Instructions](https://github.com/ashutoshkrris/iRead/blob/master/INSTRUCTIONS.md).
- Please follow the [CODE OF CONDUCT](https://github.com/ashutoshkrris/iRead/blob/master/CODE_OF_CONDUCT.md)

## 💥 Our Valuable Contributors.

<a href="https://github.com/ashutoshkrris/iRead/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ashutoshkrris/iRead" />
</a>
