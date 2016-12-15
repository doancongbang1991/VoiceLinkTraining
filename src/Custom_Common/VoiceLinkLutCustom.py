'''
Created on Dec 15, 2016

@author: BangDoan
'''
from common.VoiceLinkLut import VoiceLinkLut
from vocollect_core import class_factory
from pending_odrs import wait_for_pending_odrs
from vocollect_core.utilities.localization import itext
from vocollect_core.dialog.base_dialog import BaseDialog
import dialogs
from Globals import sign_off
from voice import globalwords as gw
from vocollect_core.dialog.functions import prompt_ready, prompt_words

class VoiceLinkLut_Custom(VoiceLinkLut):
    
    def do_transmit(self, *fields):
        ''' transmit method for LUT
            Parameters:
            *fields - variable number of fields to transmit
            
            return: Returns 0 if no error occurred, otherwise the error code
        '''
        
        #first check if any pending ODRs        
        wait_for_pending_odrs('VoiceLink')
        result = self._transmit(*fields)
    
        if result < 0:
            # turn off globals
            sign_off_current = gw.words['sign off'].enabled
            #take_a_break_current = gw.words['take a break'].enabled
            gw.words['sign off'].enabled = False
            #gw.words['take a break'].enabled = False
            message = itext('generic.errorContactingHost.prompt')

            #Disable dynamic vocabulary
            try:
                #Disable Dynamic Vocab for this prompt only
                BaseDialog.exclude_dynamic_vocab = True

                response = dialogs.prompt_ready(itext('generic.sayReadyTryAgain.prompt', message), 
                                                additional_vocab = {'sign off' : True})
                if response == 'sign off':
                    sign_off()
                    
            finally:
                # reset globals
                #gw.words['take a break'].enabled = take_a_break_current
                gw.words['sign off'].enabled = sign_off_current        

        return result
    
    def _process_error(self, error, message):
        ''' Protected method to process error codes. 
        Override if any special errors 
        
        Parameters:
                error - error code received
                message - message received
        returns: error code modified if handled
        '''
        # just return error if error is 0
        if error == 0:
            return error
        
        #save current state of globals
        sign_off_current = gw.words['sign off'].enabled
        #take_a_break_current = gw.words['take a break'].enabled

        try:
            #Disable globals
            gw.words['sign off'].enabled = False
            #gw.words['take a break'].enabled = False
            
            return_error = error
            if error == 99:
                #Disable Dynamic Vocab for this prompt only
                BaseDialog.exclude_dynamic_vocab = True
                
                prompt_ready(itext('generic.sayReady.prompt', message))
                return_error = 0
                
            elif error == 98:
                #Disable Dynamic Vocab for this prompt only
                BaseDialog.exclude_dynamic_vocab = True
                
                # Need to turn off the dynamic dialog; this is really the only place we need to do this right now
                # ...If we come up with a general need for this functionality, we should think about moving
                # ...this into the prompt as a input. --jgeisler
                spoken = prompt_words(itext('generic.error.say.sign.off.prompt', message), 
                                              False, {'sign off' : False})
                if spoken == 'sign off':
                    sign_off();
                    
            elif error > 0:
                #Disable Dynamic Vocab for this prompt only
                BaseDialog.exclude_dynamic_vocab = True

                spoken = prompt_ready(itext('generic.continue.prompt', message), 
                                              True, {'sign off' : True})
                if spoken == 'sign off':
                    sign_off();
        finally:
            #always re-enable globals before leaving function.
            gw.words['sign off'].enabled = sign_off_current
            #gw.words['take a break'].enabled = take_a_break_current
            
        return return_error

class_factory.set_override(VoiceLinkLut, VoiceLinkLut_Custom)

