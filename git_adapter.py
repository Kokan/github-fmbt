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

def get_next_pr_id_gen(project):
    prid = get_free_pr_slot(project)
    while True:
        yield prid
        prid += 1

def get_free_pr_slot(project):
    API = "https://api.github.com/repos/{}/issues?state=all&sort=created&direction=desc".format(project)

    raw_response = urlopen(API).read().decode("utf-8")
    json_response = loads(raw_response)
    issues = list(json_response)
    last_id = int(issues[0]["number"])

    return last_id + 1

def createDriver():
    return GithubPR("Kokan/github-fmbt")

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
    filename = "tmp/pr{}.txt".format(prid)
    gitrepo = git.Repo(os.getcwd())

    origin = gitrepo.remote(name="origin")

    # create new head and get it tracked in the origin
    reference = gitrepo.create_head(branch_name)
    reference.set_tracking_branch(origin.refs.master).checkout()

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

class GithubPR:
    def __init__(self, project):
        self.__createDriver()
        self.project = project
        self.prid = None
        self.prid_generator = get_next_pr_id_gen(project)

    def __del__(self):
        self.driver.close()

    def __ClickOnXPath(self, xpath):
        self.driver.get("https://github.com/{}/pull/{}".format(self.project, self.prid))
        elem = self.driver.find_element_by_xpath(xpath)

        elem.click()

    def __ClickOnText(self, text):
        self.__ClickOnXPath("//*[text() = '{}']".format(text))

    def __get_next_pr_id(self):
        return next(self.prid_generator)

    def OpenNewPR(self):
        self.prid = self.__get_next_pr_id()
        branch_name = git_new_branch(self.prid)
        github_new_pr(self.driver, self.project, branch_name)
        return self.prid

    def ClosePR(self):
        sh.gh.pr.close(self.prid, _env=get_env())

    def Open2Draft(self):
        self.__ClickOnText("Convert to draft")
        for_sure = self.driver.find_element_by_xpath("//*[contains(@class, 'js-convert-to-draft')]")

        for_sure.click()
        time.sleep(1)

    def MergePR(self):
        sh.gh.pr.merge(self.prid, '--merge', _env=get_env())

    def Approve(self):
        sh.gh.pr.review(self.prid, '--approve', '--body', 'ok', _env=get_env())

    def ChangeRequest(self):
        sh.gh.pr.review(self.prid, '--request-changes', '--body', 'nok', _env=get_env())

    def ReopenPR(self):
        sh.gh.pr.reopen(self.prid, _env=get_env())

    def Draft2Open(self):
        self.__ClickOnText('Ready for review')
        time.sleep(1)

    def __hasText(self, text):
        self.driver.get("https://github.com/{}/pull/{}".format(self.project, self.prid))
        return text in self.driver.page_source

    def GetPRStatus(self):
        isDraft=self.__hasText("Draft pull requests")
        if isDraft:
            return 1 #Draft

        isClosed=self.__hasText("Closed with unmerged commits")
        if isClosed:
            return 3 #Closed

        isOpen=self.__hasText("Close pull request")
        if isOpen:
            return 2 #Open

        isMerged=self.__hasText("Merged")
        if isMerged:
            return 4 #Merged

        return 0 #None

    def isReady2Merge(self):
        mergeBlocked=self.__hasText("Merging is blocked")
        changeRequest=self.__hasText("Changes requested")
        changeApproved=self.__hasText("Changes approved")

        return not mergeBlocked and not changeRequest and changeApproved

    def __createDriver(self):
        options = Options()
        options.add_argument("user-data-dir=/tmp/github-fmbt")
        self.driver = webdriver.Chrome(chrome_options=options)

