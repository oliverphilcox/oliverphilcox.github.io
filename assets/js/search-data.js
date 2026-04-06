// don't remove the above lines
// they are required to make the code work

// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "About",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-publications",
          title: "Publications",
          description: "Publications in reverse chronological order, auto-fetched from InspireHEP. papers preprints arXiv InspireHEP cosmology astrophysics galaxy survey CMB inflation",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-code",
          title: "Code",
          description: "Recent public research codes on GitHub. software GitHub open source Python C++ RascalC PolySpec ENCORE HIPster PolyBin3D covariance matrix estimator",
          section: "Navigation",
          handler: () => {
            window.location.href = "/code/";
          },
        },{id: "nav-talks",
          title: "Talks",
          description: "Selected recent talks with slides and recordings. seminars conferences lectures slides PDF presentations colloquia invited talks",
          section: "Navigation",
          handler: () => {
            window.location.href = "/talks/";
          },
        },{id: "nav-research",
          title: "Research",
          description: "An overview of my research interests and key results. galaxy clustering bispectrum power spectrum CMB primordial non-Gaussianity inflation parity violation Hubble constant dark energy simulation-based inference BOSS DESI Planck cosmological collider neutrino masses trispectrum perturbation theory EFT large-scale structure",
          section: "Navigation",
          handler: () => {
            window.location.href = "/research/";
          },
        },{id: "nav-current-group-members",
          title: "Current Group Members",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/group/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "Curriculum vitae. curriculum vitae resume positions education awards fellowships postdoc Stanford",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "project-hipster",
      title: "HIPSTER",
      description: "HIPSTER: HIgh-k Power SpecTrum and bispectrum EstimatoR",
      section: "Projects",
      handler: () => {
        window.open("https://github.com/oliverphilcox/HIPSTER", "_blank");
      },
    },{id: "project-class-pt",
      title: "CLASS-PT",
      description: "Nonlinear perturbation theory extension of the Boltzmann code CLASS",
      section: "Projects",
      handler: () => {
        window.open("https://github.com/Michalychforever/CLASS-PT", "_blank");
      },
    },{id: "project-polyspec",
      title: "PolySpec",
      description: "Full-sky estimators for binned polyspectra and primordial template amplitudes",
      section: "Projects",
      handler: () => {
        window.open("https://github.com/oliverphilcox/PolySpec", "_blank");
      },
    },{id: "project-cosmological-collider-bispectra",
      title: "cosmological-collider-bispectra",
      description: "Visualization of the inflationary scalar-exchange bispectra",
      section: "Projects",
      handler: () => {
        window.open("https://github.com/oliverphilcox/cosmological-collider-bispectra", "_blank");
      },
    },{id: "project-oneloopbispectrum",
      title: "OneLoopBispectrum",
      description: "Computation of the one-loop bispectrum of galaxies in redshift space",
      section: "Projects",
      handler: () => {
        window.open("https://github.com/oliverphilcox/OneLoopBispectrum", "_blank");
      },
    },{id: "project-rascalc",
      title: "RascalC",
      description: "RascalC: A Fast Code for Galaxy Covariance Matrix Estimation",
      section: "Projects",
      handler: () => {
        window.open("https://github.com/oliverphilcox/RascalC", "_blank");
      },
    },{id: "project-encore",
      title: "encore",
      description: "encore: Efficient isotropic 2-, 3- and 4-point correlation functions in C++ and CUDA",
      section: "Projects",
      handler: () => {
        window.open("https://github.com/oliverphilcox/encore", "_blank");
      },
    },{id: "project-polybin3d",
      title: "PolyBin3D",
      description: "Binned polyspectrum estimation for 3D large-scale structure, optionally mask-deconvolved ",
      section: "Projects",
      handler: () => {
        window.open("https://github.com/oliverphilcox/PolyBin3D", "_blank");
      },
    },{id: "project-full-shape-likelihoods",
      title: "full_shape_likelihoods",
      description: "Full-Shape Power Spectrum and Bispectrum Likelihoods",
      section: "Projects",
      handler: () => {
        window.open("https://github.com/oliverphilcox/full_shape_likelihoods", "_blank");
      },
    },{id: "project-spectra-without-windows",
      title: "Spectra-Without-Windows",
      description: "Estimators and data for window-free analysis of power spectra and bispectra",
      section: "Projects",
      handler: () => {
        window.open("https://github.com/oliverphilcox/Spectra-Without-Windows", "_blank");
      },
    },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];