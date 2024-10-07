## What is this script?
The purpose of this script is to help with creating a summarized biographical source material for SillyTavern AI frontend's "data bank" that utilizes RAG.
I figured there's no better source material for a historical AI character's "lore" than a massive, 700-page biography. The problem with this is that there's
unnecessary dialogue that does nothing but fills the chunks with irrelevant information. This script splits the source (ebook) material into digestable
chunks for whatever Ollama LLM you're using and prompts it to spit out the relevant details for a summarized historical "data bank".

Feel free to play around with the prompt. The current one is not very good, but it works.


## There's tons of duplicate entries in the output data
Yes, the method is not very good, and it's a WIP. Still yet to figure a way for deduplication.


## The data is all over the place, it can't possibly work with RAG?
Figuring out a way to group the data by meaningful topics and/or keywords is a WIP. It does work as it is if you pull multiple entires with RAG, but it's not perfect, and sometimes
you get nonsensical garbage from it that the character uses in a weird way. In my experience, this only gets exacerbated when you something like XTC to filter out the GPT-ism.

## Why hepburn.epub?
I love Audrey Hepburn, and I'll make a believable AI character card of her, or die trying.

## Usage
```
python -m venv /path/to/venv
source /path/to/venv/bin/activate (activate.fish on fish)
pip install requirements.txt
python parse_epub.py <path/to/source.epub> <path/to/output.txt>
```
