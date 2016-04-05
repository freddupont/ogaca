#########################################################
#opti_section_poutre.py
#contient l'ensemble des macro necessaire pour utiliser blind_opti sur de l'optimisation de section de poutre
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


#bibli_dir='/home/fred/asteretude/blindopti/bibli'
#import sys
#sys.path.append(bibli_dir)

import blind_opti
import catalogue_beta

from Cata.cata import *
from Utilitai.partition import *
from Accas import _F

from math import ceil
#l etat est compose comme suit
#etat_i={}
#etat_i["MAIL"]=MA
#etat_i["MODELE"]=MO
#etat_i["MATERIAU"]=MATR
#etat_i["CHAM_MATER"]=CHMAT
#etat_i["GMASECTIONPOSSIBLE"]=gmasection 
#etat_i["CATALOGUE"]=cata
#
#mais seul le catalogue change sur un nouvel etat

#gmasection est une liste ordonne de (gma,(section1,section2,..))
#attention les sections doivent etre par ordre de resistance croissante




##########################
#fonction support
#fonction qui sont indispensable pour la gestion de blind opti
#elle decrive comment manipuler les elements interessant


#fn_evol
#def macro_opti_sec_fn_evol_prod(self,**args):
#        return table_sdaster
def macro_opti_sec_fn_evol_ops(self,etat,newetat,gradient,alpha,**args):
    self.set_icmd(1)
    #self.DeclareOut('retour',self.sd)
    
    #on copie les donnees fixe
    newetat["MAIL"]=etat["MAIL"]
    newetat["MODELE"]=etat["MODELE"]
    newetat["MATERIAU"]=etat["MATERIAU"]
    newetat["CHAM_MATER"]=etat["CHAM_MATER"]
    newetat["GMASECTIONPOSSIBLE"]=etat["GMASECTIONPOSSIBLE"]
    
    #on copy le catalogue
    newetat["CATALOGUE"]=etat["CATALOGUE"].copie()
    #aster.affiche('MESSAGE',  str(newetat["CATALOGUE"].association))
    #aster.affiche('RESULTAT',  "fn_evol_ops"+str(newetat["CATALOGUE"].association))
    #IMPR_TABLE(TABLE=gradient)
    
    #on parcour chaque groupe de section a optimiser
    for i in range(0,len(newetat["GMASECTIONPOSSIBLE"])):
        gma=newetat["GMASECTIONPOSSIBLE"][i][0]
        listesection=newetat["GMASECTIONPOSSIBLE"][i][1]
        #nom de la section actuel:
        #print gma
        #print newetat["CATALOGUE"].association
        nomsecactuel=newetat["CATALOGUE"].association[gma]
        
        #position de cette section dans la liste
        ii=listesection.index(nomsecactuel)
        iii=ii+int(ceil(gradient['R',i+1]*alpha))
        if iii>len(listesection)-1:
            iii=len(listesection)-1
        if iii<0:
            iii=0
        #aster.affiche('RESULTAT', "gma:"+gma+" grad:"+str(gradient['R',i+1])+ " ii:"+str(ii)+" iii:"+str(iii))
        newetat["CATALOGUE"].affecter_GRMA_TYPE(gma,listesection[iii])
    #aster.affiche('MESSAGE',  str(newetat["CATALOGUE"].association))
    #aster.affiche('RESULTAT',  "fn_evol_ops"+str(newetat["CATALOGUE"].association))
    
    
    return 0
macro_opti_sec_fn_evol= MACRO (nom="macro_opti_sec_fn_evol", op=macro_opti_sec_fn_evol_ops,
                   fr="Sauvegarde du champ", sd_prod=None,
                   etat		        =SIMP(statut='o',typ=str,max='**'),
                   newetat		=SIMP(statut='o',typ=str,max='**'),
                   gradient		=SIMP(statut='o',typ=table_sdaster),
                   alpha		=SIMP(statut='o',typ='R'),
                   );

#fn_update_grad
def macro_opti_sec_fn_update_grad_prod(self,retour,**args):
    self.type_sdprod(retour,table_sdaster)
    return None
