# Introduction #

Based on the algorithm from CMAP polythecnique http://www.cmap.polytechnique.fr/~allaire/freefem.html
a SIMP optimization has been done under code aster.

The Principle of simp algorithm is the following:

  1. compute the of elastic energies

> 2)	from this field a new density fiel dis calculated (the young modulus is proportional to this density field)

> 3)	apply this field to the mesh and go to step 1)
more information with the link above


# Details #

This has been done under CA but only young modulus field is generated. the scipy.optimise.brent function has been used.
## the example is aviable ##
here http://code.google.com/p/ogaca/downloads/detail?name=astersimp.zip

### introduction ###
this is a simple canteliver plate fixed on the right and with a vertical load on the left.

https://sites.google.com/site/ogacasite/simp-picture/SIMPmesh.PNG

### Result of 20 no-penalised step ###

https://sites.google.com/site/ogacasite/simp-picture/SIMPmesh1.PNG

In red there is more density and in blue no material. We can see the need of material in top and bottom of the right part

### result of 20 more penalized step ###

https://sites.google.com/site/ogacasite/simp-picture/SIMPmesh2.PNG

The penalization work as there is less 0.5 density material.
In the web area of the  canteliver we see the shape of the material used to resist shear. But is seems that the soft find a way around penalization. Maybe is a constant field by element will give beter result and expose a triangulation in the “web” area.

### Comment ###

The example provided work with plate but it should work with any type of model provided that
> elastic density of energy can be compute: (field TOTALE from ENEL\_NOEU)
> A group\_ma is defined precisely on the mail that will be optimised
Therefore it should work with 3d elements (not tested)

## Todo list ##
(well it’s not only for me, but for those who have some time)

  * try with a CHYOUNG constant by element.
  * try with 3d example
  * record the total elastic energy in each step (to see the optimization process)
  * use a better penalization algorithm (as Allaire’s one)