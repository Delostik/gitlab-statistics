# -*- coding: utf-8 -*-
import requests


def get_all_commits(base_url, token, project_id, filter_author=''):
    res = []
    next_page = 1
    url_format = '{}/api/v4/projects/{}/repository/commits?ref=master&per_page=100&page={}'
    while next_page != '':
        url = url_format.format(base_url, project_id, next_page)
        resp = requests.get(url, headers={'Private-Token': token})
        next_page = resp.headers.get('X-Next-Page')
        if filter_author == '':
            res.extend(resp.json())
        else:
            for commit in resp.json():
                if commit['author_name'] == filter_author:
                    res.append(commit)
    return res


def get_commit_detail(base_url, token, project_id, commit_id):
    url = '{}/api/v4/projects/{}/repository/commits/{}'.format(base_url, project_id, commit_id)
    resp = requests.get(url, headers={'Private-Token': token})
    return resp.json()
