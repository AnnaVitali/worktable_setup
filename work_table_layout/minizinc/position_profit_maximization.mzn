int: capacity;

int: max_resources;
int: security_distance;

int: number_of_object;
set of int: OBJECT = 1..number_of_object;

array[OBJECT] of int: object_sizes;
array[OBJECT] of int: object_profit;

array[OBJECT] of var 0..1: object_selected;

constraint sum([object_sizes[i] * object_selected[i] | i in OBJECT]) <= capacity;
constraint sum([object_selected[i] | i in OBJECT]) <= max_resources;
constraint forall(i in OBJECT where object_selected[i] == 1)
           (
              forall(ds in 1..(object_sizes[i] - 1) where i + ds in OBJECT)
              (object_selected[i + ds] == 0)
           );
           
solve :: int_search(object_selected, first_fail, indomain_min) maximize sum(i in OBJECT)(object_profit[i] * object_selected[i])
