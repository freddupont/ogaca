#IOBeam.py
#fichier destiner a ecrire des fichier de poutre dans differents style de fichier texte
#et pour differents logiciel.
# ======================================================================
# COPYRIGHT (C) 2011  FREDERIC RENOU frederic.renou.pb@gmail.com
# THIS PROGRAM IS FREE SOFTWARE; YOU CAN REDISTRIBUTE IT AND/OR MODIFY
# IT UNDER THE TERMS OF THE GNU GENERAL PUBLIC LICENSE AS PUBLISHED BY
# THE FREE SOFTWARE FOUNDATION; EITHER VERSION 2 OF THE LICENSE, OR
# (AT YOUR OPTION) ANY LATER VERSION.
#
# THIS PROGRAM IS DISTRIBUTED IN THE HOPE THAT IT WILL BE USEFUL, BUT
# WITHOUT ANY WARRANTY; WITHOUT EVEN THE IMPLIED WARRANTY OF
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. SEE THE GNU
# GENERAL PUBLIC LICENSE FOR MORE DETAILS.
#
# YOU SHOULD HAVE RECEIVED A COPY OF THE GNU GENERAL PUBLIC LICENSE
# ALONG WITH THIS PROGRAM;
# ======================================================================


#les donnes d entre doive etre au format suivant
#file string qui contien la chaine de caractere du fichier de sauvegarde
#newnode tableau des noeuds de dime N ligne et 3 colone x,y,z
#newline tableau de lien entre les noeuds la numerotation des noeud commencant a zero
#groupline table des groupe de la forme [["gr1",(1,4,...)],["gr2",(20,2,...)],...]

try :
    import aster
    from Cata.cata import *
    from Accas import _F
    #aster_dir=aster.repout()
    #print "aster_dir",aster_dir
    #print aster.__dict__()
    #sys.path.append(aster_dir+'bibpyt/Utilitai')
    #from Utilitai.sup_gmsh import *
    #from Utilitai.partition import *
    #print "print repout",aster.repout()
except :
    print "i"*40
    print 'Fonctionnalites Aster indisponibles'
    print 'certaine fonction ne sont pas disponnible'
    print "i"*40

try :
    import geompy
    import salome, SMESH
    import smesh
except :
    print "i"*40
    print 'Fonctionnalites Salome indisponibles'
    print 'certaine fonction ne sont pas disponnible'
    print "i"*40
    
import numpy

def help():
    print """les donnes d entre doive etre au format suivant
file string qui contien la chaine de caractere du fichier de sauvegarde
newnode tableau des noeuds de dime N ligne et 3 colone x,y,z de type numpy
newline tableau de lien entre les noeuds la numerotation des noeud commencant a zero
groupline table des groupe de la forme [["gr1",(1,4,...)],["gr2",(20,2,...)],...]"""

def WriteGEO(geofile,newnode,newline,groupline=[],groupnode=[]):
    """impression du fichier format .geo de gmsh
    voir print .writeentre pour plus d'aide"""
    
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

