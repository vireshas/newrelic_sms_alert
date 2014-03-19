import urllib
import urllib2
import settings

class Sms:
    smsUrl = settings.smsUrl
    smsParams = settings.smsParams

    def send(self, mobile_no, data, PNR='', txnId=''):
        if(len(data)<= 320):
            sms_post = Sms.smsParams
            sms_post['text'] = data
            sms_post['to'] = mobile_no
            sms_post['pnr'] = PNR
            sms_post['txnid'] = txnId
            print "sending sms to %s message %s" % (mobile_no, data)
            post_data = urllib.urlencode(sms_post)
            req = urllib2.Request(Sms.smsUrl, post_data)
            response = urllib2.urlopen(req)
            print "sms sent %s" % response.read()
            return True
