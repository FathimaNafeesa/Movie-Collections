import requests
from checkvulnerabilty.check_vulnerability import CheckVulnerability


class WebhookTriggers:
    def __init__(self):
        pass

    def trigger_password_vulnerability_test_(self, name, email):
        webhook = 'https://b297-96-79-235-37.ngrok.io/webhooks/v1/webhook/a26f63d4-bbde-4fcc-812a-c747f9c534e6/CaptureUserInfo'
        data = {
            "user_details": {
                "name": name,
                "email": email
            }
        }

        return requests.post(url=webhook, json=data, verify=False)

    def task_api_action(self, name, email):
        return CheckVulnerability(name, email).execute()

    def trigger_test_(self):
        webhook = 'https://j6vvu2bvwi.execute-api.ap-northeast-1.amazonaws.com/dev/movie_collection/create_task/'
        data = {
                "name": 'name',
                "email": 'email',
                "actual_password":"dddddd"
            }

        return requests.post(url=webhook, json=data, verify=False)

if __name__ == '__main__':
    print(WebhookTriggers().trigger_test_())