def ReadSTR(strfile):
    """lecture du fichier format .str de robot
    voir print .writeentre pour plus d'aide"""
    
    fstr=file(strfile,"r");
    
    print "lecture du fichier au format str de robot:",strfile
    


    
    
    line=fstr.readline();
    while (line!="" and line[:7]!="ROBOT97"):
        line=fstr.readline();
    if (line[:7]!="ROBOT97"):
        print "format de fichier incorrecte"
        return -1
    
    print "format de fichier correcte"
    line=fstr.readline();
    line=fstr.readline();
    line=fstr.readline();
    line=fstr.readline();
    line=fstr.readline();
    line=fstr.readline();
    
    #lecture de la ligne
    #NODes 1207  ELEments 4651
    assert line[:3]=="NOD"
    a=line.split()
    nbnode=int(a[1])
    nbele=int(a[3])
    print "nombre de noeuds a lire",nbnode," nombre de barres:",nbele
    
    line=fstr.readline();
    while (line!="" and line[:3] !='NOD'):
        line=fstr.readline();
    if (line[:3] !='NOD'):
        print "format de fichier incorrecte"
        return -1
    
    dictnode={}
    listnode=numpy.empty((0,3),dtype='float64');
    line=fstr.readline();
    while (line[0]==";"):
        line=fstr.readline();
    curnnode=0
    for a in range(0,nbnode):
        ls=line.split()
        #print ls
        listnode=numpy.vstack((listnode,numpy.array( (float(ls[1]),float(ls[2]),float(ls[3])) ) ))
        curnnode+=1
        dictnode[int(ls[0])]=curnnode-1
        line=fstr.readline();
        
    
    line=fstr.readline();
    while (line!="" and line[:3] !='ELE'):
        line=fstr.readline();
    if (line[:3] !='ELE'):
        print "format de fichier incorrecte"
        return -1
    
    listline=[]
    dictline={}
    line=fstr.readline();
    while (line[0]==";"):
        line=fstr.readline();
    for a in range(0,nbele):
        ls=line.split()
        #print ls
        listline.append((dictnode[int(ls[1])],dictnode[int(ls[2])]))
        dictline[int(ls[0])]=len(listline)-1
        line=fstr.readline();
    #print dictline[10]

    #definition des boucles de lecture
    def decripte(text,dico):
        #print "decripte" ,text
        li=[]
        texts=text.rsplit('to')
        if len (texts)==1:
            return [dico[int(text)]]
        pas=1
        textss=texts[1].rsplit('By')
        beg=int(texts[0])
        end=int(textss[0])
        if len (textss)==2:
            pas=int(textss[1])
        for a in range(beg,end+pas,pas):
            li.append(dico[a])
        return li
    
    #pour tester
    #print decripte("4to8By2")
    
    
    def section(fstr,dico,group,groupname=None,prefixe=''):
        #on avance jusqua la premiere ligne avec des chiffres
        line=fstr.readline();
        while (line!=""):
            ls=line.split()
            if len(ls)>0:
                if ls[0][0].isdigit():
                    break
            line=fstr.readline();
        while (line!="" and len(line)!=2):
            ls=line.split()
            if len(ls)>1:
                li=[]
                for a in range(0,len(ls)):
                    if not(ls[a][0].isdigit()):
                        break
                    li.extend(decripte(ls[a],dico))
                #print a
                
                gname=''.join(ls[a:])
                if groupname!=None:
                    gname=groupname
                gname=prefixe+gname
                
                num=0
                for num in range (0,len(group)):
                    if group[num][0]==gname:
                        break
                if num>=len(group):
                    #print "append"
                    #print group
                    group.append((gname,[]))
                    num=len(group)-1
                #print "num",num," group[num][0]",group[num][0]
                if group[num][0]!=gname:
                    group.append((gname,[]))
                    num=len(group)-1
                #print num,group
                group[num][1].extend(li)
                #print group[-1]
            line=fstr.readline();
        return line
        
    def LOADCASEsection(fstr,curline,diconode,groupnode,dicoline,groupline):
        ls=curline.split()
        gn=None
        prefixe=ls[3]
        #print prefixe
        line=fstr.readline();
        while (line!="" and len(line)!=2 and line[:3]!='CAS'):
            if (line[:3]=='NOD'):
                print "prefixe node",prefixe
                line=section(fstr,diconode,groupnode,groupname=gn,prefixe=prefixe)
            elif (line[:3]=='ELE'):
                print "prefixe line",prefixe
                line=section(fstr,dicoline,groupline,groupname=gn,prefixe=prefixe)
            else:
                line=fstr.readline();
        return line
            


    ##definition des groupes
    groupline=[]
    groupnode=[]
    #
    line=fstr.readline();
    while (line!="" ):
        #print "main",groupnode
        if line[:3]=='PRO':#profile
            line=section(fstr,dictline,groupline)
        elif line[:3]=='SUP':#suport
            line=section(fstr,dictnode,groupnode,prefixe='F')
        elif line[:3]=='CAS':#case from loadcase
            line=LOADCASEsection(fstr,line,dictnode,groupnode,dictline,groupline)
        else:
            line=fstr.readline();

    fstr.close()
    return listnode,listline,groupline,groupnode
    


def WriteSTR(strfile,newnode,newline,groupline=[],groupnode=[]):
    """impression du fichier format .str de robot
    voir print .writeentre pour plus d'aide"""
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
def CreateSalomeMesh(newnode,newline,groupline=[],groupnode=[]):
    """creation a la volle d un mesh dans salome
    n'est disponible que depuis salome"""
    
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
#ce script est tres long surtout pour la creation des groupes
def CreateSalomeGeom(newnode,newline,groupline=[],groupnode=[]):
    """creation a la volle d une geometrie dans salome
    n'est disponible que depuis salome"""
    
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

