[![Django Runtest](https://github.com/Pong50887/ku-polls/actions/workflows/python-unittest.yml/badge.svg)](https://github.com/Pong50887/ku-polls/actions/workflows/python-unittest.yml)

## KU Polls: Online Survey Questions 

An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/4.1/intro/tutorial01/), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

## Installation

Read how to install and configure application from [Installation.md](Installation.md).

## Running the Application

1. Activate the virtual environment.
   * macOS / Linux
     ```
     . venv/bin/activate 
     ```
   * Windows
     ```
     venv\Scripts\activate
     ```
2. Starting development server.
    ```
    python manage.py runserver
    ```
    > Note : If you can't use **python**, change it to **python3**.
3. To use the application, open the browser and access http://localhost:8000.
4. To close the application, quit the server with CONTROL-C.
5. Deactivate the virtual environment.
   ```
    deactivate
    ```
## Demo Users
| Username | Password |
|-------|----------|
| demo1 | hackme11 |
| demo2 | hackme22 |
| demo3 | hackme33 |

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision-and-Scope)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project-Plan)
- [Domain Model](../../wiki/Domain-Model)
- [Iteration 1](../../wiki/Iteration-1-Plan)
- [Iteration 2](../../wiki/Iteration-2-Plan)
- [Iteration 3](../../wiki/Iteration-3-Plan)
