from config import sns_client
from config import celery
from models.push import Push

@celery.task(bind=True)
def send_push(self, message, installations, push_id):
    total = len(installations)
    i = 0
    for installation in installations:
        response = sns_client.publish(
            TargetArn=installation['endpoint_arn'],
            Message=message
        )
        self.update_state(state="PROGRESS", meta={
            'device_id':installation['device_id'],
            'message_id':response['MessageId'],
            'total':total,
            'current':i
        })
        i += 1
    push = Push.query.filter_by(
        uuid=push_id
    ).one_or_none()
    push.sent = True
    push.save()
    return {'device_id':0, 'total':total, 'status':"Completed!", 'current':total, 'message_id':0}
