'''
Created on Dec 26, 2016

@author: BangDoan
'''
from core.VehicleTask import VehicleTask
from vocollect_core.utilities import class_factory
from voice import globalwords as gw


class VehicleTask_Custom(VehicleTask):
    def execute(self):
        super(VehicleTask, self).execute()
        gw.words['change vehicle'].enabled = True


class_factory.set_override(VehicleTask, VehicleTask_Custom)