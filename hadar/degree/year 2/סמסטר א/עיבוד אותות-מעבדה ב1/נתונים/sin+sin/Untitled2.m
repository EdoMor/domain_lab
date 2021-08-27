a=0; b=79.51; c=11.628; d=-30; e=18.72;

S = xlsread('150+500.xlsx');
x = S(8:end,1);

y = a+(b+0.5.*sin(500.*x)).*0.5.*sin(150.*x)+(b+0.5.*sin(150.*x)).*0.5.*sin(500.*x)...
+0.5.*((c+0.5.*sin(500.*x)).*((0.5^2).*(sin(150.*x)).^2)+4*b.*(0.5.^2).*sin(150.*x).*sin(500.*x)...
+(b+0.5.*sin(150.*x)).*((0.5.^2).*(sin(500.*x)).^2))+(1/6).*((d+0.5.*sin(500.*x)).*(0.5.*sin(150.*x)).^3 ...
+3.*(b+c).*((0.5.*sin(150.*x)).^2).*0.5.*sin(500.*x)+3.*(b+c).*((0.5.*sin(500.*x)).^2).*0.5.*sin(150.*x)...
+(d+0.5.*sin(150.*x)).*(0.5.*sin(500.*x)).^3)+(1/24).*((e+0.5.*sin(500.*x)).*(0.5.*sin(150.*x)).^4 ...
+4.*(d+b).*((0.5.*sin(150.*x)).^3).*(0.5.*sin(500.*x))+12*c*((0.5.*sin(150.*x)).^2).*(0.5.*sin(500.*x).^2)...
+4*(b+d).*((0.5.*sin(500.*x)).^3).*(0.5.*sin(150.*x))+(e+0.5.*sin(150.*x)).*(0.5.*sin(500.*x)).^4);

Fs = 5000;                 % Sampling frequency(The number of times the SIGNAL is SENT per second)  
T = 1/Fs;                   % Sampling period       
L = 1000;                   % Length of signal
measurement_time = T*L;     % measurement_time
 
figure
Y = fft(y);
f = 1/measurement_time*(1:L/2);
amp = abs(Y(1:L/2));
plot(f,amp)

