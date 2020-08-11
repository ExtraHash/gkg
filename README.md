# gkg

Grabs ssh keyfiles for a specified username from the GitHub API and writes them into the authorized_key file of the user.

## usage

`python3 -u ExtraHash -w`

## Flags

```
-u  The username to fetch for
-w  Write to the keyfile. If not appended, keys will be printed to the terminal.
-l  Loops the script forever.
```
