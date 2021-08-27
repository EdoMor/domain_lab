Fs = 5000;                  % Sampling frequency(The number of times the SIGNAL is SENT per second)  
T = 1/Fs;                   % Sampling period       
L = 1000;                   % Length of signal
measurement_time = T*L;     % measurement_time

x1 = xlsread('500hz.xlsx');
x2 = x1(8:end,2);

figure
Y = fft(x2);
f = 1/measurement_time*(1:L/2);
plot(f,abs(Y(1:L/2)))