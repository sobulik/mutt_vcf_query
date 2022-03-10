# Description

A simple utility for mutt users to search their contacts stored in a vCard file.

# Usage

Add the following to your .muttrc file
```sh
set query_command = "mutt_vcf_query.py <your_vcf_file> %s"
```
See [Mutt documentation](http://www.mutt.org/doc/manual/#query) for more details.
