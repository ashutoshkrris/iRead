<h1 align="center">
Contribution Guidlines
</h1>

We want contributing to iRead Blog Project to be fun, enjoyable, and educational for anyone and everyone. All contributions are welcome, including issues, new docs as well as updates, and more.

Please note we have a [code of conduct](https://github.com/ashutoshkrris/iRead/blob/master/CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

Before you begin:
- Check out the [existing issues](https://github.com/ashutoshkris/iRead/issues).

## Don't see your issue? Open one

If you spot something new, open an issue using a [template](https://github.com/ashutoshkris/iRead/issues/new/choose). We'll use the issue to have a conversation about the problem you want to fix.

## How to Open a Pull Request

A big part of contributing to open source is submitting changes to a project: improvements to source code or tests, updates to docs content, even typos or broken links. This doc will cover what you need to know to **open a pull request**.

In case you aren’t familiar, here’s how the folks at GitHub [define a pull request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/about-pull-requests):

> *Pull requests let you tell others about changes you've pushed to a branch in a repository on GitHub. Once a pull request is opened, you can discuss and review the potential changes with collaborators and add follow-up commits before your changes are merged into the base branch.*

iRead Blog Project uses the PR process to review and test changes before they’re added to Project's GitHub repository. Anyone can open a pull request. The same process is used for all contributors, whether this is your first open source contribution or you’re a core member of the iRead Blog Project Team.

When someone wants to contribute to any repo, they open a request to pull their code into the repo.

### Opening PRs in iRead Blog Project

For any kind of change to files in our repo, you can follow the below steps. Be sure to check out additional tips for contributing to various parts of the repo later in this doc, such as docs changes, starters, or code improvements and tests.

* [Fork and clone the repo](#fork-clone-and-branch-the-repository).
* Run `pub get` to pull in all the dependencies.
* Make your changes to the project.
* [Create a branch in Git](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging) to isolate your changes:
	```
	git checkout -b <branch-name>
	```
* Once you have changes in Git you want to push, add them and create a commit.
	* Using a dot character . will add all untracked files in the current directory and subdirectories.
		```
		git add .
		```
	* Add any specific file using the command :
		```
		git add <file-name>
		```
* Commit your changes using the command :
	```
	git commit -m "your message here"
	```
* Push your changes to your fork, assuming it is set up as origin:
	```
	git push origin head
	```

### Update your fork with the latest original repo changes

Our repo is very active, so it’s likely you’ll need to update your fork with the latest changes to be able to merge in your code. This requires adding original repo as an upstream remote:

* Set our repo URL as a remote source. The name of the remote is arbitrary; this example uses upstream.
	```
	git remote add upstream <original-repo-url>
	```
* Fetch the latest changes from our repo:
	```
	git fetch upstream master
	```
* In the branch you want to update, merge any changes from our repo into your fork:
	```
	git merge upstream/master
	```
* Once your branch is in good working order, push the changes to your fork:
	```
	git push origin head
	```

## Fork, clone, and branch the repository

* Fork the official [iRead Blog Project](https://github.com/ashutoshkrris/iRead) repository.
* Clone the fork:
	```
	git clone https://github.com/ashutoshkrris/iRead.git
	```
* Set up repo and install dependencies.
* Create your branch : `git checkout -b <branch-name>`

<br>
<h5 align="center">
< Happy Contributing />
<br>
<a href="https://ashutoshkrris.tk">Ashutosh Krishna</a> | © 2021
</h5>