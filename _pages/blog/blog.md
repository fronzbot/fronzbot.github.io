---
layout: default
title: "Blog"
permalink: "/blog/"
navbar: true
---
<div class="page-content wrapper">
  <h1>Blog Archive</h1>  
  {% for post in site.posts %}
  	{% capture currentyear %}{{post.date | date: "%Y"}}{% endcapture %}
  	{% if currentyear != year %}
    	{% unless forloop.first %}</ul>{% endunless %}
    		<h5>{{ currentyear }}</h5>
    		<ul class="posts">
    		{% capture year %}{{currentyear}}{% endcapture %}
  		{% endif %}
    <li><a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a></li>
    {% if forloop.last %}</ul>{% endif %}
{% endfor %}
</div>