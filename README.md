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
    + better secret management using python-decuple    
    + Improved Dashboard (change info, deregister)
    + Statistics
    + Messages
    + Quizzes
    + Improved Error Output
    + Cleaner runner system
    + Shibboleth Support
    + Backup system
    + Ability to link images stored in static files
    + Update scores using a Exercise-Student model and post_save hooks on Submissions
    + Add 1-to-Many relationship to Lectures that limit objects seen in Admin panel
    + Fix permissions for ListViews
    + Fix overwriting issue with two lesson resources with same name
