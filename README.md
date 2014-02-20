NewRelic alerts via SMS
=========================

    With NewRelic webhooks, one can write a custom web app to play with alerts.  
    Here is an attempt to send an SMS whenever we receive an alert.  
    
    NewRelic doesnt give us an interface to add users to a plugin's alerts, this  
    project gives a web and REST api based interface to manage users data and   
    plugin alerts.

    Change settings.py.sample and run python webhook.py. If python complains about missing  
    librarys, install them and re-run the command. It starts a service at port 8080. Use  
    something like runscope.com, if you want to test it with newrelic, before deploying.  
    With runscope.com, you can quickly expose a localservice to public.  

    Google about creating webhook channels in newrelic. Create a channel for webhook and  
    go to an alert policy(should be found in tools>alert policy) add this webhook as an alert channel.  
    Now whenever an alert is raised from this alert policy, a SMS will be sent to the corresponding users   
    in user channels. A SMS is also sent to the default person that you have configured in settings.

    Any change in settings.py file can be quickly consumed by the app without restarting by sending it  
    a USR1 signal. Ex: ps aux | grep webhook #note down the pid and then run this command,   
    kill -s USR1 pid the service will pick the new set of plugins.   

    Visit localhost:8080/usage, to manage users and to subscribe to a plugin.

##More features:  
    1. Phone call on critical errors
