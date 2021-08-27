p22=p2(122:1232);
t22=t2(122:1232);
p33=p3(682:1681);
t33=t3(682:1681);
p44=p4(282:1102);
t44=t4(282:1102);
p55=p5(402:873);
t55=t5(402:873);
p66=p6(562:1509);
t66=t6(562:1509);
p77=p7(522:1089);
t77=t7(522:1089);
p88=p8(882:1453);
t88=t8(882:1453);
p99=p9(322:1783);
t99=t9(322:1783);
p1010=p10(842:1459);
t1010=t10(322:1459);

w12=[2 3 4 2.25 2.5 3.5 2.75 2.85 2.9];
    
[av2,ep2,em2]=avrega(p22);
[av3,ep3,em3]=avrega(p33);
[av4,ep4,em4]=avrega(p44);
[av5,ep5,em5]=avrega(p55);
[av6,ep6,em6]=avrega(p66);
[av7,ep7,em7]=avrega(p77);
[av8,ep8,em8]=avrega(p88);
[av9,ep9,em9]=avrega(p99);
[av10,ep10,em10]=avrega(p1010);

ampl12=[av2 av3 av4 av5 av6 av7 av8 av9 av10];
EPampl=[ep2 ep3 ep4 ep5 ep6 ep7 ep8 ep9 ep10];
EMampl=[em2 em3 em4 em5 em6 em7 em8 em9 em10];

figure
errorbar(w12,ampl12,EMampl,EPampl,Ew,Ew,'.','Color','b','LineWidth',2)
set(gca,'FontSize',14)
title('spring 1 with mass 2 Amplitude as a function of The excitation frequency')
xlabel('Frequency(seconds^{-1})','FontSize',16)
ylabel('Amplitude','FontSize',16)
box on
grid on



