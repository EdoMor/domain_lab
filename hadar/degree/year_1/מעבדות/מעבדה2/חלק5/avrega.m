function [av,ep,em]=avrega(x)
xmaxl=islocalmax(x);
xminl=islocalmin(x);
xmax=x(xmaxl);
xmin=x(xminl);
if length(xmin)<=length(xmax)
    xmax=xmax(1:length(xmin),1);
elseif length(xmin)>=length(xmax)
    xmin=xmin(1:length(xmax),1);
end
av=mean((abs(xmax)+abs(xmin))/2);
ep=max((abs(xmax)+abs(xmin))/2)-av;
em=av-min((abs(xmax)+abs(xmin))/2);
end