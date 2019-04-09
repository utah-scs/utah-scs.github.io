---
layout: default
title: Splinter
---

<center>
<img src="{{ site.baseurl }}/img/splinter/osdi18.jpg" width="75%"/><br>
<h3>Splinter Team at OSDI'18</h3>
</center>

<div class="people" style="width: 100%; text-align: center;">
{% for item in site.data.people %}
  {% assign person = item[1] %}
  {% if person.splinter == true %}
    <span style="text-align: center; display: inline;">
      <a href="{{ person.webpage |escape }}">
         <span>
           <img class="img-circle" src="{{person.headshot}}" alt="{{person.display_name}}" width="75" height="75" alt="{{ person.display_name }}">
         </span>
      </a>
     </span>
  {% endif %}
{% endfor %}
</div>

<br>

Splinter is a new cloud in-memory key-value store that combats data movement
between disaggregated storage and compute nodes with untrusted tenant
extensions that are pushed to it at runtime.  Splinter's key insight is that
storage extensions can use language-level isolation to eliminate hardware
isolation overheads that cannot be avoided today: not with virtual machines,
containers, nor serverless Lambdas. Splinter also eliminates copying data for
safety, so extensions benefit from low-level hardware functionality like
zero-copy network transmission.
 - [Splinter paper OSDI '18](https://www.usenix.org/node/222600)
 - [Splinter Source Code](https://github.com/utah-scs/splinter/) ([OSDI Source](https://github.com/utah-scs/splinter/releases/tag/v1.0))

### Funding
 - [NSF CAREER CNS-1750558](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1750558&HistoricalAwards=false)
 - [NSF CRII CNS-1566175](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1566175&HistoricalAwards=false)
