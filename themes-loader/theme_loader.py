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
import time
from dotenv import load_dotenv
import base64
import re

# load .env file
load_dotenv()

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
        print("old vscode file deleted")
    else:
        print(f"File not found: {vs_file_name}")

    if os.path.exists(jetbrains_file_name):
        os.remove(jetbrains_file_name)
        print("old jetbrains file deleted")
    else:
        print(f"File not found: {jetbrains_file_name}")


def print_request_error(response):
    print(f"Failed to retrieve themes. Status code: {response.status_code}")
    print(f"Response content: {response.content.decode()}")


def load_vscode_themes():
    del_old_file()

    # Send the POST request
    response = requests.post(vscode_api_url, headers=headers, data=json.dumps(payload))
    d = []

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract and print the list of themes
        for extension in data["results"][0]["extensions"]:
            theme_publisher = extension["publisher"]["publisherName"]
            theme_name = extension.get("extensionName", "")
            #print(f"Name: {extension['displayName']}, Publisher: {extension['publisher']['publisherName']}")
            # vsoode auto install link: vscode:extension/publisher.theme-name
            d.append({
                "id": extension.get("extensionId", ""),
                "theme_name": theme_name,
                "description": extension.get("shortDescription", ""),
                "install_link": f"vscode:extension/{theme_publisher}.{theme_name}",
                "last_update": extension.get("lastUpdated", ""),
                "author": theme_publisher,
                "publisherId": extension["publisher"]["publisherId"],
                "previewImage": "",
            })
    else:
        print_request_error(response)

    # write data into file
    with open(vs_file_name, "w") as f:
        json.dump(d, f, indent=4)

gh_search_url = "https://api.github.com/search/repositories"

gh_username = os.getenv("GITHUB_USERNAME")
gh_pac = os.getenv("GITHUB_PAC") # personal access token

"""
github response but shortened:
{
    "total_count":735900,
    "incomplete_results":false,
    "items":[
        {
            "id":21872392,
            "node_id":"MDEwOlJlcG9zaXRvcnkyMTg3MjM5Mg==",
            "name":"awesome-machine-learning",
            "full_name":"josephmisiti/awesome-machine-learning",
            "private":false,
            "owner":{
                "login":"josephmisiti",
                "id":246302,
                "node_id":"MDQ6VXNlcjI0NjMwMg==",
                "avatar_url":"https://avatars.githubusercontent.com/u/246302?v=4",
            },
            "description":"A curated list of awesome Machine Learning frameworks, libraries and software.",
            "created_at":"2014-07-15T19:11:19Z",
            "updated_at":"2025-01-10T02:15:24Z",
            "pushed_at":"2024-12-16T21:26:20Z",
            "visibility":"public",
            "forks":14723,
            "open_issues":0,
        }
    ]
}"""
def add_vscode_preview_images():
    # open file and go through each element in the list
    with open(vs_file_name, "r") as f:
        data = json.load(f) # parse json file into data

    # iterate through each entry
    for item in data:
        print("data len:", len(data))
        if "theme_name" in item:
            theme_name = item["theme_name"]
            print(theme_name)

            # get the first image from the README.md (hopefully this is a preview image)
            params = {
                "q": theme_name,
                "sort":"starts", # most popular
                "order":"desc",
                "per_page":1
            }
            
            # headers used for auth
            headers = {
                "Authorization": f"Basic {gh_username}:{gh_pac}"
            }
            
            response = requests.get(gh_search_url, params=params, headers=headers)
            
            # get rate limiting headers
            rate_remaining = response.headers.get("X-RateLimit-Remaining") # requests remaining
            rate_reset = int(response.headers.get("X-RateLimit-Reset")) # time in epoch seconds until reset
            print(f"r_rem {rate_remaining} r_res {rate_reset}")
            
            # if there is only 1 request remaining, just wait until the reset
            # from doc: If you exceed your primary rate limit, you will receive a 403 or 429
            if rate_remaining == 1 or response.status_code == 403 or response.status_code == 429:
                current_epoch = time.time()
                time_to_wait = rate_reset - current_epoch
                
                if time_to_wait > 0:
                    print(f"we have to wait {time_to_wait} epoch seconds...")
                    time.sleep(time_to_wait)
                    print("!!!continuing!!!")
            
            if response.status_code == 200:
                repos = response.json().get("items")
                
                # get the first search result
                if repos:
                    repo = repos[0]                
                    repo_name = repo["name"]
                    owner = repo["owner"]["login"]
                    
                    # get readme content
                    readme_url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"
                    readme_response = requests.get(readme_url, headers=headers)
                    found = False # used to check if an img was found in the readme file
                    if readme_response.status_code == 200:
                        rdme_data = readme_response.json()
                        content_base64 = rdme_data.get("content")
                        if content_base64:
                            readme_content_bytes = base64.b64decode(content_base64)
                            readme_content = readme_content_bytes.decode("utf-8")
                                                        
                            ### extract the first img found ###
                            # search for ![alt txt](img url)
                            
                            # exclude keywords like badge and only search for img endings
                            img_pattern = r'!\[.*?\]\((?!.*badge.*)(.*?\.(?:png|jpe?g|gif|svg))\)' 
                            match = re.search(img_pattern, readme_content, re.IGNORECASE)
                            if match:
                                first_img_url = match.group(1)
                                found = True
                            else:
                                print("no image found for ![alt txt](img url), trying <img>....")
                            
                            # search for <img> html tag
                            img_pattern = r'^<img[^>]*src=["\'](.*?)["\']'
                            match = re.search(img_pattern, readme_content, re.IGNORECASE)
                            if match:
                                first_img_url = match.group(1)
                                found = True
                            else:
                                print("no image found.... weird")

                            # update the theme["preview_image"] key in array if something was found
                            if found:
                                item["previewImage"] = first_img_url
                                print(f"FOUND! updated preview_image for {theme_name}")

                    else:
                        # unable to retrieve README.md from repo
                        # non existant? (very weird) 
                        d = readme_response.json()
                        print("error while getting readme", d)
            else:
                # no repos returned from github search api with that exact name
                d = response.json()
                print("error while search for repo on github", d)


    print(data[0])
    # update the file
    with open(vs_file_name, "w") as f:
        json.dump(data,f,indent=4)

def load_jetbrains_themes():
    # params = {
    #    "query":"",
    #    "build":"IC-2024.3",
    #    "max":50,
    # }
    response = requests.get(jetbrains_api_url)
    dj = []
    preview_image_base_url = "https://downloads.marketplace.jetbrains.com"

    if response.status_code == 200:
        #print(response.json())
        extensions = response.json().get("plugins",[])
        # print(extensions)
        for extension in extensions:
            author = extension.get("vendor", {})
            theme_name = extension.get("name","")
            theme_id = extension.get("id","")
            #print(extension)
            # jetbrains auto install link: jetbrains://plugins.jetbrains.com/plugin/12345
            dj.append({
                "id": theme_id,
                "theme_name": theme_name,
                "description": extension.get("preview", ""),
                "install_link": f"jetbrains://plugins.jetbrains.com/{theme_name}/{theme_id}",
                "last_update": "",
                "author": author.get("name"),
                "publisherId": "",
                "previewImage": preview_image_base_url + extension.get("previewImage", ""),
            })
    else:
        print_request_error(response)

    with open(jetbrains_file_name, "w") as f:
        json.dump(dj, f, indent=4)


load_vscode_themes()
add_vscode_preview_images()
print("vscode themes loaded")

load_jetbrains_themes()
print("jetbrains themes loaded")
