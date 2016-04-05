#scalarsearch.py
#utilise les fonctions scipy de recherche scalare modifier pour prendre en compte
#les specificite de CA utilise par blind_opti
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
from scipy.optimize import minpack2
import numpy as np
#from numpy.compat import asbytes



#def scalar_search_wolfe1(phi,args=(), phi0=None, old_phi0=None, derphi0=None,
#                         c1=1e-4, c2=0.9,
#                         amax=50, amin=1e-8, xtol=1e-14):
#    """
#    Scalar function search for alpha that satisfies strong Wolfe conditions
#
#    alpha > 0 is assumed to be a descent direction.
#
#    Parameters
#    ----------
#    phi : callable phi(alpha)
#        Function at point `alpha`
#    derphi : callable dphi(alpha)
#        Derivative `d phi(alpha)/ds`. Returns a scalar.
#
#    phi0 : float, optional
#        Value of `f` at 0
#    old_phi0 : float, optional
#        Value of `f` at the previous point
#    derphi0 : float, optional
#        Value `derphi` at 0
#    amax : float, optional
#        Maximum step size
#    c1, c2 : float, optional
#        Wolfe parameters
#
#    Returns
#    -------
#    alpha : float
#        Step size, or None if no suitable step was found
#    phi : float
#        Value of `phi` at the new point `alpha`
#    phi0 : float
#        Value of `phi` at `alpha=0`
#
#    Notes
#    -----
#    Uses routine DCSRCH from MINPACK.
#
#    """
#
#    if phi0 is None or derphi0 is None:
#        phi0,derphi0 = phi(0.)
#
#
#    if old_phi0 is not None:
#        alpha1 = min(1.0, 1.01*2*(phi0 - old_phi0)/derphi0)
#        if alpha1 < 0:
#            alpha1 = 1.0
#    else:
#        alpha1 = 1.0
#
#    phi1 = phi0
#    derphi1 = derphi0
#    isave = np.zeros((2,), np.intc)
#    dsave = np.zeros((13,), float)
#    task = asbytes('START')
#
#    while 1:
#        stp, phi1, derphi1, task = minpack2.dcsrch(alpha1, phi1, derphi1,
#                                                   c1, c2, xtol, task,
#                                                   amin, amax, isave, dsave)
#        if task[:2] == asbytes('FG'):
#            alpha1 = stp
#            phi1,derphi1 = phi(stp)
#
#        else:
#            break
#
#    if task[:5] == asbytes('ERROR') or task[:4] == asbytes('WARN'):
#        stp = None  # failed
#
#    return stp, phi1, phi0


def scalar_search_wolfe2(phi, derphi=None, phi0=None,
                         old_phi0=None, derphi0=None,
                         c1=1e-4, c2=0.9, amax=50):
    """Find alpha that satisfies strong Wolfe conditions.

    alpha > 0 is assumed to be a descent direction.

    Parameters
    ----------
    phi : callable f(x,*args)
        Objective scalar function.

    derphi : callable f'(x,*args), optional
        Objective function derivative (can be None)
    phi0 : float, optional
        Value of phi at s=0
    old_phi0 : float, optional
        Value of phi at previous point
    derphi0 : float, optional
        Value of derphi at s=0
    args : tuple
        Additional arguments passed to objective function.
    c1 : float
        Parameter for Armijo condition rule.
    c2 : float
        Parameter for curvature condition rule.

    Returns
    -------
    alpha_star : float
        Best alpha
    phi_star
        phi at alpha_star
    phi0
        phi at 0
    derphi_star
        derphi at alpha_star

    Notes
    -----
    Uses the line search algorithm to enforce strong Wolfe
    conditions.  See Wright and Nocedal, 'Numerical Optimization',
    1999, pg. 59-60.

    For the zoom phase it uses an algorithm by [...].

    """

    if phi0 is None:
        phi0 = phi(0.)

    if derphi0 is None and derphi is not None:
        derphi0 = derphi(0.)

    alpha0 = 0
    if old_phi0 is not None:
        alpha1 = min(1.0, 1.01*2*(phi0 - old_phi0)/derphi0)
    else:
        alpha1 = 1.0

    if alpha1 < 0:
        alpha1 = 1.0

    if alpha1 == 0:
        # This shouldn't happen. Perhaps the increment has slipped below
        # machine precision?  For now, set the return variables skip the
        # useless while loop, and raise warnflag=2 due to possible imprecision.
        alpha_star = None
        phi_star = phi0
        phi0 = old_phi0
        derphi_star = None

    phi_a1 = phi(alpha1)
    #derphi_a1 = derphi(alpha1)  evaluated below

    phi_a0 = phi0
    derphi_a0 = derphi0

    i = 1
    maxiter = 10
    while 1:         # bracketing phase
        if alpha1 == 0:
            break
        print c1
        print alpha1
        print derphi0
        if (phi_a1 > phi0 + c1*alpha1*derphi0) or \
           ((phi_a1 >= phi_a0) and (i > 1)):
            alpha_star, phi_star, derphi_star = \
                        _zoom(alpha0, alpha1, phi_a0,
                              phi_a1, derphi_a0, phi, derphi,
                              phi0, derphi0, c1, c2)
            break

        derphi_a1 = derphi(alpha1)
        if (abs(derphi_a1) <= -c2*derphi0):
            alpha_star = alpha1
            phi_star = phi_a1
            derphi_star = derphi_a1
            break

        if (derphi_a1 >= 0):
            alpha_star, phi_star, derphi_star = \
                        _zoom(alpha1, alpha0, phi_a1,
                              phi_a0, derphi_a1, phi, derphi,
                              phi0, derphi0, c1, c2)
            break

        alpha2 = 2 * alpha1   # increase by factor of two on each iteration
        i = i + 1
        alpha0 = alpha1
        alpha1 = alpha2
        phi_a0 = phi_a1
        phi_a1 = phi(alpha1)
        derphi_a0 = derphi_a1

        # stopping test if lower function not found
        if i > maxiter:
            alpha_star = alpha1
            phi_star = phi_a1
            derphi_star = None
            break

    return alpha_star, phi_star, phi0, derphi_star


