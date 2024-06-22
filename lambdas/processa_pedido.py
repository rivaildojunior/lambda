import json
import boto3
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PedidoDB')

def main(event, context):
    if 'message' in event:
        message = event['message']
        try:
            event_dict = json.loads(message)
            
            cliente = event_dict.get('cliente')
            items = event_dict.get('items')
            
            if cliente and items:
                total_pedido = sum(item['qtd'] * item['valor'] for item in items)
                
                pedido_id = str(uuid.uuid4())
                
                try:
                    response = table.put_item(
                        Item={
                            'id': pedido_id,
                            'nome_cliente': cliente,
                            'valor_pedido': total_pedido
                        }
                    )
                    print("Dados gravados com sucesso no DynamoDB:", response)
                except ClientError as e:
                    print("Erro ao gravar dados no DynamoDB:", e.response['Error']['Message'])
                
                response = {
                    'statusCode': 200,
                    'body': json.dumps({
                        'cliente': cliente,
                        'valor': total_pedido,
                        'pedido_id': pedido_id
                    })
                }
                return response
            else:
                print("Cliente ou items não foram encontrados na mensagem.")
        except json.JSONDecodeError as e:
            print("Erro ao decodificar JSON:", str(e))
    
    response = {
        'statusCode': 400,
        'body': json.dumps({
            'error': 'Dados inválidos ou faltando no evento'
        })
    }
    return response
