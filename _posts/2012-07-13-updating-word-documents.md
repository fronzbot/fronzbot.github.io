---
layout: post
title: Updating Word Documents
date: 2012-07-13 12:16
description: Word document parsing script I made while an intern
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - python
  - scripts
use_math: false
project: true
feature: false
---

The other day at work I found myself without much to do since I was waiting for some data analysis to be sent back to me.  I talked to another Engineer looking for some work I could do in the meantime and he gave me some Word Documents (maybe around a 15 or so) that needed to be updated.  Essentially this meant combing through the documents and replacing all the old references with new ones.  Now I didn't feel like opening each document and doing this tedious task over and over again so I didn't!  Instead I wrote a script to do it for me.
I had never parsed a Word Document before with any language (never have really needed to) so using my google-fu I was able to find a module for Python called <a href="http://sourceforge.net/projects/pywin32/">Pywin32</a>.  After poking around I found that everything I needed to do (basically just find-and-replace) was already implemented and I just needed to call the right messages.  Awesome!  So here is the basic code I used in chunks and then again in full:
<div>The following imports all the important modules and creates a word instance.

```python
import os, re
import win32com.client
if win32com.client.gencache.is_readonly == True:
    win32com.client.gencache.is_readonly = False
    win32com.client.gencache.Rebuild()
from win32com.client.gencache import EnsureDispatch
from win32com.client import constants
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
```

</div>
Next I needed to process the document, find/replace elements, and save a new file. To do this I need to open my document (don't worry about the variable names - it'll all come together with the full code).

```python
word.Documents.Open(os.getcwd() + "\\" + directory + "\\" + file)
doc = word.Documents(1)
```

Now for the fun part - the find and replace! I wrapped this in a function since I had multiple things I needed to replace, but it's very straight-forward. First I need to look for the word without any formatting, find the word and then replace the word. There are some other items in there that allow for more control over what counts as a match but it's not something to worry too much about.

```python
def do_replace(search_str, replace_str):
    find = word.Selection.Find
    find.ClearFormatting()
    find.Replacement.ClearFormatting()
    find.Text = search_str
    find.Replacement.Text = replace_str
    find.Forward = True
    find.Wrap = constants.wdFindContinue
    find.MatchWildcards = True
    find.Execute(Replace= constants.wdReplaceAll)
```


So that's all well and good- but I have multiple files. I don't want to have to find the name of the file, input it to the program, etc. I want to click run and be done. So I added in a function that walks through my directory and finds anything with a 'doc' or 'docx' extension.

```python
def find_docs(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file[0] != "~" and (file[-3:] == "doc" or file[-4:] == "docx"):
                process(directory, file)
```

The 'process' function that is executed contains the word opening methods (above) and calls to do_replace. However, I also needed to add in file name checking (since some of the file names needed to be updated too) as well as the document saving method. To do this I simply used the 're' package to substitute names and then I checked for directory existence and saved my new Word file. I then closed the document instance (very important!).

```python
new_name = re.sub('old', 'new', file)
if not os.path.exists(os.getcwd() + "\ew_support" + "\\" + directory):
    os.mkdir(os.getcwd() + "\ew_support" + "\\" + directory)
doc.SaveAs(os.getcwd() + "\ew_support" + "\\" + directory + "\\" + new_name)
```

Finally I just need to create a function that is called on run-time that creates the 'new_support' directory if it does not exist and loop through the directories I needed it to (stored in the list dir_list - in this code they're made up names).

```python
dir_list = ['BIN', 'BOX', 'CKT', 'HELP', 'TEST', 'SYS']
def main():
    if not os.path.exists(os.getcwd() + "\ew_support"):
        os.mkdir(os.getcwd() + "\ew_support")
    for directory in dir_list:
        find_docs(directory)
    word.Quit()
```

Now, here's the full code in action:

```python
import os, re
import win32com.client
if win32com.client.gencache.is_readonly == True:
    win32com.client.gencache.is_readonly = False
    win32com.client.gencache.Rebuild()
from win32com.client.gencache import EnsureDispatch
from win32com.client import constants
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
dir_list = ['BIN', 'BOX', 'CKT', 'HELP', 'TEST', 'SYS']
def process(directory, file):
    word.Documents.Open(os.getcwd() + "\\" + directory + "\\" + file)
    doc = word.Documents(1)
    # Search and replace
    do_replace('FAIL', 'SUCCESS')
    do_replace('linux', 'xunil')
    do_replace('Xilinx', 'Altera')
    do_replace('Perl', 'Python')
    do_replace('test', 'prototype')
    #re-save in the modified folder
    new_name = re.sub('old', 'new', file)
    if not os.path.exists(os.getcwd() + "\ew_support" + "\\" + directory):
        os.mkdir(os.getcwd() + "\ew_support" + "\\" + directory)
    doc.SaveAs(os.getcwd() + "\ew_support" + "\\" + directory + "\\" + new_name)
    #close the stream
    doc.Close()
def do_replace(search_str, replace_str):
    find = word.Selection.Find
    find.ClearFormatting()
    find.Replacement.ClearFormatting()
    find.Text = search_str
    find.Replacement.Text = replace_str
    find.Forward = True
    find.Wrap = constants.wdFindContinue
    find.MatchWildcards = True
    find.Execute(Replace= constants.wdReplaceAll)
def find_docs(directory):
    #look at what's local
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file[0] != "~" and (file[-3:] == "doc" or file[-4:] == "docx"):
                process(directory, file)
def main():
    if not os.path.exists(os.getcwd() + "\ew_support"):
        os.mkdir(os.getcwd() + "\ew_support")
    for directory in dir_list:
        find_docs(directory)
    word.Quit()
    print("Complete!")
if __name__ == "__main__":
    main()
```

Thanks for reading!
