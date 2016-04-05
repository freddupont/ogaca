#SalomeIOBeam.py
#fichier destiner a ecrire des fichier de poutre dans differents style de fichier texte
#et pour differents logiciel.

#les donnes d entre doive etre au format suivant
#___file string qui contien la chaine de caractere du fichier de sauvegarde
#newnode tableau des noeuds de dime N ligne et 3 colone x,y,z
#newline tableau de lien entre les noeuds la numerotation des noeud commencant a zero
#groupline table des groupe de la forme [["gr1",(1,4,...)],["gr2",(20,2,...)],...]


#########################################################
#impression du fichier format .geo de gmsh
def GeoWrite(geofile,newnode,newline,groupline=[],groupnode=[]):
    fo=file(geofile,"w");
    print "sauvegarde du fichier au format geo de gmsh"
    
    #format du point
    #Point(1) = {0, 0., 0};
    for i in range(0,newnode.shape[0]):
            fo.write("Point(%d) = {%f, %f, %f};\n"%(i+1,newnode[i,0],newnode[i,1],newnode[i,2]));
            
    #format de la ligne
    #Line(1) = {2, 3};
    for i in range(0,len(newline)):
            fo.write("Line(%d) = {%d, %d};\n"%(i+1,newline[i][0]+1,newline[i][1]+1));
            
    
    #format du groupe
    
    
    #creation des groupes line
    #Physical Line("linet") = {1, 2};
    for groupe in groupline:
        if (len(groupe[1])>0):
            fo.write("Physical Line(\"%s\") = {%d"%(groupe[0],groupe[1][0]+1));
            compteur=0;
            for i in groupe[1][1:]:
                fo.write(", %d"%(i+1));
                if compteur==20:
                    fo.write("\n");
                    compteur=0;
                compteur+=1
            fo.write("};\n");

    #creation des groupes point
    #Physical Point(1) = {1, 3, 5};
    for groupe in groupnode:
        if (len(groupe[1])>0):
            fo.write("Physical Point(\"%s\") = {%d"%(groupe[0],groupe[1][0]+1));
            compteur=0;
            for i in groupe[1][1:]:
                fo.write(", %d"%(i+1));
                if compteur==20:
                    fo.write("\n");
                    compteur=0;
                compteur+=1
            fo.write("};\n");
    
    fo.close();
    print "geo done"
    return

#########################################################
#impression du fichier format .geo de gmsh
def STRWrite(strfile,newnode,newline,groupline=[],groupnode=[]):
    fstr=file(strfile,"w");
    print "sauvegarde du fichier au format str de robot"
    
    fstr.write(";+---------------------------+-------------------------+---------------------+\n");
    fstr.write(";! done by pythonscript       !\n");
    fstr.write(";+---------------------------+-------------------------+---------------------+\n");
    
    fstr.write("ROBOT97\n");
    fstr.write("FRAme SPAce\n");
    fstr.write("NUMbering DIScontinuous\n");
    
    fstr.write("NODes " + str(len(newnode)) + "  ELEments " + str(len(newline))+"\n");
    
    fstr.write("UNIts\n");
    fstr.write("LENgth=m	Force=kN\n");
    
    fstr.write(";+------+-------------------+--------------------+--------------------+\n");
    fstr.write(";! No.  !        X          !         Y          !         Z          !\n");
    fstr.write(";+------+-------------------+--------------------+--------------------+\n");
    fstr.write("NODes\n");
    for i in range(0,len(newnode)):
        fstr.write("%d %f %f %f\n"%((i + 1),newnode[i][0],newnode[i][1],newnode[i][2]));
    fstr.write("\n");
    
    fstr.write("ELEments\n");
    fstr.write(";+------+-------+-------+\n");
    fstr.write(";! No.  ! STRT  ! END   !\n");
    fstr.write(";+------+-------+-------+\n");
    for i in range(0,len(newline)):
        fstr.write("%d %d %d\n"%((i + 1),newline[i][0]+1,newline[i][1]+1));
    fstr.write("\n");    
    
    
    
    
    #creation des groupes comme de faux cas de charge
    fstr.write("LOAds\n");

    nbgroupe=0;
    ini=100;
    for groupe in groupnode:
        if (len(groupe[1])>0):
            fstr.write("CASe # %d %s\nNODes\n"%(nbgroupe+ini,groupe[0]));
            nbgroupe+=1;
            compteur=0;
            for i in groupe[1]:
                fstr.write(" %d"%(i+1));
                if (compteur==20):
                    fstr.write(" FZ=1.0 \n");
                    compteur=0;
                compteur+=1
            fstr.write(" FZ=1.0 \n");
            fstr.write("\n");
            
    for groupe in groupline:
        if (len(groupe[1])>0):
            fstr.write("CASe # %d %s\nELEments\n"%(nbgroupe+ini,groupe[0]));
            nbgroupe+=1;
            compteur=0;
            for i in groupe[1]:
                fstr.write(" %d"%(i+1));
                if (compteur==20):
                    fstr.write(" PZ=1.0 \n");
                    compteur=0;
                compteur+=1
            fstr.write(" PZ=1.0 \n");
            fstr.write("\n");

    
    #fin du fichier
    fstr.write("\n");
    fstr.write("END\n");
    fstr.write("\n");
    fstr.close();
    print "done str"
    return

