import os

from flask import Flask, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-projects.db'
# CREATE THE EXTENSION
db = SQLAlchemy()
# INITIALISE THE APP WITH THE EXTENSION
db.init_app(app)


# CREATE TABLE
class ProjectTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    category = db.Column(db.String(250), nullable=False)
    client = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    project_description = db.Column(db.String(250), nullable=False)


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


# ADD RECORDS
def add_records_to_db():
    titles = ['Drawing Opening Application', 'Tender Design Tool', 'Maintenance Breakdown Log System', 'Process Project Log Application', 'Supplier NCR Application']
    categories = ['Desktop Application', 'Desktop Application', 'PowerApp', 'PowerApp', 'PowerApp']
    clients = ['SSPM', 'SSPM', 'SSPM', 'SSPM', 'SSPM']
    dates = ['April 2022', 'Jan 2022', 'July 2020', 'Feb 2019', 'May 2019']
    descriptions = [
        'This application allows users to open pdf internal designs on local repository network drives and online SharePoint. Additionally, it reads multiple excel workbooks for data analysis and also simplify navigating through SharePoint.',
        'This application allows mechanical designers to pull transformer data from excel and text files and populate the information on another excel file designed with VBA to generate Solidworks models for tender technical drawings.',
        'This is an internal PowerApp application designed to help all SSPM employees log Production or Office equipment breakdowns. This sends email notifications to maintenance personnel to alert them of the mechanical, electrical, plumbing, wiring, etc. issues needing attention',
        'This PowerApp application allows process engineers to track their progress on projects they are dealing with.',
        'This is an internal PowerApp application designed to help Quality Control Inspectors for incoming goods to raise Non-conformance encountered when they are recieving goods from the suppliers. It auto creates forms sent to suppliers for notifications. Forwards mails to SCM before payments can be done to rectify these issues. It also enables Quality Control Manager to analyse data for yearly management review meetings.'
    ]

    # CREATE RECORDS
    with app.app_context():
        for id_, title, category, client, date, description in zip(range(1, len(titles)+1), titles, categories, clients, dates, descriptions):
            db.session.add(ProjectTable(id=id_, title=title, category=category, client=client, date=date, project_description=description))

        db.session.commit()


# UNCOMMENT THE BELOW LINE WHEN YOU HAVE TO REFRESH THE DATABASE WITH NEW INFO
# add_records_to_db()


@app.route('/')
def home_page():
    current_year = datetime.now().year
    age = current_year - 1996
    return render_template('index.html', age=age)


@app.route('/<project_title>')
def portfolio_details(project_title):
    # GET RESULTS WHERE THE SELECTED PROJECT TITLE IS EQUAL TO THE PROJECT TITLE IN THE DB
    project = db.session.execute(db.Select(ProjectTable).filter_by(title=project_title)).scalar()
    print(project.title)
    return render_template('portfolio-details.html', selected_project=project)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
