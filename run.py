#just to run the website 
from market import app

#Checks if run.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True)
