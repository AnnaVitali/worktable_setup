include "alldifferent_except.mzn";
include "diffn.mzn";
include "increasing.mzn";
include "knapsak.mzn";

int: capacity;
int: max_resources;
int: max_positions;

set of int: POSITIONS = 1..max_positions;
set of int: OBJECT = 1..max_resources;

array[OBJECT] of int: object_size_in_x; %weight
array[POSITIONS] of int: position_profit; %profit_for_position;

var int: profit;
var int: weight;
var int: W;
var int: P;

array[OBJECT] of var 0..max_positions: object_x;

array[OBJECT] of var 0..1: selected;

constraint profit = sum([position_profit[object_x[i]] * selected[i] | i in OBJECT]);
constraint weight = sum([object_size_in_x[object_x[i]] * selected[i] | i in OBJECT]);


% -1 indicates that the object hasn't been selected
%constraint alldifferent_except(object_x, {0});

% the space occupied by objects must not exceed the total capacity
constraint W <= capacity;

% we want as output the value of the coordinates in increasing order
constraint increasing(object_x);

%objects must not overlap
%constraint forall(i in 1..max_resources - 1)((object_x[i]+ object_size_in_x[i]) * selected[i] < object_x[i + 1]);
%constraint diffn(object_x, [0 | i in OBJECT], object_size_in_x,  [0 | i in OBJECT]);
%constraint forall(i in 1..max_resources - 1)
%           ((object_x[i] != -1 /\ object_x[i + 1] != -1) -> object_x[i] + object_size_in_x[i] < object_x[i + 1]);

constraint knapsak(weight, profit, object_x, W, P);

%profit-maximising positions must be prioritised
solve maximize P %sum(i in OBJECT)(position_profit[object_x[i]] * selected[i])
