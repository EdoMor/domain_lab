S = xlsread('42 (1).xlsx');

x = S(8:end,2);
t = S(8:end,1);

plot(t,x)