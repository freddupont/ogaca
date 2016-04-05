#Class blind_opti
#realise une otimisation sur un element de dimention infine seul f et f' sont connue
#V1
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

import aster
from Cata.cata import *

import math
import numpy
print "numpy.version.version",numpy.version.version

#def power(x):
#    print "power x:",x
#    return (x-4)**4+5*x**2;
#def derpower(x):
#    print "derpower x:",x
#    return 4*(x-4)**3+10*x;

#from scipy.optimize import fmin,brent,fmin_cobyla
#from scipy.optimize import fmin_cobyla
#
#
##def simpleobj(x):
#                             return x[0]**2+x[1]**2;
#def simpleconstrain(x):
#                             return (x[0]**2+x[1]**2)-3;
#
#print "cobyla"
#out=fmin_cobyla(simpleobj, [0.0, 0.1], [simpleconstrain],maxfun=3)
#print out

#from scipy.optimize import brent,line_search
#import scipy.version 
#print "scipy.version.version",scipy.version.version
##test of brent (minimise for scalaire)
#                             
#(a,b,c,d)=brent(power,brack=[0,1],full_output=True);
##(xmin,fmin,nbiter,nbeval)
#print "xmin value"
#print a
#print "fmin value"
#print b
#print "nb iter"
#print c
#print "nb eval"
#print d

import scalarsearch
#a=scalarsearch.brent(power,brack=[0,1],full_output=True);
#print "scalarsearch.brent",a
#from scalarsearch import scalar_search_wolfe2,scalar_search_armijo
#
####test of scalar_search_wolfe2
#a=scalar_search_wolfe2(phi=power,phi0=256.,derphi=derpower)
#print "wolfe2 result",a
##does not work without derphi
#
#a=scalar_search_armijo(phi=power,phi0=256.,derphi0=-64.)
#print "armijo result",a

class barriere_fred:
    """
    classe barriere ecrite par fred
    elle doit retourner les valeurs suivantes
    valeur(real) qui retourne la barriere
    derive(real)
    integral(real)
    """
    def __init__(self,ncon,err_con):
        self.ncon=ncon
        self.err_con=err_con
        self.beta1=((1+ncon)*(1+err_con)-1)/(1-(1+ncon))
        self.beta2=(self.beta1+1)/(self.beta1)
        self.beta3=-(self.beta1+1)*math.log(-self.beta1-1)+self.beta2/2.
        self.beta4=(self.beta1+1)*(math.log(-self.beta1-err_con-1))-self.beta2*(-((1+err_con)**2)/2.+(1+err_con))-self.beta3-(2+self.beta2)*(1+err_con)-((1+err_con)**2)/2.
    def valeur(self,val):
        c=val+1.
        if (c<(1+self.ncon)):
            return (self.beta1+1)/(c+self.beta1)-self.beta2*(1-c)
        else:
            return 2+c+self.beta2
    def derive(self,val):
        c=val+1.
        if (c<(1+self.ncon)):
            return -(self.beta1+1)/(c+self.beta1)**2-self.beta2
        else:
            return 1
    def intergal(self,val):
        c=val+1.
        if (c<(1+self.ncon)):
            return -(self.beta1+1)*math.log(-c-self.beta1)-self.beta2*(c-(c**2)/2.)+self.beta3
        else:
            return (2+self.beata2)*c+(c**2)/2.+self.beata4

class barriere_vide:
    """
    classe barriere vide
    elle doit retourner les valeurs suivantes
    valeur(real) qui retourne la barriere
    derive(real)
    integral(real)
    """
    def valeur(self,val):
        return val
    def derive(self,val):
        return 1
    def intergal(self,val):
        return val**2/2

class barriere_log:
    """
    classe barriere log
    elle doit retourner les valeurs suivantes
    valeur(real) qui retourne la barriere
    derive(real)
    integral(real)
    """
    def __init__(self,seuil=0.5):
        assert (seuil<1.)
        self.seuil=seuil
        self.c2=1/(1-seuil)-2*seuil
        self.c1=math.log(1.-seuil)-seuil**2-self.c2*seuil
    def valeur(self,val):
        print "vallog",val
        if (val>self.seuil):
            print val**2+self.c1+self.c2*val
            return val**2+self.c1+self.c2*val
        print -math.log(-val+1)
        return -math.log(-val+1)
    def derive(self,val):
        if (val>self.seuil):
            return 2*val+self.c2
        return 1/(-val+1)
    def intergal(self,val):
        return 1


