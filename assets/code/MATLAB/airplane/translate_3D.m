%% Kevin Fronczak
%  EE703 - Matrix Methods
%  Project #2 Due Oct. 8th 2012

function [ B ] = translate_3D( A, values, reflect )
% This function translates an object by the amount in the values varible.
% Values is a 1x3 array corresponding to translations in the x, y and z
% directions.  Reflect can be 0, x, y, or z.  If 0, no reflection is
% performed.  If x, y, or z, the object is returned reflected about that
% axis (this ignored the translate variables).
    R = -1*eye(3);
    switch(reflect)
        case 'x'
            R(1,1) = 1;
            B = R*A;
        case 'y'
            R(2,2) = 1;
            B = R*A;
        case 'z'
            R(3,3) = 1;
            B = R*A;
        otherwise    
            T = eye(4);
            T(1:3, 4) = values.';
            A = cat(1, A, ones(1,length(A))); % Need to add row for correct dimensionality
            B = T*A;

            B(4,:) = []; % Properly resize matrix
    end

end
