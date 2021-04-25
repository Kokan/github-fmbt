import os
from git_adapter import *
import aalmodel
class _gen_github(aalmodel.AALModel):
    def __init__(self):
        aalmodel.AALModel.__init__(self, globals())
    adapter_init_list = []
    initial_state_list = []
    adapter_exit_list = []
    push_variables_set = set()

    def initial_state1():
        global state, approved, SUT
        state = PRState.NONE
        approved = 0
        pass
    initial_state1.func_code = aalmodel.setCodeFileLine(initial_state1.func_code, '''github.aal''', 7)
    initial_state_list.append(initial_state1)
    push_variables_set.update(initial_state1.func_code.co_names)

    def adapter_init1():
        global state, approved, SUT
        log("Start")
        SUT=GithubPR("Kokan/github-fmbt")
        return 1
    adapter_init1.func_code = aalmodel.setCodeFileLine(adapter_init1.func_code, '''github.aal''', 11)
    adapter_init_list.append(adapter_init1)

    def adapter_exit1(verdict,reason):
        global state, approved, SUT
        if verdict == "pass":
           log("PASS")
        log("cleaning up ")
        pass
    adapter_exit1.func_code = aalmodel.setCodeFileLine(adapter_exit1.func_code, '''github.aal''', 15)
    adapter_exit_list.append(adapter_exit1)

    action1name = "i:Open new PR"
    action1type = "input"
    def action1guard():
        global state, approved, SUT
        action_name = "i:Open new PR"
        input_name ="Open new PR"
        action_index = 0
        return (state in [PRState.NONE, PRState.CLOSED, PRState.MERGED])
    action1guard.requires = []
    action1guard.func_code = aalmodel.setCodeFileLine(action1guard.func_code, '''github.aal''', 17, "guard of action \"i:Open new PR\"")
    def action1body():
        global state, approved, SUT
        action_name = "i:Open new PR"
        input_name ="Open new PR"
        action_index = 0
        state = PRState.OPEN
        approved = 0
    action1body.func_code = aalmodel.setCodeFileLine(action1body.func_code, '''github.aal''', 23, "body of action \"i:Open new PR\"")
    def action1adapter():
        global state, approved, SUT
        action_name = "i:Open new PR"
        input_name ="Open new PR"
        action_index = 0
        prid = SUT.OpenNewPR()
        log("Create PR {}".format(p))
        return 1
    action1adapter.func_code = aalmodel.setCodeFileLine(action1adapter.func_code, '''github.aal''', 19, "adapter of action \"i:Open new PR\"")

    action2name = "i:Merge PR"
    action2type = "input"
    def action2guard():
        global state, approved, SUT
        action_name = "i:Merge PR"
        input_name ="Merge PR"
        action_index = 0
        return ((state == PRState.OPEN) and (approved>0))
    action2guard.requires = []
    action2guard.func_code = aalmodel.setCodeFileLine(action2guard.func_code, '''github.aal''', 28, "guard of action \"i:Merge PR\"")
    def action2body():
        global state, approved, SUT
        action_name = "i:Merge PR"
        input_name ="Merge PR"
        action_index = 0
        state = PRState.MERGED
    action2body.func_code = aalmodel.setCodeFileLine(action2body.func_code, '''github.aal''', 33, "body of action \"i:Merge PR\"")
    def action2adapter():
        global state, approved, SUT
        action_name = "i:Merge PR"
        input_name ="Merge PR"
        action_index = 0
        log("Merge PR")
        SUT.MergePR()
        return 2
    action2adapter.func_code = aalmodel.setCodeFileLine(action2adapter.func_code, '''github.aal''', 30, "adapter of action \"i:Merge PR\"")

    action3name = "i:Close PR"
    action3type = "input"
    def action3guard():
        global state, approved, SUT
        action_name = "i:Close PR"
        input_name ="Close PR"
        action_index = 0
        return state == PRState.OPEN
    action3guard.requires = []
    action3guard.func_code = aalmodel.setCodeFileLine(action3guard.func_code, '''github.aal''', 36, "guard of action \"i:Close PR\"")
    def action3body():
        global state, approved, SUT
        action_name = "i:Close PR"
        input_name ="Close PR"
        action_index = 0
        state = PRState.CLOSED
    action3body.func_code = aalmodel.setCodeFileLine(action3body.func_code, '''github.aal''', 41, "body of action \"i:Close PR\"")
    def action3adapter():
        global state, approved, SUT
        action_name = "i:Close PR"
        input_name ="Close PR"
        action_index = 0
        log("Close PR")
        SUT.ClosePR()
        return 3
    action3adapter.func_code = aalmodel.setCodeFileLine(action3adapter.func_code, '''github.aal''', 38, "adapter of action \"i:Close PR\"")

    action4name = "i:Reopen PR"
    action4type = "input"
    def action4guard():
        global state, approved, SUT
        action_name = "i:Reopen PR"
        input_name ="Reopen PR"
        action_index = 0
        return state == PRState.CLOSED
    action4guard.requires = []
    action4guard.func_code = aalmodel.setCodeFileLine(action4guard.func_code, '''github.aal''', 44, "guard of action \"i:Reopen PR\"")
    def action4body():
        global state, approved, SUT
        action_name = "i:Reopen PR"
        input_name ="Reopen PR"
        action_index = 0
        state = PRState.OPEN
    action4body.func_code = aalmodel.setCodeFileLine(action4body.func_code, '''github.aal''', 49, "body of action \"i:Reopen PR\"")
    def action4adapter():
        global state, approved, SUT
        action_name = "i:Reopen PR"
        input_name ="Reopen PR"
        action_index = 0
        log("Reopen PR")
        SUT.ReopenPR()
        return 4
    action4adapter.func_code = aalmodel.setCodeFileLine(action4adapter.func_code, '''github.aal''', 46, "adapter of action \"i:Reopen PR\"")

    action5name = "i:Change PR to Draft"
    action5type = "input"
    def action5guard():
        global state, approved, SUT
        action_name = "i:Change PR to Draft"
        input_name ="Change PR to Draft"
        action_index = 0
        return state == PRState.OPEN
    action5guard.requires = []
    action5guard.func_code = aalmodel.setCodeFileLine(action5guard.func_code, '''github.aal''', 52, "guard of action \"i:Change PR to Draft\"")
    def action5body():
        global state, approved, SUT
        action_name = "i:Change PR to Draft"
        input_name ="Change PR to Draft"
        action_index = 0
        state = PRState.DRAFT
    action5body.func_code = aalmodel.setCodeFileLine(action5body.func_code, '''github.aal''', 57, "body of action \"i:Change PR to Draft\"")
    def action5adapter():
        global state, approved, SUT
        action_name = "i:Change PR to Draft"
        input_name ="Change PR to Draft"
        action_index = 0
        log("Change PR to Draft")
        SUT.Open2Draft()
        return 5
    action5adapter.func_code = aalmodel.setCodeFileLine(action5adapter.func_code, '''github.aal''', 54, "adapter of action \"i:Change PR to Draft\"")

    action6name = "i:Change PR to Open"
    action6type = "input"
    def action6guard():
        global state, approved, SUT
        action_name = "i:Change PR to Open"
        input_name ="Change PR to Open"
        action_index = 0
        return state == PRState.DRAFT
    action6guard.requires = []
    action6guard.func_code = aalmodel.setCodeFileLine(action6guard.func_code, '''github.aal''', 60, "guard of action \"i:Change PR to Open\"")
    def action6body():
        global state, approved, SUT
        action_name = "i:Change PR to Open"
        input_name ="Change PR to Open"
        action_index = 0
        state = PRState.OPEN
    action6body.func_code = aalmodel.setCodeFileLine(action6body.func_code, '''github.aal''', 65, "body of action \"i:Change PR to Open\"")
    def action6adapter():
        global state, approved, SUT
        action_name = "i:Change PR to Open"
        input_name ="Change PR to Open"
        action_index = 0
        log("Change PR to Open")
        SUT.Draft2Open()
        return 6
    action6adapter.func_code = aalmodel.setCodeFileLine(action6adapter.func_code, '''github.aal''', 62, "adapter of action \"i:Change PR to Open\"")

    action7name = "i:Approve"
    action7type = "input"
    def action7guard():
        global state, approved, SUT
        action_name = "i:Approve"
        input_name ="Approve"
        action_index = 0
        return state == PRState.OPEN
    action7guard.requires = []
    action7guard.func_code = aalmodel.setCodeFileLine(action7guard.func_code, '''github.aal''', 68, "guard of action \"i:Approve\"")
    def action7body():
        global state, approved, SUT
        action_name = "i:Approve"
        input_name ="Approve"
        action_index = 0
        approved = min(1,approved+1)
    action7body.func_code = aalmodel.setCodeFileLine(action7body.func_code, '''github.aal''', 73, "body of action \"i:Approve\"")
    def action7adapter():
        global state, approved, SUT
        action_name = "i:Approve"
        input_name ="Approve"
        action_index = 0
        log("Approve")
        SUT.Approve()
        return 7
    action7adapter.func_code = aalmodel.setCodeFileLine(action7adapter.func_code, '''github.aal''', 70, "adapter of action \"i:Approve\"")

    action8name = "i:Change request"
    action8type = "input"
    def action8guard():
        global state, approved, SUT
        action_name = "i:Change request"
        input_name ="Change request"
        action_index = 0
        return state == PRState.OPEN
    action8guard.requires = []
    action8guard.func_code = aalmodel.setCodeFileLine(action8guard.func_code, '''github.aal''', 76, "guard of action \"i:Change request\"")
    def action8body():
        global state, approved, SUT
        action_name = "i:Change request"
        input_name ="Change request"
        action_index = 0
        approved = 0
    action8body.func_code = aalmodel.setCodeFileLine(action8body.func_code, '''github.aal''', 81, "body of action \"i:Change request\"")
    def action8adapter():
        global state, approved, SUT
        action_name = "i:Change request"
        input_name ="Change request"
        action_index = 0
        log("Change request")
        SUT.ChangeRequest()
        return 8
    action8adapter.func_code = aalmodel.setCodeFileLine(action8adapter.func_code, '''github.aal''', 78, "adapter of action \"i:Change request\"")

    tag1name = "Open"
    def tag1guard():
        global state, approved, SUT
        tag_name = "Open"
        return (state == PRState.OPEN) and (0 == approved)
    tag1guard.requires=[]
    tag1guard.func_code = aalmodel.setCodeFileLine(tag1guard.func_code, '''github.aal''', 87, "guard of tag \"Open\"")
    def tag1adapter():
        global state, approved, SUT
        tag_name = "Open"
        assert SUT.GetPRStatus() == PRState.OPEN
    tag1adapter.func_code = aalmodel.setCodeFileLine(tag1adapter.func_code, '''github.aal''', 88, "adapter of tag \"Open\"")

    tag2name = "Ready to merge"
    def tag2guard():
        global state, approved, SUT
        tag_name = "Ready to merge"
        return ((approved>0) and (state == PRState.OPEN))
    tag2guard.requires=[]
    tag2guard.func_code = aalmodel.setCodeFileLine(tag2guard.func_code, '''github.aal''', 91, "guard of tag \"Ready to merge\"")
    def tag2adapter():
        global state, approved, SUT
        tag_name = "Ready to merge"
        assert SUT.isReady2Merge()
    tag2adapter.func_code = aalmodel.setCodeFileLine(tag2adapter.func_code, '''github.aal''', 92, "adapter of tag \"Ready to merge\"")

    tag3name = "Closed"
    def tag3guard():
        global state, approved, SUT
        tag_name = "Closed"
        return state == PRState.CLOSED
    tag3guard.requires=[]
    tag3guard.func_code = aalmodel.setCodeFileLine(tag3guard.func_code, '''github.aal''', 95, "guard of tag \"Closed\"")
    def tag3adapter():
        global state, approved, SUT
        tag_name = "Closed"
        assert SUT.GetPRStatus() == PRState.CLOSED
    tag3adapter.func_code = aalmodel.setCodeFileLine(tag3adapter.func_code, '''github.aal''', 96, "adapter of tag \"Closed\"")

    tag4name = "Merged"
    def tag4guard():
        global state, approved, SUT
        tag_name = "Merged"
        return state == PRState.MERGED
    tag4guard.requires=[]
    tag4guard.func_code = aalmodel.setCodeFileLine(tag4guard.func_code, '''github.aal''', 99, "guard of tag \"Merged\"")
    def tag4adapter():
        global state, approved, SUT
        tag_name = "Merged"
        assert SUT.GetPRStatus() == PRState.MERGED
    tag4adapter.func_code = aalmodel.setCodeFileLine(tag4adapter.func_code, '''github.aal''', 100, "adapter of tag \"Merged\"")

    tag5name = "Draft"
    def tag5guard():
        global state, approved, SUT
        tag_name = "Draft"
        return state == PRState.DRAFT
    tag5guard.requires=[]
    tag5guard.func_code = aalmodel.setCodeFileLine(tag5guard.func_code, '''github.aal''', 103, "guard of tag \"Draft\"")
    def tag5adapter():
        global state, approved, SUT
        tag_name = "Draft"
        assert SUT.GetPRStatus() == PRState.DRAFT
    tag5adapter.func_code = aalmodel.setCodeFileLine(tag5adapter.func_code, '''github.aal''', 104, "adapter of tag \"Draft\"")
    def adapter_init():
        for x in _gen_github.adapter_init_list:
            ret = x()
            if not ret and ret != None:
                return ret
        return True
    def initial_state():
        for x in _gen_github.initial_state_list:
            ret = x()
            if not ret and ret != None:
                return ret
        return True
    def adapter_exit(verdict,reason):
        for x in _gen_github.adapter_exit_list:
            ret = x(verdict,reason)
            if not ret and ret != None:
                return ret
        return True

Model = _gen_github