class blind_opti:
    def __init__(self,fn_evol,fn_copy,fn_mult_grad,fn_update_grad,
                 fn_prod_scalaire_grad,fn_sauv_etat,fn_sauv_grad,fn_smoothgrad,
                 fn_detruire_etat,fn_detruire_gradient,fn_detruire_table,class_barriere=None):
        """
        definition des operations specifique a cette optimisation
        """
        
            
        self.fn_evol=fn_evol
        """
            Format (etat,newetat,gradient,alpha)
            Retourne un nouvel etat: newetat= (etat+alpha*gradient)
            doit etre initialise comme suit
                newetat={}
                newetat['ini']=0
        """
        
        self.fn_mult_grad=fn_mult_grad
        """
            format fn_update_grad(etat,retour,grad1,alpha)
            detruit grad1 et retourne grad1*alpha
        """
        
        self.fn_update_grad=fn_update_grad
        """
            format fn_update_grad(etat,retour,grad1,alpha,grad2)
            detruit grad1 et retourne grad1+alpha*grad2
        """
            
        #self.fn_copy=fn_copy
        self.fn_prod_scalaire_grad=fn_prod_scalaire_grad
        """
            format table=fn_prod_scalaire_grad(etat,grad1,grad2)
            retourne le produit scalaire de grad1 et grad2
        """
        self.fn_sauv_grad=fn_sauv_grad
        self.fn_sauv_etat=fn_sauv_etat
        """
            format fn_sauv_etat(etat,i)
            sauvegarde l etat 
        """
        self.fn_detruire_etat=fn_detruire_etat
        """
            fn_detruire_etat(etat)
            purge la memoire de l etat
        """
        self.fn_detruire_gradient=fn_detruire_gradient
        """
            fn_detruire_gradient(gradient)
            purge la memoire du gradient
        """
        self.fn_detruire_table=fn_detruire_table
        self.fn_smoothgrad=None
        self.class_barriere=class_barriere
        self.chemin_de_sauvegarde=''
        
    def __evol_et_eval(self,pas,etat,gradient):
        print "__evol_et_eval",pas
        if type(pas)==list:pas=pas[0]
        if (pas==0.):
            return self.obji
        tempetat={}
        tempetat["i"]=0.
        self.fn_evol(etat=etat,newetat=tempetat,gradient=gradient,alpha=pas)
        #ajouter un teste ici en cas d echec de l evolution
        
        b=[]
        for a in range(0,len(self.tab_fn_contrainte)):
            b.append(1.)
        
        
        obji=0
        for k in range(0,len(self.tab_fn_contrainte)):
            if (k==0):
                objtemp=CO('objtemp')
                self.tab_fn_contrainte[k][0](etat=tempetat,valeur=objtemp,fn_para=self.tab_fn_contrainte[k][1])
                obji=objtemp['R',1]
                self.fn_detruire_table(table=objtemp)
            else:
                objk=CO('objk')
                self.tab_fn_contrainte[k][0](etat=tempetat,valeur=objk,fn_para=self.tab_fn_contrainte[k][1])
                        
                if (self.class_barriere!=None):
                    b[k]=self.class_barriere.valeur(objk['R',1])
                else:
                    b[k]=objk['R',1]
                
                obji=obji+b[k]*self.adapt_coef[k]
                self.fn_detruire_table(table=objk)
        aster.affiche('RESULTAT',"   evol et eval alpha=%f retour%f etat:"%(pas,obji))
        self.fn_detruire_etat(etat=tempetat)
        return obji
    
    def __evol_et_eval_avec_der(self,pas,etat,gradient):
        print "__evol_et_eval_avec_der",pas
        if type(pas)==list:pas=pas[0]
        if (pas==0.):
            return self.obji
        tempetat={}
        tempetat["i"]=0.
        self.fn_evol(etat=etat,newetat=tempetat,gradient=gradient,alpha=pas)
        #ajouter un teste ici en cas d echec de l evolution
        
        b=[]
        for a in range(0,len(self.tab_fn_contrainte)):
            b.append(1.)
        
        obji=0
        for k in range(0,len(self.tab_fn_contrainte)):
            objtemp=objtemp=CO('objtemp')
            objkval=0.
            
            if (k==0):
                
                gradj=CO('gradj')
                self.tab_fn_contrainte[k][0](etat=etat_courrant,valeur=objtemp,gradient=gradj,fn_para=self.tab_fn_contrainte[k][1])
                objkval=objtemp['R',1]
                self.fn_detruire_table(table=objtemp)
                
                obji=objkval

                #on vas dans la direction oppose a celle indique par le gradient 
                gradineg=CO('gradjneg')
                self.fn_mult_grad(etat=etat_courrant,retour=gradjneg,gradient=gradj,alpha=-1.)
                gradj=gradjneg
                    #gradi=self.__normalise_grad(etat=etat_courrant,gradient=gradi)
            else:
                gradjk=CO('gradjk')
                self.tab_fn_contrainte[k][0](etat=etat_courrant,valeur=objtemp,gradient=gradjk,fn_para=self.tab_fn_contrainte[k][1])
                objkval=objtemp['R',1]
                self.fn_detruire_table(table=objtemp)
                
                if (self.class_barriere!=None):
                    derb[k]=self.class_barriere.derive(objkval)
                    b[k]=self.class_barriere.valeur(objkval)
                else:
                    b[k]=objkval
                    
                obji=obji+self.adapt_coef[k]*b[k]
                
                gijkn=CO('gijk%d'%k)
                #self.fn_sauv_etat(etat=etat_courrant,text=" "*10+"sauvegarde etat")
                #self.fn_sauv_grad(etat=etat_courrant,gradient=gradj,text=" "*10+"sauvegarde gradi avant mise a jour")
                out=" "*10+"sauvegarde gradk adapt:%f, derb:%f"%(self.adapt_coef[k],derb[k])
                aster.affiche('RESULTAT',out)
                self.fn_update_grad(etat=etat_courrant,retour=gijkn,grad1=gradj,grad2=gradjk,alpha=-self.adapt_coef[k]*derb[k])
                gradj=gijkn
                #self.fn_sauv_grad(etat=etat_courrant,gradient=gradj,text=" "*10+"sauvegarde gradi")
                
                self.fn_detruire_gradient(gradient=gradjk)

        a=CO('a')
        #print "gradi=gradient",gradient['R',1]
        self.fn_prod_scalaire_grad(etat=tempetat,retour=a,grad1=gradient,grad2=gradi)
        der=a['R',1]
        self.fn_detruire_table(table=a)

        aster.affiche('RESULTAT',"   sauvegarde evol et eval et der alpha=%f retour(%f,%f) etat:"%(pas,obji,der))
        
        self.fn_detruire_etat(etat=tempetat)
        return obji,der
    
    def __normalise_grad(self,etat,retour,gradient):
        
        a=CO('a')
        #print "gradi=gradient",gradient['R',1]
        self.fn_prod_scalaire_grad(etat=etat,retour=a,grad1=gradient,grad2=gradient)
        ae=math.sqrt(a['R',1])
        self.fn_detruire_table(table=a)
        
        if (ae!=0.):
            #print "__normalise_grad avant:",gradient['R',1]," ",gradient['R',2]
            #print " prod scalaire: ae",ae
            self.fn_mult_grad(etat=etat,retour=retour,gradient=gradient,alpha=1./ae)
            #print "__normalise_grad apres", retour['R',1], " ", retour['R',2]
        else:
            retour=gradient
    
    def descente_gradient(self,tab_fn_contrainte,etat_init,nb_pas,pas_init,
                          adaptative_penality=False,adaptative_penality_beta1=1.6,
                          adaptative_penality_beta2=1.4,adaptative_penality_nb_iter=3,adaptative_penality_coef=[],
                          residu=10-3,pas_mini=0.01,normalise=False,normalise_iteration=False,
                          pas_optimal=None,pas_optimal_nb_brent_iter=5):
        
        self.tab_fn_contrainte=tab_fn_contrainte
        """
            la premiere fn_contrainte est l'objectif
            chaque fn contrainte est une class qui possede la proprietes suivantes
            (etat,gradient=CO(out),fn_para)
            on ne peut utiliser les propriete de classe que par l'ajout de .opti_vale=[]
            qui retourne la valeur de la fonction et le gradient si (out) est fournis
            gradient est toujours un objet aster (table ou champ)
            etat est toujours un dictionnaire
            
            a la fin toute les fonction contrainte doivent etre <=0
            """
        
        i=0
        alpha=pas_init
        etat_courrant=etat_init
        
        #coefficient de la fonction barriere
        b=[]
        derb=[]
        for a in range(0,len(self.tab_fn_contrainte)):
            b.append(1.)
            derb.append(1.)
        
        #coefficient pour l adaptation
        self.adapt_coef=adaptative_penality_coef
        self.adapt_historique=[]
        if (len(self.adapt_coef)==0):
            for a in range(0,len(self.tab_fn_contrainte)):
                self.adapt_coef.append(1.)
                self.adapt_historique.append(0)
        else:
            for a in range(0,len(self.tab_fn_contrainte)):
                self.adapt_historique.append(0)


            
        historique_convergence=[]
        convergence=False
        while (i<nb_pas and convergence!=True):
            aster.affiche('RESULTAT', "\n\ndescente de gradient iteration %d pas %f"%(i,alpha))
            gradi=0
            self.obji=0
            objectif=[]
            #print "construction du gradient avec les fonctions criteres"
            for k in range(0,len(self.tab_fn_contrainte)):
                objtemp=objtemp=CO('objtemp')
                objkval=0.
                if (k==0):
                    
                    gradi=CO('gradi')
                    self.tab_fn_contrainte[k][0](etat=etat_courrant,valeur=objtemp,gradient=gradi,fn_para=self.tab_fn_contrainte[k][1])
                    objkval=objtemp['R',1]
                    self.fn_detruire_table(table=objtemp)
                    
                    self.obji=objkval
                    objectif.append(objkval)
                    
                    #Si le gradient doit etre normalise
                    if (normalise):
                        gradinor=CO('gradin')
                        #print "gradi",gradi['R',1]
                        self.__normalise_grad(etat=etat_courrant,retour=gradinor,gradient=gradi)
                        gradi=gradinor
                        
                    #on vas dans la direction oppose a celle indique par le gradient 
                    gradineg=CO('gradineg')
                    self.fn_mult_grad(etat=etat_courrant,retour=gradineg,gradient=gradi,alpha=-1.)
                    gradi=gradineg
                        #gradi=self.__normalise_grad(etat=etat_courrant,gradient=gradi)
                else:
                    gradk=CO('gradk')
                    self.tab_fn_contrainte[k][0](etat=etat_courrant,valeur=objtemp,gradient=gradk,fn_para=self.tab_fn_contrainte[k][1])
                    objkval=objtemp['R',1]
                    self.fn_detruire_table(table=objtemp)
                    
                    objectif.append(objkval)

                    if (normalise):
                        gradkn=CO('gradkn')
                        self.__normalise_grad(etat=etat_courrant,retour=gradkn,gradient=gradk)
                        gradk=gradkn
                        
                    if (self.class_barriere!=None):
                        derb[k]=self.class_barriere.derive(objkval)
                        b[k]=self.class_barriere.valeur(objkval)
                    else:
                        b[k]=objkval
                        
                    if (adaptative_penality):
                        print "adaptative penality",self.adapt_historique
                        if (objkval>0):
                            self.adapt_historique[k]+=1
                        else:
                            self.adapt_historique[k]-=1
                        if ((i+1)%(adaptative_penality_nb_iter)==0):
                            print "adaptative penality i",i," self.adapt_historique[k]",self.adapt_historique[k]
                            if (self.adapt_historique[k]==adaptative_penality_nb_iter):
                                print "increase"
                                self.adapt_coef[k]=self.adapt_coef[k]*adaptative_penality_beta1
                            if (self.adapt_historique[k]==-adaptative_penality_nb_iter):
                                print "decrease"
                                self.adapt_coef[k]=self.adapt_coef[k]/adaptative_penality_beta2
                            self.adapt_historique[k]=0
                            
                    print self.adapt_coef[k]
                    print "bk",b[k],"derbk",derb[k]
                    
                    self.obji=self.obji+self.adapt_coef[k]*b[k]
                    
                    gikn=CO('gik%d'%k)
                    #analytique
                    self.fn_sauv_etat(etat=etat_courrant,text=self.chemin_de_sauvegarde+"etati.%d"%i)
                    self.fn_sauv_grad(etat=etat_courrant,gradient=gradi,text=self.chemin_de_sauvegarde+"gradi%davantk%d"%(i,k))
                    aster.affiche('RESULTAT'," "*10+"sauvegarde gradk adapt:%f, derb:%f"%(self.adapt_coef[k],derb[k]))
                    
                    self.fn_update_grad(etat=etat_courrant,retour=gikn,grad1=gradi,grad2=gradk,alpha=-self.adapt_coef[k]*derb[k])
                    gradi=gikn
                    
                    #analytique
                    self.fn_sauv_grad(etat=etat_courrant,gradient=gradi,text=self.chemin_de_sauvegarde+"gradi%dapresk%d"%(i,k))
                    
                    self.fn_detruire_gradient(gradient=gradk)
                out=" "*5+"tab_fn_contrainte i:"+str(k)+" objk:"+str(objkval)+" barriere"+str(b[k])+" derbarriere"+str(derb[k]);
                aster.affiche('RESULTAT', out)
            #if (self.fn_smoothgrad!=None):
            #    gradi=self.fn_smoothgrad(gradi)
            
            #si on normalise le gradien a chaque iteration
            if (normalise_iteration):
                gradifn=CO('gradifn')
                self.__normalise_grad(etat=etat_courrant,retour=gradifn,gradient=gradi)
                gradi=gradifn

            #determination du pas optimal
            if (pas_optimal!=None):
                
                if (pas_optimal=="brent"):
                    aster.affiche('RESULTAT', "Calcul du pas optimal avec brent")
                    if (alpha==0.):
                        alpha=pas_init
                    rbrent=scalarsearch.brent(self.__evol_et_eval,func0=self.obji,args=(etat_courrant,gradi),brack=[0.,alpha],maxiter=pas_optimal_nb_brent_iter,full_output=True);
                    out= "retour brent"+str(rbrent)
                    aster.affiche('RESULTAT', out)
                    alpha=rbrent[0]
                    
                if (pas_optimal=="armijo"):
                    aster.affiche('RESULTAT', "Calcul du pas optimal avec armijo")
                    if (alpha<pas_mini):
                        alpha=pas_init
                        
                    a=CO('a')
                    self.fn_prod_scalaire_grad(etat=etat_courrant,retour=a,grad1=gradi,grad2=gradi)
                    normgrad=a['R',1]
                    self.fn_detruire_table(table=a)
                    
                    retourls=scalarsearch.scalar_search_armijo(phi=self.__evol_et_eval,phi0=self.obji,derphi0=normgrad,alpha0=alpha,args=(etat_courrant,gradi),);
                    out= "retour arjimo"+str(retourls)
                    aster.affiche('RESULTAT', out)
                    alpha=retourls[0]

                #scalar_search_wolfe1
                if (pas_optimal=="wolfe1"):
                    aster.affiche('RESULTAT', "Calcul du pas optimal avec wolfe1")
                    #alpha=pas_init
                    if (alpha==0.):
                        alpha=pas_init
                        
                    a=CO('a')
                    self.fn_prod_scalaire_grad(etat=etat_courrant,retour=a,grad1=gradi,grad2=gradi)
                    normgrad=a['R',1]
                    self.fn_detruire_table(table=a)
                    
                    retourls=scalarsearch.scalar_search_wolfe1(phi=self.__evol_et_eval_avec_der,phi0=self.obji,derphi0=normgrad,alpha0=alpha,args=(etat_courrant,gradi),);
                    out= "retour wolfe1"+str(retourls)
                    aster.affiche('RESULTAT', out)
                    alpha=retourls[0]
                
                if (alpha==0.):
                    if(adaptative_penality):
                        for k in range(1,len(self.tab_fn_contrainte)):
                            if (objectif[k]>0):
                                print "increase"
                                self.adapt_coef[k]=self.adapt_coef[k]*adaptative_penality_beta1
                            if (objectif[k]<0):
                                print "decrease"
                                self.adapt_coef[k]=self.adapt_coef[k]/adaptative_penality_beta2
                            self.adapt_historique[k]=0
                    else:
                        convergence=True
                
            #analytique
            aster.affiche('RESULTAT',"sauvegarde iter %d, self.obji:%f"%(i,self.obji))
            self.fn_sauv_grad(etat=etat_courrant,gradient=gradi,text=self.chemin_de_sauvegarde+"gradi%d"%i)
            self.fn_sauv_etat(etat=etat_courrant,text=self.chemin_de_sauvegarde+"sauvegardeavanti.%d"%i)
            if (len(historique_convergence)>=1):
                self.variation_absolue=self.obji-historique_convergence[len(historique_convergence)-1][1][0]
                if (self.obji!=0):
                    self.variation_relative=self.variation_absolue/self.obji
                else:
                    self.variation_relative=self.variation_absolue
            else:
                self.variation_absolue=self.variation_relative=self.obji
            
            tempetat={}
            tempetat["i"]=0.
            self.fn_evol(etat=etat_courrant,newetat=tempetat,gradient=gradi,alpha=alpha)
            self.fn_detruire_etat(etat=etat_courrant)
            etat_courrant=tempetat
            
            self.fn_sauv_etat(etat=etat_courrant,text=self.chemin_de_sauvegarde+"sauvegardefini.%d"%i)
            
            historique_convergence.append((i,(self.obji,self.variation_absolue,self.variation_relative),alpha,list(self.adapt_coef),objectif))
            out= "historique_convergence (num_ iteration, [objectif,variation_absolue,variation_relative], pas ,[coeficient de lagrange],[objectif])"
            for aa in historique_convergence:
                out=out+"\n"+" "*5+str(aa)
            aster.affiche('RESULTAT', out)

            self.fn_detruire_gradient(gradient=gradi)
            i+=1
        
        print "fin de descente de grad"


        return etat_courrant
        
    
