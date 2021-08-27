Fs = 5000;                  % Sampling frequency(The number of times the SIGNAL is SENT per second)  
T = 1/Fs;                   % Sampling period       
L = 1000;                   % Length of signal
measurement_time = T*L;     % measurement_time
A = 1;                      % amplitude


t = (0:T:measurement_time-T)' ;
x1 = A*sin(2*pi*100*t) + A*sin(2*pi*350*t) ;
x2 = A*sin(2*pi*100*t) + A*sin(2*pi*150*t) ;

x3 = A*sin(2*pi*80*t).*sin(2*pi*1500*t) ; %modulated signal

S1 = [t,x1];
S2 = [t,x2];
S3 = [t,x3];