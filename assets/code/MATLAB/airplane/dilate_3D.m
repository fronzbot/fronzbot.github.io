%% Kevin Fronczak
%  EE703 - Matrix Methods
%  Project #2 Due Oct. 8th 2012

function [ B ] = dilate_3D( A, values )
% This function dilates an object by values in the x, y and z directions

D = eye(3);
D(1,1) = values(1);
D(2,2) = values(2);
D(3,3) = values(3);

B = D*A;

end