def macro_opti_sec_fn_update_grad_ops(self,etat,retour,grad1,alpha,grad2,**args):
    self.set_icmd(1)
    self.DeclareOut('retour',retour)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')
    
    listretour=[]
    for i in range(0,len(etat["GMASECTIONPOSSIBLE"])):
        listretour.append(grad1['R',i+1]+alpha*grad2['R',i+1])

    retour=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=listretour)));
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(grad1),),ALARME='NON');
    return 0

macro_opti_sec_fn_update_grad= MACRO (nom="macro_opti_sec_fn_update_grad", op=macro_opti_sec_fn_update_grad_ops,
                   fr="Sauvegarde du champ", sd_prod=macro_opti_sec_fn_update_grad_prod,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   retour               =SIMP(statut='o',typ=CO),
                   grad1		=SIMP(statut='o',typ=table_sdaster),
                   grad2		=SIMP(statut='o',typ=table_sdaster),
                   alpha		=SIMP(statut='o',typ='R'),
                   );

#fn_mult_grad
def macro_opti_sec_fn_mult_grad_prod(self,retour,**args):
    self.type_sdprod(retour,table_sdaster)
    return None
def macro_opti_sec_fn_mult_grad_ops(self,etat,retour,gradient,alpha,**args):
    self.set_icmd(1)
    self.DeclareOut('retour',retour)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')
    
    listretour=[]
    for i in range(0,len(etat["GMASECTIONPOSSIBLE"])):
        listretour.append(gradient['R',i+1]*alpha)

    retour=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=listretour)));
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(gradient),),ALARME='NON');
    return 0

macro_opti_sec_fn_mult_grad= MACRO (nom="macro_opti_sec_fn_mult_grad", op=macro_opti_sec_fn_mult_grad_ops,
                   fr="Sauvegarde du champ", sd_prod=macro_opti_sec_fn_mult_grad_prod,
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   retour               =SIMP(statut='o',typ=CO),
                   gradient		=SIMP(statut='o',typ=table_sdaster),
                   alpha		=SIMP(statut='f',typ='R'),
                   );


#fn_prod_scalaire_grad

def macro_opti_sec_fn_prod_scalaire_grad_prod(self,retour,**args):
    self.type_sdprod(retour,table_sdaster)
    return None
def macro_opti_sec_fn_prod_scalaire_grad_ops(self,retour,etat,grad1,grad2,**args):
    self.set_icmd(1)
    self.DeclareOut('retour',retour)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')
    
    val=0.
    for i in range(0,len(etat["GMASECTIONPOSSIBLE"])):
        val=val+grad1['R',i+1]*grad2['R',i+1]


    retour=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=val)));
    print "ok"
    return 0

macro_opti_sec_fn_prod_scalaire_grad= MACRO (nom="macro_opti_sec_fn_prod_scalaire_grad", op=macro_opti_sec_fn_prod_scalaire_grad_ops,
                   fr="Sauvegarde du champ", sd_prod=macro_opti_sec_fn_prod_scalaire_grad_prod,
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   retour               =SIMP(statut='o',typ=CO),
                   grad1		=SIMP(statut='o',typ=table_sdaster),
                   grad2		=SIMP(statut='o',typ=table_sdaster),
                   );


#fn_sauv_etat
def macro_opti_sec_fn_sauv_etat_ops(self,etat,text,**args):
    self.set_icmd(1)
    #self.DeclareOut('retour',self.sd)
    
    aster.affiche('MESSAGE',  "pas de sauvegarde du fichier etat "+text)
    aster.affiche('MESSAGE',  str(etat["CATALOGUE"].association))
    aster.affiche('RESULTAT',  "pas de sauvegarde du fichier etat "+text)
    aster.affiche('RESULTAT',  str(etat["CATALOGUE"].association))
    
    return 0

macro_opti_sec_fn_sauv_etat= MACRO (nom="macro_opti_sec_fn_sauv_etat", op=macro_opti_sec_fn_sauv_etat_ops,
                   fr="Sauvegarde du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   text		=SIMP(statut='f',typ=str,max='**'),
                   );

