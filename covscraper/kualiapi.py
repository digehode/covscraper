import requests
from covscraper import auth
import datetime, sys, re
import json
import urllib
import io, csv

def _decode_csv( csvstr ):
    # extract csv data
    csvfile = io.StringIO( csvstr )
    csvdata = list( csv.reader( csvfile, delimiter=',' ) )

    # convert to dict of dicts, key is module code
    modules = {}
    for row in range(1,len(csvdata)):
        fields = { key: val for key, val in zip(csvdata[0], csvdata[row]) }           
        modules[fields["reversedCode"]] = fields["id"]

    return modules

def get_uid( session, module ):
    url = "https://coventry.kuali.co/api/v0/cm/search?status=active&index=courses_latest&q={module}"
    #url = "https://coventry.kuali.co/api/v0/cm/search/results.csv?index=courses_latest&q={module}"
    
    response = session.get(url.format(module=module))
    data=json.loads(response.text)
    # import code
    # code.interact(local=locals())
    return data[0]["id"]
    #_decode_csv( response.text ).get(module, None)

def _decode_mid( data ):
    # TODO
    return json.loads(data)

def get_assessment(session, aid):
    #TODO: process this
    #Currently the keys are "0" "1" "2" etc. Could easily change to better keys so they descrive the content
    url = "    https://coventry.kuali.co/api/cm/options/{aid}"
    response = session.get( url.format(aid=aid), headers={'Accept': 'application/json, text/plain, */*', "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZDBjOThhODM5OTNiMDAxNGRiMjA1ZiIsImlzcyI6Imt1YWxpLmNvIiwiZXhwIjoxNjA4NzI4MjAyLCJpYXQiOjE2MDc1MTg2MDJ9.iBVoMZWcz-o2apRv-OVY6-L757rIB8WnRYMXgqfWvLs"} )
    #print("Got: "+response.text)
    return json.loads(response.text)

def get_component_types(session):
    url="https://coventry.kuali.co/api/cm/options/types/Component%20Type?limit=1200&active=true"
    response = session.get( url, headers={'Accept': 'application/json, text/plain, */*', "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZDBjOThhODM5OTNiMDAxNGRiMjA1ZiIsImlzcyI6Imt1YWxpLmNvIiwiZXhwIjoxNjA4NzI4MjAyLCJpYXQiOjE2MDc1MTg2MDJ9.iBVoMZWcz-o2apRv-OVY6-L757rIB8WnRYMXgqfWvLs"} )
    #print("Got: "+response.text)
    types= json.loads(response.text)
    dTypes={}
    for i in types:
        dTypes[i["id"]]=i
    return dTypes
def get_module_mid( session, module ):
    url = "https://coventry.kuali.co/api/cm/courses/changes/{uid}?denormalize=true"
    
    uid = get_uid( session, module )
    #print(f"Got UID: {uid}")
    response = session.get( url.format(uid=uid) )

    return _decode_mid( response.text )

def get_bos(session, bosid):
    #urgh, this needs work. Can't just paste these tokens in here
    #TODO: actual tokens
    url = "https://coventry.kuali.co/api/v1/groups/{bosid}/"
    response = session.get( url.format(bosid=bosid), headers={'Accept': 'application/json, text/plain, */*', "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZDBjOThhODM5OTNiMDAxNGRiMjA1ZiIsImlzcyI6Imt1YWxpLmNvIiwiZXhwIjoxNjA4NzI4MjAyLCJpYXQiOjE2MDc1MTg2MDJ9.iBVoMZWcz-o2apRv-OVY6-L757rIB8WnRYMXgqfWvLs"} )
    #print("Got: "+response.text)
    return json.loads(response.text)
