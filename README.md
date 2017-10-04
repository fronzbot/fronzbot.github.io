[![Build Status](https://travis-ci.org/fronzbot/fronzbot.github.io.svg?branch=master)](https://travis-ci.org/fronzbot/fronzbot.github.io)
# Personal Website

Source code for my website [https://kevinfronczak.com](https://kevinfronczak.com)

# License and Copyright
This repo is covered under the [MIT license](LICENSE.md) with the exception of the following directories:

`_posts/*`

`images/*`

`assets/docs/*`

Unauthorized reproduction or distribution of the any work in those directories without my (Kevin Fronczak's) prior written consent is considered copyright infringement and is forbidden.

# Why Jekyll?

Before moving to [Jekyll](http://jekyllrb.com/) I had been using a [Wordpress](https://wordpress.com/) blog hosted on paid [Namecheap](https://www.namecheap.com/) servers.  The thing is, my blog is pretty much entirely static so that set-up was mostly useless.  Also, I routinely would get terrible scores on [Google's Site Tester](https://testmysite.thinkwithgoogle.com/) and their [PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/) despite my best efforts.  After some research, I decided Jekyll with Github Pages made the most sense for what I needed so I decided to make the jump.  Revision control with a remote Github repo was definitely a plus.

# Development

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
  sed -i -e 's/https\:\/\/kevinfronczak\.com//g' _config_dev.yml
  bundle exec jekyll build --config _config_dev.yml
  bundle exec jekyll serve --config _config_dev.yml
fi
```

The `sed` command is used to replace the url set within `_config.yml` with an empty string, which allows me to navigate to `localhost:4000` to verify website changes locally.

# Continuous Integration

I opted to use [travis-ci](https://travis-ci.org/) for continuous integration, since I've used it before on other projects.  Here, I run a few tests:

* Check that the site can be built via [cibuild](https://github.com/fronzbot/fronzbot.github.io/script/cibuild)
* Check HTML to make sure no linking errors via `htmlproofer` call in [cibuild](https://github.com/fronzbot/fronzbot.github.io/script/cibuild)
* Verify frontmatter in posts have valid tags (for future tag linking) via [check_frontmatter.py](https://github.com/fronzbot/fronzbot.github.io/script/pyscripts/check_frontmatter.py)
* Verify any posts that are set to be featured on the [project](https://kevinfronczak.com/projects/) page have the required `feature_image` key via [check_frontmatter.py](https://github.com/fronzbot/fronzbot.github.io/script/pyscripts/check_frontmatter.py)
* Check that all posts are markdown only (no html) and both equations and images are properly centered on the page via [post_linter.py](https://github.com/fronzbot/fronzbot.github.io/script/pyscripts/post_linter.py)

The first two tests (in `cibuild`) are what is recommended by [Jekyll](http://jekyllrb.com/).  All of the python tests are custom implementations that helped me quickly iterate through changes I needed to make while working on porting the Wordpress site over to Github Pages.
