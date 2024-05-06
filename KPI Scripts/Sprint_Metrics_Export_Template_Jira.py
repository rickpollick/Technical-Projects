import matplotlib
matplotlib.use('Agg')  # Set the backend for matplotlib
import matplotlib.pyplot as plt
import csv
import requests
from datetime import datetime, timezone, timedelta
from requests.auth import HTTPBasicAuth
import os
import pandas as pd

# Jira credentials and setup
jira_url = ''
api_token = ''
username = ''
board_id = ''
auth = HTTPBasicAuth(username, api_token)

headers = {
   "Accept": "application/json"
}

sprint_url = f'{jira_url}/rest/agile/1.0/board/{board_id}/sprint?state=active'
sprint_response = requests.get(sprint_url, headers=headers, auth=auth, verify=False)

active_sprint_id = None
team_name = ''
team_size = 8
sprint_name = ''
sprint_start_date = ''
if sprint_response.status_code == 200:
    sprint_data = sprint_response.json()
    if sprint_data['values']:
        active_sprint_id = sprint_data['values'][0]['id']
        sprint_name = sprint_data['values'][0]['name']
        sprint_start_date = sprint_data['values'][0]['startDate']
else:
    print(f"Failed to fetch active sprint: HTTP {sprint_response.status_code}")

if not active_sprint_id or not sprint_start_date:
    print("No active sprint found for the board.")
