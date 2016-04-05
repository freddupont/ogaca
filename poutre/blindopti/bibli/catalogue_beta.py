#Class catalogue
#V4
#permet de generer des caracteristiques de section puis de les reinjecter dans CA
#permet de sauvegarder un catalogue de profile
#permet d exporter un script salome qui genere une vue volumique
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


#on a besoin des bibliotheque suivante
import sys
import math
import marshal
from time import time

#importation du module de determination des orientations des poutres
try :
    import orientation_poutre_beta
    from sup_gmsh2 import *
except :
    print "i"*40
    print 'Fonction sauvegard 3d indisponible'
    print 'orientation_poutre non disponible'
    print "i"*40



try :
    import aster
    from Cata.cata import *
    from Accas import _F
    #aster_dir=aster.repout()
    #print "aster_dir",aster_dir
    #print aster.__dict__()
    #sys.path.append(aster_dir+'bibpyt/Utilitai')
    #from Utilitai.sup_gmsh import *
    from Utilitai.partition import *
    #print "print repout",aster.repout()
except :
    print "i"*40
    print 'Fonctionnalites Aster indisponibles'
    print 'certaine fonction ne sont pas disponnible'
    print "i"*40

try :
    import geompy
    import salome
except :
    print "i"*40
    print 'Fonctionnalites Salome indisponibles'
    print 'certaine fonction ne sont pas disponnible'
    print "i"*40
    
