## Database design
user:
    email
    username
    password
    active_notebook_id

notebook:
    name
    user_id
    active_page_id

pages:    
    index
    content
    notebook_id


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
    - delete a notebook
    - modify a notebook's name
    - modify a notebook's position
    - retrieve all notebooks' information
    - retrieve a specific notebook's information
* page
    - create a page
    - delete a page
    - save content of a page
    - modify a page's position
    - modify a page's belonging notebook
    - retrieve a specific page's information