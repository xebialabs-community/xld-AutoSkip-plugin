# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re

class AutoSkip(object):
    def __init__(self, phraseToSkip=""):
        self.skipPhrase = phraseToSkip
        self.task = ""

    def print_all_steps(self, theTask):
        step_ids = []
        self.task = theTask
        for phase_block in theTask.block.blocks:
            self.loop_through_block(phase_block.block, theTask.id)

    def loop_through_block(self, b, tid):
        if hasattr(b, "blocks"):
            for subBlock in b.blocks:
                self.check_for_steps(subBlock, tid)
        else:
            self.check_for_steps(b, tid)

    def check_for_steps(self, b, tid):
        if hasattr(b, "blocks"):
            self.loop_through_block(b, tid)
        else:
            step_block_state = task2.steps(tid, b.id)
            step_index = 0
            step_ids = []
            for st in step_block_state.steps:
                step_index += 1
                step_ids.append("%s_%s" % (b.id,step_index))
                bill = b.getDescription()
                if(self.scanForPhrase(st.getDescription())):
                    if st.getSkippable():
                        skipList = []
                        skipList.append("%s_%s" % (b.id,step_index))
                        task2.skip(self.task.id, skipList)
                        print "skipped %s" % st.getDescription()
                    else:
                        print "This step cannot be skipped %s" % st.getDescription()

    def scanForPhrase(self, description):
        phraseWChar = "(?i)%s" % self.skipPhrase
        x = re.findall(phraseWChar, description)
        if(len(x) and len(self.skipPhrase)):
            return True
        else:
            return False

    def start_deployment(self, packagePath, environmentPath, phraseToSkip = "", orchestrator = []):
       package = repository.read(packagePath)
       environment = repository.read(environmentPath)
       deploymentRef = deployment.prepareInitial(package.id, environment.id)
       depl = deployment.prepareAutoDeployeds(deploymentRef)
       if len(orchestrator):
           depl.deployedApplication.values['orchestrator'] = orchestrator
       self.task = deployment.createDeployTask(depl)
       if len(phraseToSkip):
           self.skipPhrase = phraseToSkip
           self.print_all_steps(self.task)
       deployit.startTaskAndWait(self.task.id)
