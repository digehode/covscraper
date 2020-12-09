#!/usr/bin/env python3
import getpass, getopt
import covscraper
import datetime
import sys
import json,yaml
from optparse import OptionParser
from nested_lookup import nested_lookup


if __name__ == "__main__":
    
    usage = "usage: %prog [options] modulecode [modulecode modulecode ...]"

    parser=OptionParser(usage=usage)
    parser.add_option("-u","--user", dest="user", help="specify Kuali username", metavar="USER", default=None)
    parser.add_option("-p","--password", dest="password", help="specify Kuali password. Not recommended!", metavar="PASS", default=None)
    parser.add_option("-f","--format", dest="format", help="format for result. Valid options are: json, yaml", metavar="FORMAT", default="json", type="choice", choices=["json","yaml"])
    parser.add_option("-d","--deep", dest="deep", help="When set, also pull referenced objects",  default=False, action="store_true")
    (options,args)=parser.parse_args()
    params = {"user": options.user, "pass": options.password}
    

    # handle defaults
    if not params["user"]: params["user"] = input("username: ")
    if not params["pass"]: params["pass"] = getpass.getpass("password: ")

    if len(args)<1:
        print("You must supply at least one module code")
        sys.exit(1)
    modules={}
    #Add auth details to session
    session = covscraper.auth.Authenticator(params["user"], params["pass"])

    # bosid="4JMHmYpcl"

    # uid=covscraper.kualiapi.get_module_mid(session, "4061CEM")
    # covscraper.kualiapi.get_bos(session,bosid)
    
    for i in args:      
        mid = covscraper.kualiapi.get_module_mid(session,i)
        modules[i]=mid

    result={"modules":modules}

    #Now check if "deep" is requested and run through references if it is
    #TODO: all the rest of these
    if options.deep:
        result["assessmentType"]=covscraper.kualiapi.get_component_types(session)
        result["bos"]={}
        for k in nested_lookup("boardOfStudy",modules):
            #print(f"BoS: {k}")
            if not k in result["bos"]:
                result["bos"][k]=covscraper.kualiapi.get_bos(session,k)
        result["assessment"]={}

        for ass in nested_lookup("newAssessmentTable", modules):
            for a in ass:
                # print("Assessment: ",end="")
                # print(a)

                if not a["0"] in result["assessment"]:
                    result["assessment"][a["0"]]=covscraper.kualiapi.get_assessment(session,a["0"])
            
        
    
    out=""
    if options.format=="json":
        out=json.dumps(result)
    elif options.format=="yaml":
        out=yaml.dump(result)
    else:
        print(f"Unknown format: {options.format}")
        sys.exit(1)
    print(out)
            
    sys.exit(0)
