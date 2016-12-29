'''
Created on Dec 26, 2016

@author: BangDoan
'''

from vocollect_core.task.task_runner import TaskRunnerBase
from voice import globalwords as gw
from core.VehicleTask import VehicleTask



def changeVehicle():
    runner = TaskRunnerBase.get_main_runner()
    cur_task = runner.get_current_task()
    gw.words['change vehicle'].enabled = False
    
    #off you go
    cur_task.launch(VehicleTask(runner), cur_task.current_state)