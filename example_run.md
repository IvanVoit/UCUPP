# Example run

This is a real example of UCUPP in action, using fictional lab data —
none of this corresponds to a real person.

## Input

```
$ python3 ucupp.py

[+] Enter the target's information (leave blank if not applicable)

> First name: John
> Surname: Doe
> Nickname: johnny
> Pet's name: Rex
> Child's name: Alex
> Partner's name:
> Company name: AcmeCorp
> Extra keywords, comma-separated:

[+] Dates (DDMMYYYY format, leave blank if not applicable)

> Target's birthdate: 15061990
> Partner's birthdate:
> Child's birthdate:
> Enable leetspeak? (Y/n): Y
> Combine words with dates? (Y/n): Y
> Maximum number of combinations [800000]:
> Output file name [ucupp_output.txt]: example_output.txt
```

## Output

```
[+] Generating combinations, this may take a few seconds...

[+] Done. Generated 20250 combinations.
[+] Saved to: example_output.txt
```

## Verification

With this input, UCUPP does generate cross-combined entries such as:

```
j0hn_1990
John1990
johnny-15061990
J0hnny.1990!
1990_john
```

Unlike classic CUPP, which with the exact same input data does **not**
produce `j0hn_1990`, because it doesn't combine its leetspeak mode with
date fragments using separators.

## Using the output with John the Ripper

```bash
sudo unshadow /etc/passwd /etc/shadow > /tmp/hashes.txt
john --wordlist=example_output.txt /tmp/hashes.txt
john --show /tmp/hashes.txt
```
