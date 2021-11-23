## Wiki

A Wikipedia-like online encyclopedia.

## Features

The following pages are available

* Index Page: User can click on any entry name to be taken directly to that entry page.

* Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.

* Search Page: Allows the user to type a query into the search box in the sidebar to search for an encyclopedia entry.

* New Page: Clicking “Create New Page” in the sidebar takes the user to a page where they can create a new encyclopedia entry.

* Edit Page: On each entry page, the user is able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.

* Random Page: Clicking “Random Page” in the sidebar takes user to a random encyclopedia entry.


## Installation

1. Clone repository

2. In the repository directory create a virtual environment and activate it

```bash
python3 -m venv <venv_name>
source <venv_name>/bin/activate
```
3. Install packages from requirements.txt in the virtual environment

```bash
pip install -r requirements.txt
```

## Usage
Inside wiki app directory run:

```bash
python manage.py runserver
