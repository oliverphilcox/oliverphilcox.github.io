---
layout: archive
title: "Code"
permalink: /code/
author_profile: true
redirect_from:
  - /codes
---

{% include base_path %}

EffectiveHalos
---------------

[EffectiveHalos](https://EffectiveHalos.readthedocs.io) is a fast Python code to accurately compute the matter power spectrum and halo covariances across a large range of scales using the Effective Halo model developed in [Philcox et al. 2020](coming soon). The matter power spectrum is *percent-level accurate* for scales between 0.02 and 1 h/Mpc for a variety of cosmologies (and expected to also have good accuracy beyond these scales), and uses Effective Field Theory to generate a model for the quasi-linear power spectrum which is combined with halo model terms. In addition, the code can be used to compute the covariance between halo number counts in two mass bins, or the covariance between halo number counts and the matter power spectrum. This includes all relevant effects; the intrinsic covariance, halo exclusion and super-sample effects. The code is simple to run, with a tutorial and full API documentation available online.

HIPSTER
--------

[HIPSTER](https://Hipster.readthedocs.io) (HIgh-k Power Spectrum EstimatoR) is a fast C++ code to compute galaxy power spectra and bispectra from surveys of arbitrary shapes, based on [Philcox & Eisenstein 2020](https://arxiv.org/abs/1912.01010) and [Philcox 2020](coming soon). These have quadratic order and are optimized for *small-scale* spectral computation, since they use a configuration-space algorithm to compute the spectra as weighted pair counts, rather than using Fast Fourier Transforms (FFTs). As such, they doesn't suffer from many of the common problems of FFTs; aliasing, shot-noise and window function convolution. For computing the power spectrum and bispectrum in cosmological simulations (with periodic boundary conditions), we include a variant of HIPSTER with minimal dependence on random particles. Extensive documentation is provided for HIPSTER, and it can be run in a single line of code.

RascalC
--------

[RascalC](https://RascalC.readthedocs.io) is a C++ code to quickly compute covariance matrices of galaxy two- and three-point correlation functions in arbitrary survey geometries, based on ([Philcox et al. 2019](https://arxiv.org/abs/1904.11070); [Philcox & Eisenstein 2019](https://arxiv.org/abs/1910.04764)). This is a fast Monte Carlo integrator of the relevant 12-18 dimensional integrals, and has been shown to give highly accurate covariances in a fraction of the time required from mock catalogs, fully taking into account anisotropies from the survey window. Covariances can be computed both for correlation functions in Legendre multipoles, correlation functions in angular bins and jackknife correlation functions. This is currently being used by a number of teams, including eBOSS, and extensive documentation is available online.

HADES
------

[HADES](https://github.com/oliverphilcox/HADES) (Hexadecapolar Analysis for Dust Estimation in Simulations) follows the work of [Philcox et al. 2018b](https://arxiv.org/abs/1805.09177), using polarized dust anisotropy properties to measure the amount of dust contamination in Cosmic Microwave Background (CMB) B-mode maps. In particular, it allows for discrimination between unsubstracted dust and Inflationary Gravitational Waves (IGWs) well below the current constraints on IGW amplitudes. A basic tutorial is provided online.

Chempy
------

[Chempy](https://github.com/oliverphilcox/ChempyMulti) was originally developed by [Jan Rybizki](http://www.mpia.de/homes/rybizki/index.html) in Heidelberg, Germany and is a fast and flexible Python model of galactic chemical evolution, which can be used to infer Galactic parameters using Markov Chain Monte Carlo (MCMC) methods. In [Philcox et al. 2018a](https://arxiv.org/abs/1712.05686), this was extended to include a *scoring system* for nucleosynthetic yield tables (judging them by their ability to reproduce proto-solar abundances) and in [Philcox & Rybizki 2019](https://arxiv.org/pdf/1909.00812.pdf), we extended the statistics to use multiple stars via modern statistical methods. A selection of tutorials are available online.
