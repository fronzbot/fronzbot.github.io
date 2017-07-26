---
layout: page
title: "Projects"
permalink: "/projects/"
navbar: true
---

{% for post in site.posts %}
  <div class="post postContent">
  
    {% if post.project %}
      <div  class="postDate"><time datetime="{{ post.date | date_to_xmlschema }}" itemprop= "datePublished">{{ post.date | date: "%b %-d, %Y" }}</time>
      </div>
      <br>
      <div class="postArchive">
        <a class='postLink' href="{{site.url}}{{site.baseurl}}{{post.url}}">{{post.title}}</a>
      </div>
      <div class="postExt">
      <!-- {% if post.feature %}
        <img src="{{ site.baseurl }}{{ post.feature_image }}" alt="{{ post.title }}"><br>
      {% else %} -->
        {{ post.excerpt }} <a href="{{ site.baseurl }}{{post.url}}">Read more</a>
      </div>
      <!-- {% endif %} -->
    
    {% endif %}
    
  </div>
{% endfor %}