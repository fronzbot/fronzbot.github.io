%% Kevin Fronczak
%  EE703 - Matrix Methods
%  Project #2 Due Oct. 8th 2012

function [  ] = plot_3D_object( original, A, title )
% Plot 3D object of 3xn size
X = A(1,:);
Y = A(2,:);
Z = A(3,:);

figure('name', title)
plot3(X,Y,Z, original(1,:), original(2,:), original(3,:))
axis equal
xlabel('X-axis')
ylabel('Y-axis')
zlabel('Z-axis')

end
