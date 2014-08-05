
How it works
===============
I went with worker-manager architecture, but maybe I should have gone with
something less classist? Peer-to-peer connections are annoying because
of port blocking of various sorts, but that would be nice because then I
don't need to be responsible. Well anyway, here's how it works.

Asking for directions
-----------------------
The worker contacts the manager asking for a job. It provides the following
information.

Username
    Chosen by the user
Password-like thing
    Hash of a salted installation ID, which is created when the program is first run
IP address (implicitly)
    The manager is able to determine the IP address from which the request came.

The username is there so that the person can be recognized for her efforts.

The password-like thing is there to trace provenance of the data. This is
mainly here in case someone fakes the data, so that I can figure out which
data not to trust. It could also be helpful for debugging issues specific to
certain systems.

The IP address is used for determining whether the rate limit is close to being
reached. The manager directs workers not to query the Delaware site if they are
approaching rate limit. The IP address is wholy separate from username and
installation ID, as the same IP address can be accessed by multiple devices
associated with the same user and by devices associated with multiple users.

Receiving work orders
--------------------------
In response to the above directions request,
the worker will receive either a status code of 429
(too many requests) or a status code of 200. The manager decides which one
based on how many requests have come from this IP address recently.

If the manager provides a status code of 200, it also provides the following
information.

File number
    The company to look up
An IP address
    This will be passed back to the manager for rate limiting purposes.

The IP address is the worker's own IP address, but it needed to contact the
manager to figure that out. 

The file number is chosen randomly (with uniform weights) from the file numbers
with the lowest amount of responses so far.

For example, all file numbers (0 to 8 million) are possible when we start because
there have been zero responses so far. Soon, some file numbers will be selected,
so there will be some file numbers with zero responses and some with one response.
Once all file numbers have been chosen at least once, the manager will begin
repeating file numbers. By repeating file numbers, we check for consistency between
different responses (in case someone is trying to fake data), and we continue to
update the data (in case companies change).

I chose this approach so that we can be intelligent about which file numbers
we query without assigning jobs to particular workers.

Querying the website
----------------------
Once the bot has been directed to look up a particular file number, it queries
the Deleware corporations site accordingly. It goes to the starting page for
the General Information Name Search (called ``home`` in the code). It enters
the file number and receives a list of up to one company. (This page is called
a ``search`` in the code.) It then goes to this maybe-company page (called
``result`` in the code).

At every step, the bot

1. minimally parses the web page so that it may advance to the next step,
2. sends information about the HTTP response to the manager
3. pauses randomly for a time on the order of a second to avoid looking so obviously like a bot

When it sends the response information to the manager,

"Before" IP address
    The previous IP address that the manager told the worker
Current IP address (implicitly)
    The IP address that the manager currently detects from the worker
Simplified HTTP response from Delaware
    This the main information that we are looking for.
Whether the request appeared successful
    Based on a rough parse, the worker says whether the request was successful. The manager uses this for selecting file numbers for job assignments (in the first step of the process)

Saving information on the manager
---------------------------------------
XXX FIX THIS SECTION XXX

When the manager recieves a response, it first needs to determine an
additional piece of information. The worker has provided the "before"
IP address; the manager now determines the "after" IP address.

Having determined this, it writes the following stuff to a simple log file.

* username
* installation id
* before ip address
* after ip address
* serialized request

It also saves the IP address(es) in an IP address table. We maintain this
table so we can avoid exceeding thresholds for IP blocking. If the before
and after IP addresses are different, we conservatively count the request
as having come from both addresses.

Finally, it parses the file number from the response and updates the
sampling weights for the file number selection.

A separate process comes along later, reads the log files, and reads more
information from the response. The involved parsing is moved to a separate
task for two main reasons. First, this reduces the load of the manager.
Second, we can reuse the separate task for loading backups; we don't need
to write a separate thing for that.

Waiting
--------------
The worker waits a random time on the order of seconds before
repeating the above process. This way, the bots may look a bit less like
bots and thus be harder to block.

Questions you might have
============================
Why not just in-browser Javascript?
    We can't make cross-domain requests, so we'd have to inject something into the Deleware page, and that's annoying, especially for this site.

Doesn't OpenCorporates already have it?
    OpenCorporates doesn't have it.

Have people done similar things in terms of this distibuted API?
    Probably

Why Python rather than something that people with Windows can run?
    Because it's easier

Has anyone tried talking to Delaware?
    Dunno

How many companies?
    Dunno, but less than 600,000

Other references
===================

* https://delecorp.delaware.gov/tin/FieldDesc.jsp#FILE%20NUMBER
* http://corp.delaware.gov/directwebvend.shtml

To do
=========

Do now
-----------

Add a global rate limit to avoid denying the service of the website;
if we get like over 9,000 workers running at once, instruct many of them
not to work for a little while so that we don't crash Delaware's server.

The rate-limit query on the database isn't working. Fix it.

Figure out what the actual rate limit is. Or just stick with something
arbitrary and low. One company takes about two requests, and we're
searching a range of 8 million companies; 1600 requests per IP address
per day would give us one pass in 10,000 IP-address-days. That's about
three months with 100 IP addresses.

Do later
-----------------
Invent a confidence measure for the validity of a response, to deal
with faked data. I think this would be based on the salted installation
identifier, manual assessments of samples of the responses, and a look
at the various components of the request.

Switch the user agent to be a link to a website with an explanation for
the Delaware people of what is going on. (It currently has a link to the
page on PyPI, which is okay for now.)

Package it for people who don't have Python.

* http://www.pyinstaller.org/
* https://pypi.python.org/pypi/py2app/
* http://www.py2exe.org/

Allow results to be sent to multiple servers, as a backup in case something
goes wrong with the main server. (For configuration
`this <http://stackoverflow.com/a/11866695>`_ will help.)
