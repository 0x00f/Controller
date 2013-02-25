# -*- coding: iso-8859-1 -*-
# Don't modify comment 
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       (c) Navin Bhaskar 2013


"""
@file       MyDlg.py
@author     Navin Bhaskar
@brief      Describes the dialog frame
"""


import wx
import wx.gizmos
#[inc]add your include files here
from TransLayer import TransLayer
import ControllerExceptions
import sys
from ConfigHandler import ConfigHandler
#[inc]end your include

class MyDlg(wx.Frame):
    def __init__(self,parent,conf_file='conf.txt',id = -1,title = '',pos = wx.Point(0,0),size = wx.Size(495,550),style = wx.DEFAULT_DIALOG_STYLE,name = 'dialogBox'):
        #pre=wx.PreDialog()
        self.OnPreCreate()
        
        try:
            self.conf = ConfigHandler(conf_file)
        except IOError:
            wx.MessageBox("Could not find the config file, %s" %conf_file)
            self.__del__()
            sys.exit(1)
            
        board = self.conf.getBoard()
        #pre.Create(parent,id,title + ' ' + board,pos,size,wx.CAPTION|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.CLOSE_BOX|wx.DIALOG_NO_PARENT|wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX,name)
        wx.Frame.__init__(self, parent, id,title + ' ' + board,pos,size,wx.CAPTION|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.CLOSE_BOX|wx.MINIMIZE_BOX,name)
        self.statusBar = self.CreateStatusBar()
        #self.PostCreate(pre)
        self.initBefore()
        self.VwXinit()
        self.initAfter()

    def __del__(self):
        self.Ddel()
        return


    def VwXinit(self):
        self.main_pannel = wx.Panel(self,-1,wx.Point(-5,0),wx.Size(609,493))
        self.DigiOpPin = wx.StaticBox(self.main_pannel,-1,"",wx.Point(10,100),wx.Size(468,71))
        self.DigiOpPin.SetLabel('Digital output pins')
        digi_pins = self.conf.getDigiPinNames()
        self.cmbDigiOpPins = wx.ComboBox(self.main_pannel,-1,"",wx.Point(125,125),wx.Size(80,21),digi_pins,wx.CB_READONLY)
        self.cmbDigiOpPins.SetLabel("Select Pin")
        self.stDigitalOut = wx.StaticText(self.main_pannel,-1,"",wx.Point(25,125),wx.Size(99,13),wx.ST_NO_AUTORESIZE)
        self.stDigitalOut.SetLabel("Select a Digital Pin")
        self.btDigiOutSet = wx.Button(self.main_pannel,-1,"",wx.Point(380,120),wx.Size(85,30))
        self.btDigiOutSet.SetLabel("Set")
        self.Bind(wx.EVT_BUTTON,self.OnDigiSet,self.btDigiOutSet)
        self.stDigiOpSelState = wx.StaticText(self.main_pannel,-1,"",wx.Point(220,125),wx.Size(69,13),wx.ST_NO_AUTORESIZE)
        self.stDigiOpSelState.SetLabel("Select State")
        self.cmbHighLow = wx.ComboBox(self.main_pannel,-1,"",wx.Point(290,125),wx.Size(65,21),[r'High',r'Low'],wx.CB_READONLY)
        self.cmbHighLow.SetLabel("State")
        self.sbDigigInpPins = wx.StaticBox(self.main_pannel,-1,"",wx.Point(10,190),wx.Size(463,76))
        self.sbDigigInpPins.SetLabel('Digital Input Pins')
        self.stDigiOutPin = wx.StaticText(self.main_pannel,-1,"",wx.Point(25,225),wx.Size(94,13),wx.ST_NO_AUTORESIZE)
        self.stDigiOutPin.SetLabel("Select a Digital Pin")
        self.cmbSerPort = wx.ComboBox(self.main_pannel,-1,"",wx.Point(120,35),wx.Size(145,21),[],wx.CB_READONLY)
        self.cmbSerPort.SetLabel("Select Pin")
        self.btOpenPrt = wx.Button(self.main_pannel,-1,"",wx.Point(285,30),wx.Size(85,30))
        self.btOpenPrt.SetLabel("Open")
        self.Bind(wx.EVT_BUTTON,self.OnOpenPrt,self.btOpenPrt)
        self.ledPinState = wx.gizmos.LEDNumberCtrl(self.main_pannel,-1,wx.Point(350,220),wx.Size(70,40))
        self.sbAnalogOut = wx.StaticBox(self.main_pannel,-1,"",wx.Point(10,290),wx.Size(463,86))
        self.sbAnalogOut.SetLabel('Analog Out')
        self.stAnIn = wx.StaticText(self.main_pannel,-1,"",wx.Point(20,420),wx.Size(104,13),wx.ST_NO_AUTORESIZE)
        self.stAnIn.SetLabel("Select an Analog pin")
        self.cmbAnalogOut = wx.ComboBox(self.main_pannel,-1,"",wx.Point(125,325),wx.Size(80,21),self.conf.getAnaOutPinNames(),wx.CB_READONLY)
        self.cmbAnalogOut.SetLabel("Select pin")
        self.txAnalogOut = wx.TextCtrl(self.main_pannel,-1,"",wx.Point(300,320),wx.Size(60,21))
        self.stAnoutVal = wx.StaticText(self.main_pannel,-1,"",wx.Point(225,325),wx.Size(69,13),wx.ST_NO_AUTORESIZE)
        self.stAnoutVal.SetLabel("Enter a value")
        self.btAnalogOut = wx.Button(self.main_pannel,-1,"",wx.Point(370,315),wx.Size(85,30))
        self.btAnalogOut.SetLabel("Set")
        self.Bind(wx.EVT_BUTTON,self.OnAnaSet,self.btAnalogOut)
        self.sbAnalogIn = wx.StaticBox(self.main_pannel,-1,"",wx.Point(10,390),wx.Size(463,81))
        self.sbAnalogIn.SetLabel('Analog In')
        self.stSelAnOut = wx.StaticText(self.main_pannel,-1,"",wx.Point(20,325),wx.Size(104,13),wx.ST_NO_AUTORESIZE)
        self.stSelAnOut.SetLabel("Select an Analog pin")
        self.cmbAnalogIn = wx.ComboBox(self.main_pannel,-1,"",wx.Point(125,420),wx.Size(80,21),self.conf.getAnaInPinNames(),wx.CB_READONLY)
        self.cmbAnalogIn.SetLabel("Select pin")
        self.btAnalogRead = wx.Button(self.main_pannel,-1,"",wx.Point(225,415),wx.Size(85,30))
        self.btAnalogRead.SetLabel("Read")
        self.Bind(wx.EVT_BUTTON,self.OnAnaRead,self.btAnalogRead)
        self.ledAnalogRead = wx.gizmos.LEDNumberCtrl(self.main_pannel,-1,wx.Point(350,415),wx.Size(75,40))
        self.SerPort = wx.StaticBox(self.main_pannel,-1,"",wx.Point(10,10),wx.Size(468,71))
        self.SerPort.SetLabel('Serial port selection')
        self.stSelPort = wx.StaticText(self.main_pannel,-1,"",wx.Point(20,35),wx.Size(100,13),wx.ST_NO_AUTORESIZE)
        self.stSelPort.SetLabel("Select a serial port")
        self.cmbDigiRead = wx.ComboBox(self.main_pannel,-1,"",wx.Point(125,225),wx.Size(80,21),digi_pins,wx.CB_READONLY)
        self.cmbDigiRead.SetLabel("Select Pin")
        self.btClosePrt = wx.Button(self.main_pannel,-1,"",wx.Point(385,30),wx.Size(85,30))
        self.btClosePrt.SetLabel("Close")
        self.Bind(wx.EVT_BUTTON,self.OnClosePrt,self.btClosePrt)
        self.btDigiRead = wx.Button(self.main_pannel,-1,"",wx.Point(225,220),wx.Size(85,30))
        self.btDigiRead.SetLabel("Read")
        self.Bind(wx.EVT_BUTTON,self.OnDigiRead,self.btDigiRead)
        self.Refresh()
        return
    def VwXDelComp(self):
        return

