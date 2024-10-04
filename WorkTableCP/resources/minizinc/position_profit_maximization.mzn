include "alldifferent_except.mzn";
include "diffn.mzn";
include "increasing.mzn";

int: capacity;
int: max_resources;
int: max_positions;

set of int: POSITION = 1..max_positions;
set of int: OBJECT = 1..max_resources;

array[OBJECT] of int: object_size;
array[POSITION] of int: position_profit;

array[OBJECT] of var 0..max_positions: object_position;

array[OBJECT] of var 0..1: object_selected;

% the space occupied by objects must not exceed the total capacity
constraint sum(i in OBJECT)(object_size[i] * object_selected[i]) <= capacity;

% we want as output the value of the coordinates in increasing order
constraint increasing(object_position);

%objects must not overlap
constraint forall(i in 1..max_resources - 1)((object_position[i]+ object_size[i]) * object_selected[i] < object_position[i + 1]);

% don't work beacause dimensions are not variable but parameters, library treats dimensions as variables
%constraint diffn(object_x, [0 | i in OBJECT], object_size_in_x,  [0 | i in OBJECT]);

%old constraint with -1
%constraint forall(i in 1..max_resources - 1)
%           ((object_x[i] != -1 /\ object_x[i + 1] != -1) -> object_x[i] + object_size_in_x[i] < object_x[i + 1]);

%profit-maximising positions must be prioritised
solve maximize sum(i in OBJECT)(position_profit[object_position[i]] * object_selected[i])
