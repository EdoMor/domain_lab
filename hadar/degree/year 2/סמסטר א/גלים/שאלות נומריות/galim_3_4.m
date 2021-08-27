dt = 0.003;
N = 2^11;

% time vecter
if mod(N,2)==0
    t=((-N/2):1:(N/2-1))*dt;
else
    t=((-(N-1)/2):1:((N-1)/2))*dt;
end

% freq vecter
if mod(N,2)==0
    f=(-1:(2/N):(1-1/N))*1/(2*dt);
else
    f=((-(N-1)/2):1:((N-1)/2))/(N*dt);
end
df=f(2)-f(1);

w = 4*pi;
% x01 = (cos(w*t)).^3;
x02 = (3/2)*cos(w*t)-((cos(w*t)).^3);


% FFT
u=fftshift(fft(ifftshift(x02)))*dt;
%inverse transform
x2=fftshift(ifft(ifftshift(u)))/dt;

figure;
subplot(2,1,1);
plot(f,real(u), f,imag(u),f,abs(u),'linewidth',4);legend('real','imag','abs');
xlabel('frequency (Hz)');
ylabel('amplitude (a.u.)');
xlim([-15, 15])


subplot(2,1,2);
plot(t,x02,'.b'); hold on; plot(t,real(x2),'g'); %note -assumes real signal
legend('original','F^{(-1)}F[original]');
xlabel('time (sec)');
ylabel('amplitude (a.u.)');
title ('original and FFT^-1(FFT(original))');


