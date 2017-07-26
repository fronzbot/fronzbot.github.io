%% Kevin Fronczak
%  EE703 - Matrix Methods
%  Project #2 Due Oct. 8th 2012

%% Aircraft definition
aircraft = [...
    0.00  0.00  0.00;
    0.25  0.50  0.00;
    0.75  0.80  0.00;
    1.00  1.00  0.00;
    2.00  1.00  0.00;
    3.00  3.00  0.00;
    3.25  3.40  0.00;
    3.50  3.40  0.00;
    4.00  3.50  0.00;
    3.25  1.00  0.00;
    5.00  1.00  0.00;
    5.75  1.50  0.00;
    5.85  1.50  0.00;
    6.00  0.00  0.00;
    6.00  0.00  0.00; % Negative y reflection
    5.85 -1.50  0.00;
    5.75 -1.50  0.00;
    5.00 -1.00  0.00;
    3.25 -1.00  0.00;
    4.00 -3.50  0.00;
    3.50 -3.40  0.00;
    3.25 -3.40  0.00;
    3.00 -3.00  0.00;
    2.00 -1.00  0.00;
    1.00 -1.00  0.00;
    0.75 -0.80  0.00;
    0.25 -0.50  0.00;
    0.00  0.00  0.00;
    0.50  0.00  0.50; % Z frame
    0.25  0.50  0.00;
    1.00  1.00  0.00;
    0.50  0.00  0.50;
    2.00  0.00  0.50;
    1.00  1.00  0.00;
    2.00  1.00  0.00;
    2.00  0.00  0.50;
    3.25  0.00  0.50;
    3.25  1.00  0.00;
    2.00  1.00  0.00;
    3.25  0.00  0.50;
    5.00  0.00  0.50;
    5.00  1.00  0.00;
    6.00  0.00  0.00;
    5.00  0.00  0.50;
    3.25  1.00  0.00;
    3.25  0.00  0.50;
    5.00  0.00  0.50;
    3.25  0.00  0.50; % Reflect Z
    3.25 -1.00  0.00;
    5.00  0.00  0.50;
    6.00  0.00  0.00;
    5.00 -1.00  0.00;
    5.00  0.00  0.50; 
    5.00 -1.00  0.00;
    5.00  0.00  0.50;
    3.25  0.00  0.50;
    2.00 -1.00  0.00;
    3.25 -1.00  0.00;
    3.25  0.00  0.50;
    2.00  0.00  0.50;
    2.00 -1.00  0.00;
    1.00 -1.00  0.00;
    2.00  0.00  0.50;
    0.50  0.00  0.50;
    1.00 -1.00  0.00;
    0.25 -0.50  0.00;
    0.50  0.00  0.50;
    0.00  0.00  0.00;
    1.00  0.00  0.00; % Bottom
    1.00  1.00  0.00;
    5.00 -1.00  0.00;
    5.00  1.00  0.00;
    1.00 -1.00  0.00;
    1.00  0.00  0.00;
    0.00  0.00  0.00;];

aircraft = aircraft.';

plot_3D_object(aircraft, aircraft, 'Original Aircraft');


%% Dilate by 1.5
new_aircraft = dilate_3D(aircraft, [1.5 1.5 1.5]);
plot_3D_object(aircraft,new_aircraft, 'Dilate by 1.5');


%% Reflect about Y axis
new_aircraft = translate_3D(aircraft, [], 'y');
plot_3D_object(aircraft,new_aircraft, 'Reflect Y-axis');

%% Rotate about X-axis by 60 degrees
new_aircraft = rotate_3D(aircraft, 'x', 60);
plot_3D_object(aircraft,new_aircraft, 'Rotate around X-axis by 60');


%% Yaw 45 degrees (rotate around Z by 45 degrees)
new_aircraft = rotate_3D(aircraft, 'z', 45);
plot_3D_object(aircraft,new_aircraft, 'Yaw of 45');

%% Pitch of 30 degrees (rotate around Y by 30 degrees)
new_aircraft = rotate_3D(aircraft, 'y', 30);
plot_3D_object(aircraft,new_aircraft, 'Pitch of 30');

%% Roll of 30 degrees (rotate around X by 30 degrees)
new_aircraft = rotate_3D(aircraft, 'x', 30);
plot_3D_object(aircraft,new_aircraft, 'Roll of 30');

%% Translate by [10 10 0] -> Rotate X by 30 degrees -> Dilate by 2
N = translate_3D(aircraft, [10 10 0], 0);
N = rotate_3D(N, 'x', 30);
N = dilate_3D(N, [2 2 2]);
plot_3D_object(aircraft,N, 'Translate -> Rotate -> Dilate');

%% Comparison of prev -> Rotate, translate, dilate
N = rotate_3D(aircraft, 'x', 30);
N = translate_3D(N, [10 10 0], 0);
N = dilate_3D(N, [2 2 2]);
plot_3D_object(aircraft,N, 'Rotate X(30) -> Translate YZ(10) -> Dilate 2');

%% Rotate X (30) -> Rotate Y (60) -> Translate Z (10) -> Rotate Z (60)
N = rotate_3D(aircraft, 'x', 30);
N = rotate_3D(N, 'y', 60);
N = translate_3D(N, [0 0 10], 0);
N = rotate_3D(N, 'z', 60);
plot_3D_object(aircraft,N, 'Rotate X(30) -> Rotate Y(60) -> Translate Z(10) -> Rotate Z(60)');
