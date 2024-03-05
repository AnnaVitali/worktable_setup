int: workpiece_width;
set of int: WIDTH = 1..workpiece_width;

int: workpiece_height;
set of int: HEIGHT = 1..workpiece_height;

array[HEIGHT, WIDTH] of int: workpiece_processing;

array[HEIGHT, WIDTH] of var -1..workpiece_width * workpiece_height: workpiece_heat_map;

constraint forall(j in WIDTH where workpiece_processing[1, j] == 0)(workpiece_heat_map[1, j] = 2);
constraint forall(j in WIDTH where workpiece_processing[workpiece_height, j] == 0)
                 (workpiece_heat_map[workpiece_height, j] = 2);

constraint forall(i in HEIGHT where workpiece_processing[i, 1] == 0)(workpiece_heat_map[i, 1] = 2);
constraint forall(i in HEIGHT where workpiece_processing[i, workpiece_width] == 0)
                 (workpiece_heat_map[i, workpiece_width] = 2);
                 
constraint forall(i in HEIGHT, j in WIDTH where workpiece_processing[i, j] != -1)
                 (workpiece_heat_map[i, j] >= 1);
                 
% suction cups should not be under pass-through processing
constraint forall(i in HEIGHT, j in WIDTH where workpiece_processing[i,j] == -1)
          (
           forall(dr in -1..1, dc in -1..1 
           where i + dr in HEIGHT /\ j + dc in WIDTH /\ workpiece_heat_map[i + dr, j + dc] != -1)
            (
              workpiece_heat_map[i + dr, j + dc] = 2
            )
          );

constraint forall(i in HEIGHT, j in WIDTH where workpiece_processing[i,j] == -1)
          (
           workpiece_heat_map[i, j] = -1
          );

constraint forall(i in HEIGHT, j in WIDTH where workpiece_processing[i,j] == 2)
          (
           workpiece_heat_map[i, j] = 2
          );
