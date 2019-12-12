開發環境設定
===

## Python

我們用 Python 3.7。

```sh
$ python -V   # check Python version
```

如果你的系統沒有 Python 3.7，有幾個辦法可以安裝：

* macOS 的話，用 Homebrew 安裝：`brew install python@3`
* 用 conda 的 Python 3.7
* 用 [pyenv](https://github.com/pyenv/pyenv) 安裝：先安裝[這份文件](https://github.com/pyenv/pyenv/wiki/Common-build-problems)裡的 Prerequisites，再來執行 [pyenv-installer](https://github.com/pyenv/pyenv-installer)
  ```sh
  $ curl https://pyenv.run | bash
  # restart shell
  $ pyenv install 3.7.0
  $ pyenv global 3.7.3
  ```

## Git

```sh
$ git clone git@github.com:disinfoRG/NewsScraping.git
$ cd NewsScraping
```

## Pipenv

我們用 [Pipenv](https://pipenv.readthedocs.io/en/latest/)。

```sh
$ pip install pipenv    # or "pip3 install pipenv" depending on your Python
$ pipenv install --dev
$ pipenv shell          # enter virtualenv
$ pipenv install myawesomethings  # add new dependencies
```

要離開 virtualenv 的話，按 `ctrl-d`。

修改過 `Pipfile` 與 `Pipfile.lock` 的話，都要 commit 到 git repo 裡。

## MySQL

我們用 MySQL 5.7。如果你的系統裡沒有 MySQL，有幾個辦法可以安裝：

* macOS 的話，用 Homebrew 安裝：`brew install mysql`，然後每次開發時啟動服務：`mysql.server start`
* 有 Docker 的話，另開一個 shell 用 MySQL docker image：`docker run --name newsscraping -e 'MYSQL_ROOT_PASSWORD=mysecret' -p 3306:3306 -p 33060:33060 -d mysql:latest`，然後每次開發時啟動container：`docker start -a newsscraping`

開一個 database：

```sh
$ mysql -u root -p -e 'CREATE DATABASE NewsScraping CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'
```

設定 database connection：

```sh
$ cd NewsScraping
$ echo DB_URL=mysql+pymysql://root:mysecret@127.0.0.1/NewsScraping > .env
```

## Alembic

我們用 [Alembic](https://alembic.sqlalchemy.org/) 管理 database schema。Alembic 在 "Pipenv" 那一段已經裝好了。

```sh
$ pipenv shell          # if you are not in project virtualenv
# make sure the DB_URL in .env is correct
$ alembic upgrade head
```

## black

我們用 [black](https://black.readthedocs.io/en/stable/) 排版 Python 程式碼。我們用 [pre-commit](https://pre-commit.com/) 在下 git commit 指令的時候自動重排修改過的那部份程式碼。black 跟 pre-commit 在 "Pipenv" 那一段已經裝好了。

手動重排所有 Python 程式碼：

```sh
$ pipenv shell          # if you are not in project virtualenv
$ black .
```

以後在 git commit 時都自動重排修改過的那部份程式碼：

```sh
$ pipenv shell          # if you are not in project virtualenv
$ pre-commit install    # only need to do this once
```

## Github flow

我們用 [Github flow](https://guides.github.com/introduction/flow/) 分工：

* 每個功能都開一個新的 branch 開發，完成以後才會 merge 回 master。
* master branch 總是可以直接 deploy 使用。
* 對於重要的開發 branch，開一個 pull request 討論細節，並且拉人 review。
* merge 回 master 以後，儘快 deploy 到 middle2（沒有 release master，每個人都可以做）。
