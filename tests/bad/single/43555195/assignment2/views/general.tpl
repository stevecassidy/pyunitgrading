% rebase('base.tpl')
% import interface

         % if posts:

             % for post in posts:
             <article>
                 <div id="postid">
                     <img src="{{post[3]}}"><br>
                     <a href="\users\{{post[2]}}">{{post[2]}}</a><br>
                         {{post[1]}}<br>
                 </div>
                 <div id="postcontent">
                    {{!interface.post_to_html(post[4])}}
                 </div>
             </article>
             % end
