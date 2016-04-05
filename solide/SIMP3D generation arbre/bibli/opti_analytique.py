#opti_analytique.py
#permet de parametrer blind_opti pour des tests analytiques depuis CA
#########################################################
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

#simple test analytique


#bibli_dir='/home/fred/asteretude/blindopti/bibli'
#import sys
##importation du catalogue
#sys.path.append(bibli_dir)
import blind_opti


from Cata.cata import *
from Accas import _F

##########################
#fonction support
#fn_evol
#def macro_opti_ana_fn_evol_prod(self,**args):
#        return table_sdaster
def macro_opti_ana_fn_evol_ops(self,etat,newetat,gradient,alpha,**args):
    self.set_icmd(1)
    #self.DeclareOut('retour',self.sd)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')

    _retour=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=(etat['valeurs']['R',1]+alpha*gradient['R',1],etat['valeurs']['R',2]+alpha*gradient['R',2]))));
    newetat['valeurs']=_retour
    return 0
macro_opti_ana_fn_evol= MACRO (nom="macro_opti_ana_fn_evol", op=macro_opti_ana_fn_evol_ops,
                   fr="Sauvegarde du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   newetat		    =SIMP(statut='o',typ=str,max='**'),
                   gradient		=SIMP(statut='o',typ=table_sdaster),
                   alpha		=SIMP(statut='o',typ='R'),
                   );

#fn_update_grad
def macro_opti_ana_fn_update_grad_prod(self,retour,**args):
    self.type_sdprod(retour,table_sdaster)
    return None
def macro_opti_ana_fn_update_grad_ops(self,retour,grad1,alpha,grad2,**args):
    self.set_icmd(1)
    self.DeclareOut('retour',retour)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')

    retour=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=(grad1['R',1]+alpha*grad2['R',1],grad1['R',2]+alpha*grad2['R',2]))));
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(grad1),),ALARME='NON');
    return 0

macro_opti_ana_fn_update_grad= MACRO (nom="macro_opti_ana_fn_update_grad", op=macro_opti_ana_fn_update_grad_ops,
                   fr="Sauvegarde du champ", sd_prod=macro_opti_ana_fn_update_grad_prod,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   retour               =SIMP(statut='o',typ=CO),
                   grad1		=SIMP(statut='o',typ=table_sdaster),
                   grad2		=SIMP(statut='o',typ=table_sdaster),
                   alpha		=SIMP(statut='f',typ='R'),
                   );

#fn_mult_grad
def macro_opti_ana_fn_mult_grad_prod(self,retour,**args):
    self.type_sdprod(retour,table_sdaster)
    return None
def macro_opti_ana_fn_mult_grad_ops(self,retour,gradient,alpha,**args):
    self.set_icmd(1)
    self.DeclareOut('retour',retour)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')

    retour=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=(alpha*gradient['R',1],alpha*gradient['R',2]))));
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(gradient),),ALARME='NON');
    return 0

macro_opti_ana_fn_mult_grad= MACRO (nom="macro_opti_ana_fn_mult_grad", op=macro_opti_ana_fn_mult_grad_ops,
                   fr="Sauvegarde du champ", sd_prod=macro_opti_ana_fn_mult_grad_prod,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   retour               =SIMP(statut='o',typ=CO),
                   gradient		=SIMP(statut='o',typ=table_sdaster),
                   alpha		=SIMP(statut='f',typ='R'),
                   );


#fn_prod_scalaire_grad

def macro_opti_ana_fn_prod_scalaire_grad_prod(self,retour,**args):
    self.type_sdprod(retour,table_sdaster)
    return None
def macro_opti_ana_fn_prod_scalaire_grad_ops(self,retour,etat,grad1,grad2,**args):
    self.set_icmd(1)
    self.DeclareOut('retour',retour)
    CREA_TABLE	= self.get_cmd('CREA_TABLE')

    retour=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=(grad1['R',1]*grad2['R',1]+grad1['R',2]*grad2['R',2]))));
    print "ok"
    return 0

macro_opti_ana_fn_prod_scalaire_grad= MACRO (nom="macro_opti_ana_fn_prod_scalaire_grad", op=macro_opti_ana_fn_prod_scalaire_grad_ops,
                   fr="Sauvegarde du champ", sd_prod=macro_opti_ana_fn_prod_scalaire_grad_prod,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   retour               =SIMP(statut='o',typ=CO),
                   grad1		=SIMP(statut='o',typ=table_sdaster),
                   grad2		=SIMP(statut='o',typ=table_sdaster),
                   );


