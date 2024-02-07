## About The Project
<p>Sometimes your favourite TV-show files become un-ordered and you were too bored to make them ordered and named properly. 
So it should be a tool that can make this for you, right?
<p>I believe this utility task coud be made in different ways, but let's play with trending ML-tools and test them!

### Warning
This repo is just <b>a working proto</b> written for a manual run on Linux (Ubuntu), please use at <b>your own risk</b> and make sure you have your <b>data backuped</b>.

### Pre-history
<p>My favourite TV-show series files become lost because of corrupted drive, but I was able to re-store most of the media with help of <a href='https://en.wikipedia.org/wiki/PhotoRec'>PhotoRec</a>. As a start point I have a list of media files named like <i>'f[0-9*].mkv'</i>

But I need them sorted by a season and renamed properly like <i>'TV show name - sXXeXX - Episode name.mkv'</i>

So the idea was to get subtitles from the Internet and use them as a source, as they are usually named like <i>'TV-show-name - sXXeXX - Episode name.srt'</i>, so I can get all needed data: TV-show name, Season number, Episode number, Episode name and subtitles. I just need something that can transcript speach from the video into text and compare it with subtitles.

### Built With

* basic <b>Shell</b> scripting (made for use on Ubuntu, not cross-platform)
* basic <b>Python</b> scripting
* <b>ffmpeg</b>: to prepare sound fragments
* <b>openai/whisper</b>: a general-purpose speech recognition model to transcript sound fragments
* <b>Redis Stack</b>: to store data and make vector-based search
* <b>SentenceTransformers</b> framework: to generate embeddings on text
* <b>python-colorcodes</b> class: to make text print fancy


## Getting Started

All needed packages I've installed locally to make hands dirty, but I believe the same goal could be achieved using Google Colab. You can use this awesome tutorial [Similarity Search with Redis as a Vector Database](https://github.com/RedisVentures/redis-vss-getting-started/blob/main/vector_similarity_with_redis.ipynb) as an example of how to use Redis as Vector database on Google Colab.

### Prerequisites

1. Installed <b>Python</b>
2. Python librares: [Pandas](https://pandas.pydata.org/getting_started.html), [redis-py](https://redis-py.readthedocs.io/en/stable/), [NumPy](https://numpy.org/install/), [sentence_transformers](https://www.sbert.net/docs/installation.html)
3. Installed [Redis Stack](https://redis.io/docs/install/install-stack/)
4. Installed [openai/whisper](https://github.com/openai/whisper)
5. Installed [ffmpeg](https://ffmpeg.org/download.html)

### Dataset

1. Copy subtitles files (now it should work with filenames like <i>'TV-show-name - sXXeXX.srt'</i>) into <code>dataset/subtitles</code> directory
2. Copy video files into <code>dataset/video</code> directory, no subfolders allowed. At the moment it works with one predefined file extension.
3. Adjust video files extension variable [VIDEO_EXT] at <i>dataroutine.sh</i> file.

## Usage

Run start.sh file
   ```sh
   ./start.sh
   ```

If successfull, check results.csv file: it should contains video filename, computed season number, computed subtitles filename and score. You can use this file as a source to sort and rename your files.

### Notes

* <b>FFMPEG</b>: I'm extracting 30 seconds of audio (in my case starting from 1:30 minute) just to make it faster to analyze by whipser, but it's more wise to use longer sound fragments
* <b>Whisper</b>: [Base English model](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages) is in use
* <b>SentenceTransformers</b>: I've played with [several models](https://huggingface.co/sentence-transformers) and found that [sentence-t5-base model](https://www.sbert.net/docs/pretrained_models.html) is most accurate on my dataset (short sentences conversations)
* Final results: 90% accuracy on 61 row dataset. There is a room to improve :-)
