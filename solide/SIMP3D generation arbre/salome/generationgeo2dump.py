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
sys.path.insert( 0, r'/home/fred/asteretude/kenyatta/salome')

import iparameters
ipar = iparameters.IParameters(salome.myStudy.GetCommonParameters("Interface Applicative", 1))

#Set up visual properties:
ipar.setProperty("AP_ACTIVE_VIEW", "OCCViewer_0_0")
ipar.setProperty("AP_WORKSTACK_INFO", "0000000100000000000000020100000001000003f8000000040000000200000001000000080000001a004f00430043005600690065007700650072005f0030005f00300000000102000000080000001a00560054004b005600690065007700650072005f0030005f00300000000202")
ipar.setProperty("AP_ACTIVE_MODULE", "Geometry")
ipar.setProperty("AP_SAVEPOINT_NAME", "GUI state: 1")
#Set up lists:
# fill list AP_VIEWERS_LIST
ipar.append("AP_VIEWERS_LIST", "OCCViewer_1")
ipar.append("AP_VIEWERS_LIST", "VTKViewer_2")
# fill list OCCViewer_1
ipar.append("OCCViewer_1", "OCC scene:1 - viewer:1")
ipar.append("OCCViewer_1", "scale=3.566525200501e+01*centerX=1.697056023410e+01*centerY=4.082483521536e+00*projX=5.773502588272e-01*projY=-5.773502588272e-01*projZ=5.773502588272e-01*twist=0.000000000000e+00*atX=0.000000000000e+00*atY=0.000000000000e+00*atZ=0.000000000000e+00*eyeX=2.886751294136e+02*eyeY=-2.886751294136e+02*eyeZ=2.886751294136e+02*scaleX=1.000000000000e+00*scaleY=1.000000000000e+00*scaleZ=1.000000000000e+00*isVisible=1*size=100.00*gtIsVisible=0*gtDrawNameX=1*gtDrawNameY=1*gtDrawNameZ=1*gtNameX=X*gtNameY=Y*gtNameZ=Z*gtNameColorRX=255*gtNameColorGX=0*gtNameColorBX=0*gtNameColorRY=0*gtNameColorGY=255*gtNameColorBY=0*gtNameColorRZ=0*gtNameColorGZ=0*gtNameColorBZ=255*gtDrawValuesX=1*gtDrawValuesY=1*gtDrawValuesZ=1*gtNbValuesX=3*gtNbValuesY=3*gtNbValuesZ=3*gtOffsetX=2*gtOffsetY=2*gtOffsetZ=2*gtColorRX=255*gtColorGX=0*gtColorBX=0*gtColorRY=0*gtColorGY=255*gtColorBY=0*gtColorRZ=0*gtColorGZ=0*gtColorBZ=255*gtDrawTickmarksX=1*gtDrawTickmarksY=1*gtDrawTickmarksZ=1*gtTickmarkLengthX=5*gtTickmarkLengthY=5*gtTickmarkLengthZ=5")
# fill list VTKViewer_2
ipar.append("VTKViewer_2", "VTK scene:1 - viewer:1")
ipar.append("VTKViewer_2", """<?xml version="1.0"?>
<ViewState>
    <Position X="738.946" Y="-738.946" Z="738.946"/>
    <FocalPoint X="0" Y="0" Z="0"/>
    <ViewUp X="0" Y="0" Z="1"/>
    <ViewScale Parallel="363.749" X="1" Y="1" Z="1"/>
    <DisplayCubeAxis Show="0"/>
    <GraduatedAxis Axis="X">
        <Title isVisible="1" Text="X" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="1" G="0" B="0"/>
        </Title>
        <Labels isVisible="1" Number="3" Offset="2" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="1" G="0" B="0"/>
        </Labels>
        <TickMarks isVisible="1" Length="5"/>
    </GraduatedAxis>
    <GraduatedAxis Axis="Y">
        <Title isVisible="1" Text="Y" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="0" G="1" B="0"/>
        </Title>
        <Labels isVisible="1" Number="3" Offset="2" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="0" G="1" B="0"/>
        </Labels>
        <TickMarks isVisible="1" Length="5"/>
    </GraduatedAxis>
    <GraduatedAxis Axis="Z">
        <Title isVisible="1" Text="Z" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="0" G="0" B="1"/>
        </Title>
        <Labels isVisible="1" Number="3" Offset="2" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="0" G="0" B="1"/>
        </Labels>
        <TickMarks isVisible="1" Length="5"/>
    </GraduatedAxis>
    <Trihedron isShown="1" Size="3"/>
</ViewState>
""")
# fill list AP_MODULES_LIST
ipar.append("AP_MODULES_LIST", "Geometry")
ipar.append("AP_MODULES_LIST", "Mesh")


