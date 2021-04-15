#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pickle
import time
import os

from urllib2 import urlopen
from json import loads


import git

import sh

def get_next_pr_id(project):
    API = "https://api.github.com/repos/{}/issues?state=all&sort=created&direction=desc".format(project)

    raw_response = urlopen(API).read().decode("utf-8")
    json_response = loads(raw_response)
    issues = list(json_response)
    last_id = int(issues[0]["number"])

    return last_id + 1

def createDriver():
    options = Options()
    options.add_argument("user-data-dir=/tmp/github-fmbt")
    return webdriver.Chrome(chrome_options=options)
    return None

def github_new_pr(driver, project, branch_name):
    sh.gh.pr.create("--fill", "--head", branch_name, _env=get_env("github-fmbt.token"))

def get_env(token_file="kokan.token"):
    env = os.environ.copy()
    env['GH_TOKEN'] = get_token(token_file)
    return env

def get_token(path):
    with open(path) as f:
        gh_token = f.read()
    return gh_token.strip()

def touch(filepath):
    open(filepath, 'wb').close()

def git_new_branch(prid):
    branch_name = "pr{}".format(prid)
    filename = "pr{}.txt".format(prid)
    gitrepo = git.Repo(os.getcwd())

    origin = gitrepo.remote(name="origin")

    # create new head and get it tracked in the origin
    gitrepo.head.reference = gitrepo.create_head(branch_name)
    gitrepo.head.reference.set_tracking_branch(origin.refs.master).checkout()

    # create a file for the purposes of this example
    touch(filename)

    # stage the changed file and commit it
    gitrepo.index.add([filename])
    gitrepo.index.commit("Adding " + filename + "to repo")

    # push the staged commits
    push_res = origin.push(branch_name)[0]
    print(push_res.summary)

    getattr(gitrepo.heads, 'master').checkout()

    return branch_name

def ClickOnXPath(driver, project, ID, xpath):
    driver.get("https://github.com/Kokan/github-fmbt/pull/{}".format(ID))
    elem = driver.find_element_by_xpath(xpath)

    elem.click()

def ClosePR(driver, project, ID):
    sh.gh.pr.close(ID, _env=get_env())

def Open2Draft(driver, project, ID):
    ClickOnXPath(driver, project, ID, '/html/body/div[4]/div/main/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/form/div/details')
    for_sure = driver.find_element_by_xpath('/html/body/div[4]/div/main/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/form/div/details/details-dialog/div[3]/button')

    for_sure.click()
    time.sleep(1)

def MergePR(driver, project, ID):
    sh.gh.pr.merge(ID, '--merge', _env=get_env())

def Approve(driver, project, ID):
    sh.gh.pr.review(ID, '--approve', '--body', 'ok', _env=get_env())

def ChangeRequest(driver, project, ID):
    sh.gh.pr.review(ID, '--request-changes', '--body', 'nok', _env=get_env())

def ReopenPR(driver, project, ID):
    sh.gh.pr.reopen(ID, _env=get_env())

def Draft2Open(driver, project, ID):
    ClickOnXPath(driver, project, ID, '/html/body/div[4]/div/main/div[2]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[1]/form/button')
    time.sleep(1)

def OpenNewPR(driver, project):
    prid = get_next_pr_id(project)
    branch_name = git_new_branch(prid)
    github_new_pr(driver, project, branch_name)
    return prid

# driver=createDriver()
# ID=OpenNewPR(driver, "Kokan/github-fmbt")
# Open2Draft(driver, "Kokan/github-fmbt", ID)
# time.sleep(1)
# Draft2Open(driver, "Kokan/github-fmbt", ID)
# ClosePR(driver, "Kokan/github-fmbt", ID)
# driver.close()


