---
layout: page
permalink: /talks/
title: Talks
description: Selected recent talks with slides and recordings.
nav: true
nav_order: 4
---

<div class="talks-list">

{% assign talks = "
stanford-outreach-26|Public Talk (2026)|Echoes from the Beginning: How Galaxies Encode the Early Universe|[Slides](/assets/pdf/stanford-outreach-26.pdf), [Video](https://www.youtube.com/watch?v=SK2OxDiCUk8);
inflation-paris|2025|Colliders in the Sky: Constraining Primordial Non-Gaussianity with CMB and LSS Observations|[Slides](/assets/pdf/inflation-paris.pdf);
benasque25|2025|An Unofficial DESI Analysis|[Slides (60 mins)](/assets/pdf/benasque25.pdf), [Slides (10 mins)](/assets/pdf/santa-barbara26.pdf), [Video](https://online.kitp.ucsb.edu/online/cmblss-c26/philcox);
cmb_4pt|2024|Particle Colliders in the Sky (High Energy Physics with the CMB Trispectrum)|[Slides](/assets/pdf/cmb_4pt.pdf);
cotb24|2024|How to Model a Galaxy Survey|[Slides (180 mins)](/assets/pdf/cotb24.pdf), [Slides (60 mins)](/assets/pdf/eft_talk.pdf), [Notes](/assets/pdf/eft_intro.pdf);
hotspots|2024|Searching for Massive Particles in the CMB|[Slides](/assets/pdf/hotspots.pdf);
galactic_collider|2023|The Galactic Cosmological Collider|[Slides](/assets/pdf/galactic_collider.pdf);
job-talk-24|Job Talk (2024)|Galaxy Surveys: A Precision Probe of Inflation|[Slides](/assets/pdf/job-talk-24.pdf);
parity2|2023|Hints of Cosmological Parity Violation|[Slides (45 min)](/assets/pdf/parity2.pdf), [Slides (10 min)](/assets/pdf/parity-short.pdf);
madrid-inflation|2022|Constraining Inflation with BOSS DR12|[Slides (technical)](/assets/pdf/madrid-inflation.pdf), [Slides (outline)](/assets/pdf/safari_inflation.pdf);
thesis-public|Thesis Talk|Probing Fundamental Cosmology with Galaxy Surveys|[Slides (public)](/assets/pdf/thesis-public.pdf), [Slides (specialist)](/assets/pdf/thesis-private.pdf);
psz|2022|Can We Learn Anything from pSZ x Shear?|[Slides](/assets/pdf/psz.pdf);
cca22|2022|An Unofficial BOSS DR12 Analysis: Cosmology from the Galaxy Power Spectrum and Bispectrum|[Slides](/assets/pdf/cca22.pdf);
jobtalk|Job Talk (2021)|Large Scale Structure Beyond the Two-Point Function|[Slides](/assets/pdf/jobtalk.pdf);
cosm_from_home21|2021|Cosmology from the Galaxy Four-Point Correlation Function|[Slides](/assets/pdf/cosm_from_home21.pdf), [Video](https://www.youtube.com/watch?v=pmo1QigLsn4);
geneva_pk_talk|2021|Have We Exhausted the Galaxy Two-Point Function?|[Slides](/assets/pdf/geneva_pk_talk.pdf);
svd_data_compression|2020|Fewer Mocks and Less Noise: Reducing the Dimensionality of Cosmological Observables with Subspace Projections|[Slides](/assets/pdf/svd_data_compression.pdf);
mk_density|2020|Cosmology with the Marked Density Field|[Slides](/assets/pdf/mk_density.pdf);
cosm_from_home|2020|Measuring H0 from Galaxy Surveys: With and Without the Sound Horizon|[Slides](/assets/pdf/cosm_from_home.pdf), [Video](https://www.youtube.com/embed/QM_pGTMhJTc);
uk_cosmo|2020|What's Next for the Effective Field Theory of Large Scale Structure?|[Slides (15 mins)](/assets/pdf/uk_cosmo.pdf), [Slides (45 mins)](/assets/pdf/future_eft.pdf), [Video](http://pirsa.org/20060054);
ehm|2020|The Effective Halo Model: Accurate Models for the Power Spectrum and Cluster Count Covariances|[Slides](/assets/pdf/ehm.pdf);
h0_eft|2020|Combining Galaxy Full-Shape and BAO Information|[Slides](/assets/pdf/h0_eft.pdf);
dust_aniso|2019|Detection and Removal of CMB B-mode Dust Foregrounds with Signatures of Statistical Anisotropy|[Slides](/assets/pdf/dust_aniso.pdf);
asa_talk|2018|Inferring Galactic Parameters from Chemical Abundances|[Slides (15 mins)](/assets/pdf/asa_talk.pdf), [Slides (45 mins)](/assets/pdf/chem_evol.pdf)
" | strip | split: ";" %}

{% for talk_data in talks %}
  {% assign fields = talk_data | strip | split: "|" %}
  {% assign slide_id = fields[0] | strip %}
  {% assign year_label = fields[1] | strip %}
  {% assign title = fields[2] | strip %}
  {% assign links = fields[3] | strip %}
  {% if slide_id == "" %}{% continue %}{% endif %}

  <div class="talk-entry row mb-4 align-items-start">
    <div class="col-md-3 col-sm-4 mb-2">
      <a href="/assets/pdf/{{ slide_id }}.pdf">
        <img src="/assets/img/talks/{{ slide_id }}.png" alt="{{ title }}" class="img-fluid rounded z-depth-1" onerror="this.style.display='none'">
      </a>
    </div>
    <div class="col-md-9 col-sm-8">
      <h6 class="talk-title mb-1">
        {% if year_label contains "Talk" or year_label contains "Thesis" %}
          <strong>{{ year_label }}</strong>:
        {% else %}
          <span class="text-muted">({{ year_label }})</span>
        {% endif %}
        {{ title }}
      </h6>
      <p class="talk-links mb-0">{{ links | markdownify | remove: '<p>' | remove: '</p>' }}</p>
    </div>
  </div>

{% endfor %}

</div>
