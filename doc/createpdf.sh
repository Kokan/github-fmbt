#!/bin/bash

pandoc -V title:"Github Pull Request lifecycle test" -V author:"Peter Kokai" -f gfm -o pdf doc/doc.md -o doc/doc.pdf

