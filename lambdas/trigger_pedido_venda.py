import json
import boto3

step_functions = boto3.client('stepfunctions')

def main(event, context):
    try:
        message = event['Records'][0]['body']
        
        response = step_functions.list_state_machines()
        
        if 'stateMachines' in response and len(response['stateMachines']) > 0:
            target_state_machine = None
            for state_machine in response['stateMachines']:
                if 'PedidoStateMachine' in state_machine['name']:
                    target_state_machine = state_machine
                    break
          
            if target_state_machine:
                response = step_functions.start_execution(
                    stateMachineArn=target_state_machine['stateMachineArn'],
                    input=json.dumps({"message": message})
                )
                
                return {
                    'statusCode': 200,
                    'body': json.dumps('Step Function started')
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error starting Step Function: {}'.format(str(e)))
        }
