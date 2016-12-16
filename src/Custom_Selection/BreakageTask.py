'''
Created on Dec 15, 2016

@author: BangDoan
'''
from vocollect_core.task.task import TaskBase
from vocollect_core.dialog.functions import prompt_ready, prompt_alpha_numeric,\
    prompt_yes_no, prompt_only, prompt_digits
from vocollect_core.utilities.localization import itext
from common.VoiceLinkLut import VoiceLinkLut
from vocollect_core.utilities import obj_factory
DUMMY = 'dummyState'
#state
GET_ITEM_NUMBER         = 'getItemNumber'
CONFIRM_ITEM_NUMBER     = 'confirmItemNumber'
GET_BROKEN_QUANTITY     = 'getBrokenQuantity'
TRANSMIT_BREAKAGE_DATA  = 'transmitBreakageData'

class BreakageTask(TaskBase):
    
    def __init__(self,pickLut, taskRunner = None, callingTask = None):
        
        super(BreakageTask,self).__init__(taskRunner, callingTask)
        
        self.name  = 'breakage'
        self._pickLut = pickLut
        self._breakageLut = obj_factory.get(VoiceLinkLut, 'prTaskLUTBreakage')
        
    def initializeStates(self):
        
        self.addState(GET_ITEM_NUMBER, self.getItemNumber)
        self.addState(CONFIRM_ITEM_NUMBER, self.confirmItemNumber)
        self.addState(GET_BROKEN_QUANTITY, self.getBrokenQuantity)
        self.addState(TRANSMIT_BREAKAGE_DATA, self.transmitBreakageData)
        
    def getItemNumber(self):
        self._itemNumber, is_scanned = prompt_alpha_numeric(#@UnusedVariable
                                                            itext('selection.breakage.item.number'),
                                                            itext('selection.breakage.item.number.help'),
                                                            1, 10, False, True)
        
    def confirmItemNumber(self):
        #prompt_ready('confirm item state')
        for self._match in self._pickLut:
            item, description = self._match['itemNumber'], self._match['description']
            if item == self._itemNumber and int(self._match['qtyPicked']) > 0:
                if not prompt_yes_no(itext('selection.breakage.confirm.item', item, description)):
                    prompt_only(itext('selection.breakage.abort'))
                    self.next_state = ''
                return
        
        prompt_ready(itext('selection.breakage.item.not.found'), self._itemNumber)
        self.next_state = GET_ITEM_NUMBER
        
    def getBrokenQuantity(self):
        self._breakageQty = prompt_digits(itext('selection.breakage.quantity'),
                                          itext('selection.breakage.quantity.help'),
                                          1,10,True,False)
        if int(self._breakageQty) == 0:
            prompt_only(itext('selection.breakage.abort'))
            self.next_state = ''
        else:
            pickedQty = self._match['qtyPicked']
            if int(self._breakageQty) > int(pickedQty):
                prompt_ready(itext('selection.breakage.quantity.too.large',
                                   self._breakageQty, pickedQty))
                self.next_state = self.current_state
    def transmitBreakageData(self):
        result = self._breakageLut.do_transmit(self._itemNumber, self._breakageQty)
        
        if result < 0:
            self.next_state = self.current_state
        elif result > 0:
            self.next_state = GET_ITEM_NUMBER
        
        
        
        
        
        
    def dummyState(self):
        prompt_ready('You are in the breakage task')