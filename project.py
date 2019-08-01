# -*- coding: utf-8 -*-
import requests


def get_contribute_project_ids(base_url, token):
    res = {}
    next_page = 1
    while next_page != '':
        url = '{}/api/v4/events?per_page=100&page={}&action=pushed'.format(base_url, next_page)
        resp = requests.get(url, headers={'Private-Token': token}, timeout=1)
        next_page = resp.headers.get('X-Next-Page')
        for event in resp.json():
            project_id = event['project_id']
            if not res.__contains__(project_id):
                res[project_id] = True
    return res


def get_project_info(base_url, token, project_id):
    url = '{}{}/{}'.format(base_url, '/api/v4/projects', project_id)
    resp = requests.get(url, headers={'Private-Token': token}, timeout=1)
    return resp.json()
