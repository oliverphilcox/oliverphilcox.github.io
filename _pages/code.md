---
layout: archive
title: "Code"
permalink: /code/
author_profile: true
redirect_from:
  - /codes
---

{% include base_path %}

HIPSTER
--------

[HIPSTER](https://Hipster.readthedocs.io) (HIgh-k Power Spectrum EstimatoR) is a fast C++ code to compute galaxy power spectra from surveys of arbitrary shapes, based on [Philcox & Eisenstein 2019](https://arxiv.org/abs/1912.01010). This is optimized for *small-scale* power spectrum computation, since it uses a configuration-space algorithm to compute the power as a weighted pair count, rather than using Fast Fourier Transforms (FFTs). As such, it doesn't suffer from many of the common problems of FFTs; aliasing, shot-noise and window function convolution. A variant of HIPSTER optimized for computing the power spectrum and bispectrum in N-body simulations is currently in creation. Extensive documentation is provided for HIPSTER, and it can be run in a single line of code.


RascalC
--------

[RascalC](https://RascalC.readthedocs.io) is a C++ code to compute covariance matrices of galaxy two- and three-point correlation functions in arbitrary survey geometries, based on ([Philcox et al. 2019](https://arxiv.org/abs/1904.11070); [Philcox & Eisenstein 2019](https://arxiv.org/abs/1910.04764)). This is a fast Monte Carlo integrator of the relevant 12-18 dimensional integrals, and has been shown to give highly accurate covariances in a fraction of the time required from mock catalogs, fully taking into account anisotropies from the survey window. Covariances can be computed both for correlation functions in Legendre multipoles, correlation functions in angular bins and jackknife correlation functions. This is currently being used by a number of teams, including eBOSS, and extensive documentation is available online.

HADES
------

[HADES](https://github.com/oliverphilcox/HADES) (Hexadecapolar Analysis for Dust Estimation in Simulations) follows the work of [Philcox et al. 2018](https://arxiv.org/abs/1805.09177), using polarized dust anisotropy properties to measure the amount of dust contamination in Cosmic Microwave Background (CMB) B-mode maps. In particular, it allows for discrimination between unsubstracted dust and Inflationary Gravitational Waves (IGWs) well below the current constraints on IGW amplitudes. A basic tutorial is provided online.


Chempy
------

[Chempy](https://github.com/oliverphilcox/ChempyMulti) was originally developed by [Jan Rybizki](http://www.mpia.de/homes/rybizki/index.html) in Heidelberg, Germany and is a fast and flexible Python model of galactic chemical evolution, which can be used to infer Galactic parameters using Markov Chain Monte Carlo (MCMC) methods. In [Philcox et al. 2018](https://arxiv.org/abs/1712.05686), this was extended to include a *scoring system* for nucleosynthetic yield tables (judging them by their ability to reproduce proto-solar abundances) and in [Philcox & Rybizki 2019](https://arxiv.org/pdf/1909.00812.pdf), we extended the statistics to use multiple stars via modern statistical methods. A selection of tutorials are available online.
