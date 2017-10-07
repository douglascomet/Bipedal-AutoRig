#!/usr/bin/env python
#title           :autoRig.py
#description     :Locator based Bipedal AutoRig
#author          :Doug Halley
#date            :20170606
#version         :3.0
#usage           :Function to execute autoRig.transUI()
#notes           :
#python_version  :2.7.6  
#==============================================================================

import sys
import math
from maya import cmds as cmds
from maya import OpenMaya as om 
#import Qt
from Qt import QtWidgets as qw
from Qt import QtCore as qc
from Qt import QtGui as qg
from functools import partial
import json
import collections


#if using PySide(PyQt4) QDialog is in qg, if using PySide2(PyQt5) QDialog is in qw
class Auto_Rig(qw.QDialog):
    def __init__(self):
        qw.QDialog.__init__(self)
        self.setModal(False)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Auto_Rig")

        self.locGrp = ""
        self.rootJnt = ""

        """
        PARENT LAYOUT
        """
        self.setLayout(qw.QVBoxLayout())
        
        """
        LAYOUT FOR STACKED BUTTONS
        """
        buttonMenu_layout = qw.QHBoxLayout()
        
        AutoRig_bttn = qw.QPushButton("Generate Rig")
        Help_bttn = qw.QPushButton("Help: How to Use")
        
        buttonMenu_layout.addWidget(AutoRig_bttn)
        buttonMenu_layout.addWidget(Help_bttn)
        self.layout().addLayout(buttonMenu_layout)


        """
        STACKED LAYOUT
        """
        self.stacked_layout = qw.QStackedLayout()
        self.layout().addLayout(self.stacked_layout)

        """
        Character Presets
        """

        characterPreset_widget = qw.QWidget()
        characterPreset_widget.setLayout(qw.QHBoxLayout())

        self.characterPreset_lbl = qw.QLabel("Step 2. Character Presets:")
        self.halio_radio = qw.QRadioButton("Halia")
        self.lover_radio = qw.QRadioButton("Lover")
        self.femHollow_radio = qw.QRadioButton("Female Hollow")
        self.god_radio = qw.QRadioButton("God")
        self.defaultBiped_radio = qw.QRadioButton("Default Biped")
        self.defaultIKBiped_radio = qw.QRadioButton("Default IK Biped")
        self.nonBiped_radio = qw.QRadioButton("Non Biped")
        self.clear_radio = qw.QRadioButton("Clear Selection")

        characterPreset_widget.layout().addWidget(self.characterPreset_lbl)
        characterPreset_widget.layout().addWidget(self.halio_radio)
        characterPreset_widget.layout().addWidget(self.lover_radio)
        characterPreset_widget.layout().addWidget(self.femHollow_radio)
        characterPreset_widget.layout().addWidget(self.god_radio)
        characterPreset_widget.layout().addWidget(self.defaultBiped_radio)
        characterPreset_widget.layout().addWidget(self.defaultIKBiped_radio)
        characterPreset_widget.layout().addWidget(self.nonBiped_radio)
        characterPreset_widget.layout().addWidget(self.clear_radio)

        """
        LIMBS LAYOUT
        """

        limbPreset_widget = qw.QWidget()
        limbPreset_widget.setLayout(qw.QHBoxLayout())

        self.LimbPreset_lbl = qw.QLabel("Limb Presets:")
        self.Left_Arm_check = qw.QCheckBox("Left Arm")
        self.Right_Arm_check = qw.QCheckBox("Right Arm")
        self.Left_Leg_check = qw.QCheckBox("Left Leg")
        self.Right_Leg_check = qw.QCheckBox("Right Leg")
        self.Center_Leg_check = qw.QCheckBox("Center Leg")

        limbPreset_widget.layout().addWidget(self.LimbPreset_lbl)
        limbPreset_widget.layout().addWidget(self.Left_Arm_check)
        limbPreset_widget.layout().addWidget(self.Right_Arm_check)
        limbPreset_widget.layout().addWidget(self.Left_Leg_check)
        limbPreset_widget.layout().addWidget(self.Right_Leg_check)
        limbPreset_widget.layout().addWidget(self.Center_Leg_check)

        """
        LAYOUT OF ACCESSORIES CHECKS
        """
        accessory_widget = qw.QWidget()
        accessory_widget.setLayout(qw.QHBoxLayout())

        #Accessory Label
        accessory_lbl = qw.QLabel("Character Accessories")
        accessory_lbl.setAlignment(qc.Qt.AlignCenter)



        """
        Head Accessories
        """
        head_accessory_widget = qw.QWidget()
        head_accessory_widget.setLayout(qw.QVBoxLayout())

        head_accessory_lbl = qw.QLabel("Head/Neck Accessories")
        head_accessory_lbl.setAlignment(qc.Qt.AlignTop)

        head_accessory_widget.layout().addWidget(head_accessory_lbl)

        self.ears_check = qw.QCheckBox("Ears")
        #self.ears_check.setChecked(True)
        head_accessory_widget.layout().addWidget(self.ears_check)

        self.earRings_check = qw.QCheckBox("Ear Rings")
        #self.earRings_check.setChecked(True)
        head_accessory_widget.layout().addWidget(self.earRings_check)

        self.hairBun_check = qw.QCheckBox("Hair Bun")
        #self.hairBun_check.setChecked(True)
        head_accessory_widget.layout().addWidget(self.hairBun_check)

        self.hairStrand_check = qw.QCheckBox("Hair Strand")
        #self.hairStrand_check.setChecked(True)
        head_accessory_widget.layout().addWidget(self.hairStrand_check)

        self.floatingOrb_check = qw.QCheckBox("Floating Orb")
        #self.floatingOrb_check.setChecked(True)
        head_accessory_widget.layout().addWidget(self.floatingOrb_check)

        self.beads_check = qw.QCheckBox("Neck Beads")
        #self.beads_check.setChecked(True)
        head_accessory_widget.layout().addWidget(self.beads_check)

        self.hornChain_check = qw.QCheckBox("Horn Chains")
        #self.hornChain_check.setChecked(True)
        head_accessory_widget.layout().addWidget(self.hornChain_check)

        """
        Arm Accessories
        """
        arm_accessory_widget = qw.QWidget()
        arm_accessory_widget.setLayout(qw.QVBoxLayout())

        arm_accessory_lbl = qw.QLabel("Arm Accessories")
        arm_accessory_lbl.setAlignment(qc.Qt.AlignTop)

        arm_accessory_widget.layout().addWidget(arm_accessory_lbl)

        self.shoulderSleeve_check = qw.QCheckBox("Shoulder Sleeve")
        #self.shoulderSleeve_check.setChecked(True)
        arm_accessory_widget.layout().addWidget(self.shoulderSleeve_check)

        self.elbowSleeve_check = qw.QCheckBox("Elbow Sleeve")
        #self.shoulderSleeve_check.setChecked(True)
        arm_accessory_widget.layout().addWidget(self.elbowSleeve_check)


        """
        Torso/Pelvis Accessories
        """
        pelvis_accessory_widget = qw.QWidget()
        pelvis_accessory_widget.setLayout(qw.QVBoxLayout())

        pelvis_accessory_lbl = qw.QLabel("Torso/Pelvis Accessories")
        pelvis_accessory_lbl.setAlignment(qc.Qt.AlignTop)

        pelvis_accessory_widget.layout().addWidget(pelvis_accessory_lbl)

        self.breasts_check = qw.QCheckBox("Breasts")
        #self.skirt_check.setChecked(True)
        pelvis_accessory_widget.layout().addWidget(self.breasts_check) 

        self.skirt_check = qw.QCheckBox("Skirt")
        #self.skirt_check.setChecked(True)
        pelvis_accessory_widget.layout().addWidget(self.skirt_check)         

        self.satchel_check = qw.QCheckBox("Satchel")
        #self.satchel_check.setChecked(True)
        pelvis_accessory_widget.layout().addWidget(self.satchel_check) 

        self.HipChain_check = qw.QCheckBox("Hip Chain")
        #self.HipChain_check.setChecked(True)
        pelvis_accessory_widget.layout().addWidget(self.HipChain_check) 


        """
        LAYOUT OF IK CHECKS
        """
        ik_widget = qw.QWidget()
        ik_widget.setLayout(qw.QVBoxLayout())

        IK_lbl = qw.QLabel("IK Limbs")
        IK_lbl.setAlignment(qc.Qt.AlignTop)

        ik_widget.layout().addWidget(IK_lbl)

        self.ikArms_check = qw.QCheckBox("IK Arms")
        #self.ikArms_check.setEnabled(False)
        ik_widget.layout().addWidget(self.ikArms_check)

        self.ikLegs_check = qw.QCheckBox("IK Legs")
        ik_widget.layout().addWidget(self.ikLegs_check)

        self.ikSpine_check = qw.QCheckBox("IK Spine")
        ik_widget.layout().addWidget(self.ikSpine_check)

        self.ikSideChain_check = qw.QCheckBox("IK Hip Chain")
        ik_widget.layout().addWidget(self.ikSideChain_check)
        
        """
        LAYOUT OF AUTORIG TAB
        """
        locJnt_widget = qw.QWidget()
        locJnt_widget.setLayout(qw.QVBoxLayout())

        loc_widget = qw.QWidget()
        loc_widget.setLayout(qw.QHBoxLayout())
        
        loc_lbl = qw.QLabel("Step 1. Create Locator Framework")
        loc_lbl.setAlignment(qc.Qt.AlignCenter)
        loc_bttn = qw.QPushButton("Generate Locators")
        #saveLoc_bttn = qw.QPushButton("Save")
        saveAsLoc_bttn = qw.QPushButton("Save As")
        loadLoc_bttn = qw.QPushButton("Load")

        jnt_widget = qw.QWidget()
        jnt_widget.setLayout(qw.QHBoxLayout())

        jnt_lbl = qw.QLabel("Step 3. Replace Locators with Joints")
        jnt_lbl.setAlignment(qc.Qt.AlignCenter)
        jnt_bttn = qw.QPushButton("Generate Joints")
        
        
        loc_widget.layout().addWidget(loc_lbl)
        #loc_widget.layout().addWidget(loc_bttn)
        #loc_widget.layout().addWidget(saveLoc_bttn)
        loc_widget.layout().addWidget(saveAsLoc_bttn)
        loc_widget.layout().addWidget(loadLoc_bttn)

        jnt_widget.layout().addWidget(jnt_lbl)
        jnt_widget.layout().addWidget(jnt_bttn)

        locJnt_widget.layout().addWidget(loc_widget)        
        locJnt_widget.layout().addWidget(characterPreset_widget)
        locJnt_widget.layout().addWidget(jnt_widget)

        accessory_widget.layout().addWidget(head_accessory_widget)        
        accessory_widget.layout().addWidget(arm_accessory_widget)        
        accessory_widget.layout().addWidget(pelvis_accessory_widget)        
        accessory_widget.layout().addWidget(ik_widget)

        #locJnt_widget.layout().addWidget(accessory_lbl)
        locJnt_widget.layout().addWidget(limbPreset_widget)
        locJnt_widget.layout().addWidget(accessory_widget)


        """
        LAYOUT OF CONTROL GENERATE BUTTON
        """

        ctrl_widget = qw.QWidget()
        ctrl_widget.setLayout(qw.QHBoxLayout())

        ctrl_lbl = qw.QLabel("3. Add Controls")
        ctrl_lbl.setAlignment(qc.Qt.AlignCenter)
        ctrl_bttn = qw.QPushButton("Generate Controls")     
        
        ctrl_widget.layout().addWidget(ctrl_lbl)
        ctrl_widget.layout().addWidget(ctrl_bttn)

        locJnt_widget.layout().addWidget(ctrl_widget)

        """
        LAYOUT FOR DOCUMENTATION
        """
        help_widget = qw.QWidget()
        help_widget.setLayout(qw.QVBoxLayout())
        
        directions_lbl = qw.QPlainTextEdit("Explanation of how to use the autorig\n\n\n1. This auto rig generates joints and controls based on locators which can be modified after locators are generated\n\n2. After locators are set in desired locations, joints and controls are generated\n\n3. IK is optional for arms and legs\n\n4. Character Accessories are also optional")
        
        directions_lbl.setReadOnly(True)

        help_widget.layout().addWidget(directions_lbl)
        
        """
        BUTTON BINDINGS FOR AUTO RIGGER
        """
        #loc_bttn.clicked.connect(lambda: self.locTemplate())

        self.halio_radio.clicked.connect(self.presetHalia)
        self.lover_radio.clicked.connect(self.presetLover)
        self.femHollow_radio.clicked.connect(self.presetFemHollow)
        self.god_radio.clicked.connect(self.presetGod)
        self.defaultBiped_radio.clicked.connect(self.defaultBiped)
        self.defaultIKBiped_radio.clicked.connect(self.defaultIKBiped)
        self.clear_radio.clicked.connect(self.clearFeatureSelection)

        loadLoc_bttn.clicked.connect(lambda: self.loadLocJSON())
        saveAsLoc_bttn.clicked.connect(lambda: self.saveLocJSON())

        jnt_bttn.clicked.connect(partial(lambda: self.replaceLocs(self.locGrp)))
        ctrl_bttn.clicked.connect(partial(lambda: self.addJntCtrls(self.rootJnt)))

        """
        ADD WIDGETS TO STACKED LAYOUT
        """
        
        self.stacked_layout.addWidget(locJnt_widget)        
        self.stacked_layout.addWidget(help_widget)
        
        AutoRig_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 0))
        Help_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 1))

    def presetHalia(self):
        self.ears_check.setChecked(True)
        self.skirt_check.setChecked(True)
        self.shoulderSleeve_check.setChecked(True)
        self.elbowSleeve_check.setChecked(True)
        
        self.floatingOrb_check.setChecked(True)
        self.hairStrand_check.setChecked(True)
        self.hairBun_check.setChecked(True)
        self.beads_check.setChecked(True)
        self.satchel_check.setChecked(True)

        self.Left_Arm_check.setChecked(True)
        self.Right_Arm_check.setChecked(True)
        self.Left_Leg_check.setChecked(True)
        self.Right_Leg_check.setChecked(True)
        self.ikArms_check.setChecked(True)
        self.ikLegs_check.setChecked(True)
        self.ikSpine_check.setChecked(True)

        self.hornChain_check.setChecked(False)
        self.HipChain_check.setChecked(False)
        self.ikSideChain_check.setChecked(False)        
        self.earRings_check.setChecked(False)

    def presetLover(self):
        self.ears_check.setChecked(True)
        self.floatingOrb_check.setChecked(True)
        self.HipChain_check.setChecked(True)
        self.ikSideChain_check.setChecked(True)


        self.Left_Arm_check.setChecked(True)
        self.Right_Arm_check.setChecked(True)
        self.Left_Leg_check.setChecked(True)
        self.Right_Leg_check.setChecked(True)
        self.ikArms_check.setChecked(True)
        self.ikLegs_check.setChecked(True)
        self.ikSpine_check.setChecked(True)          

        self.hornChain_check.setChecked(False)       
        self.earRings_check.setChecked(False)
        self.hairStrand_check.setChecked(False)
        self.hairBun_check.setChecked(False)
        self.beads_check.setChecked(False)
        self.satchel_check.setChecked(False)
        self.skirt_check.setChecked(False)
        self.shoulderSleeve_check.setChecked(False)
        self.elbowSleeve_check.setChecked(False)

    def presetFemHollow(self):
        
        self.Left_Arm_check.setChecked(True)
        self.Right_Arm_check.setChecked(True)
        self.Left_Leg_check.setChecked(True)
        self.Right_Leg_check.setChecked(True)
        self.ikArms_check.setChecked(True)
        self.ikLegs_check.setChecked(True)
        self.ikSpine_check.setChecked(True)

        self.ears_check.setChecked(True)
        self.hornChain_check.setChecked(True)
        self.HipChain_check.setChecked(True)
        self.ikSideChain_check.setChecked(True)        
        self.earRings_check.setChecked(True)

        self.skirt_check.setChecked(False)
        self.shoulderSleeve_check.setChecked(False)
        self.elbowSleeve_check.setChecked(False)
        self.floatingOrb_check.setChecked(False)
        self.hairStrand_check.setChecked(False)
        self.hairBun_check.setChecked(False)
        self.beads_check.setChecked(False)                
        self.satchel_check.setChecked(False)

    def presetGod(self):
        
        self.Left_Arm_check.setChecked(True)
        self.Right_Arm_check.setChecked(True)
        self.Center_Leg_check.setChecked(True)
        
        self.ikArms_check.setChecked(True)
        self.ikLegs_check.setChecked(True)
        self.ikSpine_check.setChecked(True)
        
        self.hornChain_check.setChecked(True)
        self.elbowSleeve_check.setChecked(True)      

        self.Left_Leg_check.setChecked(False)
        self.Right_Leg_check.setChecked(False)

        self.HipChain_check.setChecked(False)
        self.ikSideChain_check.setChecked(False)        
        self.earRings_check.setChecked(False)
        self.ears_check.setChecked(False)
        self.skirt_check.setChecked(False)
        self.shoulderSleeve_check.setChecked(False)
        
        self.floatingOrb_check.setChecked(False)
        self.hairStrand_check.setChecked(False)
        self.hairBun_check.setChecked(False)
        self.beads_check.setChecked(False)                
        self.satchel_check.setChecked(False)

    def defaultBiped(self):

        self.Left_Arm_check.setChecked(True)
        self.Right_Arm_check.setChecked(True)
        self.Left_Leg_check.setChecked(True)
        self.Right_Leg_check.setChecked(True)

        self.ikArms_check.setChecked(True)
        self.ikLegs_check.setChecked(True)

        self.elbowSleeve_check.setChecked(False)
        self.ikSpine_check.setChecked(False)
        self.ears_check.setChecked(False)
        self.hornChain_check.setChecked(False)
        self.HipChain_check.setChecked(False)
        self.ikSideChain_check.setChecked(False)        
        self.earRings_check.setChecked(False)

        self.skirt_check.setChecked(False)
        self.shoulderSleeve_check.setChecked(False)        
        self.floatingOrb_check.setChecked(False)
        self.hairStrand_check.setChecked(False)
        self.hairBun_check.setChecked(False)
        self.beads_check.setChecked(False)                
        self.satchel_check.setChecked(False)

    def defaultIKBiped(self):

        self.Left_Arm_check.setChecked(True)
        self.Right_Arm_check.setChecked(True)
        self.Left_Leg_check.setChecked(True)
        self.Right_Leg_check.setChecked(True)

        self.ikArms_check.setChecked(True)
        self.ikLegs_check.setChecked(True)
        self.ikSpine_check.setChecked(True)

        self.elbowSleeve_check.setChecked(False)
        self.ears_check.setChecked(False)
        self.hornChain_check.setChecked(False)
        self.HipChain_check.setChecked(False)
        self.ikSideChain_check.setChecked(False)        
        self.earRings_check.setChecked(False)

        self.skirt_check.setChecked(False)
        self.shoulderSleeve_check.setChecked(False)        
        self.floatingOrb_check.setChecked(False)
        self.hairStrand_check.setChecked(False)
        self.hairBun_check.setChecked(False)
        self.beads_check.setChecked(False)                
        self.satchel_check.setChecked(False)

    def clearFeatureSelection(self):

        self.Left_Arm_check.setChecked(False)
        self.Right_Arm_check.setChecked(False)
        self.Left_Leg_check.setChecked(False)
        self.Right_Leg_check.setChecked(False)
        self.Center_Leg_check.setChecked(False)

        self.ikArms_check.setChecked(False)
        self.ikLegs_check.setChecked(False)
        self.ikSpine_check.setChecked(False)

        self.elbowSleeve_check.setChecked(False)
        self.ears_check.setChecked(False)
        self.hornChain_check.setChecked(False)
        self.HipChain_check.setChecked(False)
        self.ikSideChain_check.setChecked(False)        
        self.earRings_check.setChecked(False)

        self.skirt_check.setChecked(False)
        self.shoulderSleeve_check.setChecked(False)        
        self.floatingOrb_check.setChecked(False)
        self.hairStrand_check.setChecked(False)
        self.hairBun_check.setChecked(False)
        self.beads_check.setChecked(False)                
        self.satchel_check.setChecked(False)

    def loadLocJSON(self):
        jfile = cmds.fileDialog(mode = 0)
        
        frameWorkDict = collections.OrderedDict()

        with open(jfile, 'r') as jsonFile:
            #print jsonFile
            jsonData = json.load(jsonFile, object_pairs_hook=collections.OrderedDict)
        
        #creates empty group for locGroup
        self.locGrp = cmds.group(em = True, name = "loc_frameWork_GRP")
        
        for x, y in jsonData.items():
            

            loc = self.locatorMaker(x, (jsonData[x]["X"], jsonData[x]["Y"], jsonData[x]["Z"]))
            

            if "None" in jsonData[x]["Parent"]:
                cmds.parent( x,  self.locGrp )
            else:
                cmds.parent( x,  jsonData[x]["Parent"] )

        #collect descendants of locGrp and is stored as a list of locs
        locs = cmds.listRelatives(self.locGrp, allDescendents = True)

        #iterate over locs
        for x in locs:
            #ignore shape nodes
            if "Shape" not in x:
            
                #calls function to change the color override
                self.colorOverride(x)

        return self.locGrp            
        
    def saveLocJSON(self):
        #creates an empty ordered dictionary
        #to ensure that locators are stored in the correct order
        frameWorkDict = collections.OrderedDict()

        #get selection of root locator
        root = cmds.ls( selection=True )

        #get children of root locator
        childrenList = cmds.listRelatives(root, allDescendents = True)

        #add root to list
        childrenList.append(root[0])

        #reverse list so root is first element in list
        childrenList.reverse()

        #iterate through list of locators
        for x in childrenList:

            #instantiates an empty ordered list on every iteration 
            elementDict = collections.OrderedDict()

            #ignore shape nodes
            if "Shape" in x:
                continue
            else:

                #get worldspace location of locator
                tempPos = cmds.getAttr(x + ".localPosition")
                #tempsPos is saved as a list of length 1 that contains a tuple of position data
                xPos = tempPos[0][0]
                yPos = tempPos[0][1]
                zPos = tempPos[0][2]
                
                #gets parent of locator
                parent = cmds.listRelatives(x, p = True)
                
                #if root locator set parent to None
                if "_GRP" in parent[0]:
                    parent[0] = None

                elementDict["X"] = xPos
                elementDict["Y"] = yPos
                elementDict["Z"] = zPos
                elementDict["Parent"] = str(parent[0])
                frameWorkDict[str(x)] = elementDict

        #jDict = json.dumps(frameWorkDict, indent = 4, separators = (',',':'))
        """
        try: 
            file = open("jDict.json", "w")
        except myException("File couldnt be created"):
            raise myException
        """
        jDict = json.dumps(frameWorkDict, indent = 4, separators = (',',':'))
        mayajFile = cmds.fileDialog(mode = 1)
        jFile = open(mayajFile, "w")
        jFile.write(jDict)
        jFile.close

    def locatorMaker(self, name, location):

        #creates loc at specified location
        tempLoc = cmds.spaceLocator( n = name, p = location )

        #center pivot
        cmds.xform(tempLoc, pivots = location, centerPivots = True)

        return tempLoc

    def colorOverride(self, node):

        #left locators and contorls are blue, right are red, center are yellow
        #enables override and sets color to red at index 13, blue at index 6, yellow at index 17
        if "_l_" in node:
            cmds.setAttr(node + ".overrideEnabled", 1)
            cmds.setAttr(node + ".overrideColor", 6)
        elif "_r_" in node:
            cmds.setAttr(node + ".overrideEnabled", 1) 
            cmds.setAttr(node + ".overrideColor", 13)
        else:
            cmds.setAttr(node + ".overrideEnabled", 1) 
            cmds.setAttr(node + ".overrideColor", 17)

    def replaceLocs(self, locGrp):

        #freezes transforms of locators so joints can be placed at local position of locator
        cmds.select(locGrp)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 

        #creates rootJnt which is always at the origin
        self.rootJnt = self.makeJoint("root_jnt", None, (0,0,0)) 

        #creates list of locators
        locs = cmds.listRelatives(locGrp, allDescendents = True)

        #reverses locator list
        locs.reverse()

        #creates empty list to be used to contain locator nodes that aren't shape nodes
        shapeLessLocs = []

        #in order to have correct joint orientation, the main joints have to be made
        #ex: spine, arms, legs, neck, head
        postSpineGeneration = []

        #to properly parent joints a second list is made to match joint parents to those joints made post generation
        postSpineGenerationParent = []
        

        clavicleName = ""

        #creates list of the locator nodes that aren't shape nodes
        for x in locs:
            #ignore shape nodes
            if "Shape" not in x:  

                shapeLessLocs.append(x)

        #iterates over locator nodes
        for x in shapeLessLocs:
            
            #gets index value of the currentLoc in the list
            currentLoc = shapeLessLocs.index(x)

            #splits locator name by "_" to remove suffix and recombined to add new suffix
            jntName = self.changeSuffix(x, "_jnt")

            #get localPosition values
            tempPos = cmds.getAttr(x + ".localPosition")
            #tempsPos is saved as a list of length 1 that contains a tuple of position data
            xPos = tempPos[0][0]
            yPos = tempPos[0][1]
            zPos = tempPos[0][2]

            #pelvis_loc is at index 0 so it needs to be a child of the rootJnt
            if shapeLessLocs.index(x) == 0:
                
                #creates pelvis_jnt at 0,0,0 to be moved to the location of the pelvis_loc
                curJoint = self.makeJoint(jntName, self.rootJnt, (0,0,0))

                #after the joint is created it is moved to the locatorPosition
                cmds.move( xPos, yPos, zPos, curJoint, ws = True)

            #case for every locator besides pelvis_loc
            else:

                #gets parent of current locator as a list
                locParent = cmds.listRelatives(shapeLessLocs[currentLoc] , parent = True)

                #use index 0 of returned list of parent of locator which is the direct parent
                jntParent = self.changeSuffix(locParent[0], "_jnt")

                #get world position of parent joint to find midpoint between parent joint and new joint to place twist joint accurately
                jntParentPos = cmds.joint(jntParent, q = True, p = True)

                #store X and Y offset values based on distance between points formula
                xPosOffset = (xPos + jntParentPos[0])/2.0
                yPosOffset = (yPos + jntParentPos[1])/2.0
                zPosOffset = (zPos + jntParentPos[2])/2.0

                #the loc frame is simplified and during joint generation
                #the basic skeleton must be created so orientations are maitained through the spine 
                #certain joints are added to a secondary list to be created later
                #for example, shoulder needs a clavicle before the shoulder can be created
                if "shoulder_" in x:
                    
                    if "_l_" in x:
                        clavicleName = "clavicle_l_jnt"                    
                    elif "_r_" in x:
                        clavicleName = "clavicle_r_jnt"
                        
                    clavicleJnt = self.makeJoint(clavicleName, None, (0,0,0))
                    #after the joint is created it is moved to the locatorPosition
                    cmds.move( xPosOffset, yPos, zPosOffset, clavicleJnt, ws = True)

                    #creates pelvis_jnt at 0,0,0 to be moved to the location of the current locator
                    curJoint = self.makeJoint(jntName, clavicleJnt, (0,0,0)) 

                    #after the joint is created it is moved to the locatorPosition
                    cmds.move( xPos, yPos, zPos, curJoint, ws = True)

                    postSpineGeneration.append(clavicleName)

                    if self.ikSpine_check.isChecked():
                        postSpineGenerationParent.append("spine_06_jnt")
                    else:
                        postSpineGenerationParent.append(jntParent)

                #case for every locator besides pelvis_loc
                #wrist needs a twist joint to assist with deformation
                elif "wrist_" in x:
                    
                    if "_l_" in x:
                        armTwistName = "foreArm_l_jnt"
                        elbowName = "elbow_l_jnt"
                    elif "_r_" in x:
                        armTwistName = "foreArm_r_jnt"
                        elbowName = "elbow_r_jnt"
                        
                    armTwistJnt = self.makeJoint(armTwistName, elbowName, (0,0,0))
                        
                    cmds.move( xPosOffset, yPosOffset, zPosOffset, armTwistJnt, ws = True)

                    #creates pelvis_jnt at 0,0,0 to be moved to the location of the current locator
                    curJoint = self.makeJoint(jntName, armTwistJnt, (0,0,0)) 

                    #after the joint is created it is moved to the locatorPosition
                    cmds.move( xPos, yPos, zPos, curJoint, ws = True)
                
                elif "thigh_" in x or "Bead_" in x or "breast_" in x or "satchelPivot_" in x or "ear_" in x or "upperSleeve_" in x or "lowerSleeve_" in x or "head_01_" in x or "frontSkirt_" in x or "backSkirt_" in x or "sideSkirt_" in x or "earRing_" in x or "HornChain_" in x:
                    
                    curJoint = self.makeJoint(jntName, None, (0,0,0))

                    cmds.move( xPos, yPos, zPos, curJoint, ws = True)
                    
                    if self.ikSpine_check.isChecked() and self.breasts_check.isChecked() and "breast_" in x:
                        postSpineGeneration.append(jntName)
                        postSpineGenerationParent.append("spine_06_jnt")
                    else:
                        postSpineGeneration.append(jntName)
                        postSpineGenerationParent.append(jntParent)

                elif self.HipChain_check.isChecked() and "sideHipChain" in x:

                    if "sideHipChain_01_" in x:
                        jntName = "sideHipChain_01_r_jnt"
                        parentJntName = "pelvis_jnt"

                        curJoint = self.makeJoint(jntName, None, (0,0,0))

                        cmds.move( xPos, yPos, zPos, curJoint, ws = True)

                        postSpineGeneration.append(jntName)
                        postSpineGenerationParent.append(parentJntName)

                    elif "sideHipChain_02_" in x:
                        oneThirdJntName = "sideHipChain_02_r_jnt"
                        twoThirdJntName = "sideHipChain_03_r_jnt"
                        jntName = "sideHipChain_04_r_jnt"
                        parentJntName = "sideHipChain_01_r_jnt"

                        jntParentPos = cmds.joint(parentJntName, q = True, p = True)

                        xPosOffset_oneThird = jntParentPos[0] + ((xPos - jntParentPos[0]) * 1/3)
                        yPosOffset_oneThird = jntParentPos[1] + ((yPos - jntParentPos[1]) * 1/3)
                        zPosOffset_oneThird = jntParentPos[2] + ((zPos - jntParentPos[2]) * 1/3)

                        xPosOffset_twoThird = jntParentPos[0] + ((xPos - jntParentPos[0]) * 2/3)
                        yPosOffset_twoThird = jntParentPos[1] + ((yPos - jntParentPos[1]) * 2/3)
                        zPosOffset_twoThird = jntParentPos[2] + ((zPos - jntParentPos[2]) * 2/3)

                        oneThirdJnt = self.makeJoint(oneThirdJntName, parentJntName, (0,0,0))
                            
                        cmds.move( xPosOffset_oneThird, yPosOffset_oneThird, zPosOffset_oneThird, oneThirdJntName, ws = True)

                        twoThirdJnt = self.makeJoint(twoThirdJntName, oneThirdJntName, (0,0,0))
                            
                        cmds.move( xPosOffset_twoThird, yPosOffset_twoThird, zPosOffset_twoThird, twoThirdJntName, ws = True)

                        #creates pelvis_jnt at 0,0,0 to be moved to the location of the current locator
                        curJoint = self.makeJoint(jntName, twoThirdJntName, (0,0,0)) 

                        #after the joint is created it is moved to the locatorPosition
                        cmds.move( xPos, yPos, zPos, curJoint, ws = True)


                    elif "sideHipChainEnd_" in x:
                        oneThirdJntName = "sideHipChain_05_r_jnt"
                        twoThirdJntName = "sideHipChain_06_r_jnt"
                        jntName = "sideHipChainEnd_r_jnt"
                        parentJntName = "sideHipChain_04_r_jnt"

                        jntParentPos = cmds.joint(parentJntName, q = True, p = True)

                        xPosOffset_oneThird = jntParentPos[0] + ((xPos - jntParentPos[0]) * 1/3)
                        yPosOffset_oneThird = jntParentPos[1] + ((yPos - jntParentPos[1]) * 1/3)
                        zPosOffset_oneThird = jntParentPos[2] + ((zPos - jntParentPos[2]) * 1/3)

                        xPosOffset_twoThird = jntParentPos[0] + ((xPos - jntParentPos[0]) * 2/3)
                        yPosOffset_twoThird = jntParentPos[1] + ((yPos - jntParentPos[1]) * 2/3)
                        zPosOffset_twoThird = jntParentPos[2] + ((zPos - jntParentPos[2]) * 2/3)

                        oneThirdJnt = self.makeJoint(oneThirdJntName, parentJntName, (0,0,0))
                            
                        cmds.move( xPosOffset_oneThird, yPosOffset_oneThird, zPosOffset_oneThird, oneThirdJntName, ws = True)

                        twoThirdJnt = self.makeJoint(twoThirdJntName, oneThirdJntName, (0,0,0))
                            
                        cmds.move( xPosOffset_twoThird, yPosOffset_twoThird, zPosOffset_twoThird, twoThirdJntName, ws = True)

                        #creates pelvis_jnt at 0,0,0 to be moved to the location of the current locator
                        curJoint = self.makeJoint(jntName, twoThirdJntName, (0,0,0)) 

                        #after the joint is created it is moved to the locatorPosition
                        cmds.move( xPos, yPos, zPos, curJoint, ws = True)
                 

                elif self.ikSpine_check.isChecked() and "spine_" in x:


                    if "spine_01_" in x:
                        midJntName = "spine_01_jnt"
                        jntName = "spine_02_jnt"
                        parentJntName = "pelvis_jnt"
                    elif "spine_02_" in x:
                        midJntName = "spine_03_jnt"
                        jntName = "spine_04_jnt"
                        parentJntName = "spine_02_jnt"
                    elif "spine_03_" in x:
                        midJntName = "spine_05_jnt"
                        jntName = "spine_06_jnt"
                        parentJntName = "spine_04_jnt"

                    jntParentPos = cmds.joint(parentJntName, q = True, p = True)
                    xPosOffset = (xPos + jntParentPos[0])/2.0
                    yPosOffset = (yPos + jntParentPos[1])/2.0
                    zPosOffset = (zPos + jntParentPos[2])/2.0

                    midJnt = self.makeJoint(midJntName, parentJntName, (0,0,0))
                        
                    cmds.move( xPosOffset, yPosOffset, zPosOffset, midJnt, ws = True)

                    #creates pelvis_jnt at 0,0,0 to be moved to the location of the current locator
                    curJoint = self.makeJoint(jntName, midJnt, (0,0,0)) 

                    #after the joint is created it is moved to the locatorPosition
                    cmds.move( xPos, yPos, zPos, curJoint, ws = True)

                elif self.ikSpine_check.isChecked() and "neck_01" in x:
                    #creates pelvis_jnt at 0,0,0 to be moved to the location of the current locator
                    curJoint = self.makeJoint(jntName, "spine_06_jnt", (0,0,0))

                    #after the joint is created it is moved to the locatorPosition
                    cmds.move( xPos, yPos, zPos, curJoint, ws = True)
                else:
                    
                    #creates pelvis_jnt at 0,0,0 to be moved to the location of the current locator
                    curJoint = self.makeJoint(jntName, jntParent, (0,0,0))

                    #after the joint is created it is moved to the locatorPosition
                    cmds.move( xPos, yPos, zPos, curJoint, ws = True)



        #goes through list of secondary children to avoid incorrect joint rotation for spinal column and limbs
        if postSpineGeneration:
            for x in postSpineGeneration:
                
                parent = postSpineGenerationParent[postSpineGeneration.index(x)]
                
                cmds.parent(x, parent)

                cmds.joint(x, e=True, zeroScaleOrient=True, orientJoint = "xyz", secondaryAxisOrient="yup", children = True)
                
        cmds.joint(self.rootJnt, e=True, zeroScaleOrient=True, orientJoint = "xyz", secondaryAxisOrient="yup", children = True)

        """
        if cmds.objExists("thumb_01_l_jnt"):
            cmds.joint("thumb_01_l_jnt", e=True, zeroScaleOrient=True, orientJoint = "xzy", secondaryAxisOrient="zup", children = True)

        if cmds.objExists("thumb_01_r_jnt"):
            cmds.joint("thumb_01_r_jnt", e=True, zeroScaleOrient=True, orientJoint = "xzy", secondaryAxisOrient="zup", children = True)
        """  
        return self.rootJnt


    """
    @param: jName - name of input joint
    @param: myParent - input of jName parent joint
    @param: pos - position in worldspace

    Purpose of this funtion is to generate joint based on input info and connect it to parent joint
    """
    def makeJoint(self, jName = "default", myParent = None, pos = (0,0,0)):
        
        #selects parent joint if myParent is a valid input
        
        if myParent:
            cmds.select(myParent, r=True)        
        else:
            cmds.select(clear = True)
        
        myJoint = cmds.joint(position=pos, name=jName, r = True)
        
        for attr in [".jointOrientX", ".jointOrientY", ".jointOrientZ"]:
            cmds.setAttr(myJoint+attr, 0)    
        
        if myParent:
            cmds.joint(myParent, e=True, zeroScaleOrient=True, orientJoint = "xyz", secondaryAxisOrient="yup", children = True)
              
        return myJoint

    #obj2 is set to match transform of obj1 by using point and orient contraint
    def matchTrans(self, obj1, obj2):
        cmds.select(obj1)
        cmds.select(obj2, add=True)
        cmds.pointConstraint(obj1, obj2)
        cmds.orientConstraint(obj1, obj2)
        cmds.delete(obj2, constructionHistory = True, cn=True)

    """
    @param: jName - name of input joint
    @param: myParent - input of jName parent joint

    Purpose of this funtion is to generate circle ctrls based on input world position of the input joint and connect it to parent control
    """
    def makeFKControl(self, jName, myParent=None):

            #if incoming joint has a parent
            if myParent:

                #creates ctrl name based on joint name
                ctrlName = self.changeSuffix(jName, "_FK_ctrl") 
                #print "ctrl " + str(ctrlName)

                #create locator for rotation offset with name based on incoming joint name
                locOffset = self.locatorMaker(self.changeSuffix(jName, "_FK_offset_loc"), (0,0,0))
                #change color of locator
                self.colorOverride(locOffset[0])
                
                #match locOffset to incoming joint
                self.matchTrans(jName, locOffset)

                #ctrlPos = cmds.xform(locOffset, q = True, worldSpace = True, translation = True)
                
                if "thigh_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 10.0)
                    #match transform of nurb cirlce to locOffset

                    self.matchTrans(locOffset, ctrlName)
                    cmds.select( ctrlName )
                    
                    if "_l_" in jName:
                        cmds.rotate(0, 45, 0, ctrlName, relative = True, worldSpace = True, objectSpace = True )
                    elif "_r_" in jName:
                        cmds.rotate(0, -45, 0, ctrlName, relative = True, worldSpace = True, objectSpace = True )                        

                elif "clavicle_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 7.5)
                    #match transform of nurb cirlce to locOffset

                    self.matchTrans(locOffset, ctrlName)
                    cmds.select( ctrlName )
                    
                    cmds.rotate(0, 0, -45, ctrlName, relative = True, worldSpace = True, objectSpace = True )
                elif "ear_"  in jName and self.ears_check.isChecked():
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 3.5)
                    #match transform of nurb cirlce to locOffset
                    self.matchTrans(locOffset, ctrlName)

                elif self.earRings_check.isChecked() and "earRing_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 2)
                    
                    self.matchTrans(locOffset, ctrlName)
                elif "calf_"  in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 7.5)
                    #match transform of nurb cirlce to locOffset
                    self.matchTrans(locOffset, ctrlName)
                elif "middle" in jName or "index" in jName or "ring" in jName or "pinky" in jName or "thumb"  in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 1.25)
                    self.matchTrans(locOffset, ctrlName)
                    #cmds.pointConstraint(jName, locOffset, maintainOffset = True)
                elif "pelvis_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 17.5)
                    self.matchTrans(locOffset, ctrlName)
                elif "upperSleeve" in jName and self.shoulderSleeve_check.isChecked() or "lowerSleeve" in jName and self.elbowSleeve_check.isChecked():
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 3.5)
                    self.matchTrans(locOffset, ctrlName)
                    cmds.scale(1, .5, 1.5, ctrlName, relative = True)
                elif "spine_01_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 15)
                    self.matchTrans(locOffset, ctrlName)
                elif self.ikSpine_check.isChecked() and "spine_06_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 12.5)
                    self.matchTrans(locOffset, ctrlName)
                elif "spine_02_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 12.5)
                    self.matchTrans(locOffset, ctrlName)
                elif "neck_02_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 12.5)
                    self.matchTrans(locOffset, ctrlName)

                elif "eyebrow_" in jName:
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 1)
                    self.matchTrans(locOffset, ctrlName)
                    #cmds.rotate(0, 90, 0, ctrlName, relative = True)
                    cmds.move(0, 0, 5, ctrlName, relative = True,)
                elif "jaw_" in jName:
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 3)
                    self.matchTrans(locOffset, ctrlName)
                    cmds.move(15, 0, 0, ctrlName, relative = True, worldSpaceDistance = True, objectSpace = True  )
                elif "neck_01_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 7.5)
                    self.matchTrans(locOffset, ctrlName)
                    cmds.move(0, 3.5, 0, ctrlName + ".cv[0:7]", relative = True )

                    if self.beads_check.isChecked():
                        #adds toggle for bead visibility
                        cmds.addAttr(ctrlName, longName='Bead_Visibility', attributeType = "long", keyable = True, minValue = 0.0, maxValue = 1.0)

                elif self.beads_check.isChecked() and "Bead_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 1.25)
                    
                    self.matchTrans(locOffset, ctrlName)                    
                    
                    cmds.move(7.5, 0, 0, ctrlName, relative = True, worldSpaceDistance = True, objectSpace = True )
                    #match transform of nurb cirlce to locOffset

                    #get parent of ctrl
                    pName = self.changeSuffix(myParent, "_FK_ctrl")

                    #set visibility toggle on parent ctrl and vibility of current ctrl off and on to use set driven keys
                    cmds.setAttr(pName + ".Bead_Visibility", 0)
                    cmds.setAttr(ctrlName + ".visibility", 0)

                    cmds.setDrivenKeyframe( ctrlName + ".visibility", currentDriver = myParent + '.Bead_Visibility' )                    

                    cmds.setAttr(pName + ".Bead_Visibility", 1)
                    cmds.setAttr(ctrlName + ".visibility", 1)

                    cmds.setDrivenKeyframe( ctrlName + ".visibility", currentDriver = myParent + '.Bead_Visibility' )

                    cmds.setAttr(pName + ".Bead_Visibility", 0)
                    cmds.setAttr(ctrlName + ".visibility", 0)

                elif self.hornChain_check.isChecked() and "HornChain_" in jName:
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 2)
                    
                    self.matchTrans(locOffset, ctrlName)

                elif "satchelPivot_" in jName and self.satchel_check.isChecked():
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 5.0)
                    
                    self.matchTrans(locOffset, ctrlName)                    
                    
                    cmds.move(12.5, 0, 0, ctrlName + ".cv[0:7]", relative = True, objectSpace = True )
                    #match transform of nurb cirlce to locOffset

                elif "breast_" in jName and self.breasts_check.isChecked():
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 5.0)
                    
                    self.matchTrans(locOffset, ctrlName)                    
                    
                    cmds.move(15, 0, 0, ctrlName + ".cv[0:7]", relative = True, objectSpace = True )
                    #match transform of nurb cirlce to locOffset

                elif "head_02_" in jName and self.floatingOrb_check.isChecked():
                    #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 5.0)
                    
                    self.matchTrans(locOffset, ctrlName)
                    cmds.selectMode( q=True, component=True )
                    
                    cmds.move(19, 0, 0, ctrlName + ".cv[0:7]", r = True, objectSpace = True, relative = True )                    

                elif "hairBun" in jName and self.hairBun_check.isChecked():
                     #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 2.5)
                    #match transform of nurb cirlce to locOffset
                    self.matchTrans(locOffset, ctrlName)

                    cmds.move(10, 0, 0, ctrlName + ".cv[0:7]", relative = True, objectSpace = True )
                
                elif "hairStrand_" in jName and self.hairStrand_check.isChecked():
                     #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 2)
                    #match transform of nurb cirlce to locOffset
                    self.matchTrans(locOffset, ctrlName)

                elif "Skirt_" in jName and self.skirt_check.isChecked():
                     #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 2)
                    #match transform of nurb cirlce to locOffset
                    self.matchTrans(locOffset, ctrlName)

                elif "HipChain_" in jName and self.HipChain_check.isChecked():
                     #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 2)
                    #match transform of nurb cirlce to locOffset
                    self.matchTrans(locOffset, ctrlName)

                else:
                     #create nurb cirlce to be used as control
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 5.0)
                    #match transform of nurb cirlce to locOffset
                    self.matchTrans(locOffset, ctrlName)

                

                if "root_" in myParent:
                    pName = self.changeSuffix(myParent, "_ctrl") 
                else:#create temp instance of nurb parent control
                    pName = self.changeSuffix(myParent, "_FK_ctrl")                 
                

                #change color of nurb circle
                self.colorOverride(ctrlName)

                #cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 
                
                cmds.parent(ctrlName, locOffset)
                cmds.select(ctrlName)
                cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 
                """
                if "head_02_" in jName or "satchelPivot_" in jName:
                    cmds.parent(locOffset, pName)
                    #match transform of nurb cirlce to locOffsetw
                    cmds.select(ctrlName + ".cv[*]")
                    print ctrlName + ".cv[*]"
                    cmds.parentConstraint(ctrlName, jName, mo=True)
                else:
                """
                cmds.parent(locOffset, pName)
                if "middle" in jName or "index" in jName or "ring" in jName or "pinky" in jName or "thumb" in jName:
                    cmds.orientConstraint(ctrlName, jName, mo=True)                
                else:
                    if "calf_" in jName or "thigh_" in jName:
                        if self.ikLegs_check.isChecked():
                            cmds.orientConstraint(ctrlName, jName, mo=True)
                        else:
                            cmds.parentConstraint(ctrlName, jName, mo=True)
                    elif "shoulder_" in jName or "elbow_" in jName or "wrist_" in jName:
                        if self.ikArms_check.isChecked():
                            cmds.orientConstraint(ctrlName, jName, mo=True)
                        else:
                            cmds.parentConstraint(ctrlName, jName, mo=True)
                    else:
                        cmds.parentConstraint(ctrlName, jName, mo=True)

            else:
                if "root_" in jName:
                    ctrlName = self.changeSuffix(jName, "_ctrl")
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 50)
                    #print "ctrl " + str(ctrlName)
                    #only effects the root control's radius
                    
                    self.matchTrans(jName, ctrlName)
                    self.colorOverride(ctrlName)

                    cmds.makeIdentity(ctrlName, apply=True, r=True, s=True, t=True, n=False, pn=True) 
                    cmds.parentConstraint(ctrlName, jName, mo=True)  
                elif "middle" in jName or "index" in jName or "ring" in jName or "pinky" in jName or "thumb"  in jName:
                    ctrlName = self.changeSuffix(jName, "_FK_ctrl")
                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 1.25)
                elif "upperSleeve" in jName and self.shoulderSleeve_check.isChecked() or "lowerSleeve" in jName and self.elbowSleeve_check.isChecked():
                    #create nurb cirlce to be used as control
                    ctrlName = self.changeSuffix(jName, "_FK_ctrl")

                    cmds.circle( name = ctrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 3.5)
                    cmds.scale(1, .5, 1.5, ctrlName, relative = True)   
        
            return ctrlName

    def changeSuffix(self, name, newSuffix):

        #splits name at "_"
        nameSplit = name.split("_")

        #pops old suffix out of split list of the name
        nameSplit.pop()

        #if FK or IK present in name, do additional pop to remove it
        if "FK" in nameSplit or "IK" in nameSplit:
            nameSplit.pop()

        #joins remaining elements of split list of the name
        nameJoin = "_".join(nameSplit)

        #add new suffix to joined name
        newName = nameJoin + newSuffix

        return newName

    def duplicateJnt(self, jName, parent, suffix):
        jntPos = cmds.joint(jName, q = True, p = True)
        
        newName = self.changeSuffix(jName, suffix)

        if parent == None:
            newJoint = self.makeJoint(newName, None, (0,0,0))
        else:
            newParent = self.changeSuffix(parent, suffix)
            newJoint = self.makeJoint(newName, newParent, (0,0,0))


        cmds.move(jntPos[0], jntPos[1], jntPos[2], newJoint, ws = True)

        return newJoint

    def setupIKLimb(self, limbStart):

        limbChildren = cmds.listRelatives(limbStart, allDescendents = True)
      
        limbChildren.reverse()

        ikLimbChildren = []
        outputList = []
        #print "before " + str(limabChildren)

        for x in limbChildren:

            #print "index: " + str(limbChildren.index(x)) + " " + str(x) + "\n"

            #removes children, like hand joints, that shouldn't be affected by IK generation
            if "fingerPivot_" in x or "thumbPivot_" in x or "upperSleeve" in x or "lowerSleeve" in x or "thumb" in x or "index" in x or "middle" in x or "ring" in x or "pinky" in x or "breast_" in x:
                continue
            #deletes any previously made constraints from constrained joints in list
            elif "Constraint" in x:
                cmds.delete( x, cn=True )
            else:
                ikLimbChildren.append(x)

        if len(ikLimbChildren) == 4:
            limbMid = ikLimbChildren[0]
            limbBot = ikLimbChildren[1]
            limbBall = ikLimbChildren[2]
            limbBallEnd = ikLimbChildren[3]
            
        else:
            #print ikLimbChildren
            #print "WHAT KIND OF LIMB IS THIS?"
            limbMid = ikLimbChildren[0]
            limbTwist = ikLimbChildren[1]
            limbBot = ikLimbChildren[2]

        #creates ikRPsolver, usually used to get hinge joint control
        if "thigh_" in limbStart:
            
            #create names for IK joints            
            ikTop = self.duplicateJnt(limbStart, None, "_IK_jnt")
            ikMid = self.duplicateJnt(limbMid, limbStart, "_IK_jnt")
            ikBot = self.duplicateJnt(limbBot, limbMid, "_IK_jnt")
            ikBall = self.duplicateJnt(limbBall, limbBot, "_IK_jnt")
            ikBallEnd = self.duplicateJnt(limbBallEnd, limbBall, "_IK_jnt")

            #create FK jnt name locally to reference actual FK jnt
            fkTopJnt = self.changeSuffix(limbStart, "_FK_jnt")
            fkMidJnt = self.changeSuffix(limbMid, "_FK_jnt")
            fkBotJnt = self.changeSuffix(limbBot, "_FK_jnt")
            fkBallJnt = self.changeSuffix(limbBall, "_FK_jnt")
            fkBallEndJnt = self.changeSuffix(limbBallEnd, "_FK_jnt")

            #create FK jnt name locally to reference actual FK control
            fkTopCtrl = self.changeSuffix(limbStart, "_FK_ctrl")
            fkMidCtrl = self.changeSuffix(limbMid, "_FK_ctrl")
            fkBotCtrl = self.changeSuffix(limbBot, "_FK_ctrl")
            fkBallCtrl = self.changeSuffix(limbBall, "_FK_ctrl")
            fkBallEndCtrl = self.changeSuffix(limbBallEnd, "_FK_ctrl")

            #orient duplicated joint strucutre
            cmds.joint(ikTop, e=True, zeroScaleOrient=True, orientJoint = "xyz", secondaryAxisOrient="yup", children = True)
            

            if "_l_" in ikBot:
                footCtrlName = "foot_l_IK_ctrl"
                kneeIkCtrlName = "knee_l_IK_ctrl"

                ankleIkName = "ankle_l_IK_handle"
                ballIkName = "ball_l_IK_handle"
                ballEndIkName = "ballEnd_l_IK_handle"

                fkSwitchNameCtrl = "ankle_FKIK_l_ctrl"                

                ankleGrp = "ankle_l_GRP"
                ballEndGrp = "ballEnd_l_GRP"
                ballSwivelGrp = "ballSwivel_l_GRP"
                heelPeelGrp = "heelPeel_l_GRP"
                ballTapGrp = "ballTap_l_GRP"

                ikLegGRPName = "IK_L_LEG_GRP"
                ikJntGRPName = "IK_L_LEG_JNT_GRP"
                ikCtrlGRPName = "IK_L_LEG_CTRL_GRP"

            elif "_r_" in ikBot:
                footCtrlName = "foot_r_IK_ctrl"
                kneeIkCtrlName = "knee_r_IK_ctrl"

                ankleIkName = "ankle_r_IK_handle"
                ballIkName = "ball_r_IK_handle"
                ballEndIkName = "ballEnd_r_IK_handle"

                fkSwitchNameCtrl = "ankle_FKIK_r_ctrl"               

                ankleGrp = "ankle_r_GRP"
                ballEndGrp = "ballEnd_r_GRP"
                ballSwivelGrp = "ballSwivel_r_GRP"
                heelPeelGrp = "heelPeel_r_GRP"
                ballTapGrp = "ballTap_r_GRP"

                ikLegGRPName = "IK_R_LEG_GRP"
                ikJntGRPName = "IK_R_LEG_JNT_GRP"
                ikCtrlGRPName = "IK_R_LEG_CTRL_GRP"

            else:
                footCtrlName = "foot_IK_ctrl"
                kneeIkCtrlName = "knee_IK_ctrl"

                ankleIkName = "ankle_IK_handle"
                ballIkName = "ball_IK_handle"
                ballEndIkName = "ballEnd_IK_handle"

                fkSwitchNameCtrl = "ankle_FKIK_ctrl"               

                ankleGrp = "ankle_GRP"
                ballEndGrp = "ballEnd_GRP"
                ballSwivelGrp = "ballSwivel_GRP"
                heelPeelGrp = "heelPeel_GRP"
                ballTapGrp = "ballTap_GRP"

                ikLegGRPName = "IK_LEG_GRP"
                ikJntGRPName = "IK_LEG_JNT_GRP"
                ikCtrlGRPName = "IK_LEG_CTRL_GRP"

            anlkleIkHandle = cmds.ikHandle( name = ankleIkName, 
                                solver = "ikRPsolver", 
                                startJoint=ikTop, 
                                endEffector=ikBot, 
                                priority=1, 
                                weight=1,                             
                                positionWeight = 1)        

        
            ballIkHandle = cmds.ikHandle( name = ballIkName, 
                                solver = "ikSCsolver", 
                                startJoint=ikBot, 
                                endEffector=ikBall, 
                                priority=1, 
                                weight=1,                             
                                positionWeight = 1)  

            ballEndIkHandle = cmds.ikHandle( name = ballEndIkName, 
                                solver = "ikSCsolver", 
                                startJoint=ikBall, 
                                endEffector=ikBallEnd, 
                                priority=1, 
                                weight=1,                             
                                positionWeight = 1)
            """

            Foot Roll

            """
            cmds.group( anlkleIkHandle[0], name=heelPeelGrp )
            jntPos = cmds.joint(ikBot, q = True, p = True)
            cmds.xform(piv = (jntPos[0], 0, jntPos[2]))

            cmds.group( ballIkHandle[0], ballEndIkHandle[0],  name=ballTapGrp )
            jntPos = cmds.joint(ikBall, q = True, p = True)
            cmds.xform(piv = jntPos)
            
            cmds.group( ballTapGrp, heelPeelGrp, name=ballSwivelGrp )
            cmds.xform(piv = jntPos)

            cmds.group( ballSwivelGrp, name=ballEndGrp )
            jntPos = cmds.joint(ikBallEnd, q = True, p = True)
            cmds.xform(piv = jntPos)

            cmds.group( ballEndGrp, name=ankleGrp )
            jntPos = cmds.joint(ikBot, q = True, p = True)
            cmds.xform(piv = jntPos)
            
            #create nurb cirlce to be used as control
            cmds.circle( name = footCtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 5 )

            #match transform of nurb cirlce to locOffset
            self.matchTrans(ikBot, footCtrlName)

            #create nurb cirlce to be used as control
            cmds.rotate(0, 0, 90, footCtrlName, relative = True, worldSpace = True, objectSpace = True )
            
            cmds.select(footCtrlName)
            self.colorOverride(footCtrlName)
            cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 
            cmds.parent(ankleGrp, footCtrlName )

            cmds.addAttr(footCtrlName, longName='AnklePivot', attributeType = "float", keyable = True)
            cmds.connectAttr( footCtrlName + ".AnklePivot", ankleGrp + ".rotateX" )

            cmds.addAttr(footCtrlName, longName='BallTip', attributeType = "float", keyable = True)
            cmds.connectAttr( footCtrlName + ".BallTip", ballEndGrp + ".rotateX" )

            cmds.addAttr(footCtrlName, longName='BallSwivel', attributeType = "float", keyable = True)
            cmds.connectAttr( footCtrlName + ".BallSwivel", ballSwivelGrp + ".rotateY" )

            cmds.addAttr(footCtrlName, longName='HeelPeel', attributeType = "float", keyable = True)
            cmds.connectAttr( footCtrlName + ".HeelPeel", heelPeelGrp + ".rotateX" )

            cmds.addAttr(footCtrlName, longName='BallTap', attributeType = "float", keyable = True)
            cmds.connectAttr( footCtrlName + ".BallTap", ballTapGrp + ".rotateX" )
                       
            
            """

            Joint Constraints

            """
            #get FK variations to include in orientConstraint
            locMid = self.changeSuffix(limbMid, "_IK_loc")

            kneePos = cmds.joint(limbMid, q = True, p = True)
            
            kneeLoc = self.locatorMaker(locMid, (kneePos[0], kneePos[1], kneePos[2]))
                        
            #match transform of nurb cirlce to locOffset

            self.matchTrans(limbMid, kneeLoc)
            cmds.pointConstraint( ikMid, kneeLoc )
            
            
            poleLocOffset = self.poleVectorCntrl(ikTop, ikMid, ikBot)
            poleLocOffsetName = self.changeSuffix(limbMid, "_corrective_IK_loc")
            cmds.rename(poleLocOffset, poleLocOffsetName)
            cmds.parent(poleLocOffsetName, kneeLoc)

            cmds.circle( name = kneeIkCtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 5.0)
            #match transform of nurb cirlce to locOffset
            self.matchTrans(poleLocOffsetName, kneeIkCtrlName)
            
            
            cmds.move(0, 0, 40, kneeIkCtrlName, relative = True, worldSpaceDistance = True, worldSpace = True )
            self.colorOverride(kneeIkCtrlName)
            cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 

            cmds.aimConstraint( locMid, kneeIkCtrlName, maintainOffset = True)
            cmds.poleVectorConstraint( kneeIkCtrlName, anlkleIkHandle[0] )
            #cmds.pointConstraint(kneeIkCtrlName, poleLocOffset, maintainOffset = True)                    
            
            #clear selection
            cmds.select(clear = True)

            cmds.select(fkTopJnt, ikTop,  limbStart, r = True )            
            cmds.orientConstraint( offset = (0,0,0) , weight = 1.0 )            

            cmds.select(fkMidJnt, ikMid, limbMid, r = True )
            cmds.orientConstraint( offset = (0,0,0) , weight = 1.0  )            

            cmds.select(fkBotJnt, ikBot,  limbBot, r = True )
            cmds.orientConstraint( offset = (0,0,0) , weight = 1.0  )

            cmds.select(fkBallJnt, ikBall,  limbBall, r = True )
            cmds.orientConstraint( offset = (0,0,0) , weight = 1.0  )

            cmds.select(fkBallEndJnt, ikBallEnd, limbBallEnd, r = True )
            cmds.orientConstraint( offset = (0,0,0), weight = 1.0  )
            
            fkIkCtrlSwitch = self.makeSwitchCtrl("FKIK", fkSwitchNameCtrl)
            self.matchTrans(footCtrlName, fkIkCtrlSwitch)

            if "_l_" in ikBot:
                cmds.move(15, 0, 0, fkIkCtrlSwitch, relative = True, worldSpaceDistance = True, objectSpace = True )
                cmds.select(fkIkCtrlSwitch)
                cmds.scale( 7, 7, 7 )
                cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 
                cmds.select(clear = True)
            
            
            elif "_r_" in ikBot:
                cmds.move(-15, 0, 0, fkIkCtrlSwitch, relative = True, worldSpaceDistance = True, objectSpace = True )
                cmds.select(fkIkCtrlSwitch)
                cmds.scale( 7, 7, 7 )
                cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True)  
                cmds.select(clear = True)

            for y in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]:
                    cmds.setAttr(fkSwitchNameCtrl + y, lock = True, keyable = False, channelBox = False)


            cmds.setAttr(fkIkCtrlSwitch + ".IK_Enabled", 0)

            cmds.setAttr (limbStart + "_orientConstraint1." + fkTopJnt + "W0", 1)
            cmds.setAttr (limbStart + "_orientConstraint1." + ikTop + "W1", 0)

            cmds.setAttr (limbMid + "_orientConstraint1." + fkMidJnt + "W0", 1)
            cmds.setAttr (limbMid + "_orientConstraint1." + ikMid + "W1", 0)

            cmds.setAttr (limbBot + "_orientConstraint1." + fkBotJnt + "W0", 1)        
            cmds.setAttr (limbBot + "_orientConstraint1." + ikBot + "W1", 0)

            cmds.setAttr (limbBall + "_orientConstraint1." + fkBallJnt + "W0", 1)                        
            cmds.setAttr (limbBall + "_orientConstraint1." + ikBall + "W1", 0)

            cmds.setAttr (limbBallEnd + "_orientConstraint1." + fkBallEndJnt + "W0", 1)
            cmds.setAttr (limbBallEnd + "_orientConstraint1." + ikBallEnd + "W1", 0)

            cmds.setDrivenKeyframe( limbStart + "_orientConstraint1." + fkTopJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbMid + "_orientConstraint1." + fkMidJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBot + "_orientConstraint1." + fkBotJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBall + "_orientConstraint1." + fkBallJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBallEnd + "_orientConstraint1." + fkBallEndJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            
            cmds.setDrivenKeyframe( limbStart + "_orientConstraint1." + ikTop + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbMid + "_orientConstraint1." + ikMid + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBot + "_orientConstraint1." + ikBot + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBall + "_orientConstraint1." + ikBall + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBallEnd + "_orientConstraint1." + ikBallEnd + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )

            cmds.setAttr(fkTopCtrl + ".visibility", 1)
            cmds.setAttr(fkMidCtrl + ".visibility", 1)
            cmds.setAttr(fkBotCtrl + ".visibility", 1)
            cmds.setAttr(fkBallCtrl + ".visibility", 1)  

            cmds.setDrivenKeyframe( fkTopCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            cmds.setDrivenKeyframe( fkMidCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            cmds.setDrivenKeyframe( fkBotCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            cmds.setDrivenKeyframe( fkBallCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            
            cmds.setAttr(kneeIkCtrlName + ".visibility", 0)
            cmds.setDrivenKeyframe( kneeIkCtrlName + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled') 
            
            cmds.setAttr(footCtrlName + ".visibility", 0)
            cmds.setDrivenKeyframe( footCtrlName + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled') 
            
            cmds.setAttr(fkIkCtrlSwitch+".IK_Enabled", 1)

            cmds.setAttr (limbStart + "_orientConstraint1." + fkTopJnt + "W0", 0)
            cmds.setAttr (limbStart + "_orientConstraint1." + ikTop + "W1", 1)

            cmds.setAttr (limbMid + "_orientConstraint1." + fkMidJnt + "W0", 0)
            cmds.setAttr (limbMid + "_orientConstraint1." + ikMid + "W1", 1)

            cmds.setAttr (limbBot + "_orientConstraint1." + fkBotJnt + "W0", 0)        
            cmds.setAttr (limbBot + "_orientConstraint1." + ikBot + "W1", 1)

            cmds.setAttr (limbBall + "_orientConstraint1." + fkBallJnt + "W0", 0)                        
            cmds.setAttr (limbBall + "_orientConstraint1." + ikBall + "W1", 1)

            cmds.setAttr (limbBallEnd + "_orientConstraint1." + fkBallEndJnt + "W0", 0)
            cmds.setAttr (limbBallEnd + "_orientConstraint1." + ikBallEnd + "W1", 1)

            cmds.setDrivenKeyframe( limbStart + "_orientConstraint1." + fkTopJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbMid + "_orientConstraint1." + fkMidJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBot + "_orientConstraint1." + fkBotJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBall + "_orientConstraint1." + fkBallJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBallEnd + "_orientConstraint1." + fkBallEndJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            
            cmds.setDrivenKeyframe( limbStart + "_orientConstraint1." + ikTop + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbMid + "_orientConstraint1." + ikMid + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBot + "_orientConstraint1." + ikBot + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBall + "_orientConstraint1." + ikBall + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBallEnd + "_orientConstraint1." + ikBallEnd + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            
            cmds.setAttr(fkTopCtrl + ".visibility", 0)
            cmds.setAttr(fkMidCtrl + ".visibility", 0)
            cmds.setAttr(fkBotCtrl + ".visibility", 0)
            cmds.setAttr(fkBallCtrl + ".visibility", 0)          

            cmds.setDrivenKeyframe( fkTopCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            cmds.setDrivenKeyframe( fkMidCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            cmds.setDrivenKeyframe( fkBotCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            cmds.setDrivenKeyframe( fkBallCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            
            cmds.setAttr(kneeIkCtrlName + ".visibility", 1)
            cmds.setDrivenKeyframe( kneeIkCtrlName + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled') 
            
            cmds.setAttr(footCtrlName + ".visibility", 1)
            cmds.setDrivenKeyframe( footCtrlName + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled') 


            locBot = self.changeSuffix(limbBot, "_FKIK_loc")

            anklePos = cmds.joint(limbBot, q = True, p = True)
            
            ankleLoc = self.locatorMaker(locBot, (anklePos[0], anklePos[1], anklePos[2]))
                        
            #match transform of nurb cirlce to locOffset

            cmds.pointConstraint( limbBot, locBot, maintainOffset = True)

            #needs absolute parenting because since the FKIK Switch is comprised of shapes it somehow duplicates the shapes
            cmds.parent(fkIkCtrlSwitch, locBot, absolute = True)

            ikJntGRP = cmds.group(ikTop, name = ikJntGRPName, w = True)
            cmds.xform(piv = (0,0,0))

            ikCntrlGRP = cmds.group(locMid, kneeIkCtrlName, footCtrlName, locBot, name = ikCtrlGRPName, w = True)
            cmds.xform(piv = (0,0,0))

            #ikGRP = cmds.group(ikJntGRP, ikCntrlGRP, name = ikLegGRPName, w = True)
            #cmds.xform(piv = (0,0,0))

            outputList.append(ikJntGRP)
            outputList.append(ikCntrlGRP)

        elif "shoulder_" in limbStart:
            #create names for IK joints            

            """
            #get name of parent joint to find midpoint between parent joint and new joint to place twist joint accurately
            clavicleLimb = cmds.listRelatives( limbStart, parent=True )

            print clavicleLimb
            cmds.delete( clavicleLimb[0], cn=True )

            ikClavicle = self.duplicateJnt(clavicleLimb[0], None, "_IK_jnt")
            ikTop = self.duplicateJnt(limbStart, clavicleLimb[0], "_IK_jnt")
            fkClavicleJnt = self.changeSuffix(clavicleLimb[0], "_FK_jnt")            
            fkclavicleCtrl = self.changeSuffix(clavicleLimb[0], "_FK_ctrl")
            #orient duplicated joint strucutre
            cmds.joint(ikClavicle, e=True, zeroScaleOrient=True, orientJoint = "xyz", secondaryAxisOrient="yup", children = True)
            """

            ikTop = self.duplicateJnt(limbStart, None, "_IK_jnt")
            ikMid = self.duplicateJnt(limbMid, limbStart, "_IK_jnt")
            ikTwist = self.duplicateJnt(limbTwist, limbMid, "_IK_jnt")
            ikBot = self.duplicateJnt(limbBot, limbTwist, "_IK_jnt")            
            


            #create FK jnt name locally to reference actual FK jnt
            fkTopJnt = self.changeSuffix(limbStart, "_FK_jnt")
            fkMidJnt = self.changeSuffix(limbMid, "_FK_jnt")
            fkTwistJnt = self.changeSuffix(limbTwist, "_FK_jnt")
            fkBotJnt = self.changeSuffix(limbBot, "_FK_jnt")

            #create FK jnt name locally to reference actual FK control
            fkTopCtrl = self.changeSuffix(limbStart, "_FK_ctrl")
            fkMidCtrl = self.changeSuffix(limbMid, "_FK_ctrl")
            fkBotCtrl = self.changeSuffix(limbBot, "_FK_ctrl")

            #orient duplicated joint strucutre
            cmds.joint(ikTop, e=True, zeroScaleOrient=True, orientJoint = "xyz", secondaryAxisOrient="yup", children = True)



            if "_l_" in ikBot:
                armCtrlName = "wrist_l_IK_ctrl"
                armIkName = "wrist_l_IK_handle"
                clavicleIkName = "clavicle_l_IK_ctrl"

                armIkGrp = "wrist_l_IK_CTRL_GRP"
                armIkJNTGrp = "wrist_l_IK_JNT_GRP"

                elbowIkCtrlName = "elbow_l_IK_ctrl"

                fkSwitchNameCtrl = "wrist_FKIK_l_ctrl" 

                ikArmGRPName = "IK_L_ARM_GRP"
                ikJntGRPName = "IK_L_ARM_JNT_GRP"
                ikCtrlGRPName = "IK_L_ARM_CTRL_GRP"
                                
            elif "_r_" in ikBot:
                armCtrlName = "wrist_r_IK_ctrl"
                armIkName = "wrist_r_IK_handle"
                clavicleIkName = "clavicle_r_IK_ctrl"

                armIkGrp = "wrist_r_IK_CTRL_GRP"
                armIkJNTGrp = "wrist_r_IK_JNT_GRP"

                elbowIkCtrlName = "elbow_r_IK_ctrl"

                fkSwitchNameCtrl = "wrist_FKIK_r_ctrl" 

                ikArmGRPName = "IK_R_ARM_GRP"
                ikJntGRPName = "IK_R_ARM_JNT_GRP"
                ikCtrlGRPName = "IK_R_ARM_CTRL_GRP"

            else:
                armCtrlName = "wrist_IK_ctrl"
                armIkName = "wrist_IK_handle"
                clavicleIkName = "clavicle_IK_ctrl"

                armIkGrp = "wrist_IK_CTRL_GRP"
                armIkJNTGrp = "wrist_IK_JNT_GRP"

                elbowIkCtrlName = "elbow_IK_ctrl"

                fkSwitchNameCtrl = "wrist_FKIK_ctrl" 

                ikArmGRPName = "IK_ARM_GRP"
                ikJntGRPName = "IK_ARM_JNT_GRP"
                ikCtrlGRPName = "IK_ARM_CTRL_GRP"
            

            #print armCtrlName

            #create nurb cirlce to be used as control
            cmds.circle( name = armCtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 5 )

            #match transform of nurb cirlce to locOffset
            self.matchTrans(ikBot, armCtrlName)

            #create nurb cirlce to be used as control
            cmds.rotate(0, 0, 90, armCtrlName, relative = True, worldSpace = True, objectSpace = True )
            
            cmds.select(armCtrlName)
            self.colorOverride(armCtrlName)
            cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True)
            expName = self.changeSuffix(ikTwist, "_offset_twist")
            cmds.expression(name = expName, s=ikTwist + '.rotateX = ( ' + armCtrlName + '.rotateX ) / 2')

            
            armIkHandle = cmds.ikHandle( name = armIkName, 
                                solver = "ikRPsolver", 
                                startJoint=ikTop, 
                                endEffector=ikTwist)

            cmds.group( armIkHandle[0], name=armIkGrp )
            cmds.xform(piv = (0,0,0))
            
            cmds.parent(armIkGrp, armCtrlName )


            ikBotPos = cmds.joint(ikBot, q = True, p = True)
            
            
            ikTwistPos = cmds.joint(ikTwist, q = True, p = True)
            ikEffectorOffsetX = ikBotPos[0] - ikTwistPos[0]
            ikEffectorOffsetY = ikBotPos[1] - ikTwistPos[1]
            ikEffectorOffsetZ = ikBotPos[2] - ikTwistPos[2]

            print ikBotPos[0], ikBotPos[1], ikBotPos[2]
            print ikTwistPos[0],ikTwistPos[1], ikTwistPos[2]
            print ikEffectorOffsetX, ikEffectorOffsetY, ikEffectorOffsetZ
            

            
            #cmds.move(ikEffectorOffsetX, ikEffectorOffsetY, ikEffectorOffsetZ, r = True)
            cmds.move(ikEffectorOffsetX, ikEffectorOffsetY, ikEffectorOffsetZ, armIkHandle[1] + ".scalePivot", armIkHandle[1] + ".rotatePivot", rotatePivotRelative = True, relative = True)
            cmds.move(ikEffectorOffsetX, ikEffectorOffsetY, ikEffectorOffsetZ, armIkHandle[0], rotatePivotRelative = True, relative = True)
            
            #cmds.move(ikEffectorOffsetX, ikEffectorOffsetY, ikEffectorOffsetZ, armIkHandle[0], relative = True, )
            
            #break

            #with clavicle
            #cmds.group( armIkHandle[0], clavicleIkHandle[0], name=armIkGrp )
            
            
            for attr in [".jointOrientX", ".jointOrientY", ".jointOrientZ"]:
                cmds.setAttr(limbBot+attr, 0)
                cmds.setAttr(fkBotJnt+attr, 0)
                cmds.setAttr(ikBot+attr, 0)

            
            #Joint Constraints

            
            #get FK variations to include in orientConstraint
            locMid = self.changeSuffix(limbMid, "_IK_loc")


            elbowPos = cmds.joint(limbMid, q = True, p = True)

            elbowLoc = self.locatorMaker(locMid, (elbowPos[0], elbowPos[1], elbowPos[2]))
                        
            #match transform of nurb cirlce to locOffset

            self.matchTrans(limbMid, elbowLoc)

            
            #cmds.select(elbowLoc)
            #cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 
            cmds.pointConstraint( limbMid, elbowLoc )
            

            poleLocOffset = self.poleVectorCntrl(ikTop, ikMid, ikBot)
            poleLocOffsetName = self.changeSuffix(limbMid, "_corrective_IK_loc")
            cmds.rename(poleLocOffset, poleLocOffsetName)
            cmds.parent(poleLocOffsetName, elbowLoc)

            cmds.circle( name = elbowIkCtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 5.0)
                        

            #match transform of nurb cirlce to locOffset
            self.matchTrans(poleLocOffsetName, elbowIkCtrlName)            
            
            
            cmds.move(25, 0, 0, elbowIkCtrlName, relative = True, worldSpaceDistance = True, objectSpace = True )
            
            self.colorOverride(elbowIkCtrlName)
            cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 


            #cmds.aimConstraint( clavicleIkName, clavicleIkHandle[0], maintainOffset = True, worldUpType = "none")

            cmds.aimConstraint( locMid, elbowIkCtrlName, maintainOffset = True)
            cmds.poleVectorConstraint( elbowIkCtrlName, armIkHandle[0] )
            #cmds.pointConstraint(elbowIkCtrlName, poleLocOffset, maintainOffset = True)  


            
            #cmds.select(fkclavicleCtrl, clavicleIkName, clavicleLimb[0], r = True )
            #cmds.orientConstraint( offset = (0,0,0), weight = 1.0  )
            
            
            cmds.select(fkTopJnt, ikTop,  limbStart, r = True )            
            cmds.orientConstraint( offset = (0,0,0) , weight = 1.0 )            

            cmds.select(fkMidJnt, ikMid, limbMid, r = True )
            cmds.orientConstraint( offset = (0,0,0) , weight = 1.0  )

            cmds.select(fkTwistJnt, ikTwist,  limbTwist, r = True )
            cmds.orientConstraint( offset = (0,0,0) , weight = 1.0  )

            cmds.select(fkBotJnt, limbBot, r = True )
            cmds.orientConstraint( offset = (0,0,0) , weight = 1.0  )      
            cmds.select(ikBot,  limbBot, r = True )
            cmds.orientConstraint( offset = (0,0,0) , weight = 1.0  )       

            
            cmds.pointConstraint( armCtrlName, ikBot, maintainOffset = False , weight = 1.0 )

            cmds.orientConstraint( armCtrlName, ikBot, maintainOffset = True , weight = 1.0  )
            
            
            fkIkCtrlSwitch = self.makeSwitchCtrl("FKIK", fkSwitchNameCtrl)
            self.matchTrans(armCtrlName, fkIkCtrlSwitch)

            if "_l_" in ikBot:
                cmds.move(15, 0, 0, fkIkCtrlSwitch, relative = True, worldSpaceDistance = True, objectSpace = True )
                cmds.select(fkIkCtrlSwitch)
                cmds.scale( 7, 7, 7 )
                cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 
                cmds.select(clear = True)
            
            
            elif "_r_" in ikBot:
                cmds.move(-15, 0, 0, fkIkCtrlSwitch, relative = True, worldSpaceDistance = True, objectSpace = True )
                cmds.select(fkIkCtrlSwitch)
                cmds.scale( 7, 7, 7 )
                cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True)  
                cmds.select(clear = True)
             
            for y in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]:
                cmds.setAttr(fkSwitchNameCtrl + y, lock = True, keyable = False, channelBox = False)
   

            cmds.setAttr(fkIkCtrlSwitch+".IK_Enabled", 0)

            cmds.setAttr (limbStart + "_orientConstraint1." + fkTopJnt + "W0", 1)
            cmds.setAttr (limbStart + "_orientConstraint1." + ikTop + "W1", 0)

            cmds.setAttr (limbMid + "_orientConstraint1." + fkMidJnt + "W0", 1)
            cmds.setAttr (limbMid + "_orientConstraint1." + ikMid + "W1", 0)

            cmds.setAttr (limbTwist + "_orientConstraint1." + fkTwistJnt + "W0", 1)
            cmds.setAttr (limbTwist + "_orientConstraint1." + ikTwist + "W1", 0)

            cmds.setAttr (limbBot + "_orientConstraint1." + fkBotJnt + "W0", 1)        
            cmds.setAttr (limbBot + "_orientConstraint1." + ikBot + "W1", 0)

            
            #cmds.setAttr (clavicleLimb[0] + "_orientConstraint1." + fkclavicleCtrl + "W0", 1)                        
            #cmds.setAttr (clavicleLimb[0] + "_orientConstraint1." + clavicleIkName + "W1", 0)
            

            cmds.setDrivenKeyframe( limbStart + "_orientConstraint1." + fkTopJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbMid + "_orientConstraint1." + fkMidJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbTwist + "_orientConstraint1." + fkTwistJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBot + "_orientConstraint1." + fkBotJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            #cmds.setDrivenKeyframe( clavicleLimb[0] + "_orientConstraint1." + fkclavicleCtrl + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            
            cmds.setDrivenKeyframe( limbStart + "_orientConstraint1." + ikTop + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbMid + "_orientConstraint1." + ikMid + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbTwist + "_orientConstraint1." + ikTwist + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBot + "_orientConstraint1." + ikBot + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            #cmds.setDrivenKeyframe( clavicleLimb[0] + "_orientConstraint1." + clavicleIkName + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )

            cmds.setAttr(fkTopCtrl + ".visibility", 1)
            cmds.setAttr(fkMidCtrl + ".visibility", 1)
            cmds.setAttr(fkBotCtrl + ".visibility", 1)
            #cmds.setAttr(fkclavicleCtrl + ".visibility", 1)  

            cmds.setDrivenKeyframe( fkTopCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            cmds.setDrivenKeyframe( fkMidCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            cmds.setDrivenKeyframe( fkBotCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            #cmds.setDrivenKeyframe( fkclavicleCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            
            cmds.setAttr(elbowIkCtrlName + ".visibility", 0)
            cmds.setDrivenKeyframe( elbowIkCtrlName + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled') 
            
            cmds.setAttr(armCtrlName + ".visibility", 0)
            cmds.setDrivenKeyframe( armCtrlName + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled') 
            
            cmds.setAttr(fkIkCtrlSwitch+".IK_Enabled", 1)

            cmds.setAttr (limbStart + "_orientConstraint1." + fkTopJnt + "W0", 0)
            cmds.setAttr (limbStart + "_orientConstraint1." + ikTop + "W1", 1)

            cmds.setAttr (limbMid + "_orientConstraint1." + fkMidJnt + "W0", 0)
            cmds.setAttr (limbMid + "_orientConstraint1." + ikMid + "W1", 1)

            cmds.setAttr (limbTwist + "_orientConstraint1." + fkTwistJnt + "W0", 0)
            cmds.setAttr (limbTwist + "_orientConstraint1." + ikTwist + "W1", 1)

            cmds.setAttr (limbBot + "_orientConstraint1." + fkBotJnt + "W0", 0)        
            cmds.setAttr (limbBot + "_orientConstraint1." + ikBot + "W1", 1)

            
            #cmds.setAttr (clavicleLimb[0] + "_orientConstraint1." + fkclavicleCtrl + "W0", 0)                        
            #cmds.setAttr (clavicleLimb[0] + "_orientConstraint1." + clavicleIkName + "W1", 1)
            

            cmds.setDrivenKeyframe( limbStart + "_orientConstraint1." + fkTopJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbMid + "_orientConstraint1." + fkMidJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbTwist + "_orientConstraint1." + fkTwistJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBot + "_orientConstraint1." + fkBotJnt + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            #cmds.setDrivenKeyframe( clavicleLimb[0] + "_orientConstraint1." + fkclavicleCtrl + "W0", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            
            cmds.setDrivenKeyframe( limbStart + "_orientConstraint1." + ikTop + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbMid + "_orientConstraint1." + ikMid + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbTwist + "_orientConstraint1." + ikTwist + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            cmds.setDrivenKeyframe( limbBot + "_orientConstraint1." + ikBot + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            #cmds.setDrivenKeyframe( clavicleLimb[0] + "_orientConstraint1." + clavicleIkName + "W1", currentDriver = fkIkCtrlSwitch + '.IK_Enabled' )
            
            cmds.setAttr(fkTopCtrl + ".visibility", 0)
            cmds.setAttr(fkMidCtrl + ".visibility", 0)
            cmds.setAttr(fkBotCtrl + ".visibility", 0)
            #cmds.setAttr(fkclavicleCtrl + ".visibility", 0)          

            cmds.setDrivenKeyframe( fkTopCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            cmds.setDrivenKeyframe( fkMidCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            cmds.setDrivenKeyframe( fkBotCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            #cmds.setDrivenKeyframe( fkclavicleCtrl + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled')
            
            cmds.setAttr(elbowIkCtrlName + ".visibility", 1)
            cmds.setDrivenKeyframe( elbowIkCtrlName + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled') 
            
            cmds.setAttr(armCtrlName + ".visibility", 1)
            cmds.setDrivenKeyframe( armCtrlName + ".visibility", currentDriver = fkIkCtrlSwitch + '.IK_Enabled') 


            locBot = self.changeSuffix(limbBot, "_FKIK_loc")

            anklePos = cmds.joint(limbBot, q = True, p = True)
            
            ankleLoc = self.locatorMaker(locBot, (anklePos[0], anklePos[1], anklePos[2]))
                        
            #match transform of nurb cirlce to locOffset

            cmds.pointConstraint( limbBot, locBot, maintainOffset = True)

            #needs absolute parenting because since the FKIK Switch is comprised of shapes it somehow duplicates the shapes
            cmds.parent(fkIkCtrlSwitch, locBot, absolute = True)

            ikCntrlGRP = cmds.group(locMid, elbowIkCtrlName, armCtrlName, locBot, name = ikCtrlGRPName, w = True)
            cmds.xform(piv = (0,0,0))

            ikJntGRP = cmds.group(ikTop, name = ikJntGRPName, w = True)
            cmds.xform(piv = (0,0,0))
                              
            outputList.append(ikJntGRP)
            outputList.append(ikCntrlGRP)
            
        
        return outputList 

    def setupIKPelvis(self, root, end):
        pelvisCtrlName = "pelvis_IK_ctrl"
        lowerBackCtrlName = "lowerBack_IK_ctrl"
        upperBackCtrlName = "upperBack_IK_ctrl"
        spineIkName = "spine_IK_handle"
        curveIkName = "spine_IK_curve"
        upperClusterName = "upper_IK_cluster"
        midClusterName = "mid_IK_cluster"
        lowerClusterName = "lower_IK_cluster"
        backBendCtrlName = "backBend_IK_ctrl"
        spineTwist = "Spine_Twist"
        spineRoll = "Spine_Roll"
        #clavicleIkName = "clavicle_l_IK"

        spineIkGrp = "spine_IK_GRP"
        splineIkGrp = "spine_IK_Spline_GRP"

        torsoIkCtrlName = "elbow_l_IK_ctrl"

        #fkSwitchNameCtrl = "arm_FKIK_l_ctrl" 

        ikArmGRPName = "IK_L_ARM_GRP"
        ikJntGRPName = "IK_L_ARM_JNT_GRP"
        ikCtrlGRPName = "IK_L_ARM_CTRL_GRP"
        pelvisChildren = cmds.listRelatives(root, allDescendents = True)

        pelvisChildren.reverse()

        ikPelvisChildren = []
        fkControlsToDelete = []
        fkCtrlHeirarchy = []
        shapeLessfkCtrlHeirarchy = []
        fkCtrlLegs = []
        fkCtrlWaist = []
        spineCtrlList = []
        spine02CtrlChildren = []

        fkArmJnts = []
        fkLegJnts = []
        fkHeadJnts = []

        #print "before " + str(pelvisChildren)
        

        #removes children, like hand joints, that shouldn't be affected by IK generation
        
        for x in pelvisChildren:
            #print x
            if not "spine_" in x or "pelvis_" in x:
                continue
            #deletes any previously made constraints from constrained joints in list
            elif "Constraint" in x:
                #print "constraint " + str(x)
                cmds.delete( x, cn=True )
                
            else:
                ikPelvisChildren.append(x)
       
        spine01 = ikPelvisChildren[0]
        spine02 = ikPelvisChildren[1]
        spine03 = ikPelvisChildren[2]
        spine04 = ikPelvisChildren[3]
        spine05 = ikPelvisChildren[4]


        ikPelvis = self.duplicateJnt(root, None, "_IK_jnt")
        ikSpine01 = self.duplicateJnt(spine01, root, "_IK_jnt")
        ikSpine02 = self.duplicateJnt(spine02, spine01, "_IK_jnt")      
        ikSpine03 = self.duplicateJnt(spine03, spine02, "_IK_jnt")
        ikSpine04 = self.duplicateJnt(spine04, spine03, "_IK_jnt") 
        ikSpine05 = self.duplicateJnt(spine05, spine04, "_IK_jnt")
        ikSpineEnd = self.duplicateJnt(end, spine05, "_IK_jnt")
        
        cmds.joint(ikPelvis, e=True, zeroScaleOrient=True, orientJoint = "xyz", secondaryAxisOrient="yup", children = True)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True, jointOrient = True) 
        
        #create local variable to refer to ctrl equivalent
        fkPelvisCtrl = self.changeSuffix(root, "_FK_ctrl")
        #print fkPelvisCtrl

        #get children of ctrls
        fkCtrlHeirarchy = cmds.listRelatives(fkPelvisCtrl, allDescendents = True)

        #iterate through children and select locator offsets
        for x in fkCtrlHeirarchy:
            #print x
            if "_loc" in x and not "Shape" in x:
                shapeLessfkCtrlHeirarchy.append(x)

        
        for x in shapeLessfkCtrlHeirarchy:
            #print x

            if "thigh_" in x:
                #print "fkCtrls " + x
                fkCtrlLegs.append(x)

            elif "satchelPivot_" in x or "Skirt_01" in x or "sideHipChain_01_" in x:
                fkCtrlWaist.append(x)

            elif "spine_" in x:
                #print "spine " + x
                spineCtrlList.append(x)

            elif "clavicle_" in x or "neck_01_" in x or "sleeve_" in x and self.sleeve_check.isChecked() or "breast_" in x and self.breasts_check.isChecked():
                #print "spine2 " + x
                spine02CtrlChildren.append(x)
        

        fkPelvisJnt = self.changeSuffix(root, "_FK_jnt")
        #print fkPelvisJnt

        fkJntHeirarchy = cmds.listRelatives(fkPelvisJnt, allDescendents = True)

        for x in fkJntHeirarchy:
            #print x

            if "thigh_" in x and not "Constraint" in x or "Skirt_01_" in x  and not "Constraint" in x or "sideHipChain_01_" in x and not "Constraint" in x:
                fkLegJnts.append(x)
                fkGrpName = self.changeSuffix(x, "_FK_GRP")
                #print fkGrpName
                legGrp = cmds.group(x, n = fkGrpName)
                #cmds.parent(legGrp, ikPelvis)

                cmds.parent(fkGrpName, "FK_JNT_GRP")
                cmds.parentConstraint(ikPelvis, legGrp, maintainOffset = True)

            elif "clavicle_" in x and not "Constraint" in x or "neck_01" in x and not "Constraint" in x or "breast_" in x and not "Constraint" in x:
                fkLegJnts.append(x)
                fkGrpName = self.changeSuffix(x, "_FK_GRP")
                legGrp = cmds.group(x, n = fkGrpName)
                #cmds.parent(legGrp, ikSpineEnd)

                cmds.parent(legGrp, "FK_JNT_GRP")
                cmds.parentConstraint(ikSpineEnd, legGrp, maintainOffset = True)

            elif "satchelPivot_" in x and not "Constraint" in x:
                fkLegJnts.append(x)
                fkGrpName = self.changeSuffix(x, "_FK_GRP")
                legGrp = cmds.group(x, n = fkGrpName)
                #cmds.parent(legGrp, ikSpine01)

                cmds.parent(legGrp, "FK_JNT_GRP")
                cmds.parentConstraint(ikSpine01, legGrp, maintainOffset = True)

        cmds.delete(fkPelvisJnt)

        spineIkHandle = cmds.ikHandle( name = spineIkName, 
                            solver = "ikSplineSolver", 
                            startJoint=ikPelvis, 
                            endEffector=ikSpineEnd,
                            createCurve = True,
                            parentCurve = True,
                            rootOnCurve = True,
                            simplifyCurve = False,
                            twistType = "linear")
        
        #create nurb cirlce to be used as control
        cmds.circle( name = pelvisCtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 20 )

        #match transform of nurb cirlce to locOffset
        self.matchTrans(ikPelvis, pelvisCtrlName)

        #create nurb cirlce to be used as control
        cmds.rotate(90, 0, 0, pelvisCtrlName, relative = True, worldSpace = True, objectSpace = True )
        
        cmds.select(pelvisCtrlName)
        self.colorOverride(pelvisCtrlName)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 
        



        #create nurb cirlce to be used as control
        cmds.circle( name = lowerBackCtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 17.5 )


        #match transform of nurb cirlce to locOffset
        self.matchTrans(ikPelvis, lowerBackCtrlName)

        #create nurb cirlce to be used as control
        cmds.rotate(90, 0, 0, lowerBackCtrlName, relative = True, worldSpace = True, objectSpace = True )
        
        cmds.select(lowerBackCtrlName)
        self.colorOverride(lowerBackCtrlName)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True)





        #create nurb cirlce to be used as control
        cmds.circle( name = upperBackCtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 12 )

        #match transform of nurb cirlce to locOffset
        self.matchTrans(ikSpineEnd, upperBackCtrlName)

        #create nurb cirlce to be used as control
        cmds.rotate(90, 0, 0, upperBackCtrlName, relative = True, worldSpace = True, objectSpace = True )
        
        cmds.select(upperBackCtrlName)
        self.colorOverride(upperBackCtrlName)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True)




        #create nurb cirlce to be used as control
        cmds.circle( name = backBendCtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 12 )

        #match transform of nurb cirlce to locOffset
        self.matchTrans(ikSpine03, backBendCtrlName)

        #create nurb cirlce to be used as control
        cmds.rotate(90, 0, 0, backBendCtrlName, relative = True, worldSpace = True, objectSpace = True )
        
        cmds.select(backBendCtrlName)
        self.colorOverride(backBendCtrlName)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 

        cmds.connectAttr( upperBackCtrlName + ".rotateY", spineIkName + ".twist" )
        cmds.connectAttr( lowerBackCtrlName + ".rotateY", spineIkName + ".roll" )

        

        cmds.select(ikPelvis, root, r = True )            
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )            

        cmds.select(ikSpine01, spine01, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )            

        cmds.select(ikSpine02,  spine02, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )

        cmds.select(ikSpine03, spine03, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )

        cmds.select(ikSpine04, spine04, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )

        cmds.select(ikSpine05, spine05, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )

        cmds.select(ikSpineEnd, end, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )
        
        outputList = []
        outputList.append(pelvisCtrlName)
        outputList.append(splineIkGrp)
        outputList.append(spineIkGrp)
        outputList.append(ikPelvis)

        
        for x in fkCtrlLegs:
            cmds.parent(x, pelvisCtrlName)
            #print "legs " + str(x)

        for x in fkCtrlWaist:
            cmds.parent(x, lowerBackCtrlName)
            #print "spine " + str(x)

        for x in spine02CtrlChildren:
            cmds.parent(x, upperBackCtrlName)

            if "clavicle_" in x:
                children = cmds.listRelatives(x, children = True)
                print children[1]
                childFK = self.changeSuffix(children[1], "_FK_jnt")
                outputList.append(childFK)
            #print "spine02 " + str(x)
                
 
        
        #print "after " + str(pelvisChildren) 
        #print spineIkHandle
        cmds.rename(spineIkHandle[2], curveIkName)       
        
        #upperCurveCVs = cmds.ls('{0}.cv[6:8]'.format(curveIkName), fl = True)
        upperCluster = cmds.cluster(curveIkName + ".cv[6:8]", name = upperClusterName)

        midCluster = cmds.cluster(curveIkName + ".cv[3:5]", name = midClusterName)

        #lowerCurveCVs = cmds.ls('{0}.cv[0:2]'.format(curveIkName), fl = True)
        lowerCluster = cmds.cluster(curveIkName + ".cv[0:2]", name = lowerClusterName)

        
        cmds.group(ikPelvis, name = spineIkGrp)
        cmds.xform(piv = (0,0,0))

        cmds.group( spineIkHandle[0], curveIkName, name=splineIkGrp )
        cmds.xform(piv = (0,0,0))

        cmds.parent(lowerCluster[1], lowerBackCtrlName)
        cmds.parent(backBendCtrlName, lowerCluster[1])
        cmds.parent(midCluster[1], backBendCtrlName)
        cmds.parent(upperBackCtrlName, midCluster[1])
        cmds.parent(upperCluster[1], upperBackCtrlName)
        
        cmds.parent(lowerBackCtrlName, pelvisCtrlName)

        for y in [".sx", ".sy", ".sz", ".visibility"]:
            
            cmds.setAttr(pelvisCtrlName + y, lock = True, keyable = False, channelBox = False)
            cmds.setAttr(upperBackCtrlName + y, lock = True, keyable = False, channelBox = False)
            cmds.setAttr(backBendCtrlName + y, lock = True, keyable = False, channelBox = False)
            cmds.setAttr(lowerBackCtrlName + y, lock = True, keyable = False, channelBox = False)

        

        
        return outputList

    def setupIKChain(self, startJnt):
        pelvisCtrlName = "pelvis_IK_ctrl"
        chain01CtrlName = "sideHipChain_01_IK_ctrl"
        chain02CtrlName = "sideHipChain_02_IK_ctrl"
        chain03CtrlName = "sideHipChain_03_IK_ctrl"
        chain04CtrlName = "sideHipChain_04_IK_ctrl"
        chain05CtrlName = "sideHipChain_05_IK_ctrl"        

        chainIkName = "sideHipChain_IK_handle"
        curveIkName = "sideHipChain_IK_handle_IK_curve"
        
        cluster01Name = "sideHipChain_01_IK_cluster"
        cluster02Name = "sideHipChain_02_IK_cluster"
        cluster03Name = "sideHipChain_03_IK_cluster"
        cluster04Name = "sideHipChain_04_IK_cluster"
        cluster05Name = "sideHipChain_05_IK_cluster"
        
        spineTwist = "sideHipChain_Twist"
        spineRoll = "sideHipChain_Roll"
        #clavicleIkName = "clavicle_l_IK"

        sideChainIkGrp = "sideHipChain_IK_Spline_GRP"

        torsoIkCtrlName = "elbow_l_IK_ctrl"

        #fkSwitchNameCtrl = "arm_FKIK_l_ctrl" 

        ikArmGRPName = "IK_Chain_GRP"
        ikJntGRPName = "IK_Chain_JNT_GRP"
        ikCtrlGRPName = "IK_Chain_CTRL_GRP"
        chainChildren = cmds.listRelatives(startJnt, allDescendents = True)

        chainChildren.reverse()

        ikchainChildren = []
        
        #print "before " + str(chainChildren)
        

        #removes children, like hand joints, that shouldn't be affected by IK generation
        
        for x in chainChildren:
            #print x
            
            if "Constraint" in x:
                #print "constraint " + str(x)
                cmds.delete( x, cn=True )                
            else:
                ikchainChildren.append(x)

        
        #print "after " + str(chainChildren)
        #print ikchainChildren
        
        spine01 = ikchainChildren[0]
        spine02 = ikchainChildren[1]
        spine03 = ikchainChildren[2]
        spine04 = ikchainChildren[3]
        spine05 = ikchainChildren[4]
        spine06 = ikchainChildren[5]

        ikChain01 = self.duplicateJnt(startJnt, None, "_IK_jnt")
        ikChain02 = self.duplicateJnt(spine01, startJnt, "_IK_jnt")      
        ikChain03 = self.duplicateJnt(spine02, spine01, "_IK_jnt")
        ikChain04 = self.duplicateJnt(spine03, spine02, "_IK_jnt")
        ikChain05 = self.duplicateJnt(spine04, spine03, "_IK_jnt")
        ikChain06 = self.duplicateJnt(spine05, spine04, "_IK_jnt")
        ikChain07 = self.duplicateJnt(spine06, spine05, "_IK_jnt")
        
        cmds.joint(ikChain01, e=True, zeroScaleOrient=True, orientJoint = "xyz", secondaryAxisOrient="yup", children = True)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True, jointOrient = True) 
        
        fkTopChainJnt = self.changeSuffix(ikChain01, "_FK_jnt")

        cmds.delete(fkTopChainJnt)

        chainIkHandle = cmds.ikHandle( name = chainIkName, 
                            solver = "ikSplineSolver", 
                            startJoint=ikChain01, 
                            endEffector=ikChain07,
                            createCurve = True,
                            parentCurve = True,
                            rootOnCurve = True,
                            simplifyCurve = False,
                            twistType = "linear")

        
        cmds.rename(chainIkHandle[2], curveIkName) 
        
        #create nurb cirlce to be used as control
        cmds.circle( name = chain01CtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 5 )

        #match transform of nurb cirlce to locOffset
        self.matchTrans(ikChain01, chain01CtrlName)

        #create nurb cirlce to be used as control
        cmds.rotate(90, 0, 0, chain01CtrlName, relative = True, worldSpace = True, objectSpace = True )
        
        cmds.select(chain01CtrlName)
        self.colorOverride(chain01CtrlName)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 


        


        #create nurb cirlce to be used as control
        cmds.circle( name = chain02CtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 2 )

        #match transform of nurb cirlce to locOffset
        self.matchTrans(ikChain02, chain02CtrlName)

        #create nurb cirlce to be used as control
        cmds.rotate(90, 0, 0, chain02CtrlName, relative = True, worldSpace = True, objectSpace = True )
        
        cmds.select(chain02CtrlName)
        self.colorOverride(chain02CtrlName)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 



        #create nurb cirlce to be used as control
        cmds.circle( name = chain03CtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 2 )

        #match transform of nurb cirlce to locOffset
        self.matchTrans(ikChain04, chain03CtrlName)

        #create nurb cirlce to be used as control
        cmds.rotate(90, 0, 0, chain03CtrlName, relative = True, worldSpace = True, objectSpace = True )
        
        cmds.select(chain03CtrlName)
        self.colorOverride(chain03CtrlName)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 



        #create nurb cirlce to be used as control
        cmds.circle( name = chain04CtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 2 )

        #match transform of nurb cirlce to locOffset
        self.matchTrans(ikChain06, chain04CtrlName)

        #create nurb cirlce to be used as control
        cmds.rotate(90, 0, 0, chain04CtrlName, relative = True, worldSpace = True, objectSpace = True )
        
        cmds.select(chain04CtrlName)
        self.colorOverride(chain04CtrlName)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 



        #create nurb cirlce to be used as control
        cmds.circle( name = chain05CtrlName, normal = (1, 0, 0), center = (0, 0, 0), radius = 2 )


        #match transform of nurb cirlce to locOffset
        self.matchTrans(ikChain07, chain05CtrlName)

        #create nurb cirlce to be used as control
        cmds.rotate(90, 0, 0, chain05CtrlName, relative = True, worldSpace = True, objectSpace = True )
        
        cmds.select(chain05CtrlName)
        self.colorOverride(chain05CtrlName)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True)





        cmds.connectAttr( chain01CtrlName + ".rotateY", chainIkName + ".twist" )
        cmds.connectAttr( chain05CtrlName + ".rotateY", chainIkName + ".roll" )

        

        cmds.select(ikChain01, startJnt, r = True )            
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )            

        cmds.select(ikChain02, spine01, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )            

        cmds.select(ikChain03,  spine02, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )

        cmds.select(ikChain04, spine03, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )

        cmds.select(ikChain05, spine04, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )

        cmds.select(ikChain06, spine05, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )

        cmds.select(ikChain07, spine06, r = True )
        cmds.parentConstraint( maintainOffset = True , weight = 1.0 )
             
        
        #upperCurveCVs = cmds.ls('{0}.cv[6:8]'.format(curveIkName), fl = True)
        cluster01 = cmds.cluster(curveIkName + ".cv[0:1]", name = cluster01Name)
        cluster02 = cmds.cluster(curveIkName + ".cv[2:3]", name = cluster02Name)
        cluster03 = cmds.cluster(curveIkName + ".cv[4]", name = cluster03Name)
        cluster04 = cmds.cluster(curveIkName + ".cv[5:6]", name = cluster04Name)
        cluster05 = cmds.cluster(curveIkName + ".cv[7:8]", name = cluster05Name)

        
        cmds.group( chainIkHandle[0], curveIkName, name=sideChainIkGrp )

        cmds.parent(cluster01[1], chain01CtrlName)
        cmds.parent(chain02CtrlName, cluster01[1])

        cmds.parent(cluster02[1], chain02CtrlName)        
        cmds.parent(chain03CtrlName, cluster02[1])

        cmds.parent(cluster03[1], chain03CtrlName)        
        cmds.parent(chain04CtrlName, cluster03[1])

        cmds.parent(cluster04[1], chain04CtrlName)        
        cmds.parent(chain05CtrlName, cluster04[1])
        
        cmds.parent(cluster05[1], chain05CtrlName)
        
        
        
        #cmds.parent(chain05CtrlName, chain01CtrlName)

        for y in [".sx", ".sy", ".sz", ".visibility"]:
            
            cmds.setAttr(chain01CtrlName + y, lock = True, keyable = False, channelBox = False)
            cmds.setAttr(chain02CtrlName + y, lock = True, keyable = False, channelBox = False)
            cmds.setAttr(chain05CtrlName + y, lock = True, keyable = False, channelBox = False)

        
        outputList = []
        outputList.append(chain01CtrlName)
        outputList.append(sideChainIkGrp)
        outputList.append(ikChain01)

        
        return outputList

    def makeSwitchCtrl(self, switchName, parentGrpName):

        ctrlSwitch = cmds.textCurves( f='Times-Roman', t= switchName )
        switchDescendants = cmds.listRelatives(ctrlSwitch, allDescendents = True)

        switchDescendants.reverse()

        textGrp = cmds.group(name = parentGrpName, w = True)
        cmds.xform(piv = (0,0,0))

        cmds.select("curve1")
        cmds.select("curve2", add = True)
        cmds.select("curve3", add = True)
        cmds.select("curve4", add = True)
        cmds.parent(w = True)
        cmds.delete(ctrlSwitch)
        
        curve01 = self.changeSuffix(parentGrpName, "_01_letter")
        cmds.rename("curve1", curve01)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 
        
        curve02 = self.changeSuffix(parentGrpName, "_02_letter")
        cmds.rename("curve2", curve02)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True)

        curve03 = self.changeSuffix(parentGrpName, "_03_letter")
        cmds.rename("curve3", curve03)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True)

        curve04 = self.changeSuffix(parentGrpName, "_04_letter")
        cmds.rename("curve4", curve04)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True)

        shape1 = curve01+"Shape"
        shape2 = curve02+"Shape"
        shape3 = curve03+"Shape"
        shape4 = curve04+"Shape"

        cmds.select(shape1)
        cmds.select(shape2, add = True)
        cmds.select(shape3, add = True)
        cmds.select(shape4, add = True)

        cmds.select(textGrp, add = True)
        cmds.parent( r = True, s = True)

        cmds.setAttr(shape1 + ".overrideEnabled", 1)
        cmds.setAttr(shape2 + ".overrideEnabled", 1)
        cmds.setAttr(shape3 + ".overrideEnabled", 1)
        cmds.setAttr(shape4 + ".overrideEnabled", 1)
        
        #cmds.setAttr(node + ".overrideColor", 6)

        #gets bounding box of selection and saves info of the bounding box into a list as xmin, ymin, zmin, xmax, ymax, zmax
        bbox = cmds.exactWorldBoundingBox(textGrp)

        #freeze transforms prior to moving pivot
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 

        #define that the selection's pivot should be at the bottom of the bounding box
        bottomPivot = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]

        #moves pivot to the bottom of the bounding box
        cmds.xform(textGrp, piv=bottomPivot, ws=True)

        #determines the distance to the origin from the current location in worldspace of the pivot
        distanceToOrigin = [-((bbox[0] + bbox[3])/2), -(bbox[1]), -((bbox[2] + bbox[5])/2)]

        #moves the object to the origin
        cmds.xform(textGrp, t = distanceToOrigin,  ws=True) 

        #freeze transforms after the move
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 

        cmds.delete(curve01)
        cmds.delete(curve02)
        cmds.delete(curve03)
        cmds.delete(curve04)

        cmds.addAttr(textGrp, longName='IK_Enabled', attributeType = "long", keyable = True, minValue = 0.0, maxValue = 1.0)
        
        if "_l_"in parentGrpName:
            cmds.expression( unitConversion = "all", s="if (" + textGrp + ".IK_Enabled == 1)\n{\n\t" + shape1 + ".overrideColor = 1;\n\t" + shape2 + ".overrideColor = 1;\n\t" + shape3 + ".overrideColor = 6;\n\t" + shape4 + ".overrideColor = 6;\n}\nif (" + textGrp + ".IK_Enabled == 0)\n{\n\t" + shape1 + ".overrideColor = 6;\n\t" + shape2 + ".overrideColor = 6;\n\t" + shape3 + ".overrideColor = 1;\n\t" + shape4 +".overrideColor = 1;\n}")
        elif "_r_" in parentGrpName:
            cmds.expression( unitConversion = "all", s="if (" + textGrp + ".IK_Enabled == 1)\n{\n\t" + shape1 + ".overrideColor = 1;\n\t" + shape2 + ".overrideColor = 1;\n\t" + shape3 + ".overrideColor = 13;\n\t" + shape4 + ".overrideColor = 13;\n}\nif (" + textGrp + ".IK_Enabled == 0)\n{\n\t" + shape1 + ".overrideColor = 13;\n\t" + shape2 + ".overrideColor = 13;\n\t" + shape3 + ".overrideColor = 1;\n\t" + shape4 +".overrideColor = 1;\n}")



        return textGrp
    """
    @param: jName - name of input joint

    This function makes a list of all the descendents of joint and connects them with control
    """
    def addJntCtrls(self, jName):

        #entire jnt heirarchy
        jntList = cmds.listRelatives(jName, allDescendents = True)
            
        jntList.reverse() 
        

        leftIkLeg = []
        rightIkLeg = []
        fkSkeleton = []
        splineIkEnds = []
        tempIkName = ''
        handJnts = []
        shoulderSleeveJnts = []
        elbowSleeveJnts = []
        outputList = []
        
        
        
        dupSkeleton = cmds.duplicate(jntList, returnRootsOnly = True, renameChildren = True)

        ctrlRoot = self.makeFKControl(jName, None)


        ctrlGRP = cmds.group(ctrlRoot, name = "CTRL_GRP", w = True)
        cmds.xform(piv = (0,0,0))
            
        jntGRP = cmds.group(name = "JNT_GRP", w = True)
        cmds.xform(piv = (0,0,0))
        cmds.setAttr(jntGRP + ".visibility", 0)

        bindJntGRP = cmds.group(jName, name = "BIND_JNT_GRP", w = True)
        cmds.xform(piv = (0,0,0))

        fkJntGRP = cmds.group(name = "FK_JNT_GRP", w = True)
        cmds.xform(piv = (0,0,0))

        ikJntGRP = cmds.group(name = "IK_JNT_GRP", w = True)
        cmds.xform(piv = (0,0,0))

        cmds.parent(bindJntGRP, jntGRP)
        cmds.parent(fkJntGRP, jntGRP)
        cmds.parent(ikJntGRP, jntGRP)
        

        autoRigGRP = cmds.group(ctrlGRP,jntGRP, name = "Rig_GRP", w = True)
        cmds.xform(piv = (0,0,0))

        for x in dupSkeleton:
            if "middle" in x or "index" in x or "ring" in x or "pinky" in x or "thumb"  in x or "finger" in x:
                #print x
                handJnts.append(x)
            elif "shoulder_" in x or "upperSleeve" in x and self.shoulderSleeve_check.isChecked():

                #print x

                if "shoulder_" in x:
                    fkSkeleton.append(x)
                    shoulderSleeveJnts.append(x)

                if "upperSleeve" in x:
                    #print x
                    shoulderSleeveJnts.append(x)

            elif "elbow_" in x or "lowerSleeve" in x and self.elbowSleeve_check.isChecked():

                #print x

                if "elbow_" in x:
                    fkSkeleton.append(x)
                    elbowSleeveJnts.append(x)

                if "lowerSleeve" in x:
                    #print x
                    elbowSleeveJnts.append(x)
            else:

                fkSkeleton.append(x)
        
        for x in fkSkeleton:
            #print "before" + str(x)
            tempName = self.changeSuffix(fkSkeleton[fkSkeleton.index(x)], "_FK_jnt")
            cmds.rename(x , tempName)

            originalJnt = self.changeSuffix(tempName, "_jnt")
            cmds.parentConstraint( tempName, originalJnt, maintainOffset = True, weight = 1.0 )

            """
            #print "after" + str(x)
            if "pelvis_" in tempName or "clavicle_" in tempName or "thigh_" in tempName or "Bead_" in tempName or "satchel" in tempName or "hairBunPivot_" in tempName or "eyebrow_" in tempName:
                originalJnt = self.changeSuffix(tempName, "_jnt")
                #print originalJnt
                cmds.parentConstraint( tempName, originalJnt, maintainOffset = True, weight = 1.0 )
            else:
                originalJnt = self.changeSuffix(tempName, "_jnt")
                cmds.orientConstraint( tempName, originalJnt, maintainOffset = True, weight = 1.0 )
            """

        for x in fkSkeleton:
            #print "Before " + str(x)
            x = self.changeSuffix(x, "_FK_jnt")
            #print "After " + str(x)
            if not self.nonBiped_radio.isChecked():
                if "head_02_" not in x and "End_" in x or "foreArm_" in x or "head_01_" in x or "floatingOrb_" in x or "fingerPivot_" in x or "thumbPivot_" in x:
                    continue
                elif not self.ikSpine_check.isChecked() and "spine_03_" in x:
                    continue
                elif self.ikSpine_check.isChecked() and "spine_06_" in x:
                    continue
                else:
                    parent = cmds.listRelatives(x, p = True)

                    #twist joints don't need a control
                    #if the twist joint is parent, get grandparent joint
                    
                    if "foreArm_" in parent[0]:
                        parentOfParent = cmds.listRelatives(parent[0], p = True)
                        ctrl = self.makeFKControl(x, parentOfParent[0])

                        expName = self.changeSuffix(parent[0], "_offset_twist")

                        #adds expression to rotate fk foreArm and subsequently the base foreArm
                        cmds.expression(name = expName, s=parent[0] + '.rotateX = ( ' + ctrl + '.rotateX ) / 2')

                    elif "fingerPivot_" in parent[0]:
                        parentOfParent = cmds.listRelatives(parent[0], p = True)
                        ctrl = self.makeFKControl(x, parentOfParent[0])


                    elif "clavicle_" in x or "neck_01_" in x or "breast_" in x:
                        ctrl = self.makeFKControl(x, "spine_02_FK_ctrl")

                    elif "Bead_" in x or "neck_02_" in x:
                        ctrl = self.makeFKControl(x, "neck_01_FK_ctrl")
                        #head rotation is actually being controlled by control at neck_02 location, control and offset loc needed to be renamed for clarity
                        if "neck_02_" in x:
                            cmds.select( "neck_02_FK_offset_loc", r=True )
                            cmds.rename( "head_01_FK_offset_loc" )
                            cmds.select( "neck_02_FK_ctrl", r=True )
                            cmds.rename("head_01_FK_ctrl")

                    elif "ear_" in x and "_01_" in x or "earRing_" in x and "_01_" in x or "hornChain_" in x and "_01_" in x or "eyebrow_" in x:
                        ctrl = self.makeFKControl(x, "head_01_FK_ctrl")

                    elif "earEnd_" in parent[0]:

                        if "_l_" in x:
                            ctrl = self.makeFKControl(x, "ear_l_02_FK_ctrl")
                        elif "_r_" in x:
                            ctrl = self.makeFKControl(x, "ear_r_02_FK_ctrl")

                    elif "head_02_" in x and not self.floatingOrb_check.isChecked():
                        continue

                    else:
                        ctrl = self.makeFKControl(x, parent[0])
            else:
                if "head_02_" in x or "End_" in x:
                    continue
                else:
                    parent = cmds.listRelatives(x, p = True)
                    ctrl = self.makeFKControl(x, parent[0])

        for x in handJnts:
            tempName = self.changeSuffix(handJnts[handJnts.index(x)], "_FK_jnt")
            cmds.rename(x , tempName)
            if "fingerPivot_" in x:
                fingerPivotLocNameOrig = self.changeSuffix(x, "_loc")
                #print fingerPivotLocNameOrig
                fingerPivotPos = cmds.getAttr(fingerPivotLocNameOrig + ".localPosition")
                fingerPivotLocNameNew = self.changeSuffix(x, "_offset_loc")           
                fingerPivotLoc = self.locatorMaker(fingerPivotLocNameNew, fingerPivotPos[0])

                cmds.makeIdentity(fingerPivotLoc, apply=True, r=True, s=True, t=True, n=False, pn=True) 

                fingerPivotJntName = self.changeSuffix(x, "_jnt")

                cmds.parentConstraint(fingerPivotJntName, fingerPivotLocNameNew, maintainOffset = True)                

                cmds.parentConstraint(fingerPivotLocNameNew, tempName, maintainOffset = True)

                if "_l_" in fingerPivotLocNameNew:
                    handCtrlGRP = cmds.group(fingerPivotLocNameNew, name = "hand_l_ctrl_GRP")
                    cmds.xform(piv = (0,0,0))
                    handJntGRP = cmds.group(tempName, name = "hand_l_FK_jnt_GRP")
                    cmds.xform(piv = (0,0,0))

                    cmds.parent(handCtrlGRP, ctrlGRP)
                    cmds.parent(handJntGRP, fkJntGRP)
                elif "_r_" in fingerPivotLocNameNew:
                    handCtrlGRP = cmds.group(fingerPivotLocNameNew, name = "hand_r_ctrl_GRP")
                    cmds.xform(piv = (0,0,0))
                    handJntGRP = cmds.group(tempName, name = "hand_r_FK_jnt_GRP")
                    cmds.xform(piv = (0,0,0))

                    cmds.parent(handCtrlGRP, ctrlGRP)
                    cmds.parent(handJntGRP, fkJntGRP)
            elif "End_" in x:
                continue
            else:
                parent = cmds.listRelatives(tempName, p = True)

                if "fingerPivot_" in parent[0]:

                    fingerPivotLocNameNew = self.changeSuffix(parent[0], "_offset_loc")

                    ctrl = self.makeFKControl(tempName, None)
                    originalJnt = self.changeSuffix(tempName, "_jnt")
                    jntPos = cmds.joint(originalJnt, q = True, p = True)
                    
                    
                    offsetLocName = self.changeSuffix(originalJnt, "_offset_loc")

                    offsetLoc = self.locatorMaker(offsetLocName, jntPos)
                    self.colorOverride(offsetLocName)
                    self.matchTrans(originalJnt, offsetLocName)
                    self.matchTrans(offsetLocName, ctrl)
                    cmds.parent(offsetLocName, fingerPivotLocNameNew)
                    cmds.parent(ctrl, offsetLocName)
                    cmds.orientConstraint( ctrl, tempName, maintainOffset = True, weight = 1.0 )
                    cmds.scaleConstraint(originalJnt, fingerPivotLocNameNew, mo=True)
                    cmds.orientConstraint( tempName, originalJnt, maintainOffset = True, weight = 1.0 )
                    
                    
                    #cmds.parent(ctrl, offsetLocName)
                    
                else:
                    originalJnt = self.changeSuffix(tempName, "_jnt")
                    cmds.orientConstraint( tempName, originalJnt, maintainOffset = True, weight = 1.0 )
                    ctrl = self.makeFKControl(tempName, parent[0])
        
        if self.shoulderSleeve_check.isChecked():

            for x in shoulderSleeveJnts:
                #print x
                tempName = self.changeSuffix(shoulderSleeveJnts[shoulderSleeveJnts.index(x)], "_FK_jnt")
                
                if "shoulder_" in x:
                    shoulderLocNameOrig = self.changeSuffix(x, "_loc")
                    #print shoulderLocNameOrig
                    shoulderPos = cmds.getAttr(shoulderLocNameOrig + ".localPosition")
                    shoulderLocNameNew = self.changeSuffix(x, "_upperSleeve_offset_loc")           
                    shoulderLoc = self.locatorMaker(shoulderLocNameNew, shoulderPos[0])

                    shoulderJntName = self.changeSuffix(x, "_jnt")

                    cmds.parentConstraint(shoulderJntName, shoulderLocNameNew, maintainOffset = True)                

                    #cmds.parentConstraint(shoulderLocNameNew, tempName, maintainOffset = True)

                    if "_l_" in shoulderLocNameNew:
                        upperSleeveCtrlGRP = cmds.group(shoulderLocNameNew, name = "upperSleeve_l_ctrl_GRP", w = True)
                        cmds.xform(piv = (0,0,0))
                        #cmds.select(clear = True)
                        upperSleeveJntGRP = cmds.group(name = "upperSleeve_l_FK_jnt_GRP", w = True)
                        cmds.xform(piv = (0,0,0))

                        cmds.parent(upperSleeveCtrlGRP, ctrlGRP)
                        cmds.parent(upperSleeveJntGRP, fkJntGRP)

                    elif "_r_" in shoulderLocNameNew:
                        upperSleeveCtrlGRP = cmds.group(shoulderLocNameNew, name = "upperSleeve_r_ctrl_GRP", w = True)
                        cmds.xform(piv = (0,0,0))
                        #cmds.select(clear = True)
                        upperSleeveJntGRP = cmds.group(name = "upperSleeve_r_FK_jnt_GRP", w = True)
                        cmds.xform(piv = (0,0,0))

                        cmds.parent(upperSleeveCtrlGRP, ctrlGRP)
                        cmds.parent(upperSleeveJntGRP, fkJntGRP)
                    
                elif "End_" in x:
                    continue
                else:
                    cmds.rename(x , tempName)
                    parent = cmds.listRelatives(tempName, p = True)

                    if "shoulder_" in parent[0]:

                        shoulderLocNameNew = self.changeSuffix(parent[0], "_upperSleeve_offset_loc")
                        originalJnt = self.changeSuffix(tempName, "_jnt")
                        
                        
                        ctrl = self.makeFKControl(tempName, None)
                        jntPos = cmds.joint(originalJnt, q = True, p = True)
                        
                        
                        offsetLocName = self.changeSuffix(originalJnt, "_offset_loc")

                        offsetLoc = self.locatorMaker(offsetLocName, jntPos)
                        self.colorOverride(offsetLocName)
                        self.matchTrans(originalJnt, offsetLocName)
                        self.matchTrans(offsetLocName, ctrl)
                        cmds.parent(offsetLocName, shoulderLocNameNew)
                        cmds.parent(ctrl, offsetLocName)

                        
                        #cmds.parent(upperSleeveCtrlGRP, ctrlGRP)
                        cmds.parent(tempName, upperSleeveJntGRP)

                        cmds.select(ctrl)
                        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 

                        #match locOffset to incoming joint
                        #self.matchTrans(originalJnt, shoulderLocNameNew)
                        cmds.parentConstraint(ctrl, originalJnt, maintainOffset = True)
                        cmds.scaleConstraint(originalJnt, shoulderLocNameNew, mo=True)
                        cmds.parentConstraint(originalJnt, tempName, maintainOffset = True)                

                    else:
                        originalJnt = self.changeSuffix(tempName, "_jnt")
                        cmds.parentConstraint(tempName, originalJnt, maintainOffset = True)                  
                        ctrl = self.makeFKControl(tempName, parent[0])

        if self.elbowSleeve_check.isChecked():
            for x in elbowSleeveJnts:
                print x
                tempName = self.changeSuffix(elbowSleeveJnts[elbowSleeveJnts.index(x)], "_FK_jnt")
                
                if "elbow_" in x:
                    elbowLocNameOrig = self.changeSuffix(x, "_loc")
                    #print elbowLocNameOrig
                    elbowPos = cmds.getAttr(elbowLocNameOrig + ".localPosition")
                    elbowLocNameNew = self.changeSuffix(x, "_lowerSleeve_offset_loc")           
                    elbowLoc = self.locatorMaker(elbowLocNameNew, elbowPos[0])

                    elbowJntName = self.changeSuffix(x, "_jnt")

                    cmds.parentConstraint(elbowJntName, elbowLocNameNew, maintainOffset = True)                

                    #cmds.parentConstraint(elbowLocNameNew, tempName, maintainOffset = True)

                    if "_l_" in elbowLocNameNew:
                        lowerSleeveCtrlGRP = cmds.group(elbowLocNameNew, name = "lowerSleeve_l_ctrl_GRP", w = True)
                        cmds.xform(piv = (0,0,0))
                        #cmds.select(clear = True)
                        lowerSleeveJntGRP = cmds.group(name = "lowerSleeve_l_FK_jnt_GRP", w = True)
                        cmds.xform(piv = (0,0,0))

                        cmds.parent(lowerSleeveCtrlGRP, ctrlGRP)
                        cmds.parent(lowerSleeveJntGRP, fkJntGRP)

                    elif "_r_" in elbowLocNameNew:
                        lowerSleeveCtrlGRP = cmds.group(elbowLocNameNew, name = "lowerSleeve_r_ctrl_GRP", w = True)
                        cmds.xform(piv = (0,0,0))
                        #cmds.select(clear = True)
                        lowerSleeveJntGRP = cmds.group(name = "lowerSleeve_r_FK_jnt_GRP", w = True)
                        cmds.xform(piv = (0,0,0))

                        cmds.parent(lowerSleeveCtrlGRP, ctrlGRP)
                        cmds.parent(lowerSleeveJntGRP, fkJntGRP)
                    
                elif "End_" in x:
                    continue
                else:
                    cmds.rename(x , tempName)
                    parent = cmds.listRelatives(tempName, p = True)

                    if "elbow_" in parent[0]:

                        elbowLocNameNew = self.changeSuffix(parent[0], "_lowerSleeve_offset_loc")
                        originalJnt = self.changeSuffix(tempName, "_jnt")
                        
                        
                        ctrl = self.makeFKControl(tempName, None)
                        jntPos = cmds.joint(originalJnt, q = True, p = True)
                        
                        
                        offsetLocName = self.changeSuffix(originalJnt, "_offset_loc")

                        offsetLoc = self.locatorMaker(offsetLocName, jntPos)
                        self.colorOverride(offsetLocName)
                        self.matchTrans(originalJnt, offsetLocName)
                        self.matchTrans(offsetLocName, ctrl)
                        cmds.parent(offsetLocName, elbowLocNameNew)
                        cmds.parent(ctrl, offsetLocName)

                        
                        #cmds.parent(lowerSleeveCtrlGRP, ctrlGRP)
                        cmds.parent(tempName, lowerSleeveJntGRP)

                        cmds.select(ctrl)
                        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 

                        #match locOffset to incoming joint
                        #self.matchTrans(originalJnt, elbowLocNameNew)
                        cmds.parentConstraint(ctrl, originalJnt, maintainOffset = True)
                        cmds.scaleConstraint(originalJnt, elbowLocNameNew, mo=True)
                        cmds.parentConstraint(originalJnt, tempName, maintainOffset = True)                

                    else:
                        originalJnt = self.changeSuffix(tempName, "_jnt")
                        cmds.parentConstraint(tempName, originalJnt, maintainOffset = True)                
                        ctrl = self.makeFKControl(tempName, parent[0])

        if self.ikLegs_check.isChecked() and self.Right_Leg_check.isChecked():
            rLegIKList = self.setupIKLimb("thigh_r_jnt")
            cmds.parent(rLegIKList[0], ikJntGRP)
            cmds.parent(rLegIKList[1], ctrlRoot)

        if self.ikLegs_check.isChecked() and self.Left_Leg_check.isChecked():
            lLegIKList = self.setupIKLimb("thigh_l_jnt")
            cmds.parent(lLegIKList[0], ikJntGRP)
            cmds.parent(lLegIKList[1], ctrlRoot)

        if self.ikLegs_check.isChecked() and self.Center_Leg_check.isChecked():
            lLegIKList = self.setupIKLimb("thigh_jnt")
            cmds.parent(lLegIKList[0], ikJntGRP)
            cmds.parent(lLegIKList[1], ctrlRoot)

        if self.ikArms_check.isChecked() and self.Right_Arm_check.isChecked():
            
            rArmIKList = self.setupIKLimb("shoulder_r_jnt")
            #print rArmIKList
            cmds.parent(rArmIKList[0], ikJntGRP)
            cmds.parent(rArmIKList[1], ctrlRoot)

        if self.ikArms_check.isChecked() and self.Left_Arm_check.isChecked():
            lArmIKList = self.setupIKLimb("shoulder_l_jnt")
            cmds.parent(lArmIKList[0], ikJntGRP)
            cmds.parent(lArmIKList[1], ctrlRoot)

        if self.ikSpine_check.isChecked():
            #output list of start and end of spline IK
            spineIKList = self.setupIKPelvis("pelvis_jnt", "spine_06_jnt")
            """
            outputList.append(pelvisCtrlName)
            outputList.append(splineIkGrp)
            outputList.append(curveIkName)
            outputList.append(ikPelvis)
            """

            print spineIKList
            cmds.parent(spineIKList[0], ctrlRoot)
            cmds.parent(spineIKList[1], autoRigGRP)
            cmds.parent(spineIKList[2], ikJntGRP)
            cmds.parentConstraint(jName, spineIKList[2], mo=True)
            cmds.delete("pelvis_FK_offset_loc")
            cmds.setAttr(spineIKList[1] + ".visibility", 0)

            if self.Left_Leg_check.isChecked():
                cmds.parentConstraint(spineIKList[3], "thigh_l_IK_jnt", mo=True)

            if self.Right_Leg_check.isChecked():
                cmds.parentConstraint(spineIKList[3], "thigh_r_IK_jnt", mo=True)

            if self.Center_Leg_check.isChecked():
                cmds.parentConstraint(spineIKList[3], "thigh_IK_jnt", mo=True)

            if "_l_" in spineIKList[4]:
                cmds.parentConstraint(spineIKList[4], "shoulder_l_IK_jnt", mo=True)
            elif "_r_" in spineIKList[4]:
                cmds.parentConstraint(spineIKList[4], "shoulder_r_IK_jnt", mo=True)
            
            if "_r_" in spineIKList[5]:
                cmds.parentConstraint(spineIKList[5], "shoulder_r_IK_jnt", mo=True)
            elif "_l_" in spineIKList[5]:
                cmds.parentConstraint(spineIKList[5], "shoulder_l_IK_jnt", mo=True)

        if self.ikSideChain_check.isChecked():

            sideChainIKList = self.setupIKChain("sideHipChain_01_r_jnt")            
            
            cmds.parent(sideChainIKList[0], "lowerBack_IK_ctrl")
            cmds.parent(sideChainIKList[1], autoRigGRP)
            cmds.delete("sideHipChain_01_r_FK_offset_loc")
            cmds.setAttr(sideChainIKList[1] + ".visibility", 0)
            cmds.parent(sideChainIKList[2], "pelvis_IK_jnt")
            
            """

            cmds.parent(sideChainIKList[0], ctrlRoot)
            cmds.parent(sideChainIKList[1], autoRigGRP)
            cmds.parent(sideChainIKList[2], ikJntGRP)
            cmds.parentConstraint(jName, sideChainIKList[2], mo=True)
            cmds.delete("pelvis_FK_offset_loc")
            cmds.setAttr(sideChainIKList[1] + ".visibility", 0)

            #cmds.scaleConstraint(ctrlRoot, spineIKList[2], mo=True)
            """

        cmds.scaleConstraint(ctrlRoot, jntGRP, mo=True)

        self.deleteLocTemplate()
       
        self.cleanUpAttrs(autoRigGRP)

        return

    """
    @param: rootJnt - rootJoint
    @param: rootCtrl - rootControl

    This function creates the groups to organize the outliner. The inputs are the root joint and control
    so them and their children can be moved into a group.

    The root control also uses a scale constraint on the jntGRP to scale the joints as well
    """
    def deleteLocTemplate(self):
        cmds.delete(self.locGrp)

    def cleanUpAttrs(self, topRigNode):

        print topRigNode

        for y in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]:
            
            cmds.setAttr(topRigNode + y, lock = True, keyable = False, channelBox = False)


        rigNodes = cmds.listRelatives(topRigNode, allDescendents = True)
        
        for x in rigNodes:

            if "Shape" in x and cmds.objectType(x, isType = "locator"):
                cmds.setAttr(x + ".visibility", 0)

            elif "_handle" in x and cmds.objectType(x, isType = "ikHandle"):
                cmds.setAttr(x + ".visibility", 0)

            elif cmds.objectType(x, isType = "clusterHandle"):
                cmds.setAttr(x + ".visibility", 0)

            elif "foot_" in x and "_IK_ctrl" in x and not "Shape" in x:

                for y in [".sx", ".sy", ".sz", ".visibility"]:
                    cmds.setAttr(x + y, lock = True, keyable = False, channelBox = False)


            elif "_GRP" in x and cmds.objectType(x, isType = "transform"):
                for y in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]:
                    cmds.setAttr(x + y, lock = True, keyable = False, channelBox = False)

            elif "parentConstraint" in x:
                #print x
                
                ctrl = cmds.parentConstraint(x, q = True, targetList = True)

                #print "CTRL", ctrl

                if "root_" in ctrl[0]:
                    cmds.setAttr(ctrl[0] + ".visibility", lock = True, keyable = False, channelBox = False)
                else:
                    for y in [".sx", ".sy", ".sz", ".visibility"]:
                        cmds.setAttr(ctrl[0] + y, lock = True, keyable = False, channelBox = False)

            elif "orientConstraint" in x:
                
                ctrl = cmds.orientConstraint(x, q = True, targetList = True)
                if "_IK_" in x:
                    for y in [".sx", ".sy", ".sz", ".visibility"]:
                        cmds.setAttr(ctrl[0] + y, lock = True, keyable = False, channelBox = False)
                else:
                    for y in [".tx", ".ty", ".tz", ".sx", ".sy", ".sz", ".visibility"]:
                        cmds.setAttr(ctrl[0] + y, lock = True, keyable = False, channelBox = False)
                
            elif "poleVectorConstraint" in x:
                
                ctrl = cmds.poleVectorConstraint(x, q = True, targetList = True)
                for y in [".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]:
                    cmds.setAttr(ctrl[0] + y, lock = True, keyable = False, channelBox = False)
            
                """
                underScore = "_"
                constraintSplit = x.split("_")
                constraintSplit.pop()
                constraintSplit.append("ctrl")
                ctrlName = underScore.join(constraintSplit)
                """
                #if "parent" in x:
                #    for y in [".sx", ".sy", ".sz"]:
                #        cmds.setAttr(ctrlName + y, lock = True, keyable = False, channelBox = False)
            


    def poleVectorCntrl(self, top, mid, end):
        #code provided by Marco Giordano
        #https://vimeo.com/66262994    

        topJntPos = cmds.xform(top ,q= 1 ,ws = 1,t =1 )
        midJntPos = cmds.xform(mid ,q= 1 ,ws = 1,t =1 )
        endJntPos = cmds.xform(end ,q= 1 ,ws = 1,t =1 )
        startV = om.MVector(topJntPos[0], topJntPos[1], topJntPos[2])
        midV = om.MVector(midJntPos[0], midJntPos[1], midJntPos[2])
        endV = om.MVector(endJntPos[0], endJntPos[1], endJntPos[2])
        startEnd = endV - startV
        startMid = midV - startV
        dotP = startMid * startEnd
        proj = float(dotP) / float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj
        arrowV = startMid - projV
        arrowV *= 0.5 
        finalV = arrowV + midV
        cross1 = startEnd ^ startMid
        cross1.normalize()
        cross2 = cross1 ^ arrowV
        cross2.normalize()
        arrowV.normalize()
        matrixV = [arrowV.x , arrowV.y , arrowV.z , 0 , 
                    cross1.x ,cross1.y , cross1.z , 0 ,
                    cross2.x , cross2.y , cross2.z , 0,
                    0,0,0,1]

        print matrixV
        matrixM = om.MMatrix()
        print matrixM
        om.MScriptUtil.createMatrixFromList(matrixV , matrixM)
        matrixFn = om.MTransformationMatrix(matrixM)
        rot = matrixFn.eulerRotation()
        loc = cmds.spaceLocator()[0]
        cmds.xform(loc , ws =1 , t= (finalV.x, finalV.y, finalV.z))
        cmds.xform ( loc , ws = 1 , rotation = ((rot.x/math.pi*180.0),
        (rot.y/math.pi*180.0),
        (rot.z/math.pi*180.0)))


        return loc

        
        
        
        cmds.move(0, 0, -25, elbowIkCtrlName, relative = True, worldSpaceDistance = True )
        
        self.colorOverride(elbowIkCtrlName)
        cmds.makeIdentity(apply=True, r=True, s=True, t=True, n=False, pn=True) 

     
  
    def makeIkPlaneSetup(self, top, mid, end, poleVectorDistance=25.0):

        #code provided by Carlos Anguiano
        #http://www.losart3d.com/?p=907

        topJntPos = cmds.xform(top ,q= 1 ,ws = 1,t =1 )
        midJntPos = cmds.xform(mid ,q= 1 ,ws = 1,t =1 )
        endJntPos = cmds.xform(end ,q= 1 ,ws = 1,t =1 )
        

        #if len(helpers) != 3:  
        #    raise Exception('makeIkPlaneSetup input error, you need objects to pull positions from there were %s inputs\n' % len(helpers))  
      
        shld = om.MVector(topJntPos[0], topJntPos[1], topJntPos[2])  
        elbow = om.MVector(midJntPos[0], midJntPos[1], midJntPos[2]) 
        wrist = om.MVector(endJntPos[0], endJntPos[1], endJntPos[2])
      
        #figure out the upNode (plane direction)  
        planeX = wrist - shld
        print planeX.normal()
        planeXL = planeX.length()
        print planeXL 
      
        armDis = (elbow - shld).length()  
        foreArmDis = (wrist-elbow).length()  
        fraction = armDis/(foreArmDis+armDis)  
        planeP = shld + (planeX.normal() * (planeXL*fraction))  
        upNode = (elbow-planeP).normal()  
      
        pvPos = shld + (upNode * poleVectorDistance)  
      
        #shoulder orintation matrix  
        shdXAxis = (elbow-shld).normal()  
        shdYAxis = (upNode ^ shdXAxis).normal() #cross product a noramalize....  
        shdZAxis = (shdXAxis ^ shdYAxis).normal() #cross product a noramalize....  
      
        matrixShoulder = [shdXAxis.x,shdXAxis.y,shdXAxis.z,0,  
                            shdYAxis.x,shdYAxis.y,shdYAxis.z,0,  
                            shdZAxis.x,shdZAxis.y,shdZAxis.z,0,  
                            shld.x,shld.y,shld.z,1] 
      
        

        matrixM = om.MMatrix()
        

        elbowXAxis = (wrist-elbow).normal()  
        elbowYAxis = shdYAxis  
        elbowZAxis = (elbowXAxis ^ elbowYAxis).normal()  
      
        matrixElbow = [elbowXAxis.x,elbowXAxis.y,elbowXAxis.z,0,  
                             elbowYAxis.x,elbowYAxis.y,elbowYAxis.z,0,  
                             elbowZAxis.x,elbowZAxis.y,elbowZAxis.z,0,  
                             elbow.x,elbow.y,elbow.z,1]
      
        matrixWrist = [elbowXAxis.x,elbowXAxis.y,elbowXAxis.z,0,  
                             elbowYAxis.x,elbowYAxis.y,elbowYAxis.z,0,  
                             elbowZAxis.x,elbowZAxis.y,elbowZAxis.z,0,  
                             wrist.x,wrist.y,wrist.z,1]               
      
        matrixPoleVector = [shdXAxis.x,shdXAxis.y,shdXAxis.z,0,  
                          shdYAxis.x,shdYAxis.y,shdYAxis.z,0,  
                          shdZAxis.x,shdZAxis.y,shdZAxis.z,0,  
                          pvPos.x,pvPos.y,pvPos.z,1]

        om.MScriptUtil.createMatrixFromList(matrixShoulder , matrixM)
        shldM = om.MTransformationMatrix(matrixM)
        om.MScriptUtil.createMatrixFromList(matrixElbow , matrixM)
        elbowM = om.MTransformationMatrix(matrixM)
        om.MScriptUtil.createMatrixFromList(matrixWrist , matrixM)
        wristM = om.MTransformationMatrix(matrixM)
        om.MScriptUtil.createMatrixFromList(matrixPoleVector , matrixM)
        pvM = om.MTransformationMatrix(matrixM)
      
        #convert matrix values to list for xform input  
        shldML = [[0 for y in range(shldM)] for x in range(shldM)]  
        elbowML = [v for v in elbowM]  
        wristML = [v for v in wristM]  
        pvML = [v for v in pvM]  
      
        #make pole vector point  
        pv = cmds.spaceLocator()  
        cmds.select(clear=True) #we'll keep joints parented to avoid rotation offset which maya creates when parenting joints post creation  
      
        shldJ = cmds.joint()  
        elbowJ = cmds.joint()  
        wristJ = cmds.joint()  
      
        cmds.xform(shldJ,ws=True,m=shldML)  
        cmds.xform(elbowJ,ws=True,m=elbowML)  
        cmds.xform(wristJ,ws=True,m=wristML)  
        cmds.xform(pv,ws=True,m=pvML)  

ui = Auto_Rig()
ui.show()
