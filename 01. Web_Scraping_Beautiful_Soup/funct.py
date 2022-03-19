import re

def getTitle(mdata):
    title = mdata.find("h2").string
    return str(title)
def getSubtitle(mdata):
    subtitle = mdata.find("h3").string
    return str(subtitle)
def getmainID(strdat):
    intstring = strdat[36:]
    res = ""
    for i in intstring:
        if i != ".":
            res = res + i
        else:
            break
    return res
def processpara(title_para):
    title_para = (str(title_para))
    title_para = title_para.strip("<p>")
    title_para = title_para.strip("</p>")
    title_para = title_para.strip("\r")
    title_para = title_para.strip("\n")
    title_para = title_para.strip("\t")
    title_para = title_para.strip(" ")
    return title_para
def contains_substr(postfix):
    substring = 'javascript'
    if substring in postfix:
        return True
    return False

def getSeason(titlestring):
    titlestring = str(titlestring)
    res = ""
    for itertn in titlestring:
        if itertn.isdecimal():
            res = res + itertn
    return res

    