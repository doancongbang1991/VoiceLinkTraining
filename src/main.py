import Custom_core.CoreTaskCustom #@UnusedImport
import Custom_Common.VoiceLinkLutCustom #@UnusedImport
import Custom_Selection.PickPromptMultipleCustom #@UnusedImport

from common.VoiceLinkLut import lut_def_files
lut_def_files.append('LUTDefinition_Custom.properties')
import multi_scan_fix

from core.VoiceLink import voicelink_startup

from vocollect_http.httpserver import server_startup
from httpserver_receiving import ReceivingVoiceAppHTTPServer


#dummy ODR to get ODR queue working on startup
from common.VoiceLinkLut import VoiceLinkOdr
from vocollect_core.utilities.localization import itext
from vocollect_core.utilities import obj_factory
from vocollect_core import scanning
from voice import get_voice_application_property
import voice
dummyODR = obj_factory.get(VoiceLinkOdr, 'dummy')

def main():
    itext('')
    
    # Enabling triggered scanning
    use_trigger_scan_vocab = get_voice_application_property('UseTriggerScanVocab')
     
    voice.log_message("Use Trigger scan vocab value is : "+use_trigger_scan_vocab)
    if use_trigger_scan_vocab == 'true':
        trigger_scan_timeout = int(get_voice_application_property('TriggerScanTimeout'))
        scanning.set_trigger_vocab('VLINK_SCAN_VOCAB')
        scanning.set_trigger_timeout(trigger_scan_timeout)
        
    server_startup(ReceivingVoiceAppHTTPServer)
    voicelink_startup()
    
    