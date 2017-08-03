---
layout: page
title: "Projects"
permalink: "/projects/"
navbar: true
---
<div class="wrapper">
<br>
<hr>
<div class="post postTitle"><h1>FEATURED</h1></div>
<hr>
{% assign project_posts = "" | split: "" %}
{% for post in site.posts %} 
    {% if post.feature == true %}
      <div class="post postContent">
        <div  class="postDate"><time datetime="{{ post.date | date_to_xmlschema }}" itemprop= "datePublished">{{ post.date | date: "%b %-d, %Y" }}</time>
        </div>
        <br>
        <div class="postArchive">
          <a class='postLink' href="{{site.url}}{{post.url}}">{{post.title}}</a>
        </div>
        <div class="postExt">
          <a class='postLink' href="{{site.url}}{{post.url}}"><img src="{{ site.url }}{{ post.feature_image }}" height="45%" width="45%" alt="{{ post.title }}"></a><br>
          {{ post.excerpt | strip_html | truncate:300  }} <a href="{{ site.url }}{{post.url}}">Read more</a>
        </div>
      </div>
    {% else if post.project == true %}
      {% assign project_posts = project_posts | push: post %}
    {% endif %}
{% endfor %}

<br>
<hr>
<div class="post postTitle"><h1>OTHER PROJECTS</h1></div>
<hr>
{% for post in project_posts %}
  <div class="post postContent">
    <div  class="postDate"><time datetime="{{ post.date | date_to_xmlschema }}" itemprop= "datePublished">{{ post.date | date: "%b %-d, %Y" }}</time>
    </div>
    <br>
    <div class="postArchive">
      <a class='postLink' href="{{site.url}}{{post.url}}">{{post.title}}</a>
    </div>
    
    <div class="postExt">
      {{ post.excerpt | strip_html | truncate:200  }} <a href="{{ site.url }}{{post.url}}">Read more</a>
    </div>
  </div>    
{% endfor %}

</div>
