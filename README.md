## About The Project
<p>Sometimes your favourite TV-show files become un-ordered and you were too bored to make them ordered and named properly. 
So it should be a tool that can make this for you, right?
<p>I believe this utility task coud be made in different ways, but let's play with trending ML-tools and test them!

### Pre-history
<p>My favourite TV-show series files become lost becuase of corrupted drive, but I was able to re-store most of the media with help of <a href='https://en.wikipedia.org/wiki/PhotoRec'>PhotoRec</a>. As a start point I just have a list of media files named like <i>'f[0-9*].mkv'</i>

But I need them sorted by a season and renamed properly like <i>'TV show name - sXXeXX - Episode name.mkv'</i>

So the idea is to get subtitles from the Internet and use them as a source, as they are usually named like <i>'TV-show-name - sXXeXX - Episode name.srt'</i>, so I can get all data I need: TV-show name, Season number, Episode number, Episode name and subtitles. I just need something that can transcript speach from the video into text and compare it with subtitles.

### Warning
This repo is just <b>a working proto</b> written for a manual run on Linux (Ubuntu), please use at <b>your own risk</b> and make sure you have your <b>data backuped</b>.

### Built With

* basic <b>Shell</b> scripting (made for use on Ubuntu, not cross-platform)
* basic <b>Python</b> scripting
* <b>ffmpeg</b>: to prepare sound fragments
* <b>openai/whisper</b>: a general-purpose speech recognition model to transcript sound fragments
* <b>Redis Stack</b>: to store data and make vector-based search
* <b>SentenceTransformers</b> framework: to generate embeddings on text


## Getting Started

All needed packages I've installed locally, just to make my hands dirty, but I believe the same goal could be achieved using Google Colab. You can use this awesome tutorial [Similarity Search with Redis as a Vector Database](https://github.com/RedisVentures/redis-vss-getting-started/blob/main/vector_similarity_with_redis.ipynb) as an example of how to use Redis as Vector database on Google Colab, but you will just need to bring your own dataset.

### Prerequisites

1. Installed <b>Python</b>
2. Python librares: <b>[Pandas](https://pandas.pydata.org/getting_started.html)</b>, <b>[redis-py](https://redis-py.readthedocs.io/en/stable/)</b>, <b>[NumPy](https://numpy.org/install/)</b>, <b>[sentence_transformers](https://www.sbert.net/docs/installation.html)</b>
3. Installed <b>[Redis Stack](https://redis.io/docs/install/install-stack/)</b>
4. Installed <b>[openai/whisper](https://github.com/openai/whisper)</b>
5. Installed <b>[ffmpeg](https://ffmpeg.org/download.html)</b> (openai/whisper should install it for you)

### Dataset

1. Copy subtitles files (worked with filename <i>'TV-show-name - sXXeXX - Episode name.srt'</i>) into <code>dataset/subtitles</code> directory
2. Copy video files into <code>dataset/video</code> directory, no subfolders allowed
3. Adjust video files extension variable [VIDEO_EXT](https://github.com/pachopka/seasonep/blob/e96e04645d96b1250f1d92dae54fd4e79513f34e/datasetRoutine.sh#L3) if needed at datasetRoutine.sh file

## Usage

Run executable start.sh file
   ```sh
   ./start.sh
   ```
### Notes

* <b>FFMPEG</b>: I'm extracting 30 seconds of audio (in my case starting from 1:30 minute) just to make it faster to analyze by whipser, but it's more wise to use longer sound fragments and extract them from the 'middle' of the file to make dataset more diversed
* <b>Whisper</b>: [Base model](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages) is in use
* <b>SentenceTransformers</b>: I've played with [several models](https://huggingface.co/sentence-transformers) and found that [sentence-t5-base model](https://www.sbert.net/docs/pretrained_models.html) is most accurate on my dataset (short sentences dialogs)
