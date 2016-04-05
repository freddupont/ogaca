#genetridi
#genere un tridi ou une poutre treilli de manier semi automatique
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


#salome version 5.1.5

#Base sur un maillage pour la face superieur et eventuellement une forme pour la face inferieur
#note pour la generation du maillage face superieur
#1)predecouper la coque selon le cas souhaite il est possible d'utiliser dump study pour introduire des boucles
#2) utiliser quadrangle mapping
#3) si besoin utiliser submesh sur les edge pour indiquer le nombre de decoupe
#4) suprimer a la main les noeud surabondant

#import bibli classic
import salome, SMESH
import smesh
import geompy
import numpy
import math

def genetridi(groupedesmaillesdecales,groupedesmaillessuperposer,groupedesmaillespannes,hdefaut,groupedesmaillesintersecter,stepfile,medfile):
    """gener un tridi"""

    #chargement du maillage
    ([topmesh],statut)=smesh.CreateMeshesFromMED(medfile);
    
    print "number of node ", topmesh.GetMesh().NbNodes();
    print "number of element ", topmesh.GetMesh().NbElements();
    
    #########################################################
    #Fonction normale par calcul de vecteur
    
    #calcul de la normale a un plan passant par 3 noeud
    #print normal3p3v(numpy.array( [0,0,0]),numpy.array( [0,10,0]),numpy.array( [1,0,0]))
    def normal3p3v(vecta,vectb,vectc):
        v1=vectb-vecta
        v2=vectc-vecta
        prod=numpy.array( [v1[1]*v2[2]-v1[2]*v2[1],v1[2]*v2[0]-v1[0]*v2[2],v1[0]*v2[1]-v1[1]*v2[0]])
        #print "prod",prod
        prod2=prod**2
        norme=(prod2.sum())**0.5;
        #print "norme",norme
        if (prod[2]<0):
            #print "correction"
            return -1*prod/norme;
        #print prod/norme
        return prod/norme;
    
    def normal2p(vecta,vectb):
        #print vecta
        #print vectb
        v0=vecta[0]-vectb[0]
        v1=vecta[1]-vectb[1]
        v2=vecta[2]-vectb[2]
        #print v0,v1,v2
        if v2<0:
            v0=v0*-1;
            v1=v1*-1;
            v2=v2*-1;
        if (v0==0 and v1==0):
            #print "normal2p vertical ligne";
            return numpy.array( [1,0,0])
        prod=numpy.array( [-1*v0*v2/((v0**2+v1**2)**0.5),-1*v1*v2/((v0**2+v1**2)**0.5),(v0**2+v1**2)**0.5])
        prod2=prod**2
        norme=(prod2.sum())**0.5;
        #print prod/norme
        return prod/norme;
    
    #print normal2p([0,0,0],[2.6,0.4,0.6])
    #calcul de la normale a un plan d un element
    #calcule comme la moyenne des normales 3 points
    #print normalnp(numpy.array([[0,0,0],[0,10,0],[1,0,0],[-2,-2,0]]))
    def normalelem(mesh,elementid):
        lnode=mesh.GetElemNodes(elementid);
        n=len(lnode)-2;
        if n==0:
            #print "ligne",mesh.GetNodeXYZ(lnode[0]),mesh.GetNodeXYZ(lnode[1])
            return normal2p(mesh.GetNodeXYZ(lnode[0]),mesh.GetNodeXYZ(lnode[1]))
        retour=numpy.empty(3,dtype='float64');
        retour[0]=0.;
        retour[1]=0.;
        retour[2]=0.;
        for i in range(0,n):
            #print "elem",numpy.array(mesh.GetNodeXYZ(lnode[0+i])),numpy.array(mesh.GetNodeXYZ(lnode[1+i])),numpy.array(mesh.GetNodeXYZ(lnode[2+i]))
            #print "retour",retour
            retour +=normal3p3v(numpy.array(mesh.GetNodeXYZ(lnode[0+i])),numpy.array(mesh.GetNodeXYZ(lnode[1+i])),numpy.array(mesh.GetNodeXYZ(lnode[2+i])))
            #print "retour",retour;
        retour2=retour**2
        norme=(retour2.sum())**0.5;
        return retour/norme;
    
        return retour
    
    #test
    #print normalelem(topmesh,1)
    #print normalelem(topmesh,787)
    
    #########################################################
    #Fonction de recherche
    
    #petite fonction pour trouver les elements qui sont a cote de la ligne actuelle
    #y compris les lignes
    #print recherchecouple((2,17),lmail)
    print "a faire: cree un dico des couples ici pour retrouver plus rapidement les mails"
    def recherchecouple(ligne,mesh):
        #print ligne
        retour=[];
        listeelement=mesh.GetElementsId();
        for i1 in listeelement:
            listnode=mesh.GetElemNodes(i1)
            for i2 in range(0,len(listnode)-1):
                if ((listnode[i2]==ligne[0] and listnode[i2+1]==ligne[1]) or (listnode[i2]==ligne[1] and listnode[i2+1]==ligne[0])):
                    retour.append(i1);
            if ((listnode[0]==ligne[1] and listnode[len(listnode)-1]==ligne[0]) or (listnode[0]==ligne[0] and listnode[len(listnode)-1]==ligne[1])):
                retour.append(i1);
            #if len(retour)==2:
            #    return retour;
        return retour;
    
    #petite fonction pour trouver les lignes qui sont a cote du noeud actuel
    def recherchesingle(noeud,mesh):
        retour=[];
        filteredge=smesh.GetFilter(smesh.EDGE,smesh.FT_Length,smesh.FT_MoreThan,Treshold=0);
        listeelement=mesh.GetIdsFromFilter(filteredge);
        for i1 in listeelement:
            listnode=mesh.GetElemNodes(i1)
            for i2 in range(0,len(listnode)):
                if ((listnode[i2]==noeud)):
                    retour.append(i1);
            #if len(retour)==2:
            #    return retour;
        return retour;
    
    #########################################################
    
    #petite fonction qui ajoute une diagonale en verifiant quel nexiste pas deja
    def addline(newline,listline,groupe):
        rline=(newline[1],newline[0]);
        if (not((newline in listline) or (rline in listline))):
            #print "on ajoute"
            listline.append(newline);
            groupe.append(len(listline)-1);
        #else:
        #    print "existe deja"
    
    #########################################################
    #fonction intersection
    Shape = geompy.ImportSTEP(stepfile)
    
    
    
    def getnodebyintersection(shape,porigine,vect,default=(0,0,0),extend=10,tolerance=0.1):
        p0   = geompy.MakeVertex(  porigine[0]+extend*vect[0],   porigine[1]+extend*vect[1],   porigine[2]+extend*vect[2])
        p1   = geompy.MakeVertex(  porigine[0]-extend*vect[0],   porigine[1]-extend*vect[1],   porigine[2]-extend*vect[2])
        line = geompy.MakeLineTwoPnt(p0, p1)
        partition = geompy.MakeHalfPartition(line, shape)
        
        
        # recherche du point de la partition par difference avec les premiers points
        #remplir les localisation des points
        subnew=geompy.SubShapeAllSorted(partition, geompy.ShapeType["VERTEX"])
        subnewp=[]
        for a in subnew:
            subnewp.append(geompy.PointCoordinates(a))
        subold=geompy.SubShapeAllSorted(line, geompy.ShapeType["VERTEX"])
        #recuperarion des deux extremite existante de la ligne
        suboldp=[]
        for a in subold:
            suboldp.append(geompy.PointCoordinates(a))
            
        #    #affichage pour debug
        #gg = salome.ImportComponentGUI("GEOM")
        #id_partition= geompy.addToStudy(partition,"Partitionfun")
        #gg.createAndDisplayGO(id_partition)
        #id_line= geompy.addToStudy(line,"linefun")
        #gg.createAndDisplayGO(id_line)
        #gg.setDisplayMode(id_partition,1)
        #
        #print subnewp
        #print suboldp
    
        if (len(subnew)==len(subold)):
            print "default",default
            return default
        else:
            couple=[]
            for i in range(0,len(subold)):
                oldpts=suboldp[i]
                ii=0;
                poursuite=True
                while(ii<len(subnew) and poursuite):
                    newpts=subnewp[ii]
                    if not(ii in couple):
                        #print "i",i,"ii",ii
                        #print "match",newpts,oldpts
                        #print "test",abs(oldpts[0]-newpts[0])+abs(oldpts[1]-newpts[1])+abs(oldpts[2]-newpts[2])
                        if (abs(oldpts[0]-newpts[0])+abs(oldpts[1]-newpts[1])+abs(oldpts[2]-newpts[2])<tolerance):
                            #print "match",newpts,oldpts
                            poursuite=False
                            couple.append(ii)
                    ii+=1
            for i in range(0,len(subnew)):
                if (not(i in couple)):
                    #print "subnewp[i]",subnewp[i]
                    return subnewp[i]
        print "default",default
        return default
    
    #lecture de la forme
    Shape = geompy.ImportSTEP(stepfile)
    
    #test
    #print getnodebyintersection(Shape,(  7493.00853583751,   6944.40714244478,   10.772063864125),(0.,0.,1.))
    #print getnodebyintersection(Shape,(7.46921151e+03,6.93144636e+03,6.87771298e+00),(0.,0.,1.))
    
    #########################################################
    #creation de la nouvelle structure
    newline=[];#liste des lignes
    #groupe a sauvegarder
    glini=[];#groupe des lignes initiales
    gldiag=[];#groupe des diagonales
    glnew=[];#groupe des lignes du nouveau layer.
    glpanne=[];
    gnini=[]; #groupe des neoud initiaux
    gndec=[];#groupe des noeud decaler
    gnsup=[];#groupe des noeuds superposer
    
    lienmailnewnode={};
    liennodenewdecanode={};
    newnode=numpy.empty((0,3),dtype='float64');
    normalmail=numpy.empty((0,3),dtype='float64');
    #lienmailnormalmail={};
    #########################################################
    #on parcour la liste des mail pour cree les noeuds 
    
    #recuperation des noeuds existants
    liennodenewnode={};
    listenode=topmesh.GetNodesId();
    nnewnode=0;
    for a in listenode:
        liennodenewnode[a]=nnewnode
        gnini.append(nnewnode);
        newnode=numpy.vstack((newnode,topmesh.GetNodeXYZ(a)))
        nnewnode+=1;
    print "recuperation des noeuds existants... ",nnewnode
    
    ###recherche des groupes pour appliquer le bon traitement
    groupes=topmesh.GetGroups();
    groupdec=[]
    groupsup=[]
    grouppan=[]
    groupint=[]
    for a in groupes:
        if a.GetName() in groupedesmaillesdecales:
            groupdec.extend(a.GetListOfID())
        elif a.GetName() in groupedesmaillessuperposer:
            groupsup.extend(a.GetListOfID())
        elif a.GetName() in groupedesmaillespannes:
            grouppan.extend(a.GetListOfID())
        if a.GetName() in groupedesmaillesintersecter:
            groupint.extend(a.GetListOfID())
    
    #cas decaler
    for curmail in groupdec:
        lienmailnewnode[curmail]=nnewnode;
        gndec.append(nnewnode);
        curnor=normalelem(topmesh,curmail)
        curmid=topmesh.BaryCenter(curmail)
        #print curmail,curmid
        nouveaunoeud=curmid+hdefaut*curnor
        if (curmail in groupint):
            nouveaunoeud=numpy.array(getnodebyintersection(Shape,curmid,curnor,nouveaunoeud))
        newnode=numpy.vstack((newnode,nouveaunoeud))
        normalmail=numpy.vstack((normalmail,curnor))
        nnewnode+=1;
    
    #print "nouveau noeud",nnewnode
    #print "newnode",len(newnode)
    #print newnode
        
    #cassuperpose
    for curmail in groupsup:
        listnode=topmesh.GetElemNodes(curmail)
        for a in listnode:
            if (liennodenewdecanode.has_key(a)):
                #print "noeud deja fait"
                pass
            else:
                liennodenewdecanode[a]=nnewnode;
                gnsup.append(nnewnode);
                nouveaunoeud=topmesh.GetNodeXYZ(a)
                nouveaunoeud[2]=nouveaunoeud[2]+hdefaut
                if (curmail in groupint):
                    nouveaunoeud=getnodebyintersection(Shape,topmesh.GetNodeXYZ(a),(0,0,1),nouveaunoeud)
                newnode=numpy.vstack((newnode,nouveaunoeud))
                nnewnode+=1;
    
    print "creation des noeuds milieu des mails... ",nnewnode
    
    
    #########################################################
    
    print "parcour des mails pour cree les lignes"
    
    #parcour des mail decaller
    for curmail in groupdec:
        #parcour de chaque ligne de la mail
        listnode=topmesh.GetElemNodes(curmail)
        for imailline in range (0,len(listnode)):
            curline=(0,0);#on stoque la ligne courrante
            if (imailline==len(listnode)-1):
                curline=(listnode[0],listnode[imailline])
            else:
                curline=listnode[imailline:imailline+2]
            
            #on ajoute la ligne du haut
            addline((liennodenewnode[curline[0]],liennodenewnode[curline[1]]),newline,glini);
            #on ajoute les deux diagonale
            addline((liennodenewnode[curline[0]],lienmailnewnode[curmail]),newline,gldiag);
            addline((liennodenewnode[curline[1]],lienmailnewnode[curmail]),newline,gldiag);
    
            #recherche des mailles avec la meme ligne
            linkmail=recherchecouple(curline,topmesh)
            maillierused=0;
            finddeux=False
            findone=False
            i=0
            while (not(finddeux) and i<len(linkmail)):
                maillier=linkmail[i]
                if curmail==maillier:
                    #print "on ne fait rien"
                    pass
                elif (maillier in groupdec or maillier in groupsup):
                    maillierused=maillier
                    findone=True
                    if (len(topmesh.GetElemNodes(maillier))==2):
                        finddeux=True # on sort
                i+=1
            if (findone):
                if (maillierused in groupdec):
                    addline((lienmailnewnode[curmail],lienmailnewnode[maillierused]),newline,glnew);
                elif maillierused in groupsup:
                        #on ajoute les lignes du bas
                    addline((lienmailnewnode[curmail],liennodenewdecanode[curline[0]]),newline,glnew);
                    addline((lienmailnewnode[curmail],liennodenewdecanode[curline[1]]),newline,glnew);
        if (len(listnode)==2):
            #dans le cas d une ligne il faut faire d autre branchement
            for i in range(0,2):
                linkmail=recherchesingle(listnode[i],topmesh)
                for maillier in linkmail:
                    if curmail==maillier:
                            #print "on ne fait rien",curmail
                        pass
                    elif (maillier in groupdec):
                        #on ajoute la ligne du bas
                        addline((lienmailnewnode[curmail],lienmailnewnode[maillier]),newline,glnew);
                    elif (maillier in groupsup):
                        #on ajoute la ligne du bas
                        print "erreur"
                        addline((lienmailnewnode[curmail],liennodenewdecanode[listnode[i]]),newline,glnew);
                    
                
    #parcour des mail supperposer
    for curmail in groupsup:
        #parcour de chaque ligne de la mail
        listnode=topmesh.GetElemNodes(curmail)
        for imailline in range (0,len(listnode)):
            curline=(0,0);#on stoque la ligne courrante
            if (imailline==len(listnode)-1):
                curline=(listnode[0],listnode[imailline])
            else:
                curline=listnode[imailline:imailline+2]
            #on ajoute la ligne du haut
            addline((liennodenewnode[curline[0]],liennodenewnode[curline[1]]),newline,glini);
            #on ajoute les 4 diagonales
            addline((liennodenewnode[curline[0]],liennodenewdecanode[curline[0]]),newline,gldiag);
            addline((liennodenewnode[curline[1]],liennodenewdecanode[curline[0]]),newline,gldiag);
            addline((liennodenewnode[curline[0]],liennodenewdecanode[curline[1]]),newline,gldiag);
            addline((liennodenewnode[curline[1]],liennodenewdecanode[curline[1]]),newline,gldiag);
            #on ajoute la ligne du bas
            addline((liennodenewdecanode[curline[0]],liennodenewdecanode[curline[1]]),newline,glnew);
    
    #parcour des mails panne
    for curmail in grouppan:
        listnode=topmesh.GetElemNodes(curmail)
        for imailline in range (0,len(listnode)):
            curline=(0,0);#on stoque la ligne courrante
            if (imailline==len(listnode)-1):
                curline=(listnode[0],listnode[imailline])
            else:
                curline=listnode[imailline:imailline+2]
            #on ajoute la ligne du haut
            addline((liennodenewnode[curline[0]],liennodenewnode[curline[1]]),newline,glpanne);
    
    
     
    newgrl = [("glini",glini),("glnew",glnew),("gldiag",gldiag),("glpanne",glpanne),]
    newgrn = [("gnini",gnini),("gndec",gndec),("gnsup",gnsup),]
    
    return newnode,newline,newgrl,newgrn