#fn_sauv_grad
def macro_opti_sec_fn_sauv_grad_ops(self,etat,gradient,text,**args):
    self.set_icmd(1)
    #self.DeclareOut('retour',self.sd)
    
    aster.affiche('MESSAGE',  "pas de sauvegarde du fichier gradient"+text)
    aster.affiche('RESULTAT',  "pas sauvegarde du fichier gradient"+text)
    IMPR_TABLE(TABLE=gradient)

    return 0

macro_opti_sec_fn_sauv_grad= MACRO (nom="macro_opti_sec_fn_sauv_grad", op=macro_opti_sec_fn_sauv_grad_ops,
                   fr="Sauvegarde du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   gradient		    =SIMP(statut='o',typ=table_sdaster),
                   text		=SIMP(statut='f',typ=str,max='**'),
                   );

def macro_opti_sec_fn_detruire_gradient_ops(self,gradient,**args):
    self.set_icmd(1)
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(gradient),),ALARME='NON');
    return 0
    
macro_opti_sec_fn_detruire_gradient= MACRO (nom="macro_opti_sec_fn_detruire_gradient", op=macro_opti_sec_fn_detruire_gradient_ops,
                   fr="destruction du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   gradient		=SIMP(statut='o',typ=table_sdaster),
                   );

def macro_opti_sec_fn_detruire_table_ops(self,table,**args):
    self.set_icmd(1)
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(table),),ALARME='NON');
    return 0
    
macro_opti_sec_fn_detruire_table= MACRO (nom="macro_opti_sec_fn_detruire_table", op=macro_opti_sec_fn_detruire_table_ops,
                   fr="destruction du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   table		=SIMP(statut='o',typ=table_sdaster),
                   );

def macro_opti_sec_fn_detruire_etat_ops(self,etat,**args):
    self.set_icmd(1)
    return 0
    #on ne fait rien l'etat est un objet python qui ce gere tout seul;
    
