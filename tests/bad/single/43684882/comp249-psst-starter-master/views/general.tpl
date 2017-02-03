% rebase('base.tpl')

%for post in content:
<img src="{{post[3]}}" height = "240px" width = "240px">
{{post[1]}} {{post[2]}} {{!post[4]}}</article> <br>
% end