else:
    sprint_start_date = sprint_start_date.replace('Z', '+00:00')
    sprint_start_datetime = datetime.strptime(sprint_start_date, '%Y-%m-%dT%H:%M:%S.%f%z')
    
    jql_query = f"issuetype in (Story, 'User Story', 'Development Task', Chore, Spike, 'Bug', 'UX', 'Analytics', 'Tech Exploration') AND sprint = {active_sprint_id}"
    fields = "status,customfield_10006,issuetype"
    expand = "changelog"

    search_url = f"{jira_url}/rest/api/3/search?jql={jql_query}&fields={fields}&expand={expand}"

    from requests import get
    from datetime import datetime

    COMPLETED_STATUSES = ['Done', 'Closed', 'Resolved']

    total_items = 0
    total_points = 0
    items_completed = 0
    items_not_completed = 0
    points_completed = 0
    points_not_completed = 0
    total_original_items = 0
    total_original_points = 0
    original_items_completed = 0
    original_items_not_completed = 0
    original_points_completed = 0
    original_points_not_completed = 0
    total_items_added_after_start = 0
    total_points_added_after_start = 0
    items_added_after_start_completed = 0
    items_added_after_start_not_completed = 0
    points_added_after_start_completed = 0
    points_added_after_start_not_completed = 0
    total_user_stories = 0
    total_user_stories_points = 0
    user_stories_completed = 0
    user_stories_not_completed = 0
    user_stories_points_completed = 0
    user_stories_points_not_completed = 0

    response = get(search_url, headers=headers, auth=auth)

    if response.status_code == 200:
        data = response.json()
        for issue in data.get('issues', []):
            issuetype = issue['fields']['issuetype']['name']
            status = issue['fields']['status']['name']
            points = int(issue['fields'].get('customfield_10006', 0) or 0)
            
            total_items += 1
            total_points += points
            
            sprint_field_modified_after_start = False

            for history in issue.get('changelog', {}).get('histories', []):
                change_date = datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                for item in history['items']:
                    if item['field'] == 'Sprint' and change_date > sprint_start_datetime:
                        sprint_field_modified_after_start = True
                        break

            if status in COMPLETED_STATUSES:
                items_completed += 1
                points_completed += points
            else:
                items_not_completed += 1
                points_not_completed += points

            if sprint_field_modified_after_start:
                total_items_added_after_start += 1
                total_points_added_after_start += points
                if status in COMPLETED_STATUSES:
                    items_added_after_start_completed += 1
                    points_added_after_start_completed += points
                else:
                    items_added_after_start_not_completed += 1
                    points_added_after_start_not_completed += points
            else:
                total_original_items += 1
                total_original_points += points
                if status in COMPLETED_STATUSES:
                    original_items_completed += 1
                    original_points_completed += points
                else:
                    original_items_not_completed += 1
                    original_points_not_completed += points

            if issuetype == 'User Story':
                total_user_stories += 1
                total_user_stories_points += points
                if status in COMPLETED_STATUSES:
                    user_stories_completed += 1
                    user_stories_points_completed += points
                else:
                    user_stories_not_completed += 1
                    user_stories_points_not_completed += points
    else:
        print(f"Failed to fetch issues: HTTP {response.status_code}")
        exit()

    # Average Points Calculation
    items_completed_ratio = items_completed / team_size if team_size else 0
    points_completed_ratio = points_completed / team_size if team_size else 0
    original_items_completed_ratio = original_items_completed / team_size if team_size else 0
    original_points_completed_ratio = original_points_completed / team_size if team_size else 0
    items_added_after_start_completed_ratio = items_added_after_start_completed / team_size if team_size else 0
    points_added_after_start_completed_ratio = points_added_after_start_completed / team_size if team_size else 0
    user_stories_completed_ratio = user_stories_completed / team_size if team_size else 0
    user_stories_points_completed_ratio = user_stories_points_completed / team_size if team_size else 0

    # Define the filename for the plot
    safe_team_name = team_name.replace(' ', '_').replace('/', '_')
    safe_sprint_name = sprint_name.replace(' ', '_').replace('/', '_')
    plot_filename = f'{safe_team_name}_{safe_sprint_name}_Charts.png'
    script_dir = os.path.dirname(os.path.realpath(__file__))
    plot_path = os.path.join(script_dir, plot_filename)

    data = {
        'Total Items': [total_items, items_not_completed, items_completed,],
        'Total Points': [total_points, points_not_completed, points_completed,],
        'Original Items': [total_original_items, original_items_not_completed, original_items_completed],
        'Original Points': [total_original_points, original_points_not_completed, original_points_completed],
        'Items Added After Start': [total_items_added_after_start, items_added_after_start_not_completed, items_added_after_start_completed],
        'Points Added After Start': [total_points_added_after_start, points_added_after_start_not_completed, points_added_after_start_completed],
        'User Stories Count': [total_user_stories, user_stories_not_completed, user_stories_completed],
        'User Stories Points': [total_user_stories_points, user_stories_points_completed, user_stories_points_not_completed]
    }
    colors = ['#4D104A', '#904199', '#666D70']
    labels = ['Total', 'Completed', 'Not Completed']
    x = range(len(labels))

    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    axs = axs.flatten()

    # Enhanced titles with ratio data 
    plot_titles = {
    'Total Items': f'{team_name} - {sprint_name} - Total Items by Status \n (Completed Ratio: {items_completed_ratio:.2f})',
    'Total Points': f'{team_name} - {sprint_name} - Total Points by Status \n (Completed Ratio: {points_completed_ratio:.2f})',
    'Original Items': f'{team_name} - {sprint_name} - Original Items by Status \n (Completed Ratio: {original_items_completed_ratio:.2f})',
    'Original Points': f'{team_name} - {sprint_name} - Original Issues by Status \n (Completed Ratio: {original_points_completed_ratio:.2f})',
    'Items Added After Start': f'{team_name} - {sprint_name} - Items Added After Start by Status \n (Completed Ratio: {items_added_after_start_completed_ratio:.2f})',
    'Points Added After Start': f'{team_name} - {sprint_name} - Issues Added After Start by Status \n (Completed Ratio: {points_added_after_start_completed_ratio:.2f})',
    'User Stories Count': f'{team_name} - {sprint_name} - User Stories Count by Status \n (Completed Ratio: {user_stories_points_completed_ratio:.2f})',
    'User Stories Points': f'{team_name} - {sprint_name} - User Stories by Status \n (Completed Ratio: {user_stories_points_completed_ratio:.2f})'
    }

    for ax, (key, values) in zip(axs, data.items()):
        ax.bar(x, values, color=colors)
        ax.set_title(plot_titles[key])
        ax.set_xlabel('Status')
        ax.set_ylabel('Points')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)

    plt.tight_layout()
    plt.savefig(plot_path)
    plt.clf()
    print(f"Plot saved successfully at {plot_path}")

    summary_columns = [
        'Date & Time', 'Team Name', 'Sprint Name', 'Sprint Total Items', 'Sprint Items Completed', 'Sprint Items Not Completed',
        'Sprint Points Total', 'Sprint Points Not Completed', 'Sprint Points Completed', 'Sprint Points Completed Ratio', 'Original Items Total', 'Original Items Not Completed',
        'Original Items Completed', 'Original Points Total', 'Original Points Not Completed', 'Original Points Completed', 'Original Points Completed Ratio',
        'Added Items Total', 'Added Items Not Completed', 'Added Items Completed', 'Added Points Total', 'Added Points Not Completed', 'Added Points Completed', 'Points Added After Start Completed Ratio', 'User Stories Total', 'User Stories Not Completed', 'User Stories Completed', 'User Stories Total Points',
        'User Stories Points Not Completed', 'User Stories Points Completed', 'User Stories Points Completed Ratio'
    ]

    summary_csv_file = os.path.join(script_dir, 'sprint_summary_report.csv')
    file_exists = os.path.isfile(summary_csv_file) and os.path.getsize(summary_csv_file) > 0

    with open(summary_csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=summary_columns)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'Date & Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Team Name': team_name,
            'Sprint Name': sprint_name,
            'Sprint Total Items': total_items,
            'Sprint Items Completed': items_completed,
            'Sprint Items Not Completed': items_not_completed,
            'Sprint Points Total': total_points,
            'Sprint Points Not Completed': points_not_completed,
            'Sprint Points Completed': points_completed,
            'Sprint Points Completed Ratio': points_completed_ratio,
            'Original Items Total': total_original_items,
            'Original Items Not Completed': original_items_not_completed,
            'Original Items Completed': original_items_completed,
            'Original Points Total': total_original_points,
            'Original Points Not Completed': original_points_not_completed,
            'Original Points Completed': original_points_completed,
            'Original Points Completed Ratio': original_points_completed_ratio,
            'Added Items Total': total_items_added_after_start,
            'Added Items Not Completed': items_added_after_start_not_completed,
            'Added Items Completed': items_added_after_start_completed,
            'Added Points Total': total_points_added_after_start,
            'Added Points Not Completed': points_added_after_start_not_completed,
            'Added Points Completed': points_added_after_start_completed,
            'Points Added After Start Completed Ratio': points_added_after_start_completed_ratio,
            'User Stories Total': total_user_stories,
            'User Stories Not Completed': user_stories_not_completed,
            'User Stories Completed': user_stories_completed,
            'User Stories Total Points': total_user_stories_points,
            'User Stories Points Not Completed': user_stories_points_not_completed,
            'User Stories Points Completed': user_stories_points_completed,
            'User Stories Points Completed Ratio': user_stories_points_completed_ratio
        })
