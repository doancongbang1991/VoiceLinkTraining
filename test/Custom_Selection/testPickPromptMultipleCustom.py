'''
Created on Dec 26, 2016

@author: BangDoan
'''
from BaseVLTestCase import BaseVLTestCase #@UnusedImport
import main #@UnusedImport

from voicelink_test.unit_tests.testSelection import testPickPrompt
from selection.PickPrompt import  INTIALIZE_PUT,\
    CHECK_TARGET_CONTAINER, SLOT_VERIFICATION, CASE_LABEL_CD, ENTER_QTY,\
    QUANTITY_VERIFICATION, LOT_TRACKING, WEIGHT_SERIAL, XMIT_PICKS,\
    CHECK_PARTIAL, CLOSE_TARGET_CONT, NEXT_STEP, CYCLE_COUNT, PUT_PROMPT
from Custom_Selection.PickPromptMultipleCustom import PVID_VERIFICATION

class taskPickPromptMultipleCustom(testPickPrompt.testMultiplePickPromptTask):
    
    def setUp(self):
        testPickPrompt.testMultiplePickPromptTask.setUp(self)
        
    def test_initializeStates(self):

        #only run in main classes
        if self._obj is not None:     
            #test name
            self.assertEquals(self._obj.name, 'pickPrompt')
    
            #test states
            self.assertEquals(self._obj.states[0], CHECK_TARGET_CONTAINER)
            self.assertEquals(self._obj.states[1], SLOT_VERIFICATION)
            self.assertEquals(self._obj.states[2], PVID_VERIFICATION)
            self.assertEquals(self._obj.states[3], CASE_LABEL_CD)
            self.assertEquals(self._obj.states[4], ENTER_QTY)
            self.assertEquals(self._obj.states[5], QUANTITY_VERIFICATION)
            self.assertEquals(self._obj.states[6], LOT_TRACKING)
            self.assertEquals(self._obj.states[7], INTIALIZE_PUT)
            self.assertEquals(self._obj.states[8], PUT_PROMPT)
            self.assertEquals(self._obj.states[9], WEIGHT_SERIAL)
            self.assertEquals(self._obj.states[10], XMIT_PICKS)
            self.assertEquals(self._obj.states[11], CHECK_PARTIAL)
            self.assertEquals(self._obj.states[12], CLOSE_TARGET_CONT)
            self.assertEquals(self._obj.states[13], NEXT_STEP)
            self.assertEquals(self._obj.states[14], CYCLE_COUNT)
            
            #test dynamic vocab set properly
            self.assertTrue(self._obj.name in self._obj.dynamic_vocab.pick_tasks)
            
    def test_no_pvid_available(self):
        '''
        This test verifies that no PVID is prompted if none exists
        
        '''
        #setup sample data so we have _picks initialized
        self._setup_put_data()
        
        #set the PVID to blank
        self._obj._pvid = ''
        #no next state -> we move linearly through this
        self._obj.next_state = None
        
        #execute the state (should do nothing)
        self._obj.pvid_verification()
        
        #we are just moving on to the next state
        self.assertEquals(self._obj.next_state, None)
        
        #no prompts were spoken
        self.validate_prompts()
#    def test_pvid_value_blank(self):
#        self._obj._pvid = ''
#        self._obj.runState(PVID_VERIFICATION)
#        
#        self.validate_prompts()
#        self.assertEqual(self._obj.next_state, None)
#     
    def test_pvid_available(self):
        '''
        This test verifies that the PVID has to be spoken to continue
        
        '''
        #setup sample data so we have _picks initialized
        self._setup_put_data()
        
        #set the PVID to a number
        self._obj._pvid = '123'
        
        #no next state -> we move linearly through this
        self._obj.next_state = None
        
        #that's what we'll say
        self.post_dialog_responses('123')
        
        #execute the state (should do nothing)
        self._obj.pvid_verification()
        
        #we are just moving on to the next state
        self.assertEquals(self._obj.next_state, None)
        
        #no prompts were spoken
        self.validate_prompts('PVID?')
        
    def test_pvid_skip_slot(self):
        ''' 
            this test verifies that skip slot works
            Once skip slot is kicked off, it is aborted since we are at the last slot...
            
            => Actual skip slot functionality is tested in standard...
        
        '''
        #setup sample data so we have _picks initialized
        self._setup_put_data()
        
        #set the PVID to a number
        self._obj._pvid = '123'
        
        #no next state -> we move linearly through this
        self._obj.next_state = None
        
        #that's what we'll say
        self.post_dialog_responses('skip slot')
        
        #execute the state (should do nothing)
        self._obj.pvid_verification()
        
        #we are just moving on to the next state
        self.assertEquals(self._obj.next_state, PVID_VERIFICATION)
        
        #no prompts were spoken
        self.validate_prompts('PVID?', 'Last slot, skip slot not allowed')
        