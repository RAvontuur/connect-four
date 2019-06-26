from boto3 import resource

class DynamoRepository:
    def __init__(self, region='eu-west-1'):
        self.dynamodb = resource(service_name='dynamodb', region_name=region)
        self.target_dynamo_table = "plays"
        self.table = self.dynamodb.Table(self.target_dynamo_table)

    def update_dynamo_play(self, play_id, state):
        return self.table.update_item(
            Key={'PlayId': play_id},
            ExpressionAttributeValues={':state': state},
            UpdateExpression="set PlayState = :state")
