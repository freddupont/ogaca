#exemplesection_tridi_readstr.py
#exemple de lecture de fichier .str de robot depuis salome
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

biblidir="/home/fred/asteretude/blindopti/bibli"
import sys
sys.path.append(biblidir)
import IOBeam

fi="/home/fred/asteretude/blindopti/grandtopmesh22.m3.robot.str"
newnode,newline,newgrl,newgrn=IOBeam.ReadSTR(fi)
IOBeam.CreateSalomeMesh(newnode,newline,groupline=newgrl,groupnode=newgrn)
