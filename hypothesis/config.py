bearer_token = "6879-iL27ljsXNbkHRVh0WcIRv_vikgFlkizysrjL3NlCOOk"

# csv config

#If files file line is a header
HEADER = True

#Delimiter of csv file
FIELDS_DEL="\t"

TAGS = 0
TAGS_DEL = "|"

#required
TAG_REGEX = r"(?<=species:ncbi:).*$"
#To avoid it un comment next line
#TAG_REGEX = r".*$"

TAGS_TEXT = "NCBI SPECIE ID"

#optional, If you don't provied title, than it will be as UNTITLED DOCUMENT.
#It gets a list of titles
DOCUMENT_NAME = 1

#Optional
START_POS = 2

#Optional
END_POS = 3

#Required
EXACT_TEXT = 4

#Required
URL = 6





GROUP = "KKEMPvD3"
PERMISSIONS = {
    "read": [
        f"group:{GROUP}",
        "acct:ankush12@hypothes.is"
    ],
    "admin": [
        "acct:ankush12@hypothes.is"
    ],
    "update": [
        f"group:{GROUP}",
        "acct:ankush12@hypothes.is"
    ],
    "delete": [
        f"group:{GROUP}",
        "acct:ankush12@hypothes.is"
    ]
}
