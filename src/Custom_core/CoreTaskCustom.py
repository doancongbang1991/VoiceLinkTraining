'''
Created on Dec 15, 2016

@author: BangDoan
'''
from core.CoreTask import CoreTask,REQUEST_CONFIG
from vocollect_core.utilities import obj_factory
from voice import globalwords as gw
from vocollect_core.utilities.localization import itext
from vocollect_core.dialog.functions import prompt_yes_no, prompt_only

class CoreTask_Custom(CoreTask):
    
    def request_configurations(self):
        ''' request core configuration LUT '''
        self.sign_off_allowed = True
        gw.words['change vehicle'].enabled = False
        gw.words['sign off'].enabled = False
        #gw.words['take a break'].enabled = False
        if not self._transmit_configuration():
            self.next_state = REQUEST_CONFIG
            
    def request_signon(self):
        self.password = None
        gw.words['sign off'].enabled = True
        
    def sign_off_confirm(self, allowed = False):
        ''' sign off with confirm '''
        if allowed or self.sign_off_allowed:
            if prompt_yes_no(itext('core.signoff.confirm'), False):
                self.sign_off()
        else:
            prompt_only(itext('core.signoff.not.allowed'))
            
    def request_breaks(self):
        pass
            
obj_factory.set_override(CoreTask, CoreTask_Custom)