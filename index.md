---
layout: page
title: "Home"
permalink: /
---

# Welcome to My PhD Research

![Research Banner](assets/images/research-banner.jpg)

## About My Project

Brief introduction to your research (2-3 paragraphs). Explain:
- The broader context
- Your specific focus
- Why it matters

## Recent Updates

{% for post in site.posts limit:3 %}
### [{{ post.title }}]({{ post.url }})
{{ post.excerpt | strip_html | truncatewords: 30 }}
[Read more...]({{ post.url }})
{% endfor %}

[View all updates](/blog)
