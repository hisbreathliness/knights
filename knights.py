# Knight's tour

"""The main data structure used here is the path.  This is a list of x,y
coordinates as 2-element tuples."""

import optparse
import unittest

def get_destinations(x,y):
    """Returns a list of all possible coordinates a knight could move to"""
    dests = [(x + 1, y + 2),
             (x - 1, y + 2),
             (x + 1, y - 2),
             (x - 1, y - 2),
             (x + 2, y + 1),
             (x + 2, y - 1),
             (x - 2, y + 1),
             (x - 2, y - 1)]
    dests = [d for d in dests if (
        d[0] >= 0 and d[0] <= 7 and d[1] >= 0 and d[1] <=7)]
    return dests

def get_path_destinations(path, pt):
    """Returns all possible coodinates that the knight could go to from the point 
    without intersecting the path"""
    dests = get_destinations(*pt)
    dests = [d for d in dests if d not in path]
    return dests
    
def missing_spaces(path):
    """Returns a list of spaces on the chessboard that were not hit in this tour."""
    missing = []
    for x in xrange(0, 8):
        for y in xrange(0, 8):
            spot = (x,y)
            if spot not in path:
                missing.append(spot)
    return missing
    
def path_to_str(path):
    """Stringifies a path data structure in semi-readable form."""
    return "[" + " ".join(["%s,%s" % pt for pt in path]) + "]"
        

def find_tour(x, y):
    """Entry point function -- argument is the coordinates the knight starts at.
    Return value is a tuple of: number of possible moves considered, path that shows
    the knight's tour for that starting point."""
    path = [(x,y)]
    return find_tour_helper(path, get_path_destinations(path, path[-1]))
    
def find_tour_helper(path, dests):
    """ Helper function not meant to be called directly."""
    # the knight is sitting at the last spot in the path, and we just need to
    # decide which of the spots in the dests list it should go to next
    missing = missing_spaces(path)
    if len(missing) == 0:   # end the search when we've covered all the spaces
        return 1, path
    print len(path), len(dests), path_to_str(missing), path_to_str(path)
    # annotate the destinations with a list of the possible moves the knight could make from them
    next_step = [(d, get_path_destinations(path, d)) for d in dests]
    # heuristic (Warnsdorff's rule): the moves which have the least number of
    # subsequent moves, i.e. are the most constrained, are best
    next_step.sort(key=lambda ns: len(ns[1]))
    my_options = 0
    for d, next_dests in next_step:
        newp = list(path)
        newp.append(d)   # "move" the knight by creating a new path with the dest at the end
        options, best = find_tour_helper(newp, next_dests)
        my_options += options
        my_options += len(next_dests)
        if options > 0:
            return my_options, best
        # unstated else clause: if options are 0, newp wasn't a path that lead to
        # a successful result, so we need to try another move at this point
        
    return 0, path  # made it through all our dests without finding a path (or there were 0 dests)


class Tests(unittest.TestCase):
    def test_destinations(self):
        self.assertEqual(get_destinations(0,0), [(1,2), (2,1)])
        
    def test_path_destinations(self):
        self.assertEqual(get_path_destinations([(1,2)], (0,0)), [(2,1)])

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("--test", dest="test", help="Run rudimentary unit tests")
    (options, args) = parser.parse_args()
    if options.test:
        unittest.main()
    else:
        x = 0
        y = 1
        if len(args) > 1:
            x = int(args[0])
            y = int(args[1])
        tour = find_tour(x,y)
        print "Found tour starting from %s,%s considering %s moves:" % (x,y, tour[0])
        print path_to_str(tour[1])
