import json

def main(event, context):
    try:
        body = event['body']
        body_dict = json.loads(body)
        
        cliente = body_dict.get('cliente')
        valor = body_dict.get('valor')
        pedido_id = body_dict.get('pedido_id')
        
        if cliente and valor and pedido_id:
            print(f"Pedido {pedido_id} no valor de R$ {valor:.2f} enviado para {cliente}")
        else:
            print("Dados incompletos na mensagem.")
    except Exception as e:
        print(f"Erro ao processar a mensagem: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Mensagem processada com sucesso'
        })
    }
