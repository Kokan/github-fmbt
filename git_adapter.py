#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pickle
import time
import os

from urllib2 import urlopen
from json import loads


import git

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

def github_open(driver, project):
    driver.get("https://github.com/" + project)

    pr = driver.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[1]/nav/ul/li[3]/a/span[1]')
    pr.click()

    time.sleep(2)

def github_new_pr(driver, project, branch_name):
    driver.get("https://github.com/{}/pull/new/{}".format(project, branch_name))

    time.sleep(2)

    newpr = driver.find_element_by_xpath('/html/body/div[4]/div/main/div[2]/div/div[4]/form/div/div[1]/div/div[2]/div/div[2]/div')
    newpr.click()


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
    gitrepo.index.commit("Adding "+filename+ "to repo")

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
    ClickOnXPath(driver, project, ID, '/html/body/div[4]/div/main/div[2]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div[2]/form/div/div/div/div[1]/button')

def Open2Draft(driver, project, ID):
    ClickOnXPath(driver, project, ID, '/html/body/div[4]/div/main/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/form/div/details')
    for_sure = driver.find_element_by_xpath('/html/body/div[4]/div/main/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/form/div/details/details-dialog/div[3]/button')

    for_sure.click()
    time.sleep(1)

def Draft2Open(driver, project, ID):
    ClickOnXPath(driver, project, ID, '/html/body/div[4]/div/main/div[2]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/div/div[1]/form/button')
    time.sleep(1)

def OpenNewPR(driver, project):
    prid = get_next_pr_id(project)
    branch_name=git_new_branch(prid)
    github_open(driver, project)
    github_new_pr(driver, project, branch_name)
    return prid

#driver=createDriver()
#ID=OpenNewPR(driver, "Kokan/github-fmbt")
#Open2Draft(driver, "Kokan/github-fmbt", ID)
#time.sleep(1)
#Draft2Open(driver, "Kokan/github-fmbt", ID)
#ClosePR(driver, "Kokan/github-fmbt", ID)
#driver.close()