macro_opti_sec_fn_detruire_etat= MACRO (nom="macro_opti_sec_fn_detruire_etat", op=macro_opti_sec_fn_detruire_etat_ops,
                   fr="destruction du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   );


opti_sec=blind_opti.blind_opti(fn_evol=macro_opti_sec_fn_evol,
                fn_copy=None,fn_mult_grad=macro_opti_sec_fn_mult_grad,
                fn_update_grad=macro_opti_sec_fn_update_grad,fn_prod_scalaire_grad=macro_opti_sec_fn_prod_scalaire_grad,
                fn_sauv_etat=macro_opti_sec_fn_sauv_etat,fn_sauv_grad=macro_opti_sec_fn_sauv_grad,
                fn_smoothgrad=None,
                fn_detruire_etat=macro_opti_sec_fn_detruire_etat,
                fn_detruire_gradient=macro_opti_sec_fn_detruire_gradient,
                fn_detruire_table=macro_opti_sec_fn_detruire_table,
                )


###############################################################################
#utilitaire pre post tratement de l optimisation
#generation de groupe mail
def macro_opti_sec_gene_gr_ops(self,reuse,MAILLAGE,gr_ini,gr_cree,prefixe,**args):
    self.set_icmd(1)
    
    self.DeclareOut('MAILOUT',self.sd)


    mail_py=MAIL_PY();
    mail_py.FromAster(MAILLAGE);
    
    gr_cree['gr']=[]
    crea_gr=[]
    
    print "debug",mail_py.gma
    for gr in gr_ini['gr']:
        print "debug",gr
        for ma in mail_py.gma[gr]:
            crea_gr.append(_F(TYPE_MAILLE='1D',NOM="O"+str(ma+1),MAILLE='M'+str(ma+1)))
            gr_cree['gr'].append(prefixe+str(ma+1))

    MAILOUT=DEFI_GROUP(reuse=self.reuse,MAILLAGE=MAILLAGE,CREA_GROUP_MA=crea_gr)
    print "debug",gr_cree
    return 0

macro_opti_sec_gene_gr= MACRO (nom="macro_opti_sec_gene_gr", op=macro_opti_sec_gene_gr_ops,
                   fr="Creation de groupe pour chaque mail", sd_prod=maillage_sdaster,
                   reentrant='o',
                   reuse                =SIMP(statut='f',typ=maillage_sdaster),
                   MAILLAGE		=SIMP(statut='o',typ=maillage_sdaster),
                   gr_ini		    =SIMP(statut='o',typ=str,max='**'),
                   gr_cree		    =SIMP(statut='o',typ=str,max='**'),
                   prefixe		    =SIMP(statut='o',typ=str,max='**'),
                   );

#simplification de groupe mail
def macro_opti_sec_redu_gr_ops(self,reuse,MAILLAGE,gr_simpli,association,newassociation,**args):
    self.set_icmd(1)
    
    self.DeclareOut('MAILOUT',self.sd)


    mail_py=MAIL_PY();
    mail_py.FromAster(MAILLAGE);
    
    dico_gr={} #permet d inverser les groupe mail
    crea_gr=[]
    detr_gr=[]
    
    newassociation={}

    for k,v in association.iteritems():
        listma=[]
        for ma in mail_py.gma[k]:
            listma.append('M'+str(ma+1))
        if not (dico_gr.has_key(v)):
            dico_gr[v]=[]
        dico_gr[v].extend(listma)
        detr_gr.append(k)
    for k,v in dico_gr.iteritems():
        crea_gr.append(_F(TYPE_MAILLE='1D',NOM=k,MAILLE=v))
        newassociation[k]=[k]

    MAILOUT=DEFI_GROUP(reuse=self.reuse,MAILLAGE=MAILLAGE,CREA_GROUP_MA=crea_gr,DETR_GROUP_MA=_F(NOM=detr_gr))
    
    return 0

macro_opti_sec_redu_gr= MACRO (nom="macro_opti_sec_redu_gr", op=macro_opti_sec_redu_gr_ops,
                   fr="Reduction du nombre de groupe", sd_prod=maillage_sdaster,
                   reentrant='o',
                   reuse                =SIMP(statut='f',typ=maillage_sdaster),
                   MAILLAGE		=SIMP(statut='o',typ=maillage_sdaster),
                   gr_simpli		    =SIMP(statut='o',typ=str,max='**'),
                   association		    =SIMP(statut='o',typ=str,max='**'),
                   newassociation		    =SIMP(statut='o',typ=str,max='**'),
                   );



######################################
#fonctions contraintes

#pour memoire
####definition de letat
###
###etat={}
###etat["MAIL"]=MA
###etat["MODELE"]=MO
###etat["MATERIAU"]=MATR
###etat["CHAM_MATER"]=CHMAT
###etat["GMASECTIONPOSSIBLE"]=gmasection
###
####ce qui change a chaque foi
###etat["CATALOGUE"]=cata
###
###
#definition des parametre
####para={}
####para["CHARGE"]=CHARG charge applique
####para["sigmamax"]=140.e6 contrainte maximal admissible (pour prendre en compte le flambement)
####para["sigmamin"]=-220.e6 contrainte minimal admissible
####para["secdeltasigma"]=0.1 pourcentage d'augmentation entre chaque section
####para["pas_de_reduction"]=True determine si ce critere a le droit de reduire les sections (ne marche pas top)
####para["correction"]=50. degrade la note pour une section qui ne passe pas


#cas des contraintelocal
def macro_opti_sec_crit_contrainte_local_prod(self,gradient,valeur,**args):
    if (gradient!=None):
        if isinstance(gradient,CO):
            #print "macro_opti_sec_crit3_prod:grad"
            self.type_sdprod(gradient,table_sdaster)
    self.type_sdprod(valeur,table_sdaster)
    return None
def macro_opti_sec_crit_contrainte_local_ops(self,valeur,etat,gradient,fn_para,**args):
    self.set_icmd(1)
    self.DeclareOut('valeur',valeur)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')
    
    
    __CAREL=AFFE_CARA_ELEM(MODELE=etat["MODELE"],
                         INFO=1,
                         POUTRE=etat["CATALOGUE"].POUTRE()
                        )
    __Resu=MECA_STATIQUE(MODELE=etat["MODELE"],
                        CHAM_MATER=etat["CHAM_MATER"],
                        CARA_ELEM=__CAREL,
                        INST=0,
                        EXCIT=_F(CHARGE=fn_para["CHARGE"],),
                        );
    __Resu=CALC_ELEM(reuse =__Resu,
                 RESULTAT=__Resu,
                 TOUT_ORDRE='OUI',
                 OPTION=('SIPO_ELNO',))#SIGM_ELNO_DEPL
    
    #IMPR_RESU(FORMAT='MED',UNITE=80,RESU=_F(MAILLAGE=etat["MAIL"],RESULTAT=__Resu,),);
    
    __CH=CREA_CHAMP(OPERATION='EXTR',RESULTAT=__Resu,TYPE_CHAM='ELNO_SIEF_R',NOM_CHAM='SIPO_ELNO',INFO=1);
    sigmamax=fn_para["sigmamax"]
    sigmamin=fn_para["sigmamin"]
    tgradient=[]
    for gmaopti in etat["GMASECTIONPOSSIBLE"]:
        li=0
        if type(gmaopti[0])==str:
            li=[gmaopti[0]]
        else:
            li=list(gmaopti[0])
        CHTSN=__CH.EXTR_COMP('SN',li,1)
        CHTSMFY=__CH.EXTR_COMP('SMFY',li,1)
        CHTSMFZ=__CH.EXTR_COMP('SMFZ',li,1)
        deltasigma=[]
        for i in range(0,len(CHTSN.maille)):
            #pp comme positive positive
            PP=CHTSN.valeurs[i]+CHTSMFY.valeurs[i]+CHTSMFZ.valeurs[i]
            MP=CHTSN.valeurs[i]-CHTSMFY.valeurs[i]+CHTSMFZ.valeurs[i]
            PM=CHTSN.valeurs[i]+CHTSMFY.valeurs[i]-CHTSMFZ.valeurs[i]
            MM=CHTSN.valeurs[i]-CHTSMFY.valeurs[i]-CHTSMFZ.valeurs[i]
            #print gmaopti[0],i,PP,MP,PM,MM
            
            deltasigma.append(max(PP-sigmamax,MP-sigmamax,PM-sigmamax,MM-sigmamax,sigmamin-PP,sigmamin-MP,sigmamin-PM,sigmamin-MM))
        deltasigmamax=max(deltasigma)
        if fn_para["augmentationpure"]:
            deltasigmamax=max(deltasigmamax,0.)
        #print deltasigmamax
        #print fn_para["secdeltasigma"]
        tgradient.append(-deltasigmamax/fn_para["secdeltasigma"])
        #print tgradient
    
    valeurret=0.
    for a in tgradient:
        if (a<0):
            valeurret=valeurret-a*fn_para["correction"]
        else:
            valeurret=valeurret+a
    #modif ici
    
    #print etat["GMASECTIONPOSSIBLE"]
    #aster.affiche('RESULTAT', "tgradient"+str(tgradient))
    #aster.affiche('RESULTAT', str(valeurret))
    #print valeurret

    valeur=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=(valeurret,))));
    aster.affiche('MESSAGE',  'macro_opti_sec_crit_veriflocal:Valeur du retour c%f'%valeur["R",1])
    if (gradient==None):
        #print "macro_opti_sec_crit3_ops:no grad"
        return 0
    else:
        #print "macro_opti_sec_crit3_ops:grad"
        #print "test1"
        self.DeclareOut('gradient',gradient)
        #print "test2"
        gradient=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=tgradient)));
        #print "gradient['R',1]",gradient['R',1]
        return 0

