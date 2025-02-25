Lecture Note Generator
========================
Note generator for the purpose of converting lecture slide PDFs to lined/grid/blank paper with space next to the slides to write your notes.

## Downloads

- [Windows Executable (.exe)](bin/Note%20Generator.exe)
- [MacOS App (.app.zip)](bin/Note%20Generator.app.zip)

If your operating system is not listed here, good luck.

## Preview

![Preview](https://i.imgur.com/30byrUX.png/)

## Generating Executables

```bash
pyinstaller --onefile --noconsole ./AnnotateGenerator/app.py --name="Note Generator" --icon="./AnnotateGenerator/icon.png"
```

## PPTX to PDF on MacOS

This application only accepts PDFs. I use a MacBook. 

You can use an AppleScript to convert PPTX to PDF easily.

Follow the instructions [here](https://github.com/jeongwhanchoi/convert-ppt-to-pdf/blob/master/README.md).

