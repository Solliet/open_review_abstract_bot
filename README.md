# open_review_abstract_bot
OpenReview Abstract extractor for reddit

## Installation


### Pip (recommended)

1. Download and install
    ```bash
    $ pip install open_review_abstract_bot
    ```

### From Source

Requirements:

1. python 3.7
2. [poetry](https://python-poetry.org/)

Steps:

1. Clone repository
    ```bash
    $ git clone git@github.com:Solliet/open_review_abstract_bot.git
    ```
2. Build
    ```bash
    $ cd open_review_abstract_bot && poetry build
    ```
3. Install 
    ```bash
    $ pip install --upgrade dist/open_review_abstract_bot-*-py3-none-any.whl
    ```

## Running

    $ openreviewbot conf.toml

### Config example

    username = "OR_abstract_bot"
    password = "************"
    subreddit = "mysubreddit"
    client_id = "************"
    client_secret = "*************"

