import requests  
import json
from src.element import Element
import os
import sqlite3
import shortuuid
import re
from time import sleep 

for index in range(4,-2,-1):
    try:
        data = requests.post("https://www.quora.com/graphql/gql_para_POST?q=UserProfileAnswersMostRecent_RecentAnswers_Query", headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "priority": "u=1, i",
            "quora-broadcast-id": "main-w-chan56-8888-react_rhvancsuygqfyuyr-cDpr",
            "quora-canary-revision": "false",
            "quora-formkey": "c09446b6a4353625785caf758a343b55",
            "quora-page-creation-time": "1729078602586577",
            "quora-revision": "1c813001f1e3aaf70900b68e3048d997952573f5",
            "quora-window-id": "react_rhvancsuygqfyuyr",
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "cookie": "__stripe_mid=f6594168-c7f0-420b-82a8-7fe6b763193f62f4f7; m-b=i_igAWrJFmbh5MG8asajZQ==; m-b_lax=i_igAWrJFmbh5MG8asajZQ==; m-b_strict=i_igAWrJFmbh5MG8asajZQ==; m-s=Gxt5aGv550G90VnJghQ0fA==; m-theme=light; m-dynamicFontSize=regular; m-themeStrategy=auto; m-ql10n_ar=https%3A%2F%2Fqsbr.cf2.quoracdn.net%2F-4-l10n_main-30-ar-693686341370417f.translation.json; m-login=1; m-lat=BEwiRHlPCIVnpumlNW9YGfZo5PEZramsOqzoT9NdRA==; m-uid=2563106278; m-sa=1; __stripe_sid=56dea236-280f-42cc-a104-46a2fad728823aea18; __gads=ID=0fb3d626f75bb9e2:T=1729017358:RT=1729078447:S=ALNI_MYNK02o06NmmwgKSL-omaV80WcHjw; __gpi=UID=00000f3f02cef187:T=1729017358:RT=1729078447:S=ALNI_MY_mO-nrpi_D-xp4vgkNAb3bX36tA; __eoi=ID=b1ee6cd216f5e02c:T=1729017358:RT=1729078447:S=AA-AfjaWHALk6KDK3V7WejdvXFxs",
            "Referer": "https://www.quora.com/profile/Handala-2/answers",
            "Referrer-Policy": "strict-origin-when-cross-origin"
            },json={"queryName":"UserProfileAnswersMostRecent_RecentAnswers_Query","variables":{"uid":267429363,"first":3,"after":str(index),"answerFilterTid": None},"extensions":{"hash":"87c0ab1d94902029565e396a4a0483108998ce98c4f1cce6ccf4f7c7a3fc4e03"}})
        answer=json.loads(data.text)
        content=json.loads(answer["data"]["user"]["recentPublicAndPinnedAnswersConnection"]["edges"][0]["node"]["content"])
        title=answer["data"]["user"]["recentPublicAndPinnedAnswersConnection"]["edges"][0]["node"]["question"]["slug"].replace("-"," ") +" ?"
        element_list=[]
        lists=""
        ul=[]
        ol=[]
        def empty_list():
            global ul
            global ol
            if len(ul)>0:
                element="<ul>"
                for i in ul:
                    element+=i
                element+="</ul>"
                lists=""
                element_list.append(element)
                ul=[]
            elif len(ol)>0:
                element="<ol>"
                for i in ol:
                    element+=i
                element+="</ol>"
                lists=""
                element_list.append(element)
                ol=[]
        def collect_spam(element,e):
            div=""
            for span in element:
                el=Element(span)
                div+=el.createElement()
            if e["quoted"]==True:
                div=f'''<figure class="note note-secondary p-4">
                <blockquote class="blockquote">
                    <p class="pb-2">
                    {div}
                    </p>
                </blockquote>
                </figure>'''
            return div

        for e in content["sections"]:
            list_type=0
            if e["type"]=="yt-embed":
                empty_list()
                url=e["spans"][0]["modifiers"]["embed"]["url"].replace("https://www.youtube.com/","https://www.youtube.com/embed/")
                div=f'<iframe width="420" height="345" src={url}></iframe>'
                element_list.append(div)
            elif e["type"]=="tweet":
                div=e["spans"][0]["modifiers"]["embed"]["html"]
                element_list.append(div)
            elif  e["type"] in["image","plain","hyperlink_embed"]:

                empty_list()
                div=collect_spam(e["spans"],e)  
                element_list.append(div)

            elif  e["type"] in ["ordered-list","unordered-list"]:
                if e["type"] =="unordered-list" and lists=="unordered-list":
                    div=collect_spam(e["spans"],e) 
                    ul.append("<li class='llist'>"+div+"</li>")
                elif e["type"] =="ordered-list" and lists=="ordered-list":
                    div=collect_spam(e["spans"],e) 
                    ol.append("<li class='llist'>"+div+"</li>")
                elif  e["type"] =="ordered-list":
                    div=collect_spam(e["spans"],e) 
                    if len(ul)>0:
                        element="<ul>"
                        for i in ul:
                            element+=i
                        element+="</ul>"
                        element_list.append(element)
                    lists="ordered-list"
                    ul=[]
                    ol.append("<li class='llist'>"+div+"</li>")

                else:
                    div=collect_spam(e["spans"],e) 
                    if len(ol)>0:
                        element="<ol>"
                        for i in ol:
                            element+=i
                        element+="</ol>"
                        element_list.append(element)
                    lists="unordered-list"

                    ol=[]
                    ul.append("<li class='llist'>"+div+"</li>")
        html=""

        for el in element_list:
            if el!='':
                html+="<div>"+el+"</div>"
        html

        id = str(shortuuid.ShortUUID(alphabet="013456789").random(length=20))
        parent_dir = "./static/articles"
        path = os.path.join(parent_dir, id) 
        os.mkdir(path) 

        data = html
        path2 = os.path.join(path, "index.txt")
        with open( path2  ,'w') as fl:
                fl.write(data)
        db = sqlite3.connect('web_data.db')
        desciption = "Article made by handala "
        db.execute("INSERT INTO Articles (id,title,desciption) VALUES ((?),(?),(?)) ",(id, title , desciption))
        db.commit()
    except:
        print(index)
    sleep(30)
