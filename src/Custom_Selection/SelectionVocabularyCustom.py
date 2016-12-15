'''
Created on Dec 15, 2016

@author: BangDoan
'''
from vocollect_core.utilities import class_factory
from vocollect_core.utilities.localization import itext
from vocollect_core.task.dynamic_vocabulary import Vocabulary
from selection.SelectionVocabulary import SelectionVocabulary
from vocollect_core.dialog.functions import prompt_only


class SelectionVocabulary_Custom(SelectionVocabulary):
    def __init__(self, runner):
        super(SelectionVocabulary_Custom,self).__init__(runner)
        
        self.vocabs['country code'] = Vocabulary('country code', self._country_code, False)
    
    def _valid(self, vocab):
        
        if vocab == 'country code':
            vocab = 'description'
        return super(SelectionVocabulary_Custom,self)._valid(vocab)
    def _country_code(self):
        cc = self.current_picks[0]['countryCode']
        if cc == '':
            prompt_only(itext('generic.not.available'), self.word.vocab)
        else:
            prompt_only(cc)
        return True
        
        
class_factory.set_override(SelectionVocabulary, SelectionVocabulary_Custom)     