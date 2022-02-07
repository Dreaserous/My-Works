#! /usr/bin/python3

import random
import string



def main():
    print("How many tracks?")
    track_count  = int(input())

    print("How long are the tracks?")
    track_length = int(input())

    print("Random seed?")
    seed = input()

    if seed == "":
        seed = random.randint(10**5, 2**32)
        print(f"No seed provided, we will use the seed {seed}.")
    else:
        seed = int(seed)
        print(f"Initializing the random seed to {seed}.")

    random.seed(seed)
    print()

    yard = build_yard(track_count, track_length)
    for track in yard:
        track += '-' * (track_length-len(track))
        track  = track[::-1]
        print("-"+track+"-")



def build_yard(track_count, track_length):
    assert track_count >= 3
    assert track_count <= 27     # if we have more than 27 tracks, we might have more than 26 destinations
    assert track_length >= 3

    dest_count = random.randint(2, track_count-1)
    names = string.ascii_lowercase[:dest_count]

    print(dest_count)
    print(names)

    # we will try to build the tracks randomly.  If we succeed, great; if not,
    # then we'll start again from scratch.
    need_build = True
    while need_build:
        print("Attempting to build the yard...")

        # we'll turn this back on later, if we need a rebuild.
        need_build = False

        retval = [""]*track_count

        for _ in range(dest_count*track_length // 2):
            this_track = random.randint(0,track_count-1)
            this_dest  = random.randint(0, dest_count-1)

            assert len(retval[this_track]) < track_length-1
            retval[this_track] += names[this_dest]

        # assign a location for each of the locomotives.
        locos_placed = 0
        while locos_placed < dest_count:
            loco_track = random.randint(0,track_count-1)
            if len(retval[loco_track]) > 0 and retval[loco_track][0] == 'T':
                continue    # go try again!

            retval[loco_track] = "T" + retval[loco_track]
            locos_placed += 1

        # double-check that every track which has a locomotive *also* has a
        # mix of destinations, so that it doesn't immediately depart.
        for track in retval:
            if len(track) == 0 or track[0] != 'T':
                continue    # no locomotive, so we can skip this track

            destinations = set(track[1:])
            if len(destinations) == 1:     # could be zero, that's harmless
                print("Failed!  There was a track with a locomotive, but with exactly destination.")
                need_build = True
                break

    print(retval)
    print()
    return retval



if __name__ == "__main__":
    main()

