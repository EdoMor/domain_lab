% mat8
% 1)
function a=randit1(n,m,evenonly,p,q)
if nargin<4
    p=0;q=99;
end

if evenonly==true
    if ((q-p+1)/2)<(m*n)
        disp('לא ניתן לבנות מטריצה')
    else
    a=2*(round(((q-p)/2).*(rand(n,m)))+round(p/2));
    
    d=sort(a(:));
    g=sum(logical(diff(d)));
    
      while g<(numel(d)-1)
            a=2*(round(((q-p)/2).*(rand(n,m)))+round(p/2));
         d=sort(a(:));
         g=sum(logical(diff(d)));
      end
    end
else
    if (q-p+1)<(m*n)
        disp('לא ניתן לבנות מטריצה')
    else
    a=round((q-p).*(rand(n,m)))+round(p);
    d=sort(a(:));
    g=sum(logical(diff(d)));
    
      while g<(numel(d)-1)
        a=round((q-p).*(rand(n,m)))+round(p);
         d=sort(a(:));
         g=sum(logical(diff(d)));
      end
    end
   
end
% randit1(4, 5, true, 10, 40)
% לא ניתן לבנות מטריצה
% randit1(3,5, true, 10, 40)

% ans =
% 
%     30    20    18    40    24
%     12    22    26    32    16
%     38    36    14    34    28


% 2)
function n=diff2(v)
% DIFF2(V): if v is a vector, the function returns the last difference other than 0.
% if v is a matrix, the same is done per line and the function returns a vector with the value per line.
% If the vector or matrix row is not such, 0 will be returned where
% appropriate.
while diff(v,1,2)~=false(size(diff(v,1,2)))
v=diff(v,1,2);
n=v(:,1);
end
t=numel(v(1,:));
b=diff(v,t-1,2);
a=logical(b); 
n(a==1)=0

%  v=[1 4 9 16 25 36 49
%      1 8 27 64 125 216 343
%      1 2 3 4 5 6 7 
%      4 7 3 2 0 8 1];
%  
%     diff2(v);
% n =
% 
%      3
%      7
%      1
%      0
