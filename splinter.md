---
layout: default
title: Sandstorm
---

Sandstorm is a new cloud in-memory key-value store that combats data movement
between disaggregated storage and compute nodes with untrusted tenant
extensions that are pushed to it at runtime.  Sandstorm's key insight is that
storage extensions can use language-level isolation to eliminate hardware
isolation overheads that cannot be avoided today: not with virtual machines,
containers, nor serverless Lambdas. Sandstorm also eliminates copying data for
safety, so extensions benefit from low-level hardware functionality like
zero-copy network transmission.

 - [NSF CAREER CNS-1750558](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1750558&HistoricalAwards=false)
 - [NSF CRII CNS-1566175](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1566175&HistoricalAwards=false)
 - [Splinter paper OSDI '18](https://www.usenix.org/node/222600)
 - [Sandstorm/Splinter Source](https://github.com/utah-scs/Sandstorm/)
