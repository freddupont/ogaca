#orientation_poutre_beta.py
#definis des macros qui genere un fichier med avec lorientation des poutres
#V2
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


try :
    from Cata.cata import *
    from Accas import _F
except :
    print "i"*40
    print 'Fonctionnalites Aster indisponibles'
    print 'orientation_poutre non disponible'
    print "i"*40



import numpy

def orientation_poutre_vy(GROUP_MA,MAILLAGE,MODELE,CARA_ELEM,CHAM_MATER,UNITE=80,SAUVEGARDE_CHAMP=True,RETOUR_TABLE=False,):
    """cree un fichier contenant un champs de l orientation local des poutres
    usage: orientation_poutre_vy(GROUP_MA,MAILLAGE,MODELE,CARA_ELEM,MATE,UNITE=80)
    """
    ######################################################
    #Champ local Y des poutres
    __CHVY=CREA_CHAMP(OPERATION='AFFE',TYPE_CHAM='ELNO_SIEF_R', MODELE=MODELE,PROL_ZERO='OUI',
                    AFFE=_F(GROUP_MA=GROUP_MA, NOM_CMP=('VY'),VALE=1.));
    __VYinst0=CREA_RESU(OPERATION='AFFE',
                     TYPE_RESU='EVOL_ELAS',
                     NOM_CHAM='SIEF_ELNO',
                     AFFE=_F(CHAM_GD=__CHVY,INST=-1)
                     )
    __DEPL=CREA_CHAMP(OPERATION='AFFE',TYPE_CHAM='NOEU_DEPL_R', MODELE=MODELE,PROL_ZERO='OUI',
                    AFFE=_F(TOUT='OUI', NOM_CMP=('DY'),VALE=1.));
    __VYinst0=CREA_RESU(reuse=__VYinst0,
                     OPERATION='AFFE',
                     TYPE_RESU='EVOL_ELAS',
                     NOM_CHAM='DEPL',
                     AFFE=_F(CHAM_GD=__DEPL,INST=-1)
                     )
    __VYinst0=CALC_ELEM(reuse =__VYinst0,
                   RESULTAT=__VYinst0,
                   MODELE=MODELE,
                   CHAM_MATER=CHAM_MATER,
                   CARA_ELEM=CARA_ELEM,
                   OPTION=('EFCA_ELNO'),);
    if (SAUVEGARDE_CHAMP):
	IMPR_RESU(FORMAT='MED',UNITE=UNITE,RESU=_F(MAILLAGE=MAILLAGE,RESULTAT=__VYi0,NOM_CHAM='EFCA_ELNO',),);
    if (RETOUR_TABLE):
        __CH=CREA_CHAMP(OPERATION='EXTR',RESULTAT=__VYinst0,TYPE_CHAM='ELNO_SIEF_R',NOM_CHAM='EFCA_ELNO',);
        #creation d un groupe contenant les noeuds hors du domaine
        __CHTX=__CH.EXTR_COMP('FX',[],1)
        __CHTY=__CH.EXTR_COMP('FY',[],1)
        __CHTZ=__CH.EXTR_COMP('FZ',[],1)
        
        inversionmail={}
        #output={}
        for i in range(0,len(__CHTX.maille)):
            if not(inversionmail.has_key(__CHTX.maille[i])):
                inversionmail[__CHTX.maille[i]]=[i]
                #output[__CHTX.maille[i]]=[__CHTX.valeurs[i]]
        for i in range(0,len(__CHTY.maille)):
            if inversionmail.has_key(__CHTY.maille[i]):
                if (len(inversionmail[__CHTY.maille[i]])==1):
                    inversionmail[__CHTY.maille[i]].append(i)
        for i in range(0,len(__CHTZ.maille)):
            if inversionmail.has_key(__CHTZ.maille[i]):
                if (len(inversionmail[__CHTZ.maille[i]])==2):
                    inversionmail[__CHTZ.maille[i]].append(i)
        
        output={}
        for k,v in inversionmail.iteritems():
            output[k]=numpy.array([__CHTX.valeurs[v[0]],__CHTY.valeurs[v[1]],__CHTZ.valeurs[v[2]]])
            assert(v[0]==v[1] and v[2]==v[1])
            
                
        #print "/n"*10
        #print __CHTX.__dict__;
        #print __CHTY.__dict__;
        #print __CHTZ.__dict__;
        #print inversionmail
        #print output
        DETRUIRE(INFO=1,CONCEPT=_F(NOM=(__CH),));
        DETRUIRE(INFO=1,CONCEPT=_F(NOM=(__CHVY,__VYinst0,__DEPL),));
        return output;
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(__CHVY,__VYinst0,__DEPL),));
    
