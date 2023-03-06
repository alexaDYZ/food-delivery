This documnet is about the modeling of walking.

## Implementation 
fucntions defined in Rider() class:
1. find_walking_dest(rest_list)
   - given a walking rule, find the destination of walking
   - input: **rest_list**. 
   - output: **rest_loc**
2. moveTo(start_loc, dest_loc)
   - excute the action of walking.
   - input: **start_loc**, **dest_loc**, both in euclidian coordinates in a 2-D grid
   - output: generate rider arrival event, when rider arrives at **dest_loc**
3. getLocation(currTime)
   - given a certain time, return the riders location
