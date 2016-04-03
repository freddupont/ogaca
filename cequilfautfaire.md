# Introduction #

Vous trouverez ci-après les points qu'il reste à améliorer dans le code


# Details #


## item ##
difficulté +++

le bloc fondamental est le bloc d'optimisation.
on ne peut pas réutiliser des algo existant car en opti geometrique la
dimention du problème change a chaque pas!
l'idée est de recodé un algo type gradient conjugé en python.

->ce bloc doit etre generique pour s'adapter a tout type de géométrie,
de propagation et de contrainte. (on passe les fonctions qui font le
boulot)

-> il doit pouvoir gerer plusieur contrainte ( penalité/ péalité
dynamique / autre)



une foit ce bloc crée adapter couple contrainte/dérivé sera un jeux d'enfant.





## item ##

difficulté +

aprés l'idée est d'enrichir aux maximums les fonctions contraintes
(pas que rdm si possible)





## item ##

difficulté +

pour l'optimisation des coques
crée une macro qui calcul la courbure moyenne et la courbre de gauss
http://serge.mehl.free.fr/anx/triedre_ribaucour.html

doit pouvoir ce faire en partant du champ de géométrie et du champs
des normales aux noeud que nous donnes code aster.

plus un détournement du calcul du gradient en thermique pour avoir les
dérivés d'un champs de scalaire





## item ##

difficulté ++

pour l'optimisation des coques et treillis

trouver la distance entre le maillage actuel et un maillage de
référence ainsi que le gradient qui permet de se raprocher du maillage
de reference.
doit pouvoir ce faire en utilisant proj\_champ et en projetant le champ
de géométrie d'un maillage sur l'autre.





## item ##

difficulté +

pour les coques et treillis

pour les poutre crée le champs de vecteur dans le repere global
représentant les x,y,z locaux a chaque poutre

pour les coques crée le champs de vecteur dans le repere global
représentant les x1,x2,x3 locaux a chaque éléments
doit pouvoir ce faire en créeant par example le champs de force sur X
local pour en demandant le calcul des éléments généralisé





## item ##

difficulté ++++ (car j'aime pas le fortran!)
mettre au propre la fonction de propagation de xfem qui fonctione actuelement.
avec si possible des cas testes
le but est quel soit assez bonne pour etre intégré a CA par EDF


# Dans le monde du libre #

## Item 2d vers 1d ##
ça ne concerne pas directement CA mais ce serais bien pratique quand même:
Génération automatique de poutre ou de tridi à partir de la surface extérieur ou à partir de la surface exterieur et intérieur