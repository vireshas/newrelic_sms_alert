NewRelic alerts via SMS
=========================

    With NewRelic webhooks, one can write a custom web app to play with alerts.  
    Here is an attempt to send an SMS whenever we receive an alert.  
    
    NewRelic doesnt give us an interface to add users to a plugin's alerts, this  
    project gives a web and REST api based interface to manage users data and   
    plugin alerts.

    Change settings.py.sample and run python webhook.py. If python complains about missing  
    librarys, install them and re-run the command. It starts a service at port 8080. Use  
    something like runscope.com if you want to test it with newrelic before deploying.  
    With runscope.com, you can quickly expose a localservice to public.  

    Learn about creating webhook channels in newrelic. Create a channel for webhook and when you create  
    a new alert policy add this webhook as a alert channel.
