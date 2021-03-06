%test the CTDDP algorithm on some dynamical systems:

%% Inverted pendulum problem from the CTDDP paper for comparison
clear; clc;

[fIP,jIP,hIP] = InvertedPendulum(); %Get the dynamics and jacobian
x0 = [pi,;0];
xf = [0;0];
%Cost functions
Qf = diag([100,10])/1000;
R = 0.1/1000;
lagrange = @(x,u) u.'*R*u;
mayer = @(t,x) x.'*Qf*x;
constraints = [];
grad.lagrange = @(x,u) [zeros(1,2),R*u];
grad.mayer = @(x)(Qf*x)';
hess.lagrange = @(x,u) [zeros(2,3);[zeros(1,2),2*R]];
hess.mayer = @(t,x) 2*Qf;
hess.dynamics = hIP;

%Set the bounds
bounds.upper.finalTime = 0.5;
bounds.lower.finalTime = 0.5;
bounds.upper.initialState = x0;
bounds.lower.initialState = x0;
bounds.upper.finalState = xf; 
bounds.lower.finalState = xf;
bounds.lower.control = -inf;
bounds.upper.control = inf;
OCP = OptimalControlProblem(fIP, lagrange, mayer, constraints, bounds,jIP,grad, hess);
OCP.dimension.adjoint = 0; %This means we will treat the final conditions as a soft constraint

%Call the solver
sol = CTDDP(OCP,0);
figure
plot(sol.time,sol.control)
figure
plot(sol.time,sol.state)
legend('Position','Velocity')