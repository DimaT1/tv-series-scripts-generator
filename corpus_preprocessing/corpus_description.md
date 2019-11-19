# Corpus Description

Given corpus consists of Friends TV series transcripts, seasons 1-10. That is approximately 900k words.

Complete list of all series can be found in the file `index.html`.

The transcripts are stored as HTML files in the folder `series`. 
Each filename consists of two-numbered season and two-numbered episode.
For example, season 1, episode 23 transcript will be stored in `series/0123.html`.

There are also files `07outtakes.html` and `0423uncut.html`:
 - The file `07outtakes.html` contains the transcript for a special out takes episode of 7th season.
 - The file `0423uncut.html` contains the transcript of the uncut version of Ross's second wedding (season 4, episode 23).

Each file begins with the title, following up with some meta-information: screenwriter, director, transcriber.
The meta-information can also contain some commentaries, transcriber's note, air date, producer name and so on.
All in all, the meta-information block is very unstructured and noisy.
Some transcripts may have no meta-information block at all.
Every transcript ends with "End", "THE END", etc.

Files `0101.html` and `0423uncut.html` have previously unseen parts which are shown in blue (`#0000ff`) text.

Stage directions can be surrounded by `[]` or by `()`.
Stage directions can start from new line and interrupt character's line:
 - Stage direction interrupts character's line if it describes character's actions or feelings.
 - Stage direction starts from new line if it contains some of general descriptions:
   - Scene description
   - Time Lapse
   - Cut
   - Flashback scene
   - Opening Credits
   - Ending Credits

Character's lines always begin with character's name.
Character's names may be bold or uppercase in some transcripts.
Sometimes `All:` is used to indicate that all characters say a line together.

Used encodings are different:
 - text/html; charset=iso-8859-1
 - text/html; charset=unknown-8bit
 - text/html; charset=us-ascii
