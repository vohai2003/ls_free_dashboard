# DISCLAIMER
This is a small script, originally written for a small project of my own. It's extremely buggy and not really work well. It, at least, does it job. 
As the nature of our project is image classification, this script is designed for image classification, and **may/may not** work with other type of tasks.
If you want a dashboard for your small project with your team, this is **maybe** a good choice for you.
# LSDashboard
This is a dashboard for Label Studio Free, allowing you to check for your team progress even on Free plan of Label Studio. It utilizes the Label Studio API and providing basic insights about your team progress (How many percent of your dataset is labeled, how many instances exist in your dataset so far, etc.). Not much info, but should be enough for your need.
## Installation and Run
### Cloning repository:
`Waiting for repo link`
### Installing dependency:
`pip install -r requirements.txt`
Please note that I assume that you've already installed `label-studio`, so it's not included in `requirements.txt`
### Configuring secret value
Create a file `secret.json` on the same directory with `label_studio_dashboard.py`. The content of that file:
`{"project_id": <your project id>, "api_key": <api key>}`
### Running dashboard
`python label_studio_dashboard.py`
# Known Issue
There're some known issues:
- "Overlapped" may not correctly show the number of tasks with more than 1 annotation.