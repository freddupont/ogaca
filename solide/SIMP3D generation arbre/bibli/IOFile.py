#IOFile.py
#fichier destiner faciliter les sauvegardes de fichier

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

import os;
from Cata.cata import *
sortiepathwin="\"C:\\temp\"\\";
sortiepathlinux="/tmp/";

def SaveFileLinux(UNITE=80,PATH=None,FILENAME="file.med"):
       print "debug savefilewin"
       mpath="";
       if (PATH!=None):
              mpath=PATH
       else:
              mpath=sortiepathlinux       
       print 'cp fort.'+str(UNITE)+' '+mpath+FILENAME;
       EXEC_LOGICIEL(LOGICIEL='cp fort.'+str(UNITE)+' '+mpath+FILENAME,INFO=1);
       DEFI_FICHIER(ACTION='LIBERER',UNITE=UNITE,)
       EXEC_LOGICIEL(LOGICIEL='rm fort.'+str(UNITE),INFO=1)

def SaveFileWin(UNITE=80,PATH=None,FILENAME="file.med"):
       print "debug savefilewin"
       mpath="";
       if (PATH!=None):
              mpath=PATH
       else:
              mpath=sortiepathwin       
       os.system('ECHO copy fort.'+str(UNITE)+' '+mpath+FILENAME);
       os.system('copy fort.'+str(UNITE)+' '+mpath+FILENAME);
       DEFI_FICHIER(ACTION='LIBERER',UNITE=UNITE,)
       os.system('DEL fort.'+str(UNITE));