def _cubicmin(a,fa,fpa,b,fb,c,fc):
    """
    Finds the minimizer for a cubic polynomial that goes through the
    points (a,fa), (b,fb), and (c,fc) with derivative at a of fpa.
    
    If no minimizer can be found return None
    
    """
    # f(x) = A *(x-a)^3 + B*(x-a)^2 + C*(x-a) + D

    C = fpa
    D = fa
    db = b-a
    dc = c-a
    if (db == 0) or (dc == 0) or (b==c): return None
    denom = (db*dc)**2 * (db-dc)
    d1 = np.empty((2,2))
    d1[0,0] = dc**2
    d1[0,1] = -db**2
    d1[1,0] = -dc**3
    d1[1,1] = db**3
    [A,B] = np.dot(d1, np.asarray([fb-fa-C*db,fc-fa-C*dc]).flatten())
    A /= denom
    B /= denom
    radical = B*B-3*A*C
    if radical < 0:  return None
    if (A == 0): return None
    xmin = a + (-B + np.sqrt(radical))/(3*A)
    return xmin


def _quadmin(a,fa,fpa,b,fb):
    """
    Finds the minimizer for a quadratic polynomial that goes through
    the points (a,fa), (b,fb) with derivative at a of fpa,

    """
    # f(x) = B*(x-a)^2 + C*(x-a) + D
    D = fa
    C = fpa
    db = b-a*1.0
    if (db==0): return None
    B = (fb-D-C*db)/(db*db)
    if (B <= 0): return None
    xmin = a  - C / (2.0*B)
    return xmin

