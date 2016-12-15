'''
Created on Dec 15, 2016

@author: BangDoan
'''
from selection.PickPromptMultiple import PickPromptMultipleTask,SLOT_VERIFICATION
from vocollect_core.utilities import class_factory
from vocollect_core.dialog.functions import prompt_digits_required, prompt_only
from vocollect_core.utilities.localization import itext

PVID_VERYFICATION =  "pvidVerification"

class PickPromptMultipleTask_Custom(PickPromptMultipleTask):
    
    def initializeStates(self):
        super(PickPromptMultipleTask_Custom,self).initializeStates()
        self.addState(PVID_VERYFICATION, self.pvid_verification, SLOT_VERIFICATION)
    
    def pvid_verification(self):
        if self._pvid != '':
            result = prompt_digits_required(itext('selection.pick.prompt.pvid'), 
                                            itext('selection.pick.prompt.pvid.help'), 
                                            [self._pvid],
                                            [self._pick[0]['scannedPrcdID']], 
                                            {'skip slot' : False})
        if result[0] == 'skip slot':
            self.next_state = PVID_VERYFICATION
            self._skip_slot()
            
    def _verify_product_slot(self, result, is_scanned):
        '''Verifies product/slot depending on spoken check digit or spoken/scanned pvid or ready spoken'''
        #if ready is spoken and check digits is not blank prompt for check digit
        if result == 'ready' and self._picks[0]["checkDigits"] != '':
            prompt_only(itext('selection.pick.prompt.speak.check.digit'), True)
            self.next_state = SLOT_VERIFICATION
        
        
    def slot_verification(self):
        '''Multiple Prompts''' 
        result = prompt_digits_required(self._picks[0]["slot"],
                                                    itext("selection.pick.prompt.checkdigit.help"), 
                                                    [self._picks[0]["checkDigits"], self._pvid], 
                                                    None, 
                                                    {'ready' : False, 'skip slot' : False})
        if result == 'skip slot':
            self.next_state = SLOT_VERIFICATION
            self._skip_slot()
        else:
            self._verify_product_slot(result, False)
class_factory.set_override(PickPromptMultipleTask, PickPromptMultipleTask_Custom)     