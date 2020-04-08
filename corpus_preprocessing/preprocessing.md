# Preprocessing

We will use the uncut version of `0101.html` and `0423uncut.html` instead of `0423.html`.
We won't also use `07outtakes.html`, because it is a transcript of a special out takes episode.

We won't do anything special with the beginning and ending of transcripts for now.

Let us change the stage directions surrounding from `()` to `[]`.

We will use:
 - `iconv` to change the encoding to UTF-8
 - `html2text` to convert html to raw text
 - `sed`, `tr` to edit strings
 - `bash`

This code makes basic preprocessing:
```sh
for file in ./*.html; do
    html2text <(iconv -t UTF-8//IGNORE "$file" | tr '\n' ' ') | sed 's/\*//g' | sed 's/_//g' | sed 's/(/[/g' | sed 's/)/]/g' | sed 's/</[/g' | sed 's/>/]/g' > "${file//html/raw}"
done
```

Now the data is stored in `.raw` files and formatted this way:
```
Phoebe: Do it do it do it!

Monica: [Shouts to the guy] Woo-woo!

[The guy turns round, startled. Monica points to Phoebe. The guy gets hit by a
truck]

Phoebe: I can't believe you did that!

Opening Credits
```