def orientation_poutre_vyz(GROUP_MA,MAILLAGE,MODELE,CARA_ELEM,CHAM_MATER,UNITE=80,SAUVEGARDE_CHAMP=True,RETOUR_TABLE=False,):
    """cree un fichier contenant un champs de l orientation local des poutres
    usage: orientation_poutre_vyz(GROUP_MA,MAILLAGE,MODELE,CARA_ELEM,CHAM_MATER,UNITE=80)
    """
    ######################################################
    #Champ local des poutres
    __CHVY=CREA_CHAMP(OPERATION='AFFE',TYPE_CHAM='ELNO_SIEF_R', MODELE=MODELE,PROL_ZERO='OUI',
                    AFFE=_F(GROUP_MA=GROUP_MA, NOM_CMP=('VY'),VALE=1.));
    __CHVZ=CREA_CHAMP(OPERATION='AFFE',TYPE_CHAM='ELNO_SIEF_R', MODELE=MODELE,PROL_ZERO='OUI',
                    AFFE=_F(GROUP_MA=GROUP_MA, NOM_CMP=('VZ'),VALE=1.));
    __Y0_Z1=CREA_RESU(OPERATION='AFFE',
                     TYPE_RESU='EVOL_ELAS',
                     NOM_CHAM='SIEF_ELNO',
                     AFFE=_F(CHAM_GD=__CHVY,INST=0)
                     )
    __Y0_Z1=CREA_RESU(reuse=__Y0_Z1,
                     OPERATION='AFFE',
                     TYPE_RESU='EVOL_ELAS',
                     NOM_CHAM='SIEF_ELNO',
                     AFFE=_F(CHAM_GD=__CHVZ,INST=1)
                     )
    __DEPL=CREA_CHAMP(OPERATION='AFFE',TYPE_CHAM='NOEU_DEPL_R', MODELE=MODELE,PROL_ZERO='OUI',
                    AFFE=_F(TOUT='OUI', NOM_CMP=('DY'),VALE=1.));
    __Y0_Z1=CREA_RESU(reuse=__Y0_Z1,
                     OPERATION='AFFE',
                     TYPE_RESU='EVOL_ELAS',
                     NOM_CHAM='DEPL',
                     AFFE=_F(CHAM_GD=__DEPL,INST=0)
                     )
    __Y0_Z1=CREA_RESU(reuse=__Y0_Z1,
                     OPERATION='AFFE',
                     TYPE_RESU='EVOL_ELAS',
                     NOM_CHAM='DEPL',
                     AFFE=_F(CHAM_GD=__DEPL,INST=1)
                     )
    
    __Y0_Z1=CALC_ELEM(reuse =__Y0_Z1,
                   RESULTAT=__Y0_Z1,
                   MODELE=MODELE,
                   GROUP_MA=GROUP_MA,
                   CHAM_MATER=CHAM_MATER,
                   CARA_ELEM=CARA_ELEM,
                   OPTION=('EFCA_ELNO'),);
    if (SAUVEGARDE_CHAMP):
        IMPR_RESU(FORMAT='MED',UNITE=UNITE,RESU=_F(MAILLAGE=MAILLAGE,RESULTAT=__Y0_Z1,NOM_CHAM='EFCA_ELNO',),);
    if (RETOUR_TABLE):
        #premier traitement pour y
        __CH=CREA_CHAMP(OPERATION='EXTR',RESULTAT=__Y0_Z1,TYPE_CHAM='ELNO_SIEF_R',NOM_CHAM='EFCA_ELNO',INST=0);
        #creation d un groupe contenant les noeuds hors du domaine
        __CHTX=__CH.EXTR_COMP('FX',[],1)
        __CHTY=__CH.EXTR_COMP('FY',[],1)
        __CHTZ=__CH.EXTR_COMP('FZ',[],1)
        
        inversionmail={}
        #output={}
        for i in range(0,len(__CHTX.maille)):
            if not(inversionmail.has_key(__CHTX.maille[i])):
                inversionmail[__CHTX.maille[i]]=[i]
                #output[__CHTX.maille[i]]=[__CHTX.valeurs[i]]
        for i in range(0,len(__CHTY.maille)):
            if inversionmail.has_key(__CHTY.maille[i]):
                if (len(inversionmail[__CHTY.maille[i]])==1):
                    inversionmail[__CHTY.maille[i]].append(i)
        for i in range(0,len(__CHTZ.maille)):
            if inversionmail.has_key(__CHTZ.maille[i]):
                if (len(inversionmail[__CHTZ.maille[i]])==2):
                    inversionmail[__CHTZ.maille[i]].append(i)
        
        output={}
        for k,v in inversionmail.iteritems():
            output[k-1]=[numpy.array([__CHTX.valeurs[v[0]],__CHTY.valeurs[v[1]],__CHTZ.valeurs[v[2]]])]
            assert(v[0]==v[1] and v[2]==v[1])
        DETRUIRE(INFO=1,CONCEPT=_F(NOM=(__CH),));
        
        #on fait le meme traitement pour z
        __CH=CREA_CHAMP(OPERATION='EXTR',RESULTAT=__Y0_Z1,TYPE_CHAM='ELNO_SIEF_R',NOM_CHAM='EFCA_ELNO',INST=1);
        #creation d un groupe contenant les noeuds hors du domaine
        __CHTX=__CH.EXTR_COMP('FX',[],1)
        __CHTY=__CH.EXTR_COMP('FY',[],1)
        __CHTZ=__CH.EXTR_COMP('FZ',[],1)
        
        
        inversionmail={}
        #output={}
        for i in range(0,len(__CHTX.maille)):
            if not(inversionmail.has_key(__CHTX.maille[i])):
                inversionmail[__CHTX.maille[i]]=[i]
                #output[__CHTX.maille[i]]=[__CHTX.valeurs[i]]
        for i in range(0,len(__CHTY.maille)):
            if inversionmail.has_key(__CHTY.maille[i]):
                if (len(inversionmail[__CHTY.maille[i]])==1):
                    inversionmail[__CHTY.maille[i]].append(i)
        for i in range(0,len(__CHTZ.maille)):
            if inversionmail.has_key(__CHTZ.maille[i]):
                if (len(inversionmail[__CHTZ.maille[i]])==2):
                    inversionmail[__CHTZ.maille[i]].append(i)
        
        for k,v in inversionmail.iteritems():
            output[k-1].append(numpy.array([__CHTX.valeurs[v[0]],__CHTY.valeurs[v[1]],__CHTZ.valeurs[v[2]]]))
            assert(v[0]==v[1] and v[2]==v[1])

                
        #print "/n"*10
        #print __CHTX.__dict__;
        #print __CHTY.__dict__;
        #print __CHTZ.__dict__;
        #print inversionmail
        #print output
        DETRUIRE(INFO=1,CONCEPT=_F(NOM=(__CH),));
        DETRUIRE(INFO=1,CONCEPT=_F(NOM=(__CHVY,__CHVZ,__Y0_Z1,__DEPL),));
        return output;
    DETRUIRE(INFO=1,CONCEPT=_F(NOM=(__CHVY,__CHVZ,__Y0_Z1,__DEPL),));