macro_opti_sec_crit_contrainte_local= MACRO (nom="macro_opti_sec_crit_contrainte_local", op=macro_opti_sec_crit_contrainte_local_ops,
                   fr="Sauvegarde du champ", sd_prod=macro_opti_sec_crit_contrainte_local_prod,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   fn_para		    =SIMP(statut='o',typ=str,max='**'),
                   valeur		=SIMP(statut='o',typ=CO),
                   gradient		=SIMP(statut='f',typ=CO),
                   );


##############################################################
#cas de la verif local algo de type simp
def macro_opti_sec_crit_verif_local_prod(self,gradient,valeur,**args):
    if (gradient!=None):
        if isinstance(gradient,CO):
            #print "macro_opti_sec_crit3_prod:grad"
            self.type_sdprod(gradient,table_sdaster)
    self.type_sdprod(valeur,table_sdaster)
    return None
def macro_opti_sec_crit_verif_local_ops(self,valeur,etat,gradient,fn_para,**args):
    self.set_icmd(1)
    self.DeclareOut('valeur',valeur)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')
    
    
    __CAREL=AFFE_CARA_ELEM(MODELE=etat["MODELE"],
                         INFO=1,
                         POUTRE=etat["CATALOGUE"].POUTRE(),
                        )
    __Resu=MECA_STATIQUE(MODELE=etat["MODELE"],
                        CHAM_MATER=etat["CHAM_MATER"],
                        CARA_ELEM=__CAREL,
                        INST=0,
                        EXCIT=_F(CHARGE=fn_para["CHARGE"],),
                        );
    #__Resu=CALC_ELEM(reuse =__Resu,
    #             RESULTAT=__Resu,
    #             TOUT_ORDRE='OUI',
    #             OPTION=('SIEF_ELNO','SIPO_ELNO'))#SIGM_ELNO_DEPL
    
    #IMPR_RESU(FORMAT='MED',UNITE=80,RESU=_F(MAILLAGE=etat["MAIL"],RESULTAT=__Resu,),);
    #IMPR_RESU(FORMAT='RESULTAT',RESU=_F(MAILLAGE=etat["MAIL"],RESULTAT=__Resu,),);
    
    __CH=CREA_CHAMP(OPERATION='EXTR',RESULTAT=__Resu,TYPE_CHAM='ELGA_SIEF_R',NOM_CHAM='SIEF_ELGA',INFO=1);#ou ELGA ou ELNO?
    sigmamaxr=fn_para["sigmamax"] #r pour resistance et d pour design
    sigmaminr=fn_para["sigmamin"]
    tgradient=[]
    #on parcours tout les groupes a optimiser
    for gmaopti in etat["GMASECTIONPOSSIBLE"]:
        
        #on recupere tout les champs d'effort
        li=0
        if type(gmaopti[0])==str:
            li=[gmaopti[0]]
        else:
            li=list(gmaopti[0])
        CHTN=__CH.EXTR_COMP('N',li,1)
        CHTMFY=__CH.EXTR_COMP('MFY',li,1)
        CHTMFZ=__CH.EXTR_COMP('MFZ',li,1)
        
        #on recupere les caracteristique de la section courrante
        listesection=gmaopti[1]
        nomsecactuel=etat["CATALOGUE"].association[gmaopti[0]]
        #position de cette section dans la liste
        ii=listesection.index(nomsecactuel)
        
        section_cara=etat["CATALOGUE"].get_section_cara_from_sectionname(nomsecactuel)
        smaxd=0
        smind=0
        for i in range(0,len(CHTN.maille)):
            stress=etat["CATALOGUE"].section_cara_contrainte(section_cara,CHTN.valeurs[i],CHTMFY.valeurs[i],CHTMFZ.valeurs[i])
            smind=min(smind,stress[0])
            smaxd=max(smaxd,stress[1])
            #print "debug ini",ii
            #print gmaopti[0],i,CHTN.valeurs[i],CHTMFY.valeurs[i],CHTMFZ.valeurs[i]
            #print stress
        aa=0.
        if (smaxd>sigmamaxr or smind<sigmaminr):
            #print "debug section not ok"
            aa=1
        else:
            #print "debug section ok"
            aa=-1
        
        cont=True
        
        while (cont):
            if ii+aa>len(listesection)-1:
                cont=False
            elif ii+aa<0:
                aa=aa+1
                cont=False
            else:
                section_cara=etat["CATALOGUE"].get_section_cara_from_sectionname(listesection[ii+aa])
                smaxd=0
                smind=0
                for i in range(0,len(CHTN.maille)):
                    stress=etat["CATALOGUE"].section_cara_contrainte(section_cara,CHTN.valeurs[i],CHTMFY.valeurs[i],CHTMFZ.valeurs[i])
                    smind=min(smind,stress[0])
                    smaxd=max(smaxd,stress[1])
                #print "debug try",ii+aa
                #print gmaopti[0],smind,smaxd
                if aa>0:
                    if not(smaxd>sigmamaxr or smind<sigmaminr):
                        #print "debug trouve ok"
                        cont=False
                    else:
                        aa=aa+1
                else:
                    if (smaxd>sigmamaxr or smind<sigmaminr):
                        #print "debug trouve notok"
                        aa=aa+1
                        cont=False
                    else:
                        aa=aa-1

        tgradient.append(-aa)
        #print "debug fin aa=",aa
    
    valeurret=0.
    for a in tgradient:
        valeurret=valeurret-a
    #modif ici
    
    #print etat["GMASECTIONPOSSIBLE"]
    #aster.affiche('RESULTAT', "tgradient"+str(tgradient))
    #aster.affiche('RESULTAT', str(valeurret))
    #print valeurret

    valeur=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=(valeurret,))));
    aster.affiche('MESSAGE',  'macro_opti_sec_crit_verif_local:Valeur du retour c%f'%valeur["R",1])
    if (gradient==None):
        #print "macro_opti_sec_crit3_ops:no grad"
        return 0
    else:
        #print "macro_opti_sec_crit3_ops:grad"
        #print "test1"
        self.DeclareOut('gradient',gradient)
        #print "test2"
        gradient=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=tgradient)));
        #print "gradient['R',1]",gradient['R',1]
        return 0

