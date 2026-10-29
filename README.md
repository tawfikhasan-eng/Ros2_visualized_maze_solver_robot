# ROS 2 Mobile Robot Navigation in CoppeliaSim

A small robotics project that simulates a mobile robot navigating a maze
in **CoppeliaSim** using **ROS 2**. It contains three main parts:

1.  **CoppeliaSim simulation** --- the scene and simulation-side code.
2.  **ROS 2 control node** --- receives robot/sensor information,
    decides how the robot should move, and sends movement commands.
3.  **2D path visualization** --- plots the path followed by the robot.

## Requirements

-   CoppeliaSim
-   ROS 2 (use the distribution configured for this project)
-   The ROS 2 packages/dependencies used by the control node
-   Python plotting dependencies used by the 2D path script

> Before running, make sure CoppeliaSim and ROS 2 are configured to
> communicate with each other, and that the required ROS 2
> interface/plugin or bridge used by this project is enabled.

## Files

Replace the example filenames below with the actual filenames in this
repository.

-   `maze_scene.ttt` --- CoppeliaSim scene and simulation code
-   `maze_controller.py` --- ROS 2 control node
-   `plot_path` --- script that draws the robot's path in 2D

## How to Run

### 1. Start the CoppeliaSim simulation

1.  Open CoppeliaSim.
2.  Open the project scene file from `maze_scene`.
3.  Check that the simulation-side script and the ROS 2 communication
    setup are enabled.
4.  Start the simulation.

### 2. Run the ROS 2 control node

If the controller is part of a ROS 2 workspace, build and source the
workspace:

``` bash
cd "folder name in which files are in"
colcon build
source install/setup.bash
```

Then run the node using the command appropriate for this project. For a
Python ROS 2 package, it may look like:

``` bash
ros2 run <"package name"> <"maze_controller node">
```

If the node is a standalone Python script instead, run it with the
project's documented command, for example:

``` bash
python3 <controller_script.py>
```

### 3. Plot the robot's 2D path

After the robot has generated path data, open another terminal and run
the visualization script:

``` bash
python3 <path_plot_script.py>
```

If the plot script reads a saved data file, make sure that file exists
at the path expected by the script.

## Notes

-   Run the simulation first, then the ROS 2 controller, and finally the
    path visualization when path data is available.
-   Exact commands depend on the filenames, ROS 2 package structure, and
    communication method used by the project.
-   If there is any issue mail me at ahmedtawfik20007@gmail.com
