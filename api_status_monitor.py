import sys
import os
import httplib
import urllib


class PushoverSender:
    def __init__(self, user_key, api_key):
        self.user_key = user_key
        self.api_key = api_key

    def send_notification(self, text):
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        post_data = {'user': self.user_key, 'token': self.api_key, 'message': text}
        conn.request("POST", "/1/messages.json",
                     urllib.urlencode(post_data), {"Content-type": "application/x-www-form-urlencoded"})
        # print(conn.getresponse().read())


class APIStatusMonitor:

    def __init__(self, pushover_sender, endpoint):
        self.pushover_sender = pushover_sender
        self.endpoint = endpoint

    def check_api_status(self, report_when_happy):
        conn = httplib.HTTPSConnection(self.endpoint)
        conn.request("GET", "/api/status")

        response = conn.getresponse()

        if not response.status == 200:
            self.pushover_sender.send_notification("ATTENTION: Monitor ==> {0}".format(response.status))
        else:
            if report_when_happy:
                self.pushover_sender.send_notification('Monitor is happy.')


def get_key(filename):
    with open(filename) as f:
        key = f.read().strip()
    return key


def main():
    # Get Pushover keys from files
    user_key = get_key(os.path.join(os.path.dirname(__file__), 'user.key'))
    api_key = get_key(os.path.join(os.path.dirname(__file__), 'apitoken.key'))

    # Get API Endpoint from files
    endpoint = get_key(os.path.join(os.path.dirname(__file__), 'endpoint.key'))

    status_monitor = APIStatusMonitor(PushoverSender(user_key, api_key), endpoint)

    if len(sys.argv) > 1 and sys.argv[1] == 'report':
        status_monitor.check_api_status(True)
    else:
        status_monitor.check_api_status(False)


if __name__ == '__main__':
    main()