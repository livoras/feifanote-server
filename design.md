## Database design
* user:
    - id
    - email
    - username
    - password
    - active_notebook_id

* notebook:
    - id
    - name
    - index
    - user_id
    - active_page_id

* pages:    
    - id
    - index
    - content
    - notebook_id

## APIs design

* user
    - signup
        + POST /users
        + {email, username, password}
        + results:
            * created: 
                - 201 {email, username, password}
            * email conflicts: 
                - 409 {message: "Email has already existed."}
            * username conflicts: 
                - 409 {message: "Username has already existed."} 
            * request data not acceptable: 
                - 400 {message: "Email/Username/Passowrd is not correct."}
    - login
        + POST /user/me
        + {email, password}
        + results:
            * ok:
                - 200 {email, username}
            * email is not correct
                - 404 {message: "User is not found."}
            * password is not correct
                - 401 {message: "Password is not correct."}
    - logout
        + DELETE /user/me
        + results:
            * ok:
                - 200 {message: "OK."}
            * not login:
                - 401 {message: "You have to login first."}
* notebook
    - create a notebook
        + POST /notebooks
        + {name, index}
        + results:
            * not login: ..
            * name should be not empty and its length should less than 30:
                - 400 {message: "Name is not valid."}
            * name has existed:
                - 409 {message: "Name has already existed."}
    - delete a notebook
        + DELETE /notebooks/<notebook_id>
        + none
        + results:
            * not login: ..
            * notebook is not found: 
                - 404 {message: "Notebook is not found."}
    - modify a notebook's name
        + PATCH /notebooks/<notebook_id>?field=name
        + {name}
        + results:
            * not login: ..
            * notebook is not found: 
                - 404 {message: "Notebook is not found."}
            * ok:
                - 200 {message: "OK."}
            * name is not valid(0 < name.length <= 30):
                - 400 {message: "Name is not valid."}
            * name conflicts:
                - 409 {message: "Name has already existed."}
    - modify a notebook's position
        + PATCH /notebooks/<notebook_id>?field=index
        + {index}
        + results:
            * not login: ..
            * notebook is not found:
                - 404 {message: "Notebook is not found."}
            * ok:
                - 200 {message: "OK."}
    - retrieve all notebooks' information
    - retrieve a specific notebook's information
    - change active notebook
* page
    - create a page
    - delete a page
    - save content of a page
    - modify a page's position
    - modify a page's belonging notebook
    - retrieve a specific page's information
    - change active page