#exemplesalomecata1.py
#lecture et affichage des sections du catalogue prealablement sauvegarder
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

#test catalogue
bibli_dir='/home/fred/asteretude/blindopti/bibli'
fichiertemp='/home/fred/asteretude/blindopti/tridicata.tmp'

import sys

#importation du catalogue
sys.path.append(bibli_dir)
import catalogue_beta


cata=catalogue_beta.CATALOGUE_POUTRE();#chargement du catalogue

#affichage des section dans leur axe neutre
##cata.charge_et_genere_2d(fichiertemp)
#affichage des section tel que dessine
cata.charge_et_genere_2d(fichiertemp,SANS_RECALAGE="OUI")