###
### GEOM component
###

import GEOM
import geompy
import math
import SALOMEDS


geompy.init_geom(theStudy)

Box_1 = geompy.MakeBoxDXDYDZ(18, 18, 6)
listSubShapeIDs = geompy.SubShapeAllIDs(Box_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Box_1, geompy.ShapeType["FACE"])
listSubShapeIDs = geompy.SubShapeAllIDs(Box_1, geompy.ShapeType["SOLID"])
forc = geompy.CreateGroup(Box_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(forc, [33])
toutface = geompy.CreateGroup(Box_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(toutface, [3, 13, 23, 27, 31, 33])
tout = geompy.CreateGroup(Box_1, geompy.ShapeType["SOLID"])
geompy.UnionIDs(tout, [1])
geomObj_1 = geompy.GetSubShape(Box_1, [3])
geompy.addToStudy( Box_1, 'Box_1' )
geompy.addToStudyInFather( Box_1, forc, 'forc' )
geompy.addToStudyInFather( Box_1, toutface, 'toutface' )
geompy.addToStudyInFather( Box_1, tout, 'tout' )

### Store presentation parameters of displayed objects
import iparameters
ipar = iparameters.IParameters(theStudy.GetModuleParameters("Interface Applicative", "GEOM", 1))

#Set up entries:
# set up entry GEOM_1 (Box_1) parameters
objId = geompy.getObjectID(Box_1)
ipar.setParameter(objId, "OCCViewer_0_Visibility", "On")
ipar.setParameter(objId, "OCCViewer_0_Color", "1:1:0")
# set up entry GEOM_1:1 (forc) parameters
objId = geompy.getObjectID(forc)
ipar.setParameter(objId, "OCCViewer_0_Visibility", "On")
ipar.setParameter(objId, "OCCViewer_0_Color", "1:1:0")
# set up entry GEOM_1:2 (toutface) parameters
objId = geompy.getObjectID(toutface)
ipar.setParameter(objId, "OCCViewer_0_Visibility", "On")
ipar.setParameter(objId, "OCCViewer_0_Color", "1:1:0")
# set up entry GEOM_1:3 (tout) parameters
objId = geompy.getObjectID(tout)
ipar.setParameter(objId, "OCCViewer_0_Visibility", "On")
ipar.setParameter(objId, "OCCViewer_0_Color", "1:1:0")

###
### SMESH component
###

import smesh, SMESH, SALOMEDS

aMeasurements = smesh.CreateMeasurements()
smesh.SetCurrentStudy(theStudy)
import StdMeshers
Mesh_1 = smesh.Mesh(Box_1)
CompositeSegment_1D = Mesh_1.Segment(algo=smesh.COMPOSITE)
Local_Length_1 = CompositeSegment_1D.LocalLength(0.2)
Local_Length_1.SetPrecision( 1e-07 )
Quadrangle_2D = Mesh_1.Quadrangle()
Hexa_3D = smesh.CreateHypothesis('Hexa_3D')
status = Mesh_1.AddHypothesis(Hexa_3D)
forc_1 = Mesh_1.GroupOnGeom(forc,'forc',SMESH.FACE)
toutface_1 = Mesh_1.GroupOnGeom(toutface,'toutface',SMESH.FACE)
tout_1 = Mesh_1.GroupOnGeom(tout,'tout',SMESH.VOLUME)
isDone = Mesh_1.Compute()
Local_Length_1.SetLength( 0.25 )
Local_Length_1.SetPrecision( 1e-07 )

## set object names
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(CompositeSegment_1D.GetAlgorithm(), 'CompositeSegment_1D')
smesh.SetName(Local_Length_1, 'Local Length_1')
smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')
smesh.SetName(Hexa_3D, 'Hexa_3D')
smesh.SetName(forc_1, 'forc')
smesh.SetName(toutface_1, 'toutface')
smesh.SetName(tout_1, 'tout')

### Store presentation parameters of displayed objects
import iparameters
ipar = iparameters.IParameters(theStudy.GetModuleParameters("Interface Applicative", "SMESH", 1))



if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
  iparameters.getSession().restoreVisualState(1)
