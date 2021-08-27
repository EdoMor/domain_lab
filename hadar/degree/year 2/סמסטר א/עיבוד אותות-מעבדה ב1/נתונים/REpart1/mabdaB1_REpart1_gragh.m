f1 = xlsread('R100.xlsx'); f2 = xlsread('R200.xlsx'); f3 = xlsread('R300.xlsx'); f4 = xlsread('R400.xlsx');
f5 = xlsread('R500.xlsx'); f6 = xlsread('R700.xlsx'); f7 = xlsread('R1000.xlsx');
f8 = xlsread('R1250.xlsx'); f9 = xlsread('R1500.xlsx'); f10 = xlsread('R2000.xlsx');
f11 = xlsread('R2450.xlsx'); f12 = xlsread('R2500.xlsx'); f13 = xlsread('R2550.xlsx');
f14 = xlsread('R2700.xlsx'); f15 = xlsread('R3000.xlsx'); f16 = xlsread('R3500.xlsx');
f17 = xlsread('R4000.xlsx'); f18 = xlsread('R5000.xlsx'); 


data = [ f1(8:end,2), f2(8:end,2), f3(8:end,2), f4(8:end,2), f5(8:end,2)...
    ,f6(8:end,2), f7(8:end,2), f8(8:end,2), f9(8:end,2), f10(8:end,2)...
    ,f11(8:end,2), f12(8:end,2), f13(8:end,2), f14(8:end,2), f15(8:end,2)...
    ,f16(8:end,2), f17(8:end,2), f18(8:end,2)];

Fs = 5000;                  % Sampling frequency(The number of times the SIGNAL is SENT per second)  
T = 1/Fs;                   % Sampling period       
L = 1000;                   % Length of signal
measurement_time = T*L;     % measurement_time

Y = fft(data);
ampY = abs(Y(1:L/2,:));

f_axis = 1/measurement_time*(1:L/2);

[amp,index] = max(ampY(43:end,:));
f =[];
for i=1:18
    f(i) = f_axis(index(i)+42);
end

distance = [100,200,300,400,500,700,1000,1250,1500,2000,2450,2500,2550,...
                27000,3000,3500,4000,5000];

plot(distance,f,'.','MarkerSize',10)
hold on
plot(0:0.1:2500,0:0.1:2500,'--','color','red','LineWidth',0.5 )
xlable = 'Frequencies sent (hz)';
ylable = 'Frequencies measured (hz)';
xlabel(xlable,'FontSize',16)
ylabel(ylable,'FontSize',16)
title('The frequencies measured as a function of the frequencies sent')
legend('Frequencies', 'Linear fit: y = x','Location','northwest')
xlim([0,4500])
grid on


