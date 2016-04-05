#generation d'une geometrie
#cube avec un quadriallage de face sur la partie superieur
#et une face sur la partie inferieur

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.notebook
sys.path.insert( 0, r'/home/fred/asteretude/kenyatta/salome')

import iparameters
ipar = iparameters.IParameters(salome.myStudy.GetCommonParameters("Interface Applicative", 1))


###
### GEOM component
###

import GEOM
import geompy
import math
import SALOMEDS

#definition des variables
lx=24.
ly=24.
h=10.
nsub=1
phibase=2.4
phitop=0.8

geompy.init_geom(theStudy)

#generation du quadriage de noeud
node=[]
deltax=lx/nsub
deltay=ly/nsub
for a in range(0,nsub+1):
  liste=[]
  node.append(liste)
  for b in range(0,nsub+1):
    newvertex=geompy.MakeVertex(a*deltax,b*deltay,h)
    #geompy.addToStudy( newvertex, 'PX%dY%d'%(a,b) )
    liste.append(newvertex)

##generation du quadriage de line
#line=[]
#linex=[]
#liney=[]
#for a in range(0,nsub):
#  listex=[]
#  linex.append(listex)
#  listey=[]
#  linex.append(listey)
#  for b in range(0,nsub+1):
#    newlinex=geompy.MakeLineTwoPnt(node[a][b], node[a+1][b])
#    geompy.addToStudy( newlinex, 'lxX%dY%d'%(a,b) )
#    listex.append(newlinex)
#    newliney=geompy.MakeLineTwoPnt(node[b][a], node[b][a+1])
#    geompy.addToStudy( newliney, 'lyX%dY%d'%(a,b) )
#    listey.append(newliney)


#generation des faces de contact
facenodeup=[]
for a in range(0,nsub+1):
  liste=[]
  facenodeup.append(liste)
  for b in range(0,nsub+1):
    newvertex=geompy.MakeTranslation(node[a][b], 0, 0, 1)
    newline=geompy.MakeLineTwoPnt(node[a][b], newvertex)
    newface=geompy.MakeFaceObjHW(newline, phitop, phitop)
    #geompy.addToStudy( newface, 'faceX%dY%d'%(a,b) )
    liste.append(newface)


#generation du grand rectange
V0 = geompy.MakeVertex(0-phitop/2., 0-phitop/2., 0)
V1 = geompy.MakeVertex(lx+phitop/2., ly+phitop/2., h)
Box_1 = geompy.MakeBoxTwoPnt(V0, V1)
#geompy.addToStudy( Box_1, 'Box_1' )

#generation de la face inferieur grand rectange
V0 = geompy.MakeVertex(lx/2., ly/2., 0)
V1 = geompy.MakeVertex(lx/2., ly/2., h)
newline=geompy.MakeLineTwoPnt(V0, V1)
infbase=geompy.MakeFaceObjHW(newline, phibase, phibase)
infface=geompy.MakeFaceObjHW(newline, lx+phitop, ly+phitop)
inf = geompy.MakePartition([infface], [infbase], [], [], geompy.ShapeType["FACE"], 0, [], 0)
#geompy.addToStudy( infbase, 'infbase' )
#geompy.addToStudy( infface, 'infface' )
#geompy.addToStudy( inf, 'inf' )


#groupe des faces qui ont un interet
grface=[]
grface.append(infbase)
for a in facenodeup:
  for b in a:
    grface.append(b)

grfaceCompound = geompy.MakeCompound(grface)
#geompy.addToStudy( grfaceCompound, 'grfaceCompound' )

#solide final
globalsolid=geompy.MakePartition([Box_1], [grfaceCompound], [], [], geompy.ShapeType["SOLID"], 0, [], 1)
geompy.addToStudy( globalsolid, 'globalsolid' )


#generation des groupes
groupe=[]
#EDGE
#Rien

#FACE
#infbase groupe de face qui represente le pied de la structure
grinfbase=geompy.CreateGroup(globalsolid,geompy.ShapeType["FACE"])
[geomObj_248] = geompy.SubShapeAll(infbase, geompy.ShapeType["FACE"])
geomObj_temp = geompy.GetSame(globalsolid, geomObj_248)
tempid=geompy.GetSubShapeID(globalsolid,geomObj_temp)
geompy.AddObject(grinfbase,tempid)
geompy.addToStudyInFather( globalsolid, grinfbase, "infbase" )
groupe.append(grinfbase)

#faces de contacte hautes
touttop = geompy.CreateGroup(globalsolid, geompy.ShapeType["FACE"])
for a in range(0,nsub+1):
  for b in range(0,nsub+1):
    grtop=geompy.CreateGroup(globalsolid,geompy.ShapeType["FACE"])
    [tempgeomObj] = geompy.SubShapeAll(facenodeup[a][b], geompy.ShapeType["FACE"])
    geomObj_temp = geompy.GetSame(globalsolid, tempgeomObj)
    geompy.UnionList(touttop,[geomObj_temp])
    
    geompy.UnionList(grtop,[geomObj_temp])
    #legerement plus long que la ligne au dessus
    #tempid=geompy.GetSubShapeID(globalsolid,geomObj_temp)
    #geompy.AddObject(grtop,tempid)
    
    geompy.addToStudyInFather( globalsolid, grtop, "tX%dY%d"%(a,b) )
    groupe.append(grtop)
#toutes les faces du haut
geompy.addToStudyInFather( globalsolid, touttop, "touttop" )

#toutes les faces
toutface = geompy.CreateGroup(globalsolid, geompy.ShapeType["FACE"])
tempgeomObj = geompy.SubShapeAll(globalsolid, geompy.ShapeType["FACE"])
geompy.UnionList(toutface,tempgeomObj)
geompy.addToStudyInFather( globalsolid, toutface, "toutface" )
#geompy.UnionIDs(toutface,
    #newvertex=geompy.MakeTranslation(node[a][b], 0, 0, 1)
    #newline=geompy.MakeLineTwoPnt(node[a][b], newvertex)
    #newface=geompy.MakeFaceObjHW(newline, phitop, phitop)
    #geompy.addToStudy( newface, 'faceX%dY%d'%(a,b) )

#SOLID
#tout le volume
grtout=geompy.CreateGroup(globalsolid,geompy.ShapeType["SOLID"])
tempid=geompy.GetSubShapeID(globalsolid,globalsolid)
geompy.AddObject(grtout,tempid)
geompy.addToStudyInFather( globalsolid, grtout, "tout" )

salome.sg.updateObjBrowser(1)

