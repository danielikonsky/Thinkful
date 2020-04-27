from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from datetime import date
import requests
import json

AdvisorAvaiList = []

app = Flask(__name__)
CORS(app)

def formatdate(rawdate):

    dateformat = ''
    dateformatlist = list (rawdate)

    for i in range(len(dateformatlist)):
        if i == 0 or i == 3:
            if dateformatlist[i] == '0':
                pass
            else:
                dateformat = dateformat + dateformatlist[i]
        else:
            dateformat = dateformat + dateformatlist[i]

    return (dateformat)

def formatime(rawtime):

    if rawtime[0:2] == '00':
        timeformat = '12'+rawtime[2:5] + ' am'
    elif rawtime[0:2] < '10':
        timeformat = rawtime [1] + rawtime[2:5] + ' am'
    elif rawtime[0:2] < '12':
        timeformat = rawtime [0:2] + rawtime[2:5] + ' am'
    elif rawtime[0:2] == '12':
            timeformat = rawtime [0:2] + rawtime[2:5] + ' pm'
    else:
        timeformat = str(int(rawtime[0:2]) - 12) + rawtime[2:5] + ' pm'
    return (timeformat)

@app.route("/today", methods=["GET"])
def today():

    return jsonify({"today": formatdate(date.today().strftime("%m/%d/%Y"))})

@app.route("/init", methods=["GET"])
def init():
    AdvisorList = []
    AdvisorAvailDict = {'AdvisorKey':'','AdvisorId':'','TimeSpot':'','Student':''}

    if request.args.get('namefield'):

        NewAdvisorAvaiList = []
        NewAdvisorBookList = []

        _advisorkey = request.args.get('advisorkey')
        _namefield = request.args.get('namefield')

        for i in range(len(AdvisorAvaiList)):

            if AdvisorAvaiList[i]['AdvisorKey'] == _advisorkey:
                AdvisorAvaiList[i]['Student'] = _namefield
                break

        for i in range(len(AdvisorAvaiList)):
            if AdvisorAvaiList[i]['Student'] == '':
                NewAdvisorAvaiList.append(AdvisorAvaiList[i])
            else:
                NewAdvisorBookList.append(AdvisorAvaiList[i])

        NewAdvisorAvaiListSorted = sorted(NewAdvisorAvaiList, key = lambda i: (i['AdvisorKey']))

        for i in range(len(NewAdvisorAvaiListSorted)):

            if NewAdvisorAvaiListSorted[i]['AdvisorKey'][0:6] in AdvisorList:
                    NewAdvisorAvaiListSorted[i]['AdvisorId'] = ''
            else:
                NewAdvisorAvaiListSorted[i]['AdvisorId'] = NewAdvisorAvaiListSorted[i]['AdvisorKey'][0:6]
                AdvisorList.append(NewAdvisorAvaiListSorted[i]['AdvisorKey'][0:6])

        NewAdvisorBookListSorted = sorted(NewAdvisorBookList, key = lambda i: (i['AdvisorKey']))
        AdvisorList = []

        for i in range(len(NewAdvisorBookListSorted)):

            if NewAdvisorBookListSorted[i]['AdvisorKey'][0:6] in AdvisorList:
                    NewAdvisorBookListSorted[i]['AdvisorId'] = ''
            else:
                NewAdvisorBookListSorted[i]['AdvisorId'] = NewAdvisorBookListSorted[i]['AdvisorKey'][0:6]
                AdvisorList.append(NewAdvisorBookListSorted[i]['AdvisorKey'][0:6])

        AdvisorAvaiListSorted = NewAdvisorAvaiListSorted + NewAdvisorBookListSorted

    else:

        AdvisorAvaiList.clear()

        r = requests.get("https://www.thinkful.com/api/advisors/availability")
        resp = r.json()

        for k,v in resp.items():

            for k1,v1 in v.items():

                avtime = k1[5:7] + '/'+ k1[8:10] + '/' + k1[0:4] + ' ' + k1[11:16]

                AdvisorAvailDict['AdvisorKey'] = str(v1) + avtime

                AdvisorAvailDict['TimeSpot'] = formatdate(avtime[0:10]) + ' ' + formatime(avtime[11:16])

                AdvisorAvaiList.append(AdvisorAvailDict)
                AdvisorAvailDict = {'AdvisorKey':'','AdvisorId':'','TimeSpot':'','Student':''}

        AdvisorAvaiListSorted = sorted(AdvisorAvaiList, key = lambda i: (i['AdvisorKey']))

        for i in range(len(AdvisorAvaiListSorted)):

            if AdvisorAvaiListSorted[i]['AdvisorKey'][0:6] in AdvisorList:
                    AdvisorAvaiListSorted[i]['AdvisorId'] = ''
            else:
                AdvisorAvaiListSorted[i]['AdvisorId'] = AdvisorAvaiListSorted[i]['AdvisorKey'][0:6]
                AdvisorList.append(AdvisorAvaiListSorted[i]['AdvisorKey'][0:6])

    return jsonify({"init": AdvisorAvaiListSorted})
