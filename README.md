# IDNCheck

IDNcheck performs safety checks on international domain names.
This might be useful if you want to see how likely a given domain
is to be used for nefarious purposes such as phishing.
It returns the unicode restriction level passed by a string, as described
in Unicode Technical Standard #39, Unicode Security Mechanisms (see References).

## How to use

Typical usage might look something like this:

    python
    >>> import idncheck
    >>> idncheck.idncheck("hello")
    1
    >>> idncheck.idncheck("φilosoφia")
    42
    >>> idncheck.idncheck("φilosoφia", 3) # FIXME
    True
    >>> idncheck.idncheck("paypal")
    1
    >>> idncheck.idncheck("paypаl")
    4
    >>> idncheck.idncheck("раура1")
    4

or

    #!/usr/bin/env python

    import idncheck

    idncheck.idencheck("φilosoφia", 3): # FIXME
        print("I see what you're doing there")


## References

This tool serves as an implementation of the Restriction-Level detection described
in Unicode Technical Standard #39, Unicode Security Mechanisms: 

- [TR 39](http://www.unicode.org/reports/tr39/#Restriction_Level_Detection)


Additional use cases and details are available in these blog posts:

- [Gmail post](http://googleonlinesecurity.blogspot.com/2014/08/protecting-gmail-in-global-world.html)
- [Another Google post](http://googleenterprise.blogspot.com/2014/08/protecting-gmail-in-global-world.html)

## TODO

- Create a web service on a Gandi Python Simple Hosting instance

