'''
Created on Dec 16, 2016

@author: BangDoan
'''
from BaseVLTestCase import BaseVLTestCase #@UnusedImport
import main #@UnusedImport
from voicelink_test.unit_tests.testCore import testCoreTask
from core.CoreTask import REQUEST_SIGNON,REQUEST_BREAKS
from voice import globalwords as gw
import unittest
from vocollect_core.task.task_runner import Launch


class testCoreTaskCustom(testCoreTask.testCoreTask):
    def test_request_breaks(self):
        self._obj.runState(REQUEST_BREAKS)
        self.assertEquals(self._obj.next_state, None)
        self.validate_server_requests()
        self.validate_prompts()
    
    def test_request_signon(self):
        self._obj.runState(REQUEST_SIGNON)
        self.assertEquals(self._obj.next_state, None)
        self.assertEquals(self._obj.password, None)
        self.assertEquals(gw.words['sign off'].enabled, True)
        self.validate_server_requests()
        self.validate_prompts()
    def test_sign_off_confirm(self):
        #TESLINK 95552 :: Test Case Verify Sign Off Global Word
        self.start_server()
        self._obj.password='123'
        self.post_dialog_responses('yes')
        self.assertRaises(Launch, self._obj.sign_off_confirm)
        self.assertEquals(self._obj.password, None)
        self.validate_prompts('Sign off, correct?')
        self.validate_server_requests(['prTaskLUTCoreSignOff'])
        
        self._obj.password=None
        self.post_dialog_responses('yes')
        self.assertRaises(Launch, self._obj.sign_off_confirm)
        self.assertEquals(self._obj.password, None)
        self.validate_prompts('Sign off, correct?')
        self.validate_server_requests(['prTaskLUTCoreSignOff'])
        
        self._obj.password='123'
        self.post_dialog_responses('no')
        self._obj.sign_off_confirm()
        self.assertEquals(self._obj.password, '123')
        self.validate_prompts('Sign off, correct?')
        self.validate_server_requests()
       
        self._obj.password='123'
        self.post_dialog_responses('yes', 'ready')
        self.set_server_response('99,error message\n\n')
        self.assertRaises(Launch, self._obj.sign_off_confirm)
        self.assertEquals(self._obj.password, None)
        self.validate_prompts('Sign off, correct?',
                              'error message, say ready')
        self.validate_server_requests(['prTaskLUTCoreSignOff'])
       
        self._obj.password='123'
        self.post_dialog_responses('yes', 'ready')
        self.set_server_response('199,test error\n\n')
        self.set_server_response('0,\n\n')
        self.assertRaises(Launch, self._obj.sign_off_confirm)
        self.assertEquals(self._obj.password, None)
        self.validate_prompts('Sign off, correct?',
                              'test error, To continue say ready')
        self.validate_server_requests(['prTaskLUTCoreSignOff'],
                                      ['prTaskLUTCoreSignOff'])
        #---------------------------------------------------------------        
        #sign off not allowed
        self._obj.password='123'
        self._obj.sign_off_allowed = False
        self.post_dialog_responses()
        self.set_server_response('0,\n\n')
        self._obj.sign_off_confirm()
        
        self.assertEquals(self._obj.password, '123')
        self.validate_prompts('Sign off not allowed.')
        self.validate_server_requests()
        #---------------------------------------------------------------        
        #sign off not allowed, override
        self._obj.password='123'
        self._obj.sign_off_allowed = False
        self.post_dialog_responses('no')
        self.set_server_response('0,\n\n')
        self._obj.sign_off_confirm(True)
        
        self.assertEquals(self._obj.password, '123')
        self.validate_prompts('Sign off, correct?')
        self.validate_server_requests()