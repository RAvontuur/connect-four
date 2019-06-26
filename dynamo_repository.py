from boto3 import resource
from botocore.exceptions import ClientError

class DynamoRepository:
    def __init__(self, region='eu-west-1'):
        self.dynamodb = resource(service_name='dynamodb', region_name=region)
        self.target_dynamo_table = "plays"
        self.table = self.dynamodb.Table(self.target_dynamo_table)

    def update_play(self, play_id, state):
        return self.table.update_item(
            Key={'PlayId': play_id},
            ExpressionAttributeValues={':state': state},
            UpdateExpression="set PlayState = :state")

    def read_play(self, play_id):
        try:
            response = self.table.get_item(Key={'PlayId': play_id})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']['PlayState']