# UCUPP — Ultimate Common User Passwords Profiler

UCUPP is a password wordlist generator based on personal information (name,
surname, birthdates, pets, family members, keywords...), built for security
audits, penetration testing, and cybersecurity learning labs.

It's inspired by the classic [CUPP (Common User Passwords Profiler)](https://github.com/Mebus/cupp),
but fixes one of its biggest limitations: **CUPP doesn't fully combine all
the transformations it applies** (leetspeak, dates, casing, special
characters), so many realistic human passwords — like `j0hn_1990` — never
actually show up in the generated wordlist, even when all the underlying
data is there.

## Why this project exists

While testing on a lab virtual machine, I created a password from fictional
profile data (a name + birth year, with leetspeak and a separator) and found
that CUPP, despite having all the necessary information, couldn't generate
it. Its suffix/prefix lists and leet mode are computed mostly independently
of each other, so they rarely combine into the exact pattern a real user
would actually create. UCUPP exists to close that gap: real, configurable
cross-combination between every variant of the data you provide.

## Advantages over classic CUPP

- **Real cross-combination**: each base word (and its leet / lowercase /
  capitalized / uppercase variants) is combined with every fragment of every
  date provided (day, month, year, short year, and combinations of those),
  in both orders (`word+date` and `date+word`).
- **Configurable separators**: automatically tries no separator, `_`, `-`
  and `.` between word and number — the `name_year` pattern that's extremely
  common in real-world passwords.
- **Special characters at the end**, like CUPP, but applied on top of the
  already cross-combined results, not just on standalone words.
- **Configurable limit** (`max_total`, 800,000 by default) to keep the output
  file at a manageable size and avoid uncontrolled combinatorial explosion.
- **Zero external dependencies**: pure Python 3 standard library, no `pip
  install` required.
- **Works with the same tools** you'd use with a CUPP wordlist: John the
  Ripper, Hashcat, Hydra, etc.

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/ucupp.git
cd ucupp
python3 ucupp.py
```

No extra dependencies needed (Python 3.6+ is enough).

## Usage

```bash
python3 ucupp.py
```

The script will interactively ask for:

- First name, surname, nickname, pet, child, partner, company
- Extra keywords
- Birthdates (`DDMMYYYY` format) for the target, partner, and child
- Whether to enable leetspeak
- Whether to combine words with dates
- The maximum number of combinations to generate
- The output file name

Once done, you'll get a `.txt` file with one candidate password per line,
ready to use with any cracking tool:

```bash
john --wordlist=output.txt hashes.txt
john --show hashes.txt

# or with Hashcat
hashcat -m 1800 -a 0 hashes.txt output.txt

# or with Hydra, e.g. against SSH
hydra -l username -P output.txt ssh://TARGET_IP
```

## Example

See a full example run in
[`examples/example_run.md`](examples/example_run.md).

## ⚠️ Responsible use

This tool generates password wordlists from personal data for the sole
purpose of **auditing the strength of your own passwords, or systems you
have explicit authorization to test** (your own VMs, training labs,
penetration tests with a written, agreed scope).

- Do not use UCUPP against accounts, systems, or people without their
  explicit, documented consent.
- Unauthorized use of tools like this one may be illegal in most
  jurisdictions.
- The authors are not responsible for any misuse of this tool.

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE)
for details.

## Credits

Inspired by [CUPP](https://github.com/Mebus/cupp), by Muris Kurgas and
Mebus.
