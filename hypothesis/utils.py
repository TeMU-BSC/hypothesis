import os

def create_annotation(uri,  titles_list, selected_text, start_pos, end_pos, tags_list, group,text="", permissions=None):

    json_obj = {
        "uri": uri,
        "document": {
            "title": titles_list,
        },
        "text": text,
        "tags": tags_list,
        "group": group,
        "target": [{
            "selector": [
                {
                    "type": "TextQuoteSelector",
                    "exact": selected_text
                }
            ]
        }]

    }

    try:
        start_pos = int(start_pos)
        end_pos = int(end_pos)
        json_obj["target"][0]["selector"].push(
            {
                "type": "TextPositionSelector",
                "start": start_pos,
                "end": end_pos
            }
        )
    except:
        pass

    if permissions:
        json_obj.update({"permissions": permissions})

    return json_obj