#ecrite par frederic renou 2011 tout droit reserve
class CATALOGUE_POUTRE:
    class section_rect:
        def __init__(self,parent):
            self.parent=parent
            self.nom="rect"
            self.parametres=('ht:hauteur totale',
                             'lt:largeur totale',
                             'ew: epaisseur ame (web)= 0 par defaut',
                             'ef: epaisseur aile(flange)= 0 par defaut',
                             'r: rayon du conge = 0 par defaut')
            self.subdiv=3.#nombre de subdivision du plus petit element
            self.subdiv1=10.#nombre de subdivision du plus petit element
        def gen_lists(self,parametre ):
            ht=parametre[0]
            lt=parametre[1]
            if (len(parametre)>2):
               ew=parametre[2]
               ef=parametre[3]
            else:
                ew=0
                ef=0
            
            if (len(parametre)==5):
                r=parametre[4]
            else:
                r=0
            
            int=[];
            lpoint=[];
            ltype=[];#l pour une ligne et c pour une courbe
            lpoint.append((-lt/2,ht/2))
            lpoint.append((lt/2,ht/2))
            ltype.append(('l'))
            lpoint.append((lt/2,-ht/2))
            ltype.append(('l'))
            lpoint.append((-lt/2,-ht/2))
            ltype.append(('l'))
            #pour revenir au debut
            ltype.append(('l'))
            
            if (ew!=0 and ef!=0):
                #definition du trou
                lpointint=[]
                ltypeint=[]
                #cas sans conge
                if (r==0):
                    lpointint.append((-lt/2+ew,ht/2-ef))
                    lpointint.append((lt/2-ew,ht/2-ef))
                    ltypeint.append(('l'))
                    lpointint.append((lt/2-ew,-ht/2+ef))
                    ltypeint.append(('l'))
                    lpointint.append((-lt/2+ew,-ht/2+ef))
                    ltypeint.append(('l'))
                    #pour revenir au debut
                    ltypeint.append(('l'))
                else:
                    #cas avec conge
                    lpointint.append((-lt/2+ew,ht/2-ef-r))
                    lpointint.append((-lt/2+ew+r,ht/2-ef))
                    ltypeint.append(['c',(-lt/2+ew+r,ht/2-ef-r)])
                    
                    lpointint.append((lt/2-ew-r,ht/2-ef))
                    ltypeint.append(('l'))
                    lpointint.append((lt/2-ew,ht/2-ef-r))
                    ltypeint.append(['c',(lt/2-ew-r,ht/2-ef-r)])
                    
                    lpointint.append((lt/2-ew,-ht/2+ef+r))
                    ltypeint.append(('l'))
                    lpointint.append((lt/2-ew-r,-ht/2+ef))
                    ltypeint.append(['c',(lt/2-ew-r,-ht/2+ef+r)])
                    
                    lpointint.append((-lt/2+ew+r,-ht/2+ef))
                    ltypeint.append(('l'))
                    lpointint.append((-lt/2+ew,-ht/2+ef+r))
                    ltypeint.append(['c',(-lt/2+ew+r,-ht/2+ef+r)])
                    #pour revenir au debut
                    ltypeint.append(('l'))
                int=[(lpointint,ltypeint)]
                
            dcar=min(ht,lt)/self.subdiv1
            if (len(parametre)>2):
                dcar=min(dcar,min(ew,ef)/self.subdiv)
            if (r>0.):
                dcar=min(dcar,r/self.subdiv)
            return (lpoint,ltype),int,dcar
    class section_Csym:
        def __init__(self,parent):
            self.parent=parent
            self.nom="Csym"
            self.parametres=('ht:hauteur totale',
                             'lt:largeur totale',
                             'ew: epaisseur ame (web)',
                             'ef: epaisseur aile(flange)',
                             'r: rayon du conge = 0 par defaut')
            self.subdiv=3.#nombre de subdivision du plus petit element
            self.subdiv1=3.#nombre de subdivision du plus petit element
        def gen_lists(self,parametre ):
            ht=parametre[0]
            lt=parametre[1]
            ew=parametre[2]
            ef=parametre[3]
            
            if (len(parametre)==5):
                r=parametre[4]
            else:
                r=0
            
            int=[];
            lpoint=[];
            ltype=[];#l pour une ligne et c pour une courbe
            lpoint.append((0,ht/2))
            lpoint.append((lt,ht/2))
            ltype.append(('l'))
            lpoint.append((lt,ht/2-ef))
            ltype.append(('l'))
            #cas sans conge
            if (r==0):
                lpoint.append((ew,ht/2-ef))
                ltype.append(('l'))
                lpoint.append((ew,-ht/2+ef))
                ltype.append(('l'))
            else:
                #cas avec conge
                lpoint.append((ew+r,ht/2-ef))
                ltype.append(('l'))
                
                lpoint.append((ew,ht/2-ef-r))
                ltype.append(['c',(ew+r,ht/2-ef-r)])
                
                lpoint.append((ew,-ht/2+ef+r))
                ltype.append(('l'))
                
                lpoint.append((ew+r,-ht/2+ef))
                ltype.append(['c',(ew+r,-ht/2+ef+r)])
                
            lpoint.append((lt,-ht/2+ef))
            ltype.append(('l'))
            lpoint.append((lt,-ht/2))
            ltype.append(('l'))
            lpoint.append((0,-ht/2))
            ltype.append(('l'))
            #pour rejoindre le premier noeud
            ltype.append(('l'))
            
            dcar=min(ew,ef)/self.subdiv
            if (r>0.):
                dcar=min(dcar,r/self.subdiv1)
            return (lpoint,ltype),int,dcar
    class section_Isym:
        def __init__(self,parent):
            self.parent=parent
            self.nom="Isym"
            self.parametres=('ht:hauteur totale',
                             'lt:largeur totale',
                             'ew: epaisseur ame (web)',
                             'ef: epaisseur aile(flange)',
                             'r: rayon du conge = 0 par defaut')
            self.subdiv=3.#nombre de subdivision du plus petit element
            self.subdiv1=3.#nombre de subdivision du plus petit element
        def gen_lists(self,parametre ):
            ht=parametre[0]
            lt=parametre[1]
            ew=parametre[2]
            ef=parametre[3]
            
            if (len(parametre)==5):
                r=parametre[4]
            else:
                r=0
            
            int=[];
            lpoint=[];
            ltype=[];#l pour une ligne et c pour une courbe
            lpoint.append((-lt/2,ht/2))
            lpoint.append((lt/2,ht/2))
            ltype.append(('l'))
            lpoint.append((lt/2,ht/2-ef))
            ltype.append(('l'))
            #cas sans conge
            if (r==0):
                lpoint.append((ew/2,ht/2-ef))
                ltype.append(('l'))
                lpoint.append((ew/2,-ht/2+ef))
                ltype.append(('l'))
            else:
                #cas avec conge
                lpoint.append((ew/2+r,ht/2-ef))
                ltype.append(('l'))
                
                lpoint.append((ew/2,ht/2-ef-r))
                ltype.append(['c',(ew/2+r,ht/2-ef-r)])
                
                lpoint.append((ew/2,-ht/2+ef+r))
                ltype.append(('l'))
                
                lpoint.append((ew/2+r,-ht/2+ef))
                ltype.append(['c',(ew/2+r,-ht/2+ef+r)])
                
            lpoint.append((lt/2,-ht/2+ef))
            ltype.append(('l'))
            lpoint.append((lt/2,-ht/2))
            ltype.append(('l'))
            lpoint.append((-lt/2,-ht/2))
            ltype.append(('l'))
            lpoint.append((-lt/2,-ht/2+ef))
            ltype.append(('l'))
            
            if (r==0):
                lpoint.append((-ew/2,-ht/2+ef))
                ltype.append(('l'))
                lpoint.append((-ew/2,+ht/2-ef))
                ltype.append(('l'))
            else:
                #cas avec conge
                lpoint.append((-ew/2-r,-ht/2+ef))
                ltype.append(('l'))
                
                lpoint.append((-ew/2,-ht/2+ef+r))
                ltype.append(['c',(-ew/2-r,-ht/2+ef+r)])
                
                lpoint.append((-ew/2,ht/2-ef-r))
                ltype.append(('l'))
                
                lpoint.append((-ew/2-r,ht/2-ef))
                ltype.append(['c',(-ew/2-r,ht/2-ef-r)])

            lpoint.append((-lt/2,+ht/2-ef))
            ltype.append(('l'))
            #pour rejoindre le premier noeud
            ltype.append(('l'))
            
            dcar=min(ew,ef)/self.subdiv
            if (r>0.):
                dcar=min(dcar,r/self.subdiv1)
            return (lpoint,ltype),int,dcar
    class section_Iasym:
        def __init__(self,parent):
            self.parent=parent
            self.nom="Iasym"
            self.parametres=('ht:hauteur totale',
                             'ew: epaisseur ame (web)',
                             'lh:largeur haute',
                             'efh: epaisseur aile(flange)haute',
                             'lb:largeur basse',
                             'efb: epaisseur aile(flange)basse',
                             'r: rayon du conge = 0 par defaut')
            self.subdiv=3.#nombre de subdivision du plus petit element
            self.subdiv1=3.#nombre de subdivision du plus petit element
        def gen_lists(self,parametre ):
            ht=parametre[0]
            ew=parametre[1]
            lh=parametre[2]
            efh=parametre[3]
            lb=parametre[4]
            efb=parametre[5]

            
            if (len(parametre)==7):
                r=parametre[6]
            else:
                r=0
            
            int=[];
            lpoint=[];
            ltype=[];#l pour une ligne et c pour une courbe
            lpoint.append((-lh/2,ht/2))
            lpoint.append((lh/2,ht/2))
            ltype.append(('l'))
            lpoint.append((lh/2,ht/2-efh))
            ltype.append(('l'))
            #cas sans conge
            if (r==0):
                lpoint.append((ew/2,ht/2-efh))
                ltype.append(('l'))
                lpoint.append((ew/2,-ht/2+efb))
                ltype.append(('l'))
            else:
                #cas avec conge
                lpoint.append((ew/2+r,ht/2-efh))
                ltype.append(('l'))
                
                lpoint.append((ew/2,ht/2-efh-r))
                ltype.append(['c',(ew/2+r,ht/2-efh-r)])
                
                lpoint.append((ew/2,-ht/2+efb+r))
                ltype.append(('l'))
                
                lpoint.append((ew/2+r,-ht/2+efb))
                ltype.append(['c',(ew/2+r,-ht/2+efb+r)])
                
            lpoint.append((lb/2,-ht/2+efb))
            ltype.append(('l'))
            lpoint.append((lb/2,-ht/2))
            ltype.append(('l'))
            lpoint.append((-lb/2,-ht/2))
            ltype.append(('l'))
            lpoint.append((-lb/2,-ht/2+efb))
            ltype.append(('l'))
            
            if (r==0):
                lpoint.append((-ew/2,-ht/2+efb))
                ltype.append(('l'))
                lpoint.append((-ew/2,+ht/2-efh))
                ltype.append(('l'))
            else:
                #cas avec conge
                lpoint.append((-ew/2-r,-ht/2+efb))
                ltype.append(('l'))
                
                lpoint.append((-ew/2,-ht/2+efb+r))
                ltype.append(['c',(-ew/2-r,-ht/2+efb+r)])
                
                lpoint.append((-ew/2,ht/2-efh-r))
                ltype.append(('l'))
                
                lpoint.append((-ew/2-r,ht/2-efh))
                ltype.append(['c',(-ew/2-r,ht/2-efh-r)])

            lpoint.append((-lh/2,+ht/2-efh))
            ltype.append(('l'))
            #pour rejoindre le premier noeud
            ltype.append(('l'))
            
            dcar=min(ew,efh,efb)/self.subdiv
            if (r>0.):
                dcar=min(dcar,r/self.subdiv1)
            return (lpoint,ltype),int,dcar
    class section_sbox:
        def __init__(self,parent):
            self.parent=parent
            self.nom="sbox"
            self.parametres=('hr:hauteur rectangle de base',
                             'lr:largeur recangle de base',
                             'l1:longueur 1 haut a gauche',
                             'e1: epaisseur 1 haut a gauche',
                             'l2:longueur 2 haut a droite',
                             'e2: epaisseur 2 haut a droite',
                             'l3:longueur 3 bas a droite',
                             'e3: epaisseur 3 bas a droite',
                             'l4:longueur 4 bas a gauche',
                             'e4: epaisseur 4 bas a gauche',
                             'hri:hauteur rectangle interieur',
                             'lri: largeur rectangle interieur',                             
                             )
            self.subdiv=3.#nombre de subdivision du plus petit element
            self.subdiv1=10.#nombre de subdivision du plus petit element
        def gen_lists(self,parametre ):
            hr=parametre[0]
            lr=parametre[1]
            if (len(parametre)>2):
                l1=parametre[2]
                e1=parametre[3]
            else:
                l1=0
                e1=0
            if (len(parametre)>4):
                l2=parametre[4]
                e2=parametre[5]
            else:
                l2=0
                e2=0
            if (len(parametre)>6):
                l3=parametre[6]
                e3=parametre[7]
            else:
                l3=0
                e3=0
            if (len(parametre)>8):
                l4=parametre[8]
                e4=parametre[9]
            else:
                l4=0
                e4=0
            if (len(parametre)>10):
                hri=parametre[10]
                lri=parametre[11]
            else:
                hri=0
                lri=0
                             
                
            
            
            int=[];
            lpoint=[];
            ltype=[];#l pour une ligne et c pour une courbe
            
            mindist=min(hr,lr)
            
            if (l1==0 and e1==0):
                lpoint.append((-lr/2,hr/2))
            else:
                mindist=min(l1,e1)
                lpoint.append((-lr/2,hr/2-e1))
                
                lpoint.append((-lr/2-l1,hr/2-e1))
                ltype.append(('l'))
                lpoint.append((-lr/2-l1,hr/2))
                ltype.append(('l'))
                
            if (l2==0 and e2==0):
                lpoint.append((lr/2,hr/2))
                ltype.append(('l'))
            else:
                mindist=min(l2,e2,mindist)
                
                lpoint.append((lr/2+l2,hr/2))
                ltype.append(('l'))
                lpoint.append((lr/2+l2,hr/2-e2))
                ltype.append(('l'))
                lpoint.append((lr/2,hr/2-e2))
                ltype.append(('l'))

            if (l3==0 and e3==0):
                lpoint.append((lr/2,-hr/2))
                ltype.append(('l'))
            else:
                mindist=min(l3,e3,mindist)
                
                lpoint.append((lr/2,-hr/2+e3))
                ltype.append(('l'))
                lpoint.append((lr/2+l3,-hr/2+e3))
                ltype.append(('l'))
                lpoint.append((lr/2+l3,-hr/2))
                ltype.append(('l'))
                
            if (l4==0 and e4==0):
                lpoint.append((-lr/2,-hr/2))
                ltype.append(('l'))
            else:
                mindist=min(l4,e4,mindist)
                
                lpoint.append((-lr/2-l4,-hr/2))
                ltype.append(('l'))
                lpoint.append((-lr/2-l4,-hr/2+e4))
                ltype.append(('l'))
                lpoint.append((-lr/2,-hr/2+e4))
                ltype.append(('l'))
            
            ltype.append(('l'))
            
            if (hri!=0 and lri!=0):
                mindist=min(hr-hri,lr-lri,mindist)
                lpint=[]
                ltint=[]
                lpint.append((-lri/2,hri/2))
                ltint.append(('l'))
                lpint.append((lri/2,hri/2))
                ltint.append(('l'))
                lpint.append((lri/2,-hri/2))
                ltint.append(('l'))
                lpint.append((-lri/2,-hri/2))
                ltint.append(('l'))
                int=[(lpint,ltint)]
                
                
            
            
            dcar=min(min(hr,lr)/self.subdiv1,mindist/self.subdiv)
            return (lpoint,ltype),int,dcar
    #class section_Compose_symx:
    #    def __init__(self,parent):
    #        self.parent=parent
    #        self.nom="Compose_symx"
    #        self.parametres=('sb:section de base format (nom,parametre)',
    #                         'r:angle de rotation deg',
    #                         'dx: deplacement selon x',
    #                         'dy: deplacement selon y',
    #                         )
    #    def gen_lists(self,parametre ):
    #        
    #        generateur=self.parent.generation[parametre[0][0]]
    #        ext,int,dcar=generateur.gen_lists(parametre[0][1])
    #        
    #        r=parametre[1]
    #        dx=parametre[2]
    #        dy=parametre[3]
    #        
    #        listdelpoint=[ext[0]]
    #        listdeltype=[ext[1]]
    #        for a in int:
    #            listdelpoint.append(a[0])
    #            listdeltype.append(a[1])
    #        
    #        cost=math.cos(r/180.*math.pi)
    #        sint=math.sin(r/180.*math.pi)
    #        print "r",r,"cost",cost
    #        def newpoint(oldpt,cost,sint,dx,dy):
    #            return [oldpt[0]*cost-oldpt[1]*sint+dx,oldpt[0]*sint+oldpt[1]*cost+dy]
    #        for lp in listdelpoint:
    #            for i in range(0,len(lp)):
    #                lp[i]=newpoint(lp[i],cost,sint,dx,dy)
    #        for lt in listdeltype:
    #            for a in lt:
    #                if (len(a)==2):
    #                    a[1]=newpoint(a[1],cost,sint,dx,dy)
    #        return ext,int,dcar
    #class section_Compose_symxy(section_Compose_symx):
    #    def __init__(self,parent):
    #        self.parent=parent
    #        self.nom="Compose_symxy"
    #        self.parametres=('sb:section de base format (nom,parametre)',
    #                         'r:angle de rotation deg',
    #                         'dx: deplacement selon x',
    #                         'dy: deplacement selon y',
    #                         )
    class section_Lasym:
        def __init__(self,parent):
            self.parent=parent
            self.nom="Lasym"
            self.parametres=('h:hauteur totale',
                             'b:largeur totale',
                             't: eppaisseur',
                             'r1: rayon du conge interieur default=0',
                             'r2: rayon du conge aux extremite default=0')
            self.subdiv1=3.#nombre de subdivision dans la largeur ou des cercles
            self.subdiv2=10.#nombre de subdivision des longueurs
            
        def gen_lists(self,parametre ):
            h=parametre[0]
            b=parametre[1]
            t=parametre[2]
            if (len(parametre)==5):
                r1=parametre[3]
                r2=parametre[4]
            elif (len(parametre)==3):
                r1=0.0;
                r2=0.0;
            else:
                print "le nombre de parametre pour la section en L est incorecte"
            
            assert(r2<t)
            assert((r1==0 and r2==0) or (r1!=0 and r2!=0))
                        
            int=[];
            lpoint=[];
            ltype=[];#'l' pour une ligne et 'c' pour une courbe il faut aussi preciser le point centrale du cercle
            
            lpoint.append((0,0))
            lpoint.append((0,h))
            ltype.append(('l'))
            if (r2==0 and r1==0):
                lpoint.append((t,h))
                ltype.append(('l'))
                lpoint.append((t,t))
                ltype.append(('l'))
                lpoint.append((b,t))
                ltype.append(('l'))
            else :
                lpoint.append((t-r2,h))
                ltype.append(('l'))
                lpoint.append((t,h-r2))
                ltype.append(['c',(t-r2,h-r2)])
                lpoint.append((t,t+r1))
                ltype.append(('l'))
                lpoint.append((t+r1,t))
                ltype.append(['c',(t+r1,t+r1)])
                
                lpoint.append((b-r2,t))
                ltype.append(('l'))
                lpoint.append((b,t-r2))
                ltype.append(['c',(b-r2,t-r2)])
                
            lpoint.append((b,0))
            ltype.append(('l'))
            ltype.append(('l'))

            if (r2==0 and r1==0):
                dcar=min(t/self.subdiv1,h/self.subdiv2,b/self.subdiv2)
            else:
                dcar=min(r2/self.subdiv1,r1/self.subdiv1,t/self.subdiv1,h/self.subdiv2,b/self.subdiv2)
            return (lpoint,ltype),int,dcar
    class section_rond:
        def __init__(self,parent):
            self.parent=parent
            self.nom="rond"
            self.parametres=('diaext:diametre exterrieur',
                             't:thickness = 0 par defaut section pleine')
            self.subdiv1=3#nombre de subdivision dans la largeur
            self.subdiv2=10.#nombre de subdivision du cercle
            
        def gen_lists(self,parametre ):
            diaext=parametre[0]
            if (len(parametre)==2):
                diaint=parametre[0]-parametre[1]
            else:
                diaint=0.0;
            
            assert (diaint<diaext);
            
            
            int=[];
            lpoint=[];
            ltype=[];#'l' pour une ligne et 'c' pour une courbe il faut aussi preciser le point centrale du cercle
            
            lpoint.append((0,diaext/2))
            lpoint.append((diaext/2,0))
            lpoint.append((0,-diaext/2))
            lpoint.append((-diaext/2,0))
            
            ltype.append(['c',(0.0,0.0)])
            ltype.append(['c',(0.0,0.0)])
            ltype.append(['c',(0.0,0.0)])
            ltype.append(['c',(0.0,0.0)])
            
            if (diaint>0):
                lpint=[]
                ltypeint=[]
                lpint.append((0,diaint/2))
                lpint.append((diaint/2,0))
                lpint.append((0,-diaint/2))
                lpint.append((-diaint/2,0))
            
                ltypeint.append(['c',(0.0,0.0)])
                ltypeint.append(['c',(0.0,0.0)])
                ltypeint.append(['c',(0.0,0.0)])
                ltypeint.append(['c',(0.0,0.0)])
                int=[(lpint,ltypeint)]
            
            if (diaint>0):
                dcar=min((diaext-diaint)/self.subdiv1,diaint/self.subdiv2,diaext/self.subdiv2)
            else:
                dcar=diaext/self.subdiv2
            #print "dcar",dcar
            return (lpoint,ltype),int,dcar
    def __init__(self,verbose=True):
        #mise en place des fichiers de generation de forme
        self.generation={};
        a=self.section_Isym(self);
        self.generation[a.nom]=a
        a=self.section_rond(self);
        self.generation[a.nom]=a
        a=self.section_Lasym(self);
        self.generation[a.nom]=a
        a=self.section_Csym(self);
        self.generation[a.nom]=a
        a=self.section_rect(self);
        self.generation[a.nom]=a
        a=self.section_Iasym(self);
        self.generation[a.nom]=a
        a=self.section_sbox(self);
        self.generation[a.nom]=a
        #a=self.section_Compose_symx(self)
        #self.generation[a.nom]=a
        #a=self.section_Compose_symxy(self)
        #self.generation[a.nom]=a
        
        
        
        if verbose:
            print "-"*40,"CATALOGUE_POUTRE","-"*40
            print "avertissement: Version beta3"
            print "-"*96        

        #catalogue de forme
        #[type,(parametre),(caracteristique),rotation]
        self.section_catalogue={};
        #
        
        #correspondance
        #{groupema:type}
        self.association={};
        
        ##pour injection des resultats
        self.__CARA=('A','IY','IZ','AY','AZ','EY','EZ','JX','RY','RZ','RT','JG','IYR2','IZR2')
        #self.__CARAP=('A','IZ','IY','AZ','AY','EZ','EY','JX','RZ','RY','RT','JG','IZR2','IYR2')#en cas inversion a 90 on echange Z et Y
        #pour extraction des resultats
        self.__EXTRACTION=('AIRE','IY_PRIN_G','IZ_PRIN_G','AY','AZ','EY','EZ','CT','Y_MAX','Z_MAX','RT','JG','IYR2_PRIN_G','IZR2_PRIN_G','ALPHA','CDG_X','CDG_Y')
    def usage(self):
        a="""
        CATALOGUE_POUTRE
        
        fait le lien entre CA et salome pour generer un fichier volumetrique 3D avec les sections des poutres
        permet aussi de generer et d'utiliser un vaste catalogue de section
        
        ------------------------------------------------------
        commande disponible depuis CA
        #importation du catalogue
        bibli_dir='/home/fred/asteretude/kuwait/bibli'
        import sys
        sys.path.append(bibli_dir)
        import catalogue_beta
        cata=catalogue_beta.CATALOGUE_POUTRE();#chargement du catalogue
        
        -----
        partie concernant le calcul des caracterisitque des sections
        cata.affiche_generateur();#affichage des generateur de section disponnible
        
        cata.section_ajout("sbox2","sbox",(0.4,0.2,0.1,0.03,0.2,0.03))#ajout d'une section
        
        cata.section_generation("sbox2")#calcul les caracteristiques de la section
        cata.section_generation_mail("sbox2",UNITE=78);#cree un fichier med de la section
        cata.section_generation_tout()#calcul les caracteristiques de toutes les sections
        
        cata.section_sauvegarde_catalogue(fichiercata)#sauvegarde des section
        cata.section_charge_catalogue(fichiercata)#chargement (ajout a la base)
        cata.section_recharge_catalogue(fichiercata)#chargement (supprime le catalogue existant)
        cata.section_affiche("phi3025")#affichage des propriete d'une section
        cata.section_affiche_nom();#affiche les nom disponnible
        cata.section_affiche_tout();#on affiche tout le catalogue de section
        
        -------
        #Partie concernant l affectation entre les gma et les sections
        
        cata.affecter_GRMA_TYPE('LL1',"IPE100")
        ##affectation du groupe mail 'LL1' avec un "IPE100"
        
        cata.desaffecter_GRMA(groupma)
        cata.desaffecter_tout()
        cata.affiche_affectation()
        cata.get_section_cara(groupma)

        -------
        #Partie generale

        cata.affiche_tout()
        cata.sauvegarde(fichier)
        #sauvegarde de section_catalogue et des affectations
        cata.recharge(fichier)
        #rechargement de section_catalogue et des affectations
        
        #exemple de sortie pour aster qui permet d'utiliser les sections definies
        CAREL=AFFE_CARA_ELEM(MODELE=MO, INFO=1,POUTRE=cata.POUTRE())
        
        cata.sauvegarde_pour_3d(fichiertemp,MODELE=MO,MAILLAGE=MAILLAGE,CHAM_MATER=CHMAT,CARA_ELEM=CAREL)
        #cree un fichier pour une visualisation dans salome
        
        ------------------------------------------------------
        commande disponible depuis SALOME

        #importation du catalogue
        bibli_dir='/home/fred/asteretude/kuwait/bibli'
        import sys
        sys.path.append(bibli_dir)
        import catalogue_beta

        cata=catalogue_beta.CATALOGUE_POUTRE();#chargement du catalogue
        
        
        fichiertemp='/tmp/cata.mar'
        #affichage 2D des section dans leur axe neutre local
        cata.charge_et_genere_2d(fichiertemp)
        
        #affichage 2D des section tel que dessine
        cata.charge_et_genere_2d(fichiertemp,SANS_RECALAGE="OUI")
        
        #affichage de la geometrie 3D
        cata.charge_et_genere_3d(fichiertemp)
        
        
        fin de l'aide
        """
        print a
        return a
    def section_cara_contrainte(self,section_cara,N,My,Mz):
        """calcul les contraintes max dans une section en utilisant uniquement N,My et MZ"""
        #sy=My*Z_max/Iy
        sigmamy=abs(My/section_cara[2][1]*section_cara[2][9])
        
        #sz=Mz*Y_max/Iz
        sigmamz=abs(Mz/section_cara[2][2]*section_cara[2][8])
        
        sigmaN=N/section_cara[2][0]
        sigmamax=sigmaN+sigmamy+sigmamz
        sigmamin=sigmaN-sigmamy-sigmamz
        
        return (sigmamin,sigmamax)

    def gma_contrainte(self,gma,N,My,Mz):
        """calcul les contraintes max dans un gma en utilisant uniquement N,My et MZ"""
        return self.section_cara_contrainte(self.get_section_cara_from_gma(gma),N,My,Mz)
        
    def get_section_cara_from_gma(self,gma):
        """retourne les caracteristique d'un section a partir du groupe"""
        sectionname=self.association[gma]
        return self.section_catalogue[sectionname]

    def get_section_cara_from_sectionname(self,sectionname):
        """retourne les caracteristique d'un section a partir du nom de section"""
        return self.section_catalogue[sectionname]

    
    def section_ajout(self,nom,type,parametre,caracteristique=[],rotation=False):
        self.section_catalogue[nom]=[type,parametre,caracteristique,rotation]
        
    def __generation_gmshsubsurface(self,liste,dcar):
        lpgmsh=[]
        #print 'liste',liste
        for a in liste[0]:
            lpgmsh.append(Point(a[0],a[1]))
            
        llgmsh=[]
        for i in range(0,len(liste[1])-1):
            
            if liste[1][i][0]=='l':
                ligne=Line(lpgmsh[i],lpgmsh[i+1])
            elif liste[1][i][0]=='c':
                ligne=Circle(lpgmsh[i],Point(liste[1][i][1][0],liste[1][i][1][1]),lpgmsh[i+1])
            else:
                print "erreur type de ligne non reconue"
                
            dist=math.sqrt((liste[0][i][0]-liste[0][i+1][0])**2+(liste[0][i][1]-liste[0][i+1][1])**2)
            nb=int(dist/dcar)
            #print "dx**2",(liste[0][i][0]-liste[0][i+1][0])**2
            #print "dy**2",(liste[0][i][1]-liste[0][i+1][1])**2
            #print "dist",dist,"dcar",dcar,"nb",nb
            ligne.Transfinite(nb)
            llgmsh.append(ligne);
        if liste[1][len(lpgmsh)-1][0]=='l':
            ligne=Line(lpgmsh[len(lpgmsh)-1],lpgmsh[0])
        elif liste[1][len(lpgmsh)-1][0]=='c':
            ligne=Circle(lpgmsh[len(lpgmsh)-1],Point(liste[1][len(lpgmsh)-1][1][0],liste[1][len(lpgmsh)-1][1][1]),lpgmsh[0])
        else:
            print "erreur type de ligne non reconue"

        dist=math.sqrt((liste[0][len(liste[1])-1][0]-liste[0][0][0])**2+(liste[0][len(liste[1])-1][1]-liste[0][0][1])**2)
        ligne.Transfinite(int(dist/dcar))
        llgmsh.append(ligne);
        
        return lpgmsh,llgmsh
    def __generation_salomesubsurface(self,liste):
        lpsalo=[]
        #print 'liste',liste
        for a in liste[0]:
            lpsalo.append(geompy.MakeVertex(a[0],a[1],0))
            
        llsalo=[]
        for i in range(0,len(liste[1])-1):
            
            if liste[1][i][0]=='l':
                ligne=geompy.MakeLineTwoPnt(lpsalo[i],lpsalo[i+1])
            elif liste[1][i][0]=='c':
                ligne=geompy.MakeArcCenter(geompy.MakeVertex(liste[1][i][1][0],liste[1][i][1][1],0), lpsalo[i], lpsalo[i+1],0)
            else:
                print "erreur type de ligne non reconue"
                
            llsalo.append(ligne);
        if liste[1][len(lpsalo)-1][0]=='l':
            ligne=geompy.MakeLineTwoPnt(lpsalo[len(lpsalo)-1],lpsalo[0])
        elif liste[1][len(lpsalo)-1][0]=='c':
            ligne=geompy.MakeArcCenter(geompy.MakeVertex(liste[1][len(lpsalo)-1][1][0],liste[1][len(lpsalo)-1][1][1],0), lpsalo[len(lpsalo)-1], lpsalo[0],0)
        else:
            print "erreur type de ligne non reconue"

        #dist=math.sqrt((liste[0][len(liste[1])-1][0]-liste[0][0][0])**2+(liste[0][len(liste[1])-1][1]-liste[0][0][1])**2)
        #ligne.Transfinite(int(dist/dcar))
        llsalo.append(ligne);
        
        return llsalo

    def __generation_maillage_aster(self,sec,nom):
        gen=self.generation[sec[0]]
        
        extl,intl,dcar=gen.gen_lists(sec[1])
        
        lpgmshext,llgmshext=self.__generation_gmshsubsurface(extl,dcar)
        Sext=Surface(*llgmshext)
        llgmshint=[]
        for a in intl:
            lpgmshinttemp,llgmshinttemp=self.__generation_gmshsubsurface(a,dcar)
            Stemp=Surface(*llgmshinttemp)
            Sext.Holes(Stemp)
            llgmshint.extend(llgmshinttemp)
        
        mesh=Mesh()
        mesh.Physical('ext',*llgmshext)
        if len(llgmshint)>0:
            mesh.Physical('int',*llgmshint)
        mesh.Physical('Sext',Sext)
        mesh.Physical('GN',lpgmshext[0])
        __MAILT=mesh.LIRE_GMSH();
        return __MAILT


    def __section_generation_sec(self,sec,nom):
        __MAILT=self.__generation_maillage_aster(sec,nom)
        #IMPR_RESU(FORMAT='MED',UNITE=80,RESU=_F(MAILLAGE=__MAILT),);
        
        seccara=MACR_CARA_POUTRE(MAILLAGE=__MAILT,GROUP_MA_BORD='ext',GROUP_NO='GN');
        
        #IMPR_TABLE(TABLE=seccara)
        #on charge les valeur depuis la table aster
        Vex=[];
        rot=False
        for a in self.__EXTRACTION:
            Vex.append(seccara[a,2])
            #print a,seccara[a,2]
        if (Vex[14]>1e-5 or Vex[14]<-1e-5):
            print "attention angle alpha different de zero :"
            if (Vex[14]>46. or Vex[14]<-46.):
                print "Rotation de plus de 45 on corrige pour etre au plus proche du dessin initial"
                rot=True
                caratemp=[Vex[0],#AIRE
                          Vex[2],Vex[1],#'IY_PRIN_G','IZ_PRIN_G'
                          Vex[4],Vex[3],#'AY','AZ'
                          Vex[6],Vex[5],#'EY','EZ'
                          Vex[7],#'CT'
                          Vex[9],Vex[8],#'Y_MAX','Z_MAX'
                          Vex[10],Vex[11],#'RT','JG'
                          Vex[13],Vex[12],#'IYR2_PRIN_G','IZR2_PRIN_G'
                          Vex[14],Vex[15],Vex[16]]#'ALPHA','CDG_X','CDG_Y'
                Vex=caratemp
                if (Vex[14]<0):
                    Vex[14]=Vex[14]+90.
                else:
                    Vex[14]=Vex[14]-90.
                print "par default les section sont tourne de l angle ",Vex[14]
            else:
                print "par default les section sont tourne de l angle ",Vex[14]
        if (Vex[15]>1e-5 or Vex[15]<-1e-5 or Vex[16]>1e-5 or Vex[16]<-1e-5):
            print "attention centre de gravite excentre par rapport au dessin"
            print "CDG_X:",Vex[15]," CDG_Y:",Vex[16]
            print "Les poutres sont par default place sur leur centre de gravite"
        newsec=[sec[0],sec[1],Vex,rot];
        self.section_catalogue[nom]=newsec
        DETRUIRE(INFO=1,CONCEPT=_F(NOM=(__MAILT,seccara),));
        
    def section_generation_mail(self,nom,UNITE=80):
        v=self.section_catalogue[nom]
        __MAILT=self.__generation_maillage_aster(v,nom)
        IMPR_RESU(FORMAT='MED',UNITE=UNITE,RESU=_F(MAILLAGE=__MAILT),);
        DETRUIRE(INFO=1,CONCEPT=_F(NOM=(__MAILT),));
        
    def section_generation(self,nom):
        v=self.section_catalogue[nom]
        self.__section_generation_sec(v,nom)
        
    def section_generation_tout(self):
        for k,v in self.section_catalogue.iteritems():
            if len(v[2])==0:
                self.__section_generation_sec(v,k)
            
    def section_charge_catalogue(self,fichier):
        f = open(fichier,'rb')
        self.section_catalogue.update(marshal.load(f))
        f.close()
    
    def affecter_GRMA_TYPE(self,groupma,type):
        #self.association[groupma]=type
        if (isinstance(groupma,str)):
                self.association[groupma]=type
        else:
                for a in groupma:
                    self.association[a]=type

    def desaffecter_GRMA(self,groupma):
        del self.association[groupma]
    def desaffecter_tout(self):
        self.association.clear()
    
    def POUTRE(self):
        retour=[]
        reverse_asso={}
        for grit,typeit in self.association.iteritems():
            if reverse_asso.has_key(typeit):
                if type(grit)==str:
                    reverse_asso[typeit].append(grit)
                else:
                    reverse_asso[typeit].extend(grit)
            else:
                reverse_asso[typeit]=[grit]
        for typeit,grit in reverse_asso.iteritems():
            carait=self.section_catalogue[typeit]
            #print carait
            retour.append(_F(GROUP_MA=grit,SECTION='GENERALE',CARA=self.__CARA,VALE=carait[2][:14]))
        return retour;
    def BARRE(self):
        retour=[]
        for grit,typeit in self.association.iteritems():
            carait=self.section_catalogue[typeit]
            retour.append(_F(GROUP_MA=gr,SECTION='GENERALE',CARA='A',VALE=carait[2][1]))
        return retour;
    def section_affiche_nom(self,nbcolone=5):
        print "-"*40
        print "nom des sections actuellement dans le catalogue"
        i=0;
        s=" "*5
        for k,v in self.section_catalogue.iteritems():
            s+=k+" ";
            i+=1
            if (i==nbcolone):
                s+="\n"+(" "*5)
                i=0;
        print s
        print "-"*40
    def __affiche_introcata(self):
        print "-"*4
        print "nom,type"
        print "parametres"
        print "excentrement par rapport au dessin initial"
        print "bool qui indique si on a tourner de 90deg"
        print "Caracteristique: ", self.__EXTRACTION
    def __affiche_cata(self,nom,v):
        print nom,v[0]
        print "(","".join("%e,"%b for b in v[1])+")"
        if (len(v)>2 and len(v[2])>14):
            print "Alpha:",v[2][14]," CDG_X:",v[2][15]," CDG_Y:",v[2][16]
            print v[3]
            #if (v[3]):
            #    print "Attention les caracteristiques affiche sont tourne de 90 depuis par rapport a la sortie carapoutre"
            print "(","".join("%e,"%b for b in v[2])+")"
        
    def section_affiche_tout(self):
        print "-"*40
        print "Toutes les sections actuellement dans le catalogue :"
        self.__affiche_introcata()
        for k,v in self.section_catalogue.iteritems():
            print "-"*20
            self.__affiche_cata(k,v)
        print "-"*40
    def section_affiche(self,nom):
        print "-"*40
        print "La section :",nom
        if (self.section_catalogue.has_key(nom)):
            self.__affiche_introcata()
            v=self.section_catalogue[nom]
            self.__affiche_cata(nom,v)
        else:
            print "non presente dans le catalogue"
        print "-"*40
    def section_get_para(self,nom):
        if (self.section_catalogue.has_key(nom)):
            v=self.section_catalogue[nom]
            return v[2]
    def section_get_excentrement(self,nom):
        if (self.section_catalogue.has_key(nom)):
            v=self.section_catalogue[nom]
            return (v[2][14],v[2][15],v[2][16])
    def affiche_generateur(self):
        print "-"*40
        print "Generateur disponibles"
        for k,v in self.generation.iteritems():
            print v.nom
            for a in v.parametres:
                print " "*5,a
        print "-"*40
        
    def affiche_affectation(self):
        print "-"*40
        print "Groupes affecte"
        for k,v in self.association.iteritems():
            print k,v
        print "-"*40
    def affiche_tout(self):
        self.section_affiche_tout();
        self.affiche_affectation()
    def section_sauvegarde_catalogue(self,fichier):
        f = open(fichier,'wb')
        marshal.dump(self.section_catalogue, f)
        f.close()
        
    def section_recharge_catalogue(self,fichier):
        f = open(fichier,'rb')
        self.section_catalogue=marshal.load(f)
        f.close()        

    def sauvegarde_pour_3d(self,fichier,MODELE,MAILLAGE,CHAM_MATER,CARA_ELEM):
        
        reducedcata={};
        #print "reducedcata debug"
        for k,v in self.association.iteritems():
            reducedcata[v]=self.section_catalogue[v]
            #print reducedcata[v]
        
        lgroupma=[]
        for k,v in self.association.iteritems():
                lgroupma.append(k)

        orientation=orientation_poutre_beta.orientation_poutre_vyz(GROUP_MA=lgroupma,
                                               MAILLAGE=MAILLAGE,MODELE=MODELE,CARA_ELEM=CARA_ELEM,
                                               CHAM_MATER=CHAM_MATER,RETOUR_TABLE=True,SAUVEGARDE_CHAMP=False)
        mail_py=MAIL_PY();
        mail_py.FromAster(MAILLAGE);
        
        retour=[]
        for k,v in self.association.iteritems():
            #debug
            #print "k,v",k,v
            #print "mail_py.gma[k]",mail_py.gma[k]
            for ma in mail_py.gma[k]:
                if (orientation.has_key(ma)):
                    noeuds=mail_py.co[ma]
                    #retour.append((mail_py.cn[noeuds[0]],mail_py.cn[noeuds[1]],orientation[ma][0],orientation[ma][1],v))
                    retour.append(
                        ((float(mail_py.cn[noeuds[0]][0]),float(mail_py.cn[noeuds[0]][1]),float(mail_py.cn[noeuds[0]][2])),
                        (float(mail_py.cn[noeuds[1]][0]),float(mail_py.cn[noeuds[1]][1]),float(mail_py.cn[noeuds[1]][2])),
                        (float(orientation[ma][0][0]),float(orientation[ma][0][1]),float(orientation[ma][0][2])),
                        (float(orientation[ma][1][0]),float(orientation[ma][1][1]),float(orientation[ma][1][2])),
                        v)
                        )
                    
        

        f = open(fichier,'wb')
        marshal.dump(reducedcata, f)
        #print "sauvegarde de reduced"
        #for a in reducedcata:
        #    print a
        marshal.dump(retour, f)
        #print "sauvegarde de retour"
        #for a in retour:
        #    print a
        
        f.close()
    def __salome_genere_section_catalogue(self,SANS_RECALAGE=None):
        #print obj
        formecentre={}
        for k,sec in self.section_catalogue.iteritems():
            #sec=v[4]
            gen=self.generation[sec[0]]
            extl,intl,dcar=gen.gen_lists(sec[1])
            ll=self.__generation_salomesubsurface(extl)
            for a in intl:
                ll.extend(self.__generation_salomesubsurface(a))
                
            #for v in ll:
            #    geompy.addToStudy(v,k)
            surface=geompy.MakeFaceWires(ll,1)
            
            #gestion de la translation
            surfacet=surface
            if (SANS_RECALAGE!="OUI" and (sec[2][15]<-1e-5 or sec[2][15]>1e-5 or sec[2][16]<-1e-5 or sec[2][16]>1e-5)):
                surfacet=geompy.MakeTranslation(surface,-sec[2][15],-sec[2][16],0)
            surfacetr=surfacet

            #gestion de la rotation
            p0=geompy.MakeVertex(0,0,0)
            p1=geompy.MakeVertex(0,0,1)
            vecteurr=geompy.MakeVector(p0,p1)
            if (SANS_RECALAGE!="OUI" and ( sec[2][14]<-1e-5 or sec[2][14]>1e-5)):
                #print "rotation",-math.pi*sec[2][14]/180. #en 5 c des degree
                surfacetr=geompy.MakeRotation(surfacet,vecteurr,-math.pi*sec[2][14]/180.)#en 6.3 des radient
                #surfacetr=geompy.MakeRotation(surfacet,vecteurr,-sec[2][14])
            formecentre[k]=surfacetr
        return formecentre
    
    def charge_et_genere_2d(self,fichier,SANS_RECALAGE=None):
        #print marshal.version
        f = open(fichier,'rb')
        self.section_catalogue=marshal.load(f)
        f.close()
        
        #print self.section_catalogue#debug
        
        formecentre=self.__salome_genere_section_catalogue(SANS_RECALAGE)
        for k,v in formecentre.iteritems():
            geompy.addToStudy(v,k)
        salome.sg.updateObjBrowser(1)
        
    def charge_et_genere_3d(self,fichier,exportstl=None):
        #print marshal.version

        f = open(fichier,'rb')
        self.section_catalogue=marshal.load(f)
        obj=marshal.load(f)
        f.close()
        
        formecentre=self.__salome_genere_section_catalogue()
        
        newvolume=[]
        repereglobal= geompy.MakeMarker(0,0,0, 1,0,0,0,1,0)
        for a in obj:
            #impression du nom de la forme debug
            #print a[4]
            
            ori=geompy.MakeVertex(a[0][0],a[0][1],a[0][2])
            fin=geompy.MakeVertex(a[1][0],a[1][1],a[1][2])
            nouveaurepere= geompy.MakeMarker(a[0][0],a[0][1],a[0][2], a[2][0],a[2][1],a[2][2],a[3][0],a[3][1],a[3][2])
            basesurface=geompy.MakePosition(formecentre[a[4]],repereglobal,nouveaurepere)
            newvolume.append(geompy.MakePrism(basesurface,ori,fin))
            
        #for k,v in formecentre.iteritems():
        #    geompy.addToStudy(v,k)
        #for v in newvolume:
        #    geompy.addToStudy(v,"Volumique")
        outshape=geompy.MakeCompound(newvolume)

        geompy.addToStudy(outshape,"Volumique")

        if exportstl!=None:
           geompy.Export(outshape, exportstl, "STL_Bin")

        salome.sg.updateObjBrowser(1)
        
    def copie(self,new_section_catalogue=False):
        acopie=CATALOGUE_POUTRE(verbose=False)
        if(new_section_catalogue==False):
            acopie.section_catalogue=self.section_catalogue
        else:
            acopie.section_catalogue=dict(self.section_catalogue)
        acopie.association=dict(self.association)
        return acopie
    def sauvegarde(self,fichier):
        """sauvegarde de section_catalogue et de association"""
        f = open(fichier,'wb')
        marshal.dump((self.section_catalogue,self.association), f)
        f.close()
        print "sauvegarde du catalogue effectue"
    def recharge(self,fichier):
        """rechargement de section_catalogue et de association"""
        f = open(fichier,'rb')
        a=marshal.load(f)
        self.section_catalogue=a[0]
        self.association=a[1]
        f.close()
        print "chargement du catalogue effectue"


        
        
    
