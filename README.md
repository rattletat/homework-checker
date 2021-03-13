# Homework Checker
An easy way to organize programming lectures.

## Features
- Easy set up using Docker Compose
- Secure execution and automated testing of homework code
    - Currently supported: Python, R
    - Easily extendible
- Code execution feedback for debugging purposes
- Optional grading status
- Structuring of lectures into lessons and exercises
- Multiple parallel lectures supported
- Addable lecture and lessons file attachments

* TODO
    + Two different user models (Student/ Extern) vs. 1 User with two roles 
    + Change project structure (new docker folder with Dockerfiles, nginx config)
    + better secret management using python-decuple    
    + Improved Dashboard (change info, deregister)
    + Improved Lecture Sign-up (using a code)
    + Statistics
    + Messages
    + Quizzes
    + Improved Error Output
    + Cleaner runner system
    + Shibboleth Support
    + Improved security 
        + docker settings
        + backup system
    + Ability to link images stored in static files
