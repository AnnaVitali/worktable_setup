include "disjunctive.mzn";
include "alldifferent_except.mzn";
include "diffn.mzn";
include "increasing.mzn";

int: capacity;
int: max_resources;
int: max_positions;

set of int: POSITIONS = 1..max_positions;
set of int: OBJECT = 1..max_resources;

array[OBJECT] of int: object_size_in_x;
array[POSITIONS] of int: position_profit;

array[OBJECT] of var -1..max_positions: object_x;

% -1 indicates that the object hasn't been selected
constraint alldifferent_except(object_x, {-1});

% the space occupied by objects must not exceed the total capacity
constraint sum(i in OBJECT where object_x[i] != -1)(object_size_in_x[i]) <= capacity;

% we want as output the value of the coordinates in increasing order
constraint increasing(object_x);

%objects must not overlap
constraint forall(i in 1..max_resources - 1 where object_x[i] != -1 /\ object_x[i + 1] != -1)
           (object_x[i] + object_size_in_x[i] < object_x[i + 1]);

%profit-maximising positions must be prioritised
solve maximize sum(i in OBJECT where object_x[i] != -1)(position_profit[object_x[i]])
