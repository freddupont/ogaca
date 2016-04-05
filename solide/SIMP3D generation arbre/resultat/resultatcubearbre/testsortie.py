# -*- coding: iso-8859-1 -*-

###
### This file is generated automatically by SALOME v6.3.1 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.notebook
sys.path.insert( 0, r'/home/fred/asteretude/kenyatta/resultat/resultatcubearbre')

import iparameters
ipar = iparameters.IParameters(salome.myStudy.GetCommonParameters("Interface Applicative", 1))

#Set up visual properties:
ipar.setProperty("AP_ACTIVE_VIEW", "ParaView_0_0")
ipar.setProperty("AP_WORKSTACK_INFO", "00000001000000000000000201000000010000033f000000040000000100000001000000080000001800500061007200610056006900650077005f0030005f00300000000102")
ipar.setProperty("AP_ACTIVE_MODULE", "ParaViS")
ipar.setProperty("AP_SAVEPOINT_NAME", "GUI state: 1")
#Set up lists:
# fill list AP_VIEWERS_LIST
ipar.append("AP_VIEWERS_LIST", "ParaView_1")
# fill list ParaView_1
ipar.append("ParaView_1", "ParaView scene:1 - viewer:1")
ipar.append("ParaView_1", "empty")
# fill list AP_MODULES_LIST
ipar.append("AP_MODULES_LIST", "ParaViS")


###
### PARAVIS component
###


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
  iparameters.getSession().restoreVisualState(1)
