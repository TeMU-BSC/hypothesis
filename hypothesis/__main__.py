"""
    Upload annotations to Hypothesis 
"""
import click
import json
import requests
import csv
import os
import re
from hypothesis.hypothesis_api import Api
from hypothesis.utils import create_annotation
from hypothesis import config
from pprint import pprint


def add_annotations(api, file):
    api_endpoint = api.urls["links"]["annotation"]["create"]["url"]
    lines = None
    with open(file) as inputF:
        lines = inputF.readlines()
        if config.HEADER:
            lines = lines[1:]

    annotations = []
    print("")
    for line in lines:
        fields = line.split(config.FIELDS_DEL)
        start_pos = None
        end_pos = None
        tags_list = None

        uri = fields[config.URL]

        titles_list = [fields[config.DOCUMENT_NAME]]
        selected_text = fields[config.EXACT_TEXT]

        try:
            tags_list = [re.findall(config.TAG_REGEX, tag)[0]
                         for tag in fields[config.TAGS].split(config.TAGS_DEL)]
        except:
            tags_list = [tag for tag in re.findall(
                config.TAG_REGEX, fields[config.TAGS]) if tag.strip() != ""]
        try:
            start_pos = fields[config.START_POS]
            end_pos = fields[config.END_POS]
        except:
            pass

        group = config.GROUP
        text = config.TAGS_TEXT
        permissions = config.PERMISSIONS

        annotations.append(create_annotation(uri=uri,
                                             titles_list=titles_list,
                                             selected_text=selected_text,
                                             start_pos=start_pos, end_pos=end_pos,
                                             tags_list=tags_list,
                                             group=group,
                                             text=text,
                                             permissions=permissions
                                             )
                           )

    total = len(annotations)

    print("Total annotations to upload:", total)
    for i, annotation in enumerate(annotations):
        json_obj = json.dumps(annotation)
        response = requests.post(
            api_endpoint, data=json_obj, headers=api.header)

        if response.ok:
            text = "Succeed"
        else:
            text = "Failed"

        print(i, ':', text)

    return


def get_annotations(api):
    api_endpoint = api.urls["links"]["search"]["url"]
    
    response = requests.get(
            api_endpoint,headers=api.header,params={"group":config.GROUP,"wildcard_uri":None,"tag":None})

    pprint(response.json())


def fun_annotations(api, file):
    content = None

    if file:
        add_annotations(api, file)
    else:
        get_annotations(api)



def get_groups(api):
    api_endpoint = api.urls["links"]["groups"]["read"]["url"]
    response = requests.get(
            api_endpoint,headers=api.headers)

    pprint(response.json())

@click.command()
@click.option('--annotations/--no-annotations', default=False)
@click.option('--file', default=None, help="File of annotations to upload. It required, if you want to add new annotations")
@click.option('--users', default=False)
@click.option('--groups/--no-groups', default=False)
@click.option('--token', default=None)
def main(annotations, file, users, groups, token):
    bearer_token = token or config.bearer_token
    api = Api(bearer_token)

    if annotations:
        result = fun_annotations(api, file)
    elif users:
        pass
    elif groups:
        get_groups(api)
    else:
        print(
            "You must select a option: --annotations, --users, --groups\n[--help] to see help menu.")


if __name__ == '__main__':
    main()
