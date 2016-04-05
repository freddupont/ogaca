#########################################################
#test catalogue
bibli_dir='/home/fred/asteretude/kuwait/bibli'
fichiertemp='/tmp/cata.mar'

import sys

#importation du catalogue
sys.path.append(bibli_dir)
import catalogue_beta3 


cata=catalogue_beta3.CATALOGUE_POUTRE();#chargement du catalogue

#affichage des section dans leur axe neutre
##cata.charge_et_genere_2d(fichiertemp)
#affichage des section tel que dessine
cata.charge_et_genere_2d(fichiertemp,SANS_RECALAGE="OUI")
