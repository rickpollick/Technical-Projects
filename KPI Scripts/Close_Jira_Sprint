import csv
import requests
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
import os  # Import the os module

# Jira credentials and setup
jira_url = ''
api_token = ''  # Ensure you provide your API token
username = ''  # Make sure this matches your username
board_id = ''
auth = HTTPBasicAuth(username, api_token)

def get_active_sprints(board_id):
    """Return the active sprints of a given board."""
    url = f"{jira_url}/rest/agile/1.0/board/{board_id}/sprint"
    response = requests.get(url, auth=auth, params={'state': 'active'}, verify=False)  # Added verify=False
    response.raise_for_status()
    return response.json().get('values', [])

def get_issues_for_sprint(sprint_id):
    """Retrieve issues for the given sprint."""
    url = f"{jira_url}/rest/agile/1.0/sprint/{sprint_id}/issue"
    response = requests.get(url, auth=auth, params={'fields': 'status,summary'}, verify=False)
    response.raise_for_status()
    return response.json().get('issues', [])

def get_future_sprint(board_id):
    """Get the future sprint to move the issues to."""
    url = f"{jira_url}/rest/agile/1.0/board/{board_id}/sprint"
    response = requests.get(url, auth=auth, params={'state': 'future'}, verify=False)
    response.raise_for_status()
    sprints = response.json().get('values', [])
    if not sprints:
        raise ValueError("No future sprints found.")
    return sprints[0]['id']  # Assuming you want to move issues to the first future sprint

def move_issues_to_sprint(issues, sprint_id):
    """Move specified issues to the given sprint."""
    url = f"{jira_url}/rest/agile/1.0/sprint/{sprint_id}/issue"
    data = {'issues': [issue['id'] for issue in issues]}
    response = requests.post(url, json=data, auth=auth, verify=False)
    response.raise_for_status()

def close_sprint(sprint_id):
    """Close the given sprint."""
    url = f"{jira_url}/rest/agile/1.0/sprint/{sprint_id}"
    data = {
        'state': 'closed'
    }
    response = requests.post(url, json=data, auth=auth, verify=False)  # Added verify=False
    response.raise_for_status()

def close_and_move_issues(board_id, sprint_id=None):
    """Close the specified or active sprint and move unfinished issues to the next sprint."""
    if sprint_id is None:
        sprint_id = get_active_sprints(board_id)[0]['id']
    close_sprint(sprint_id)  # Corrected to use the close_sprint function
    issues = get_issues_for_sprint(sprint_id)
    unfinished_issues = [issue for issue in issues if issue['fields']['status']['name'] != 'Done']
    
    if unfinished_issues:
        future_sprint_id = get_future_sprint(board_id)
        move_issues_to_sprint(unfinished_issues, future_sprint_id)
        print(f"Moved {len(unfinished_issues)} unfinished issue(s) to sprint ID {future_sprint_id}.")
    else:
        print("No unfinished issues to move.")

if __name__ == "__main__":
    # To close the current active sprint, just call close_and_move_issues with the board ID
    close_and_move_issues(board_id='')
