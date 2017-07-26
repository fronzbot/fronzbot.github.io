%% Kevin Fronczak
%  EE703 - Matrix Methods
%  Project #2 Due Oct. 8th 2012

function [ B ] = rotate_3D( A, axis, angle )
% This function rotates an object about var axis by var angle (degrees)
    angle = degtorad(angle); % MATLAB works with radians, not degrees
    switch(axis)
        case('x')
            R = [1 0 0; 0 cos(angle) -sin(angle); 0 sin(angle) cos(angle)];
            B = R*A;
        case('y')
            R = [cos(angle) 0 sin(angle); 0 1 0; -sin(angle) 0 cos(angle)];
            B = R*A;
        case('z')
            R = [cos(angle) -sin(angle) 0; sin(angle) cos(angle) 0; 0 0 1];
            B = R*A;
        otherwise
            % Do Nothing
    end
end