def _zoom(a_lo, a_hi, phi_lo, phi_hi, derphi_lo,
          phi, derphi, phi0, derphi0, c1, c2):
    """
    Part of the optimization algorithm in `scalar_search_wolfe2`.
    """

    maxiter = 10
    i = 0
    delta1 = 0.2  # cubic interpolant check
    delta2 = 0.1  # quadratic interpolant check
    phi_rec = phi0
    a_rec = 0
    while 1:
        # interpolate to find a trial step length between a_lo and
        # a_hi Need to choose interpolation here.  Use cubic
        # interpolation and then if the result is within delta *
        # dalpha or outside of the interval bounded by a_lo or a_hi
        # then use quadratic interpolation, if the result is still too
        # close, then use bisection

        dalpha = a_hi-a_lo;
        if dalpha < 0: a,b = a_hi,a_lo
        else: a,b = a_lo, a_hi

        # minimizer of cubic interpolant
        # (uses phi_lo, derphi_lo, phi_hi, and the most recent value of phi)
        #
        # if the result is too close to the end points (or out of the
        # interval) then use quadratic interpolation with phi_lo,
        # derphi_lo and phi_hi if the result is stil too close to the
        # end points (or out of the interval) then use bisection

        if (i > 0):
            cchk = delta1*dalpha
            a_j = _cubicmin(a_lo, phi_lo, derphi_lo, a_hi, phi_hi, a_rec, phi_rec)
        if (i==0) or (a_j is None) or (a_j > b-cchk) or (a_j < a+cchk):
            qchk = delta2*dalpha
            a_j = _quadmin(a_lo, phi_lo, derphi_lo, a_hi, phi_hi)
            if (a_j is None) or (a_j > b-qchk) or (a_j < a+qchk):
                a_j = a_lo + 0.5*dalpha

        # Check new value of a_j

        phi_aj = phi(a_j)
        if (phi_aj > phi0 + c1*a_j*derphi0) or (phi_aj >= phi_lo):
            phi_rec = phi_hi
            a_rec = a_hi
            a_hi = a_j
            phi_hi = phi_aj
        else:
            derphi_aj = derphi(a_j)
            if abs(derphi_aj) <= -c2*derphi0:
                a_star = a_j
                val_star = phi_aj
                valprime_star = derphi_aj
                break
            if derphi_aj*(a_hi - a_lo) >= 0:
                phi_rec = phi_hi
                a_rec = a_hi
                a_hi = a_lo
                phi_hi = phi_lo
            else:
                phi_rec = phi_lo
                a_rec = a_lo
            a_lo = a_j
            phi_lo = phi_aj
            derphi_lo = derphi_aj
        i += 1
        if (i > maxiter):
            a_star = a_j
            val_star = phi_aj
            valprime_star = None
            break
    return a_star, val_star, valprime_star

def scalar_search_armijo(phi, phi0, derphi0, c1=1e-4, alpha0=1, amin=0,args=()):
    """Minimize over alpha, the function ``phi(alpha)``.

    Uses the interpolation algorithm (Armijo backtracking) as suggested by
    Wright and Nocedal in 'Numerical Optimization', 1999, pg. 56-57

    alpha > 0 is assumed to be a descent direction.

    Returns
    -------
    alpha
    phi1

    """
    phi_a0 = phi(*(alpha0,)+args)
    if phi_a0 <= phi0 + c1*alpha0*derphi0:
        return alpha0, phi_a0

    # Otherwise compute the minimizer of a quadratic interpolant:

    alpha1 = -(derphi0) * alpha0**2 / 2.0 / (phi_a0 - phi0 - derphi0 * alpha0)
    phi_a1 = phi(*(alpha1,)+args)
    
    
    if (phi_a1 <= phi0 + c1*alpha1*derphi0):
        return alpha1, phi_a1

    # Otherwise loop with cubic interpolation until we find an alpha which
    # satifies the first Wolfe condition (since we are backtracking, we will
    # assume that the value of alpha is not too small and satisfies the second
    # condition.

    while alpha1 > amin:       # we are assuming alpha>0 is a descent direction
        factor = alpha0**2 * alpha1**2 * (alpha1-alpha0)
        a = alpha0**2 * (phi_a1 - phi0 - derphi0*alpha1) - \
            alpha1**2 * (phi_a0 - phi0 - derphi0*alpha0)
        a = a / factor
        b = -alpha0**3 * (phi_a1 - phi0 - derphi0*alpha1) + \
            alpha1**3 * (phi_a0 - phi0 - derphi0*alpha0)
        b = b / factor

        alpha2 = (-b + np.sqrt(abs(b**2 - 3 * a * derphi0))) / (3.0*a)
        phi_a2 = phi(*(alpha2,)+args)

        if (phi_a2 <= phi0 + c1*alpha2*derphi0):
            return alpha2, phi_a2

        if (alpha1 - alpha2) > alpha1 / 2.0 or (1 - alpha2/alpha1) < 0.96:
            alpha2 = alpha1 / 2.0

        alpha0 = alpha1
        alpha1 = alpha2
        phi_a0 = phi_a1
        phi_a1 = phi_a2

    # Failed to find a suitable step length
    return None, phi_a1