#########################################################
#creation a la volle d un mesh salome
import smesh
import salome

def SalomeMesh(newnode,newline,groupline=[],groupnode=[]):
    print "creation a la volle d un mesh dans salome"
    
    mesh = smesh.Mesh()
    liennoeudsalome={}
    for i in range(0,newnode.shape[0]):
        liennoeudsalome[i]=mesh.AddNode(newnode[i,0],newnode[i,1],newnode[i,2])
    
    lienlinesalome={}
    for i in range(0,len(newline)):
        lienlinesalome[i] = mesh.AddEdge([liennoeudsalome[newline[i][0]],liennoeudsalome[newline[i][1]]])
        
    #creation des groupes
    for groupe in groupline:
        if (len(groupe[1])>0):
            grtemp=[]
            for a in groupe[1]:
                grtemp.append(lienlinesalome[a])
            a=mesh.MakeGroupByIds(groupe[0],smesh.EDGE,grtemp)
    for groupe in groupnode:
        if (len(groupe[1])>0):
            grtemp=[]
            for a in groupe[1]:
                grtemp.append(liennoeudsalome[a])
            a=mesh.MakeGroupByIds(groupe[0],smesh.NODE,grtemp)

    salome.sg.updateObjBrowser(1)
    print "salome mesh done"

#########################################################
#creation a la volle d une geometrie salome

import geompy

#ce script est tres long surtout pour la creation des groupes
def SalomeGeom(newnode,newline,groupline=[],groupnode=[]):
    print "creation a la volle d une geometrie dans salome"
    
    liennoeudsalome=[]
    for i in range(0,newnode.shape[0]):
        liennoeudsalome.append(geompy.MakeVertex(newnode[i,0],newnode[i,1],newnode[i,2]))
    
    lienlinesalome=[]
    for i in range(0,len(newline)):
        lienlinesalome.append(geompy.MakeLineTwoPnt(liennoeudsalome[newline[i][0]],liennoeudsalome[newline[i][1]]))
    
    complist=[];
    complist.extend(liennoeudsalome)
    complist.extend(lienlinesalome)
    outshape=geompy.MakeCompound(complist)
    sortie= geompy.addToStudy(outshape,"treilli")
    sortiegr=[]
    #creation des groupes
    for groupe in groupline:
        if (len(groupe[1])>0):
            newgr=geompy.CreateGroup(outshape,geompy.ShapeType["EDGE"])
            for a in groupe[1]:
                lineid=geompy.GetSubShapeID(outshape,lienlinesalome[a])
                geompy.AddObject(newgr,lineid)
            sortiegr.append(geompy.addToStudyInFather( outshape, newgr, groupe[0] ))

    #creation des groupes
    for groupe in groupnode:
        if (len(groupe[1])>0):
            newgr=geompy.CreateGroup(outshape,geompy.ShapeType["VERTEX"])
            for a in groupe[1]:
                noeudid=geompy.GetSubShapeID(outshape,liennoeudsalome[a])
                geompy.AddObject(newgr,noeudid)
            sortiegr.append(geompy.addToStudyInFather( outshape, newgr, groupe[0] ))
            
    #gg = salome.ImportComponentGUI("GEOM")
    #
    #gg.createAndDisplayGO(sortie)
    #for a in sortiegr:
    #    gg.createAndDisplayGO(a)
    salome.sg.updateObjBrowser(1)
    print "salome geom done"