macro_opti_sec_crit_verif_local= MACRO (nom="macro_opti_sec_crit_verif_local", op=macro_opti_sec_crit_verif_local_ops,
                   fr="Sauvegarde du champ", sd_prod=macro_opti_sec_crit_verif_local_prod,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   fn_para		    =SIMP(statut='o',typ=str,max='**'),
                   valeur		=SIMP(statut='o',typ=CO),
                   gradient		=SIMP(statut='f',typ=CO),
                   );



#cas de la masse total (materiaux identique partout)
def macro_opti_sec_crit_masse_prod(self,gradient,valeur,**args):
    if (gradient!=None):
        if isinstance(gradient,CO):
            #print "macro_opti_sec_crit3_prod:grad"
            self.type_sdprod(gradient,table_sdaster)
    self.type_sdprod(valeur,table_sdaster)
    return None
def macro_opti_sec_crit_masse_ops(self,valeur,etat,gradient,fn_para,**args):
    self.set_icmd(1)
    self.DeclareOut('valeur',valeur)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')
    
    
    __CAREL=AFFE_CARA_ELEM(MODELE=etat["MODELE"],
                         INFO=1,
                         POUTRE=etat["CATALOGUE"].POUTRE()
                        )
    __masse=POST_ELEM(MODELE=etat["MODELE"],CHAM_MATER=etat["CHAM_MATER"],CARA_ELEM=__CAREL,MASS_INER=_F(TOUT='OUI'))
    
    valeurret=__masse["MASSE",1]

    valeur=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=(valeurret,))));
    aster.affiche('MESSAGE',  'macro_opti_sec_crit_masse:Valeur du retour c%f'%valeur["R",1])
    if (gradient==None):
        return 0
    else:

        self.DeclareOut('gradient',gradient)

        tgradient=[]
        for gmaopti in etat["GMASECTIONPOSSIBLE"]:
            tgradient.append(1.)

        gradient=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=tgradient)));
        #print "gradient['R',1]",gradient['R',1]
        return 0