class Brent:
    #need to rethink design of __init__
    def __init__(self, func,func0, args=(), tol=1.48e-8, maxiter=500,
                 full_output=0):
        self.func = func
        self.func0 = func0
        self.args = args
        self.tol = tol
        self.maxiter = maxiter
        self._mintol = 1.0e-11
        self._cg = 0.3819660
        self.xmin = None
        self.fval = None
        self.iter = 0
        self.funcalls = 0

    #need to rethink design of set_bracket (new options, etc)
    def set_bracket(self, brack = None):
        self.brack = brack
    def get_bracket_info(self):
        #set up
        func = self.func
        args = self.args
        brack = self.brack
        ### BEGIN core bracket_info code ###
        ### carefully DOCUMENT any CHANGES in core ##
        if brack is None:
            xa,xb,xc,fa,fb,fc,funcalls = bracket(func, args=args)
        elif len(brack) == 2:
            xa,xb,xc,fa,fb,fc,funcalls = bracket(func, xa=brack[0], xb=brack[1], args=args,fa=self.func0)
        elif len(brack) == 3:
            xa,xb,xc = brack
            if (xa > xc):  # swap so xa < xc can be assumed
                dum = xa; xa=xc; xc=dum
            assert ((xa < xb) and (xb < xc)), "Not a bracketing interval."
            fa = func(*((xa,)+args))
            fb = func(*((xb,)+args))
            fc = func(*((xc,)+args))
            assert ((fb<fa) and (fb < fc)), "Not a bracketing interval."
            funcalls = 3
        else:
            raise ValueError, "Bracketing interval must be length 2 or 3 sequence."
        ### END core bracket_info code ###

        return xa,xb,xc,fa,fb,fc,funcalls

    def optimize(self):
        #set up for optimization
        func = self.func
        xa,xb,xc,fa,fb,fc,funcalls = self.get_bracket_info()
        _mintol = self._mintol
        _cg = self._cg
        #################################
        #BEGIN CORE ALGORITHM
        #we are making NO CHANGES in this
        #################################
        x=w=v=xb
        fw=fv=fx=fb
        if (xa < xc):
            a = xa; b = xc
        else:
            a = xc; b = xa
        deltax= 0.0
        
        iter = 0
        while (iter < self.maxiter):
            tol1 = self.tol*abs(x) + _mintol
            tol2 = 2.0*tol1
            xmid = 0.5*(a+b)
            if abs(x-xmid) < (tol2-0.5*(b-a)):  # check for convergence
                xmin=x; fval=fx
                break
            if (abs(deltax) <= tol1):
                if (x>=xmid): deltax=a-x       # do a golden section step
                else: deltax=b-x
                rat = _cg*deltax
            else:                              # do a parabolic step
                tmp1 = (x-w)*(fx-fv)
                tmp2 = (x-v)*(fx-fw)
                p = (x-v)*tmp2 - (x-w)*tmp1;
                tmp2 = 2.0*(tmp2-tmp1)
                if (tmp2 > 0.0): p = -p
                tmp2 = abs(tmp2)
                dx_temp = deltax
                deltax= rat
                # check parabolic fit
                if ((p > tmp2*(a-x)) and (p < tmp2*(b-x)) and (abs(p) < abs(0.5*tmp2*dx_temp))):
                    rat = p*1.0/tmp2        # if parabolic step is useful.
                    u = x + rat
                    if ((u-a) < tol2 or (b-u) < tol2):
                        if xmid-x >= 0: rat = tol1
                        else: rat = -tol1
                else:
                    if (x>=xmid): deltax=a-x # if it's not do a golden section step
                    else: deltax=b-x
                    rat = _cg*deltax

            if (abs(rat) < tol1):            # update by at least tol1
                if rat >= 0: u = x + tol1
                else: u = x - tol1
            else:
                u = x + rat
            fu = func(*((u,)+self.args))      # calculate new output value
            funcalls += 1

            if (fu > fx):                 # if it's bigger than current
                if (u<x): a=u
                else: b=u
                if (fu<=fw) or (w==x):
                    v=w; w=u; fv=fw; fw=fu
                elif (fu<=fv) or (v==x) or (v==w):
                    v=u; fv=fu
            else:
                if (u >= x): a = x
                else: b = x
                v=w; w=x; x=u
                fv=fw; fw=fx; fx=fu

            iter += 1
        #################################
        #END CORE ALGORITHM
        #################################

        self.xmin = x
        self.fval = fx
        self.iter = iter
        self.funcalls = funcalls

    def get_result(self, full_output=False):
        if full_output:
            return self.xmin, self.fval, self.iter, self.funcalls
        else:
            return self.xmin


