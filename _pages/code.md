---
layout: archive
title: "Code"
permalink: /code/
author_profile: true
redirect_from:
  - /codes
---

{% include base_path %}


encore
-------

[*encore*](https://github.com/oliverphilcox/encore) is a C++ code which computes the isotropic N-point correlation functions (NPCFs) of a set of N_g discrete points (e.g., a galaxy survey) using the O(N_g^2) method of [Philcox et al. 2021](http://arxiv.org/abs/2105.08722). The code supports N = 2, 3, 4, 5 and 6, and can additionally subtract the Gaussian contribution of the 4PCF at the estimator-level. It is fast, making use of OpenMP parallelization, AVX assembly code, and, for the higher-point functions, GPU acceleration, allowing computation of the full 4PCF for a BOSS-like survey in only a few tens of CPU-hours. It may further be extended to anisotropic NPCFs, following the methods of [Philcox & Slepian 2021b](https://arxiv.org/abs/2106.10278).

BOSS Without Windows
---------------------

The [*BOSS Without Windows*](https://github.com/oliverphilcox/BOSS-Without-Windows) repository contains the analysis code required to compute the galaxy power spectrum and bispectrum using optimal quadratic and cubic estimators, as descibed in [Philcox 2020b](https://arxiv.org/abs/2012.09389) and [Philcox 2021](https://arxiv.org/abs/2107.06287). The output measurements (which will be provided for the BOSS data-set and Patchy simulations) do not include the survey window functions, thus can be easily compared to theory models. Additionally, they give close-to-minimum-variance measurements of the power spectrum and bispectrum, which is particularly useful on small-scales. The code is written in Python, with some routines borrowed from [nbodykit](https://nbodykit.readthedocs.io/en/latest/). To compute the statistics, one requires only the survey mask, the data, and a random particle catalog.

Kepler's Goat Herd
-------------------

[Kepler's Goat Herd](https://github.com/oliverphilcox/Keplers-Goat-Herd) is a C++ code which uses the method of [Philcox et al. 2021](https://arxiv.org/abs/2103.15829) to solve Kepler's equation for elliptical orbit evolution. The code performs the relevant contour integrals numerically, and compares the results to conventional methods based on root-finding and series solutions. Our method is found to be around twice the speed of a quartic root-finder for the same level of accuracy.

EffectiveHalos
---------------

[EffectiveHalos](https://EffectiveHalos.readthedocs.io) is a fast Python code to accurately compute the matter power spectrum and halo covariances across a large range of scales using the Effective Halo model developed in [Philcox et al. 2020](https://arxiv.org/abs/2004.09515). The matter power spectrum is *percent-level accurate* for scales between 0.02 and 1 h/Mpc for a variety of cosmologies (and expected to also have good accuracy beyond these scales), and uses Effective Field Theory to generate a model for the quasi-linear power spectrum which is combined with halo model terms. In addition, the code can be used to compute the covariance between halo number counts in two mass bins, or the covariance between halo number counts and the matter power spectrum. This includes all relevant effects; the intrinsic covariance, halo exclusion and super-sample effects. The code is simple to run, with a tutorial and full API documentation available online.

HIPSTER
--------

[HIPSTER](https://Hipster.readthedocs.io) (HIgh-k Power Spectrum EstimatoR) is a fast C++ code to compute galaxy power spectra and bispectra from surveys of arbitrary shapes, based on [Philcox & Eisenstein 2020](https://arxiv.org/abs/1912.01010) and [Philcox 2020](http://arxiv.org/abs/2005.01739). These have quadratic order and are optimized for *small-scale* spectral computation, since they use a configuration-space algorithm to compute the spectra as weighted pair counts, rather than using Fast Fourier Transforms (FFTs). As such, they doesn't suffer from many of the common problems of FFTs; aliasing, shot-noise and window function convolution. For computing the power spectrum and bispectrum in cosmological simulations (with periodic boundary conditions), we include a variant of HIPSTER with minimal dependence on random particles. Extensive documentation is provided for HIPSTER, and it can be run in a single line of code.

RascalC
--------

[RascalC](https://RascalC.readthedocs.io) is a C++ code to quickly compute covariance matrices of galaxy two- and three-point correlation functions in arbitrary survey geometries, based on ([Philcox et al. 2019](https://arxiv.org/abs/1904.11070); [Philcox & Eisenstein 2019](https://arxiv.org/abs/1910.04764)). This is a fast Monte Carlo integrator of the relevant 12-18 dimensional integrals, and has been shown to give highly accurate covariances in a fraction of the time required from mock catalogs, fully taking into account anisotropies from the survey window. Covariances can be computed both for correlation functions in Legendre multipoles, correlation functions in angular bins and jackknife correlation functions. This is currently being used by a number of teams, including eBOSS, and extensive documentation is available online.

CLASS-PT
---------

[CLASS-PT](https://michalychforever.github.com/CLASS-PT) is an extension of [CLASS](https://class-code.net) used to compute one-loop perturbation theory for matter and biased tracers in real and redshift space, described in [Chudaykin et al. 2020](https://arxiv.org/abs/2004.10607). It has been used in a number of works and can be interfaced with the [MontePython](https://github.com/brinckmann/montepython_public) for fast MCMC sampling. Various custom-built likelihoods for BOSS and Euclid galaxy power spectra are available on [Github](https://github.com/michalychforever/lss_montepython).

HADES
------

[HADES](https://github.com/oliverphilcox/HADES) (Hexadecapolar Analysis for Dust Estimation in Simulations) follows the work of [Philcox et al. 2018b](https://arxiv.org/abs/1805.09177), using polarized dust anisotropy properties to measure the amount of dust contamination in Cosmic Microwave Background (CMB) B-mode maps. In particular, it allows for discrimination between unsubstracted dust and Inflationary Gravitational Waves (IGWs) well below the current constraints on IGW amplitudes. A basic tutorial is provided online.

Chempy
------

[Chempy](https://github.com/oliverphilcox/ChempyMulti) was originally developed by [Jan Rybizki](http://www.mpia.de/homes/rybizki/index.html) in Heidelberg, Germany and is a fast and flexible Python model of galactic chemical evolution, which can be used to infer Galactic parameters using Markov Chain Monte Carlo (MCMC) methods. In [Philcox et al. 2018a](https://arxiv.org/abs/1712.05686), this was extended to include a *scoring system* for nucleosynthetic yield tables (judging them by their ability to reproduce proto-solar abundances) and in [Philcox & Rybizki 2019](https://arxiv.org/pdf/1909.00812.pdf), we extended the statistics to use multiple stars via modern statistical methods. A selection of tutorials are available online.
