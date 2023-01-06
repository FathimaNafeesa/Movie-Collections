from movie_collection.checkvulnerabilty.check_vulnerability import CheckVulnerability

event = {
    'name': "user-4",
    'email': "user-4@gmail.com"
}


def lambda_handler(event, context):
    if event['name'] and event['email']:
        status = CheckVulnerability(event['name'], event['email']).execute()
        return {
            'statusCode': 200,
            'body': status
        }


if __name__ == '__main__':
    lambda_handler(event, "context")