macro_opti_sec_crit_masse= MACRO (nom="macro_opti_sec_crit_masse", op=macro_opti_sec_crit_masse_ops,
                   fr="Sauvegarde du champ", sd_prod=macro_opti_sec_crit_masse_prod,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   fn_para		    =SIMP(statut='o',typ=str,max='**'),
                   valeur		=SIMP(statut='o',typ=CO),
                   gradient		=SIMP(statut='f',typ=CO),
                   );



#cas de l'energie elastique ou compliance
def macro_opti_sec_crit_compliance_prod(self,gradient,valeur,**args):
    if (gradient!=None):
        if isinstance(gradient,CO):
            #print "macro_opti_sec_crit3_prod:grad"
            self.type_sdprod(gradient,table_sdaster)
    self.type_sdprod(valeur,table_sdaster)
    return None
def macro_opti_sec_crit_compliance_ops(self,valeur,etat,gradient,fn_para,**args):
    self.set_icmd(1)
    self.DeclareOut('valeur',valeur)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')
    
    
    __CAREL=AFFE_CARA_ELEM(MODELE=etat["MODELE"],
                         INFO=1,
                         POUTRE=etat["CATALOGUE"].POUTRE()
                        )
    __Resu=MECA_STATIQUE(MODELE=etat["MODELE"],
                        CHAM_MATER=etat["CHAM_MATER"],
                        CARA_ELEM=__CAREL,
                        INST=0,
                        EXCIT=_F(CHARGE=fn_para["CHARGE"],),
                        );
    
    __tener=POST_ELEM(RESULTAT=__Resu,
                    MODELE=etat["MODELE"],
                    CHAM_MATER=etat["CHAM_MATER"],
                    CARA_ELEM=__CAREL,
                    ENER_POT=_F(TOUT='OUI'))
    valeurret=__tener['TOTALE',1]

    valeur=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=(valeurret,))));
    aster.affiche('MESSAGE',  'macro_opti_sec_crit_compliance:Valeur du retour c%f'%valeur["R",1])
    
    if (gradient==None):
        #print "macro_opti_sec_crit3_ops:no grad"
        return 0
    else:
        #print "macro_opti_sec_crit3_ops:grad"
        #print "test1"
        self.DeclareOut('gradient',gradient)
        
        
        __Resu=CALC_ELEM(reuse =__Resu,
                     RESULTAT=__Resu,
                     TOUT_ORDRE='OUI',
                     OPTION=('SIEF_ELNO','DEGE_ELNO'))#'EPSI_ELNO','EPSI_ELGA'))#SIGM_ELNO_DEPL
        
        
        __CHSIPO=CREA_CHAMP(OPERATION='EXTR',RESULTAT=__Resu,TYPE_CHAM='ELNO_SIEF_R',NOM_CHAM='SIEF_ELNO',INFO=1);
        __CHDEGE=CREA_CHAMP(OPERATION='EXTR',RESULTAT=__Resu,TYPE_CHAM='ELNO_EPSI_R',NOM_CHAM='DEGE_ELNO',INFO=1);
    
        __FE= FORMULE(NOM_PARA= ('N','EPXX','VY','GAXY','VZ','GAXZ','MT','GAT','MFY','KY','MFZ','KZ'),
                      VALE=("(N*EPXX+VY*GAXY+VZ*GAXZ+MT*GAT+MFY*KY+MFZ*KZ)/2."))
        __CHFE=CREA_CHAMP(OPERATION='AFFE',TYPE_CHAM='ELNO_NEUT_F', MODELE=etat["MODELE"],PROL_ZERO='OUI',
                        AFFE=_F(TOUT='OUI', NOM_CMP=('X1'),VALE_F=(__FE,)));
        
        __CHE=CREA_CHAMP( OPERATION='EVAL', TYPE_CHAM='ELNO_NEUT_R', CHAM_F=__CHFE, CHAM_PARA=(__CHSIPO,__CHDEGE));
        
        IMPR_RESU(FORMAT='MED',UNITE=80,RESU=_F(MAILLAGE=etat["MAIL"],CHAM_GD=__CHE,),);
        
        tgradient=[]
        for gmaopti in etat["GMASECTIONPOSSIBLE"]:
            CHTEN=0
            if type(gmaopti[0])==str:
                CHTEN=__CHE.EXTR_COMP('X1',[gmaopti[0]],1)
            else:
                CHTEN=__CHE.EXTR_COMP('X1',list(gmaopti[0]),1)
            Emoy=0
            if (len(CHTEN.valeurs)>0):
                Emoy=sum(CHTEN.valeurs)/len(CHTEN.valeurs)
                
            tgradient.append(Emoy)
            #print tgradient
        #print tgradient
        #print sum(tgradient)/len(tgradient)
        #print valeurret

        gradient=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=tgradient)));
        #print "gradient['R',1]",gradient['R',1]
        return 0

macro_opti_sec_crit_compliance= MACRO (nom="macro_opti_sec_crit_compliance", op=macro_opti_sec_crit_compliance_ops,
                   fr="Sauvegarde du champ", sd_prod=macro_opti_sec_crit_compliance_prod,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   fn_para		    =SIMP(statut='o',typ=str,max='**'),
                   valeur		=SIMP(statut='o',typ=CO),
                   gradient		=SIMP(statut='f',typ=CO),
                   );