#fn_sauv_etat
def macro_opti_ana_fn_sauv_etat_ops(self,etat,text,**args):
    self.set_icmd(1)
    #self.DeclareOut('retour',self.sd)
    aster.affiche('MESSAGE',  text+' (%f;%f)'%(etat['valeurs']["R",1],etat['valeurs']["R",2]))
    aster.affiche('RESULTAT',  text+' (%f;%f)'%(etat['valeurs']["R",1],etat['valeurs']["R",2]))
    #retour=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=(grad1['R',1]*grad2['R',1]+grad1['R',2]*grad2['R',2]))));
    return 0

macro_opti_ana_fn_sauv_etat= MACRO (nom="macro_opti_ana_fn_sauv_etat", op=macro_opti_ana_fn_sauv_etat_ops,
                   fr="Sauvegarde du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   text		=SIMP(statut='f',typ=str,max='**'),
                   );

#fn_sauv_grad
def macro_opti_ana_fn_sauv_grad_ops(self,etat,gradient,text,**args):
    self.set_icmd(1)
    #self.DeclareOut('retour',self.sd)
    aster.affiche('MESSAGE',  text+' (%f;%f)'%(gradient["R",1],gradient["R",2]))
    aster.affiche('RESULTAT',  text+' (%f;%f)'%(gradient["R",1],gradient["R",2]))
    #retour=CREA_TABLE(LISTE=(	_F(PARA='R',LISTE_R=(grad1['R',1]*grad2['R',1]+grad1['R',2]*grad2['R',2]))));
    return 0

macro_opti_ana_fn_sauv_grad= MACRO (nom="macro_opti_ana_fn_sauv_grad", op=macro_opti_ana_fn_sauv_grad_ops,
                   fr="Sauvegarde du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   gradient		    =SIMP(statut='o',typ=table_sdaster),
                   text		=SIMP(statut='f',typ=str,max='**'),
                   );

def macro_opti_ana_fn_detruire_gradient_ops(self,gradient,**args):
    self.set_icmd(1)
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(gradient),),ALARME='NON');
    
macro_opti_ana_fn_detruire_gradient= MACRO (nom="macro_opti_ana_fn_detruire_gradient", op=macro_opti_ana_fn_detruire_gradient_ops,
                   fr="destruction du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   gradient		=SIMP(statut='o',typ=table_sdaster),
                   );

def macro_opti_ana_fn_detruire_table_ops(self,table,**args):
    self.set_icmd(1)
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(table),),ALARME='NON');
    
macro_opti_ana_fn_detruire_table= MACRO (nom="macro_opti_ana_fn_detruire_table", op=macro_opti_ana_fn_detruire_table_ops,
                   fr="destruction du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   table		=SIMP(statut='o',typ=table_sdaster),
                   );

def macro_opti_ana_fn_detruire_etat_ops(self,etat,**args):
    self.set_icmd(1)
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(etat['valeurs']),),ALARME='NON');
    
macro_opti_ana_fn_detruire_etat= MACRO (nom="macro_opti_ana_fn_detruire_etat", op=macro_opti_ana_fn_detruire_etat_ops,
                   fr="destruction du champ", sd_prod=None,
                   #MAIL		=SIMP(statut='o',typ=maillage_sdaster),
                   etat		    =SIMP(statut='o',typ=str,max='**'),
                   );


#creation de l objet d optimisation
opti_analytique=blind_opti.blind_opti(fn_evol=macro_opti_ana_fn_evol,
                fn_copy=None,fn_mult_grad=macro_opti_ana_fn_mult_grad,
                fn_update_grad=macro_opti_ana_fn_update_grad,fn_prod_scalaire_grad=macro_opti_ana_fn_prod_scalaire_grad,
                fn_sauv_etat=macro_opti_ana_fn_sauv_etat,fn_sauv_grad=macro_opti_ana_fn_sauv_grad,
                fn_smoothgrad=None,
                fn_detruire_etat=macro_opti_ana_fn_detruire_etat,
                fn_detruire_gradient=macro_opti_ana_fn_detruire_gradient,
                fn_detruire_table=macro_opti_ana_fn_detruire_table,
                )
