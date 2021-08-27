Fs = 5000;                  % Sampling frequency(The number of times the SIGNAL is SENT per second)  
T = 1/Fs;                   % Sampling period       
L = 1000;                   % Length of signal
measurement_time = T*L;     % measurement_time

x1 = xlsread('42.xlsx');
x2 = x1(8:end,2);

figure
Y1 = fft(x2);
f = 1/measurement_time*(1:L/2);
plot(f,(abs(Y1(1:L/2)))+1,'color','r')
set(gca,'YScale','log')
ylim([0,15])
xlable = 'Frequency (hz)';
ylable = 'Voltage (V)';
xlabel(xlable,'FontSize',16)
ylabel(ylable,'FontSize',16)
