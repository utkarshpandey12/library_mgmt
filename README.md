# library_mgmt

# MVT (Model View Template Architecture Webapp)

Features/Assumptions/Design:
1. User can have either Member or Librarian Roles assigned while signup
2. Roles are fetched from backend while loggin in
3. JWT token issued when logged in and set as cookie
4. User can buy multiple books
5. Librarians can filter books by keywords using search facility
6. Librarians can update other members password
7. Librarians can assign/deassign books 
8. Librarians can add/delete book resources
9. Minimum efforts have been put for styling
10. Other Users ( Members) can add/return books and view the available ones
11. Logout feature destroys JWT tokens and fresh login is required
12. Two Tables LibraryUsers - for storing Users , Books- for storing book resources
13. User_id mapped as foreign keys for books tables

### Folder Structure
- Detail Folder Structure:

        .
        └── library_management/
            ├── .envs
            ├── core - (core app - all MVT logic lives here)/
            │   ├── urls.py
            │   ├── forms.py
            │   ├── models.py
            │   ├── tokens.py
            │   └── views.py
            │   ├── decorators.py
            │   └── admin.py     
            ├── templates/
            │   ├── all templates rendered lives here/
            ├── requirements.txt
            ├── vercel.json
            |__ .gitignore
            └── manage.py

# Local test
1. Create and active virtual environment ( $ python3 -m venv env then $ source env/bin/activate)
2. git clone
3. cd to directory where manage.py lives
4. $ python manage.py migrate
5. $ python manage.py makemigrations
6. $ pyython manage.py runserver
7. Edit databases in settings.py for local dev or use sqlite defaults. Currently the repo usees railways postgres db
8. visit http://127.0.0.1:8000/core/login/
