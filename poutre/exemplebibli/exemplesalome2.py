#########################################################
#test catalogue
bibli_dir='/home/fred/asteretude/kuwait/bibli'
fichiertemp='/tmp/cata.tmp'

import sys

#importation du catalogue
sys.path.append(bibli_dir)
import catalogue_beta3 


cata=catalogue_beta3.CATALOGUE_POUTRE();#chargement du catalogue
cata.charge_et_genere_3d(fichiertemp)
