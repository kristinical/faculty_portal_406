# Education Expeditions Faculty Portal

Author: Kristin Eberman<br>
Oregon State University – Spring 2023<br>
CS406: Independent Project

* Website: http://flip3.engr.oregonstate.edu:9875
* Note: To access this website, you must be connected to Oregon State University's VPN
* View [Login credentials](#login-credentials-for-the-purposes-of-this-project-the-following-are-valid-login-credentials) to access the site

**CODE CITATION:**<br>
Project code is guided by OSU's CS340 Flask-Starter-App<br>
URL: https://github.com/osu-cs340-ecampus/flask-starter-app

## About the Project
This 1-credit independent project worked through the planning, design, and testing phases in order to develop a web portal for faculty members planning to lead a study tour program through the study abroad organization Education Expeditions (EE)[^1]. The web portal allows faculty leaders to login and access important information about their program, as well as complete required steps and upload documents needed by EE.

[^1]: Education Expeditions is a fictional study abroad organization. The organization details described here were developed by Kristin Eberman and Alexander Giardino in CS340 during the Winter 2023 term for their Education Expeditions Database portfolio project.

## About the Organization
Education Expeditions is a study abroad organization that works with colleges and universities across the United States to help administer faculty-led study programs offered to students. EE works with over 250 universities and manages over 1,000 study tour programs each academic year. On average, each study tour has 15-30 students with 1-2 faculty leaders. Programs go to over 50 countries around the world and occur each term of the academic year, typically for 2-3 weeks.

## About the Faculty Portal
The web application developed for this project includes two types of users:
1. Program Coordinators of Education Expeditions who are able to login to an Admin Portal in order to view, track, and update information for each study tour program. The Admin Portal allows the Program Coordinator to select a particular program. Once on that program page, they can add, edit or delete tasks for the Faculty Leader(s) to complete by a particular due date, such as upload a document, fill out a form, or make a payment. Program Coordinators are also able to view information that has been submitted by the Faculty Leader(s).
2. Faculty Leaders of study tour programs are able to login to their Faculty Portal page that displays information about their program, as well as a list of all tasks they have completed, plus tasks that are still required to complete in chronological order by due date.
Note: For the purposes of this project, users can view a "Sample Program" placeholder document for completed tasks to demonstrate the portal's functionality.

## Project Web Pages
This project included the development of the following web pages:
* Login – Program Coordinators and Faculty Leaders login to their Portal from the same login page
* Homepage (Admin Portal) – Program Coordinators can select a specific program to view/edit
* Program page (Admin Portal) – Program Coordinators are able to:
    - View documents and information submitted by the Faculty Leader(s)
    - Add new tasks for the Faculty Leader(s) to complete
    - Edit existing tasks (such as task name, task type, and due date)
    - Delete existing tasks
* Faculty Portal – Faculty Leader(s) are able to:
    - View details about their program, such as program name and dates
    - View their list of tasks, including information they have already completed and items they still need to complete
    - Upload a document, fill out a form, or make a payment depending on the task type

## Project Development Steps
This project involved the following phases:
1. Project description and overview
2. Supporting application documentation – Flowcharts, IPO/TOE Charts, Pseudocode
3. [UX/UI prototype](https://www.figma.com/proto/JUGF5unh3i3ZqL2CwBl9AJ/CS406-Prototype?type=design&node-id=1-4&scaling=scale-down&page-id=0%3A1&starting-point-node-id=1%3A4)
4. Beta application / local program (Frontend)
5. Testing and debugging with sample data (Backend integration with MySQL database)

## Login Credentials: For the purposes of this project, the following are valid login credentials:
* Administrator:
    - Username: **admin**
    - Password: **adminpw**
* Faculty:
    - Valid countries are England, Ghana, Japan and Peru
    - Replace '[country]' with the country name in lowercase letters
        - Username: [country]_faculty (example: **japan_faculty**)
        - Password: [country] (example: **japan**)

Use both sets of credentials to access the two sections of the website.<br>
You can also enter invalid credentials to receive a login error.
