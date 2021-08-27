Fs = 5000;                  % Sampling frequency(The number of times the SIGNAL is SENT per second)  
T = 1/Fs;                   % Sampling period       
L = 1000;                   % Length of signal
measurement_time = T*L;     % measurement_time

x1 = xlsread('42.xlsx');
x2 = x1(8:end,2);
x3 = xlsread('42 (1).xlsx');
x4 = x3(8:end,2);

figure
Y1 = fft(x2);
Y2 = fft(x4);
f = 1/measurement_time*(1:L/2);

subplot(2,1,1)
plot(f,abs(Y1(1:L/2)))
ylim([0,13.5])
subplot(2,1,2)
plot(f,abs(Y2(1:L/2)))
ylim([0,3])
xlable = 'Frequency (hz)';
ylable = '          Voltage (V)';
xlabel(xlable,'FontSize',16)
ylabel(ylable,'FontSize',16)


