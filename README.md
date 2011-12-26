Simple implementation of the Knight's Tour problem.

It uses a cool heuristic.  Take a look at line 73.  With that present, it 
finds a result very quickly, generating a graph like the one at 
http://imgur.com/a/Ycrng#pEIWc

Without that line, it struggles mightily to search the exponentially-large 
space, and produces something more like this graph:
http://imgur.com/a/Ycrng#VEJHS

Cool, huh?
