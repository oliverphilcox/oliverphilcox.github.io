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
          description: "Publications in reverse chronological order, auto-fetched from InspireHEP.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-code",
          title: "Code",
          description: "Recent public research codes on GitHub.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/code/";
          },
        },{id: "nav-talks",
          title: "Talks",
          description: "Selected recent talks with slides and recordings.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/talks/";
          },
        },{id: "nav-research",
          title: "Research",
          description: "An overview of my research interests and key results.",
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
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "project-rascalc",
      title: "RascalC",
      description: "RascalC: A Fast Code for Galaxy Covariance Matrix Estimation",
      section: "Projects",
      handler: () => {
        window.location.href = "/projects/1_rascalc/";
      },
    },{id: "project-polyspec",
      title: "PolySpec",
      description: "Full-sky estimators for binned polyspectra and primordial template amplitudes",
      section: "Projects",
      handler: () => {
        window.location.href = "/projects/2_polyspec/";
      },
    },{id: "project-encore",
      title: "encore",
      description: "encore: Efficient isotropic 2-, 3- and 4-point correlation functions in C++ and CUDA",
      section: "Projects",
      handler: () => {
        window.location.href = "/projects/3_encore/";
      },
    },{id: "project-class-pt",
      title: "CLASS-PT",
      description: "Nonlinear perturbation theory extension of the Boltzmann code CLASS",
      section: "Projects",
      handler: () => {
        window.location.href = "/projects/4_class_pt/";
      },
    },{id: "project-polybin3d",
      title: "PolyBin3D",
      description: "Binned polyspectrum estimation for 3D large-scale structure, optionally mask-deconvolved ",
      section: "Projects",
      handler: () => {
        window.location.href = "/projects/5_polybin3d/";
      },
    },{id: "project-full-shape-likelihoods",
      title: "full_shape_likelihoods",
      description: "Full-Shape Power Spectrum and Bispectrum Likelihoods",
      section: "Projects",
      handler: () => {
        window.location.href = "/projects/6_full_shape_likelihoods/";
      },
    },{id: "project-spectra-without-windows",
      title: "Spectra-Without-Windows",
      description: "Estimators and data for window-free analysis of power spectra and bispectra",
      section: "Projects",
      handler: () => {
        window.location.href = "/projects/7_spectra_without_windows/";
      },
    },{id: "project-hipster",
      title: "HIPSTER",
      description: "HIPSTER: HIgh-k Power SpecTrum and bispectrum EstimatoR",
      section: "Projects",
      handler: () => {
        window.location.href = "/projects/8_hipster/";
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