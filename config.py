WTF_CSRF_ENABLED = True
SECRET_KEY = """Maybe it's the way she walked (wow)
Straight into my heart and stole it
Through the doors and past the guards (wow)
Just like she already owned it
I said, "can you give it back to me?"
She said, "never in your wildest dreams"
And we danced all night to the best song ever
We knew every line, now I can't remember
How it goes but I know that I won't forget her
'Cause we danced all night to the best song ever
I think it went oh, oh, oh
I think it went yeah, yeah, yeah
I think it goes (ooh)
Said her name was Georgia Rose (wow)
And her daddy was a dentist
Said I had a dirty mouth (I got a dirty mouth)
But she kissed me like she meant it
I said, "can I take you home with me?"
She said, "never in your wildest dreams"
And we danced all night to the best song ever
We knew every line, now I can't remember
How it goes but I know that I won't forget her
'Cause we danced all night to the best song ever
I think it went oh, oh, oh
I think it went yeah, yeah, yeah
I think it goes (ooh)
You know, I know, you know I'll remember you
And I know, you know, I know you'll remember me
And you know, I know, you know I'll remember you
And I know, you know, I hope you'll remember
How we danced, how we danced (one, two, one, two, three)
How we danced all night to the best song ever
We knew every line, now I can't remember
How it goes but I know that I won't forget her
'Cause we danced all night (we danced, we danced)
To the best song ever (it goes something like, yeah)
And we danced all night to the best song ever
We knew every line, now I can't remember
How it goes but I know that I won't forget her
'Cause we danced all night to the best song ever
I think it went oh, oh, oh
I think it went yeah, yeah, yeah
I think it goes (ooh)
Best song ever
It was the best song ever
It was the best song ever
It was the best song ever"""

#if deployed keep session_cookie_secure as True
SESSION_COOKIE_SECURE = True


import os


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
