# Travel Planner API

## Overview

Travel Planner API is a RESTful backend application built with **FastAPI** and **SQLAlchemy**.

The application allows users to create travel projects, add places to visit, attach notes, mark places as visited, and automatically complete a project when all places have been visited.

This project was developed as a backend assessment and demonstrates REST API development, database design, third-party API integration, and business logic implementation.

---

## Features

### Projects

* Create a travel project
* Update project information
* Delete a project
* Get a project by ID
* Get a list of projects

### Places

* Add a place to an existing project
* List all places in a project
* Get a single place
* Update notes
* Mark a place as visited

### Business Rules

* Maximum **10 places** per project
* Duplicate places are not allowed
* A project cannot be deleted if it contains visited places
* A project is automatically marked as **completed** when all places are visited

### Third-party API

The application validates every place using the **Art Institute of Chicago API** before saving it.

---

## Tech Stack

* Python 3.14
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn
* Requests

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/travel-planner.git
```

Go to the project

```bash
cd travel-planner
```

Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```
