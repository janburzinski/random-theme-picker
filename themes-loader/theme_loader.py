"""
json structure:
{
    {
        "id":"",
        "theme_name": "Test",
        "description":"",
        "install_link": "",
        "last_update":"",
        "author":"",
        "extensionId":"",
        "publisherId":"",
        "previewImage:"",
    },
}

vs-code response:
{
   "results":[
      {
         "extensions":[
            {
               "publisher":{
                  "publisherId":"5f5636e7-69ed-4afe-b5d6-8d231fb3d3ee",
                  "publisherName":"ms-vscode",
                  "displayName":"Microsoft",
                  "flags":"verified",
                  "domain":"https://microsoft.com",
                  "isDomainVerified":true
               },
               "extensionId":"99b17261-8f6e-45f0-9ad5-a69c6f509a4f",
               "extensionName":"cpptools-themes",
               "displayName":"C/C++ Themes",
               "flags":"validated, public",
               "lastUpdated":"2022-10-24T21:51:14.93Z",
               "publishedDate":"2019-08-30T19:54:42.453Z",
               "releaseDate":"2019-08-30T19:54:42.453Z",
               "shortDescription":"UI Themes for C/C++ extension.",
               "deploymentType":0
            }
         ],
         "pagingToken":"None",
         "resultMetadata":[
            {
               "metadataType":"ResultCount",
               "metadataItems":[
                  {
                     "name":"TotalCount",
                     "count":15492
                  }
               ]
            }
         ]
      }
   ]
}

jetbrains response:
{
   "plugins":[
      {
         "id":11938,
         "xmlId":"com.markskelton.one-dark-theme",
         "link":"/plugin/11938-one-dark-theme",
         "name":"One Dark Theme",
         "preview":"One Dark theme for JetBrains. Do you need help? Please check the docs FAQs to see if we can solve your problem. If that does not fix your problem, please submit an...",
         "downloads":8481542,
         "pricingModel":"FREE",
         "icon":"/files/11938/605820/icon/pluginIcon.svg",
         "previewImage":"/files/11938/preview_19494.png",
         "cdate":1726780936000,
         "rating":4.8,
         "hasSource":true,
         "tags":[
            "Theme",
            "User Interface"
         ],
         "vendor":{
            "name":"Mark Skelton",
            "isVerified":false
         }
      }
   }

"""
import os.path

import requests
import json

vs_file_name = "vscode_themes.json"
vscode_api_url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json;api-version=5.2-preview.1;excludeUrls=true"
}
payload = {
    "filters": [
        {
            "criteria": [
                {"filterType": 8, "value": "Microsoft.VisualStudio.Code"},
                {"filterType": 5, "value": "Themes"}
            ],
            "pageSize": 100,  # amount of extensions that will be returned
            "sortBy": 4  # sort by install count
            # other flags are:
            # 0 => relevance
            # 1 => last updated
            # 2 => title
            # 3 => publisher name
            # 5 => published date
        }
    ],
    "flags": 0
}

jetbrains_file_name = "jetbrains_themes.json"
jetbrains_api_url = "https://plugins.jetbrains.com/api/searchPlugins?excludeTags=internal&includeTags=theme&max=100&offset=0&pricingModels=FREE&pricingModels=FREEMIUM&tags=Theme"


def del_old_file():
    if os.path.exists(vs_file_name):
        os.remove(vs_file_name)
    else:
        print(f"File not found: {vs_file_name}")

    if os.path.exists(jetbrains_file_name):
        os.remove(jetbrains_file_name)
    else:
        print(f"File not found: {jetbrains_file_name}")


def print_request_error(response):
    print(f"Failed to retrieve themes. Status code: {response.status_code}")
    print(f"Response content: {response.content.decode()}")


def load_vscode_themes():
    del_old_file()

    # Send the POST request
    response = requests.post(vscode_api_url, headers=headers, data=json.dumps(payload))
    d = [{}]

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract and print the list of themes
        for extension in data["results"][0]["extensions"]:
            print(f"Name: {extension['displayName']}, Publisher: {extension['publisher']['publisherName']}")
            d.append({
                "id": extension.get("extensionId", ""),
                "theme_name": extension.get("extensionName", ""),
                "description": extension.get("shortDescription", ""),
                "install_link": "",
                "last_update": extension.get("lastUpdated", ""),
                "author": extension["publisher"]["publisherName"],
                "publisherId": extension["publisher"]["publisherId"],
                "previewImage": "",
            })
    else:
        print_request_error(response)

    # write data into file
    with open(vs_file_name, "w") as f:
        json.dump(d, f, indent=4)


def load_jetbrains_themes():
    # params = {
    #    "query":"",
    #    "build":"IC-2024.3",
    #    "max":50,
    # }
    response = requests.get(jetbrains_api_url)
    dj = [{}]

    if response.status_code == 200:
        print(response.json())
        extensions = response.json().get("plugins",[])
        # print(extensions)
        for extension in extensions:
            author = extension.get("vendor", {})
            print(extension)
            dj.append({
                "id": extension.get("id", ""),
                "theme_name": extension.get("name", ""),
                "description": extension.get("preview", ""),
                "install_link": extension.get("link", ""),
                "last_update": "",
                "author": author.get("name"),
                "publisherId": "",
                "previewImage": extension.get("previewImage", ""),
            })
    else:
        print_request_error(response)

    with open(jetbrains_file_name, "w") as f:
        json.dump(dj, f, indent=4)


load_vscode_themes()
print("vscode themes loaded")

load_jetbrains_themes()
print("jetbrains themes loaded")
