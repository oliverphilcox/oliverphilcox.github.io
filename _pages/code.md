---
layout: page
title: Code
permalink: /code/
description: Recent public research codes on GitHub.
nav: true
nav_order: 3
---

<div class="projects">

{% assign sorted_projects = site.projects | sort: "importance" %}

<div class="row row-cols-1 row-cols-md-3">
  {% for project in sorted_projects %}
    {% include projects.liquid %}
  {% endfor %}
</div>

</div>
