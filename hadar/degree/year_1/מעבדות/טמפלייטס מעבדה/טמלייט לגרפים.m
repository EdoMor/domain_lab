x = %vector;
y = %vector;
eror_xpos = %vector;
eror_xneg = %vector;
eror_ypos = %vector;
eror_yneg = %vector;
figure
errorbar(x,y,eror_yneg,eror_ypos,eror_xneg,eror_xpos,'.','color','b','LineWidth',1)
set(gca,'FontSize',14)
xlable = 'xxx';
ylable = 'xxx';
xlabel(xlable,'FontSize',16)
ylabel(ylable,'FontSize',16)
title('xxx')
xlimL = %number;
xlimR = %number;
ylimL = %number;
ylimR = %number;
ylim([ylimL,ylimR])
descripthion1 = 'xxx';
descripthion2 = 'xxx';
legend(descripthion1, descripthion2)
box on
grid on
    
    