## Instructions for how to install and configure application

> Note : If you run the code below and find ***python : command not found***, change **python** to **python3**.

1. Clone repository from GitHub to your computer.
    ```
    git clone https://github.com/Pong50887/ku-polls.git
    ```
2. Change directory to ku-polls.
    ```
    cd  ku-polls
    ```
3. Create virtual environment.
    ```
   python -m venv venv
   ```
4. Start the virtual environment.
   * macOS / Linux
     ```
     . venv/bin/activate 
     ```
   * Windows
     ```
     venv\Scripts\activate
     ```
5. Install dependencies.
   ```
   pip install -r requirements.txt
   ```
   > Note : If you can't use **pip**, change it to **pip3**.
   
6. Migrate the Database
    ```
    python manage.py migrate
    ```

7. Load polls and users data
    ```
    python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
    ```

8. Create `.env` file
    ```
    cp sample.env .env
    ```

9. In `.env` file, set `DEBUG` to `True`
    ```
    DEBUG = True
    ```
   
