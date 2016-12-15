'''
Created on Dec 15, 2016

@author: BangDoan
'''
from vocollect_core.dialog.functions import prompt_ready
from vocollect_core.utilities.localization import itext
from selection.PickAssignment import PickAssignmentTask, PICK_ASSIGNMENT_AISLE
from vocollect_core.utilities import class_factory, obj_factory
from Custom_Selection.BreakageTask import BreakageTask
class PickAssignmentTask_Custom(PickAssignmentTask):
    def aisle(self):
        ''' directing to Aisle'''
        #if aisle is same as aisle don't prompt
        result = ''
        if self._pickList[0]["aisle"] != self._aisle_direction:
            if self._pickList[0]["aisle"] != '':
                result = prompt_ready(itext('selection.pick.assignment.aisle', 
                                                 self._pickList[0]["aisle"]), False,
                                                 {'breakage' : True,'skip aisle' : False})
                if result == 'skip aisle':
                    self.next_state = PICK_ASSIGNMENT_AISLE
                    self._skip_aisle()
                elif result == 'breakage':
                    self.launch(obj_factory.get(BreakageTask,self._picks_lut,self.taskRunner),self.current_state)

            if result != 'skip aisle':
                self._post_aisle_direction=''
                self._aisle_direction = self._pickList[0]["aisle"]
                
class_factory.set_override(PickAssignmentTask, PickAssignmentTask_Custom)