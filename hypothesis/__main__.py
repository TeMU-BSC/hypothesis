import click
import json
import requests
import csv
import os
import re
from hypothesis.hypothesis_api import Api
from hypothesis.utils import create_annotation
from hypothesis import config


def add_annotations(api, file, dir_url):
    api_endpoint = api.urls["links"]["annotation"]["create"]["url"]
    lines = None
    with open(file) as inputF:
        lines = inputF.readlines()
        if config.HEADER:
            lines = lines[1:]

    annotations = []
    print("")
    for line in lines[:5]:
        fields = line.split(config.FIELDS_DEL)
        start_pos = None
        end_pos = None
        tags_list = None

        uri = os.path.join(dir_url, fields[config.DOCUMENT_NAME])+".txt"

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

        print(i,annotation[uri],':',text)
     
    return


def get_annotations(api):
    api_endpoint = api.urls["links"]["annotation"]["search"]["url"]

    print("TODO")

def fun_annotations(api, file, dir_url):
    content = None

    if file:
        if dir_url:
            add_annotations(api, file, dir_url)
        else:
            print("Require dir url for documents. EX: --dir_url ftp://example.com/dir")
    else:
        get_annotations(api)


@click.command()
@click.option('--annotations/--no-annotations', default=False)
@click.option('--file', default=None, help="File of annotations to upload. It required, if you want to add new annotations")
@click.option('--dir_url', default=None, help="URL of parent directroy to browese the file.")
@click.option('--users', default=False)
@click.option('--groups', default=False)
@click.option('--token', default=None)
def main(annotations, file, users, groups, token, dir_url):
    bearer_token = token or config.bearer_token
    api = Api(bearer_token)

    if annotations:
        result = fun_annotations(api, file, dir_url)
    elif users:
        pass
    elif groups:
        pass
    else:
        print(
            "You must select a option: --annotations, --users, --groups\n[--help] to see help menu.")


if __name__ == '__main__':
    main()
