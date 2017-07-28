---
layout: post
title: 'Moving from Wordpress to Github Pages'
date: 2017-07-28 20:00
description: How and why I moved my site from wordpress to github-pages
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - website
  - scripts
use_math: false
project: false
feature: false
---

## Why Jekyll?

Before moving to [Jekyll](http://jekyllrb.com/) I had been using a [Wordpress](https://wordpress.com/) blog hosted on paid [Namecheap](https://www.namecheap.com/) servers.  The thing is, my blog is pretty much entirely static so that set-up was mostly useless.  Also, I routinely would get terrible scores on [Google's Site Tester](https://testmysite.thinkwithgoogle.com/) and their [PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/) despite my best efforts.  After some research, I decided Jekyll with Github Pages made the most sense for what I needed so I decided to make the jump.  Revision control with a remote Github repo was definitely a plus.

## Moving From Wordpress

This was a rather tedious process, but made much easier with the `jekyll-import` tool.  I mostly followed the [tutorial here](http://www.adamwadeharris.com/how-to-convert-a-wordpress-site-to-jekyll-with-github-pages/) but I'll go over my exact steps anyways (slightly different than the linked article):

# Create Github Page

The first thing I did was create a repo on github called [fronzbot.github.io](https://github.com/fronzbot/fronzbot.github.io) which holds the source code for this website.  Next, I ran the following command to clone the repo into my workarea `git clone git@github.com:YOUR-USERNAME/YOUR-REPO-NAME.git`.  As a note, I have a virtual machine running debian that I do all my development on (including for [Home Assistant](https://github.com/home-assistant/home-assistant)) so my directions also assume you're working on Linux.  From here I had to create an index file and push to my repo so Github knew to create a webpage:

```
cd fronzbot.github.io
touch index.html
git add .
git commit -m "Initial commit"
git push origin master
```

# Install Jekyll

Now that my Repo was set up I needed to install jekyll to begin development.  This involved running the following commands within my repo directory:

```
gem install jekyll
gem install bundler
touch Gemfile
echo "source 'https://rubygems.org'" >> Gemfile
echo "gem install github-pages, group :jekyll_plugins" >> Gemfile
```

# Create files

Now that jekyll was installed, I could create my configuration file: `touch _config.yml`.  In your editor of choice, you can open that file and put the following entries in to get started:

```yaml
name: YOUR-WEBSITE-NAME
markdown: kramdown
permalink: /blog/:title   # Make this whatever you want
```

From here you can start adding your html and css or find a theme.  I'm not going to cover that here, it's fairly straightforward with some googling.

# Export Content
Now for the important part.  In your Wordpress admin panel, simply go to `Tools > Export > Download Export File` in the wp-admin console.  You should get an xml file.  Rename it `wordpress.xml`

# Import to Jekyll
* Install importer: `gem install jekyll-import`
* Run:
```
$ ruby -rubygems -e 'require "jekyll-import"; \
JekyllImport::Importers::WordpressDotCom.run({ "source" => "wordpress.xml"})'
```

You should now have a bunch of folders that look similar to this:

```
_attachments
_drafts
_pages
_posts
assets
wordpress.xml
```

I ended up using the contents of `_posts` and `assets`.  `_pages` may also be useful to you depending on what your old site looked like.

# Fix Everything

Iterating through posts to fix image links (I wanted to redirect to a different location) and removing html (personal preference) was a bit of a pain.  Also, I wanted to thin out the frontmatter which also involved some legwork.  The following commands were INCREDIBLY helpful for this.

```
$ grep -rnw '.' -e 'FINDME'
```

This would list every occurrence of the string `'FINDME'` and show me the line it was in, line number, and which file.  In the case where there were many entries and the lines were long, I opted for the `-rnl` flag instead of `-rnw` which would only list the files containing my search string.

For global find-and-replace (like links, or broken LaTeX syntax), I used

```
$ sed -i 's/FIND/REPLACE/g' *
```

Which would iterate over all files and replace the `FIND` string with `REPLACE`.  You can use regular expressions with `sed` so it's really powerful.  For example, a previous LaTeX plugin I used with Wordpress required `[latex] EQUATION [/latex]` to be wrapped around my equation, but [Mathjax](https://www.mathjax.org/) uses `$$ EQUATION $$`.  To replace this in all of my blog posts, I used (not the use of the escape character `\`):

```
$ sed -i s/\[latex\]/\$\$/g' _posts/*.md
$ sed -i s/\[\/latex\]/\$\$/g' _posts/*.md
```

But that's pretty much all that I needed to do to migrate from Wordpress.

## Development

In order to speed up development, I created a build script which allows me to cleanup the `_site` directory locally as well as create a dev version of my config to ensure linking works properly.  My script is located in the root of my repository and called via `./build`

```shell
#!/bin/bash
if [[ $* == *--clean* ]]; then
  rm -rf ./_site
fi

if [[ $* == *--lint* ]]; then
  ./script/cibuild --clean
else
  rm _config_dev.yml
  cp _config.yml _config_dev.yml
  sed -i -e 's/kevinfronczak\.com//g' _config_dev.yml
  sed -i -e 's/https\:\/\///g' _config_dev.yml
  bundle exec jekyll build --config _config_dev.yml
  bundle exec jekyll serve --config _config_dev.yml
fi
```

The `sed` command is used to replace the url set within `_config.yml` with an empty string, which allows me to navigate to `localhost:4000` to verify website changes locally.

## Adding SSL to my custom domain

Unfortunately, github-pages doesn't allow for SSL/TLS on custom domains.  A workaround is to use Cloudflare which will encrypt the link between the user and Cloudflare and the link between Cloudflare and Github is also encrypted since, by default, Github encrypts all `USER.github.io` domains.  Kind of hacky, but it works.  Here's an [article from Cloudflare](https://blog.cloudflare.com/secure-and-fast-github-pages-with-cloudflare/) on the subject.

## Speeding Up the Site

Once everything was fairly settled, I made a conscious effort to improve my score on Google's [PageSpeed Insights](https://blog.cloudflare.com/secure-and-fast-github-pages-with-cloudflare/).  My first iteration gave me a mobile score of **74** and a desktop score of **91**.  The primary problem was *Render-blocking Javascript and CSS in above-the-fold content*.  To fix this, I used a [Critical CSS Path](https://jonassebastianohlsson.com/criticalpathcssgenerator/) tool to find my critical CSS and place it in-line within my `_includes/head.html` file.  I also removed the call to `style.css` and placed it in a javascript call such that it loads asynchronously (i.e. it doesn't block rendering of the webpage):

```javascript
<script type="text/javascript">
  var giftofspeed = document.createElement('link');
  giftofspeed.rel = 'stylesheet';
  giftofspeed.href = '{{ site.baseurl }}/assets/css/style.css';
  giftofspeed.type = 'text/css';
  var godefer = document.getElementsByTagName('link')[0];
  godefer.parentNode.insertBefore(giftofspeed, godefer);
</script>
<noscript>
  <link rel="stylesheet" type="text/css" href='{{ site.baseurl }}/assets/css/style.css' />
</noscript>
```

This javascript file was then called within my `_includes/footer.html` file like so:

```html
<footer class="site-footer">
  <!-- Bunch of stuff -->
  {% include javascripts/defer_css.html %}
</footer>
```

This, along with some other improvements (caching via Cloudflare, minify, compression, locally serving google-analytics, locally serving fonts, etc) bumped my Mobile score to **97** and my desktop score to **96**.  Not bad for a guy who has never dealt with css/javascript/html before!

## Continuous Integration

I opted to use [travis-ci](https://travis-ci.org/) for continuous integration, since I've used it before on other projects.  Here, I run a few tests:

* Check that the site can be built via [cibuild](https://github.com/fronzbot/fronzbot.github.io/script/cibuild)
* Check HTML to make sure no linking errors via `htmlproofer` call in [cibuild](https://github.com/fronzbot/fronzbot.github.io/script/cibuild)
* Verify frontmatter in posts have valid tags (for future tag linking) via [check_frontmatter.py](https://github.com/fronzbot/fronzbot.github.io/script/pyscripts/check_frontmatter.py)
* Verify any posts that are set to be featured on the [project](https://kevinfronczak.com/projects/) page have the required `feature_image` key via [check_frontmatter.py](https://github.com/fronzbot/fronzbot.github.io/script/pyscripts/check_frontmatter.py)
* Check that all posts are markdown only (no html) and both equations and images are properly centered on the page via [post_linter.py](https://github.com/fronzbot/fronzbot.github.io/script/pyscripts/post_linter.py)

The first two tests (in `cibuild`) are what is recommended by [Jekyll](http://jekyllrb.com/).  All of the python tests are custom implementations that helped me quickly iterate through changes I needed to make while working on porting the Wordpress site over to Github Pages.

## Final Thoughts

Overall, the migration took a few days of work to get exactly what I wanted, but it wasn't too bad.  At first everything was pretty daunting, but I quickly got familiar with the directory structure, syntax, and overall operation that I was able to really understand what I needed to do in order to implement what was in my head.  A++++ would migrate again.