def brent(func,func0=None, args=(), brack=None, tol=1.48e-8, full_output=0, maxiter=500):
    """Given a function of one-variable and a possible bracketing interval,
    return the minimum of the function isolated to a fractional precision of
    tol.

    :Parameters:

        func : callable f(x,*args)
            Objective function.
        args
            Additional arguments (if present).
        brack : tuple
            Triple (a,b,c) where (a<b<c) and func(b) <
            func(a),func(c).  If bracket consists of two numbers (a,c)
            then they are assumed to be a starting interval for a
            downhill bracket search (see `bracket`); it doesn't always
            mean that the obtained solution will satisfy a<=x<=c.
        full_output : bool
            If True, return all output args (xmin, fval, iter,
            funcalls).

    :Returns:

        xmin : ndarray
            Optimum point.
        fval : float
            Optimum value.
        iter : int
            Number of iterations.
        funcalls : int
            Number of objective function evaluations made.

    Notes
    -----

    Uses inverse parabolic interpolation when possible to speed up convergence
    of golden section method.

    """

    brent = Brent(func=func,func0=func0, args=args, tol=tol, full_output = full_output, maxiter=maxiter)
    brent.set_bracket(brack)
    brent.optimize()
    return brent.get_result(full_output=full_output)

def bracket(func, xa=0.0, xb=1.0,fa=None, args=(), grow_limit=110.0, maxiter=1000):
    """Given a function and distinct initial points, search in the
    downhill direction (as defined by the initital points) and return
    new points xa, xb, xc that bracket the minimum of the function
    f(xa) > f(xb) < f(xc). It doesn't always mean that obtained
    solution will satisfy xa<=x<=xb

    Parameters
    ----------
    func : callable f(x,*args)
        Objective function to minimize.
    xa, xb : float
        Bracketing interval.
    args : tuple
        Additional arguments (if present), passed to `func`.
    grow_limit : float
        Maximum grow limit.
    maxiter : int
        Maximum number of iterations to perform.

    Returns
    -------
    xa, xb, xc : float
        Bracket.
    fa, fb, fc : float
        Objective function values in bracket.
    funcalls : int
        Number of function evaluations made.

    """
    _gold = 1.618034
    _verysmall_num = 1e-21
    if (fa==None):
       fa = func(*(xa,)+args)
    fb = func(*(xb,)+args)
    if (fa < fb):                      # Switch so fa > fb
        dum = xa; xa = xb; xb = dum
        dum = fa; fa = fb; fb = dum
    xc = xb + _gold*(xb-xa)
    fc = func(*((xc,)+args))
    funcalls = 3
    iter = 0
    while (fc < fb):
        tmp1 = (xb - xa)*(fb-fc)
        tmp2 = (xb - xc)*(fb-fa)
        val = tmp2-tmp1
        if abs(val) < _verysmall_num:
            denom = 2.0*_verysmall_num
        else:
            denom = 2.0*val
        w = xb - ((xb-xc)*tmp2-(xb-xa)*tmp1)/denom
        wlim = xb + grow_limit*(xc-xb)
        if iter > maxiter:
            raise RuntimeError("Too many iterations.")
        iter += 1
        if (w-xc)*(xb-w) > 0.0:
            fw = func(*((w,)+args))
            funcalls += 1
            if (fw < fc):
                xa = xb; xb=w; fa=fb; fb=fw
                return xa, xb, xc, fa, fb, fc, funcalls
            elif (fw > fb):
                xc = w; fc=fw
                return xa, xb, xc, fa, fb, fc, funcalls
            w = xc + _gold*(xc-xb)
            fw = func(*((w,)+args))
            funcalls += 1
        elif (w-wlim)*(wlim-xc) >= 0.0:
            w = wlim
            fw = func(*((w,)+args))
            funcalls += 1
        elif (w-wlim)*(xc-w) > 0.0:
            fw = func(*((w,)+args))
            funcalls += 1
            if (fw < fc):
                xb=xc; xc=w; w=xc+_gold*(xc-xb)
                fb=fc; fc=fw; fw=func(*((w,)+args))
                funcalls += 1
        else:
            w = xc + _gold*(xc-xb)
            fw = func(*((w,)+args))
            funcalls += 1
        xa=xb; xb=xc; xc=w
        fa=fb; fb=fc; fc=fw
    return xa, xb, xc, fa, fb, fc, funcalls
