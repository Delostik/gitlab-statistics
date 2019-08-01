# -*- coding: utf-8 -*-
import project
import commit

welcome = '          _ __  __      __               __        __  _      __  _ \n\
   ____ _(_) /_/ /___ _/ /_        _____/ /_____ _/ /_(_)____/ /_(_)_________  \n\
  / __ `/ / __/ / __ `/ __ \______/ ___/ __/ __ `/ __/ / ___/ __/ / ___/ ___/  \n\
 / /_/ / / /_/ / /_/ / /_/ /_____(__  ) /_/ /_/ / /_/ (__  ) /_/ / /__(__  )   \n\
 \__, /_/\__/_/\__,_/_.___/     /____/\__/\__,_/\__/_/____/\__/_/\___/____/    \n\
/____/                                                                       '

print(welcome)
print()

token = input("gitlab user token: ")
base_url = input("gitlab index url(eg. https://git.example.com):")
author = input("author to statistic, not email: ")

print('Fetching projects you\'ve contribute')
ids = project.get_contribute_project_ids(base_url, token)
print('----There\'s' + str(len(ids)) + 'project(s) you\'ve contribute!')
project_num = len(ids)

if project_num == 0:
    print('No valid project, Bye!')
    exit(0)

project_report = []
idx = 1

for project_id in ids:
    project_info = project.get_project_info(base_url, token, project_id)
    print('(' + str(idx) + '/' + str(project_num) + ')Analyzing project: ' + project_info['path_with_namespace'])

    additions = 0
    deletions = 0
    commits = commit.get_all_commits(base_url, token, project_id, author)
    for c in commits:
        detail = commit.get_commit_detail(base_url, token, project_id, c['id'])
        stats = detail['stats']
        additions += stats['additions']
        deletions += stats['deletions']
    project_report.append({
        'name': project_info['path_with_namespace'],
        'additions': additions,
        'deletions': deletions,
        'commits': len(commits)
    })
    idx += 1

addition = 0
deletion = 0
commits = 0
name_field_width = 10
for i in range(len(project_report) - 1):
    for j in range(i + 1, len(project_report)):
        if project_report[i]['commits'] < project_report[j]['commits']:
            project_report[i], project_report[j] = project_report[j], project_report[i]
for project in project_report:
    addition += project['additions']
    deletion += project['deletions']
    commits += project['commits']
    if len(project['name']) > name_field_width:
        name_field_width = len(project['name'])
number_field_width = max(len(str(addition)), max(len(str(deletion)), 9))
name_field_width += 2
number_field_width += 2

print('+' + '-' * name_field_width + ('+' + '-' * number_field_width) * 3 + '+')
print('|' + format('name', ' ^' + str(name_field_width)) + '|' + format('additions', ' ^' + str(number_field_width))
      + '|' + format('deletions', ' ^' + str(number_field_width)) + '|'
      + format('commits', ' ^' + str(number_field_width))) + '|'
print('+' + '-' * name_field_width + ('+' + '-' * number_field_width) * 3 + '+')
for project in project_report:
    print('|' + format(project['name'], ' ^' + str(name_field_width)) + '|'
          + format(project['additions'], ' ^' + str(number_field_width)) + '|'
          + format(project['deletions'], ' ^' + str(number_field_width)) + '|'
          + format(project['commits'], ' ^' + str(number_field_width))) + '|'
    print('+' + '-' * name_field_width + ('+' + '-' * number_field_width) * 3 + '+')
print('|' + format('total', ' ^' + str(name_field_width)) + '|' + format(addition, ' ^' + str(number_field_width))
      + '|' + format(deletion, ' ^' + str(number_field_width)) + '|'
      + format(commits, ' ^' + str(number_field_width))) + '|'
print('+' + '-' * name_field_width + ('+' + '-' * number_field_width) * 3 + '+')
