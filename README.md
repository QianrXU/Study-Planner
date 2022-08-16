# Study Planner (Team 1)
This is the main repository and project planning page of Study Planner Team 1 (part of CITS5206 Professional Computing).

___

## Project planning (deliverable 1a)
### 1. Client Communication and Demonstration
+ **MVP planning**. The team took in what was said during the MVP presentation on 4 August and considered how to best go about MVP planning in the 'MVP planning' document. This doucment contains more formalised requirements, user journeys, opportunity statements and a prioritisation matrix. https://uniwa.sharepoint.com/:w:/r/teams/CITS5206SEM-22022-StudyPlannerTeam1/Shared%20Documents/Study%20Planner%20Team%201/MVP/MVP%20planning.docx?d=w77b2ab7466f84854a14c85d20c6dc65e&csf=1&web=1&e=WVYF5x 
+ **MVP presentation**. The MVP presentation was organised/structured according to the following topics: 1) Identified needs, 2) User journey, 3) Mockup, and 4) Opportunities (where opportunities detailed some of the extended functionality we wish to cover should we have time). When presenting the MVP to the client, the team used the following PowerPoint slides: https://uniwa.sharepoint.com/:p:/r/teams/CITS5206SEM-22022-StudyPlannerTeam1/Shared%20Documents/Study%20Planner%20Team%201/MVP/MVP%20Presentation.pptx?d=w8d8102e6e9b8406c8bc81da4faef5668&csf=1&web=1&e=6FOvfF.
+ **Mockup**. When we got to slide 4 of the MVP presentation (link above), we presented a user journey where a postgraduate student wanted to save a study plan to their user account. We saw this user journey as containing much of the functionality and requirements that we had elicited from conversations with the client. To visualise the MVP we used the software Figma. 
  + Find the prototype used in the MVP presentation on the following link (select Flow 2 in the left hand pane): https://www.figma.com/proto/X27Fqy4XdmQcQKOI7XOE3j/Study-Planner-Prototype?page-id=0%3A1&node-id=87%3A2774&viewport=271%2C252%2C0.07&scaling=scale-down&starting-point-node-id=87%3A2774&show-proto-sidebar=1
  + We have used Figma to make diagrams of the architecture, the database structure, as well as some extended functionality too. Please view this link for the full : https://www.figma.com/file/X27Fqy4XdmQcQKOI7XOE3j/Study-Planner-Prototype?node-id=0%3A1

### 2. Risk and Technology Assessments
The risk assessments, including a risk assessment matrix, performed by the team in terms of skills, resources and technology have been considered in the 'Working document'. Please find the link for the 'Working document' under '4. Other' below. 

### 3. Project Management and Plans
Project management is spread out across multiple spots. The team will normally type out responsibilities we have agreed on during meetings in the agenda/meeting notes, this then gets gets broken up into "work chunks" that are added to the team's Github project planning area. Additionally, the team utilises a GANTT chart to visualise the timeline and important dates/deadlines we have to consider.
+ **GitHub project planning page**. On the following link, the team will be splitting up smaller chunks of work and allocating them to their assigned team member. Here we will be able to follow the progress of each other's work, either in a table or as a Kanban board. https://github.com/users/QianrXU/projects/1
+ **GitHub repository**. The team have decided we will all create our separate branches and that we will talk to each other before merging with the main branch. The following link contains our project's repository. https://github.com/QianrXU/Study-Planner
+ **Project timeline**. The team felt the need to create a timeline where we could enter important dates and sprints in a visual way. https://uniwa.sharepoint.com/:x:/r/teams/CITS5206SEM-22022-StudyPlannerTeam1/Shared%20Documents/Study%20Planner%20Team%201/Study_Planner_Timeline%20(GANTT%20chart).xlsx?d=w2c73dcbc733846fea6abec1d7c534c20&csf=1&web=1&e=MAc9jP

### 4. Other
The following two documents cover a little bit from all three points above. 
+ **Working document**. In the file called 'Working document' on SharePoint the team has kept all agendas and notes from meetings with the clients as well as for internal team meetings. https://uniwa.sharepoint.com/:w:/r/teams/CITS5206SEM-22022-StudyPlannerTeam1/Shared%20Documents/Study%20Planner%20Team%201/Working%20document.docx?d=wf5ff12af43e04210a082c5898790e510&csf=1&web=1&e=Z4mlaV
+ **Requirements**. In addition to the agenda notes, the team have summarised requirements in an Excel file that can be reached on the following link (also on the team's SharePoint channel): https://uniwa.sharepoint.com/:x:/r/teams/CITS5206SEM-22022-StudyPlannerTeam1/Shared%20Documents/Study%20Planner%20Team%201/Requirements.xlsx?d=w45b8ff9bbd3040dcb452f1f2b446fd69&csf=1&web=1&e=i3T6C0

___

## How to run the project
1. Create a virtual environment: `$ python3 -m venv venv`
2. Activate the python virtual environment: `$ source venv/bin/activate`
3. Please see prerequisites below.
4. To run the app: `$ flask run` - This should start the app running on localhost at port 5000, i.e.  http://localhost:5000/index
5. To stop the app: `$ ^C`
6. To exit the environment: `$ deactivate`

## Prerequisites
Requires python3, flask, venv.
Use `$ pip3 install -r requirements.txt` to install the environment required.

### Installing the prerequisites
**Installing venv**
* Set up a virtual environment:
  - use pip or another package manager to install virtualenv package: `$ sudo apt-get install python3-venv`
  - start the provided virtual environment: `$ source venv/bin/activate`

## Deployment
Deployment on localhost at port 5000.