#[win]add your code here

    def OnOpenPrt(self,event): #init function
        #[51e]Code event VwX...Don't modify[51e]#
        #add your code here
        
        ser_prt = self.cmbSerPort.GetValue().encode('ASCII')
        if (ser_prt == ""):
            return 
        # lets try and create a TransLayer object
        try:
          self.ArdCtrl = TransLayer(ser_prt, self.conf.getVref(), self.conf.getRes())
          self.btOpenPrt.Enable(False)
          self.btClosePrt.Enable(True)
          self.btDigiOutSet.Enable(True)
          self.btDigiRead.Enable(True)
          self.btAnalogOut.Enable(True)
          self.btAnalogRead.Enable(True)
        except IOError, error:
          err = str(error)
          wx.MessageBox(err+"\n Application exiting...")
          sys.exit(1)
          
        return #end function

    def OnClosePrt(self,event): #init function
        #[521]Code event VwX...Don't modify[521]#
        #add your code here

        self.ArdCtrl.Stop()
        self.btOpenPrt.Enable(True)
        self.btClosePrt.Enable(False)
        self.btDigiOutSet.Enable(False)
        self.btDigiRead.Enable(False)
        self.btAnalogOut.Enable(False)
        self.btAnalogRead.Enable(False)
        return #end function


    def OnDigiRead(self,event): #init function
        #[174]Code event VwX...Don't modify[174]#
        #add your code here
        
        pin = self.cmbDigiRead.GetValue()
        
        if pin == "" :
          return
        
        pin_no = self.conf.getDigiPinValue(pin)
        
        val = self.ArdCtrl.ReadPin(pin_no)
        if (val[0] == False):
          wx.MessageBox("Could not retreive information")
          return
        
        self.ledPinState.SetValue(str(val[1]))

        return #end function

    def OnAnaSet(self,event): #init function
        #[175]Code event VwX...Don't modify[175]#
        #add your code here
        
        ana = self.cmbAnalogOut.GetValue()
        
        
        
        ana_val = self.txAnalogOut.GetValue()
        
        if ana == '' or ana_val == '':
          return
        
        ana_pin = self.conf.getAnaOutPinValue(ana)
        ana_val = int(ana_val)
        
        maxAout = self.conf.getAoutMax()
        if ana_val < 0 or ana_val > maxAout:
          wx.MessageBox("Analog output value must be in the range 0 and %d" %maxAout)
          return
        
        self.ArdCtrl.SetAnalogVal(ana_pin, ana_val)

        return #end function

    def OnAnaRead(self,event): #init function
        #[176]Code event VwX...Don't modify[176]#
        #add your code here
        
        ana = self.cmbAnalogIn.GetValue()
        
        if ana == '':
          return
        
        ana_pin = self.conf.getAnaInPinValue(ana)
        ana_val = self.ArdCtrl.ReadAnalogVal(ana_pin)
        
        if ana_val[0] == False:
          wx.MessageBox("Could not read analog value ")
          return
        
        vltg = str(ana_val[1])
        
        self.ledAnalogRead.SetValue(vltg)

        return #end function


    def OnDigiSet(self,event): #init function
        #[234]Code event VwX...Don't modify[234]#
        #add your code here
        
        pin = self.cmbDigiOpPins.GetValue()
        state = self.cmbHighLow.GetValue()
        
        if pin == "" or state == "":
          return
                
        pin_no = self.conf.getDigiPinValue(pin)
        
        if state == 'High':
          pin_st = 1
        else:
          pin_st = 0
        
        try:
            self.ArdCtrl.SetPinData(pin_no, pin_st)
        except ControllerExceptions.InvalidPinException:
            wx.MessageBox("Invalid pin specified ")
        except ControllerExceptions.InvalidParameterException:
            wx.MessageBox("Invalid parameter ")
        except ControllerExceptions.ResponseTimedOutException:
            wx.MessageBox("The board timed out ")
        

        return #end function


    def initBefore(self):
        #add your code here

        return

    def initAfter(self):
        #add your code here
        from GetSerPorts import GetSerPorts
        serPrtsLister = GetSerPorts()
        serPrts = serPrtsLister.get_ports()
        for prt in serPrts:
            self.cmbSerPort.Append(prt)
        
        self.btOpenPrt.Enable(True)
        self.btClosePrt.Enable(False)
        self.btDigiOutSet.Enable(False)
        self.btDigiRead.Enable(False)
        self.btAnalogOut.Enable(False)
        self.btAnalogRead.Enable(False)
        self.Centre()
        return

    def OnPreCreate(self):
        #add your code here

        return

    def Ddel(self): #init function
        #[158]Code VwX...Don't modify[157]#
        #add your code here

        return #end function

#[win]end your code
