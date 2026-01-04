from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

MERCADO_PAGO_TOKEN = 'APP_USR-1062188237322463-010320-eedfc0c59fd646c15fd957f7141688b1-131807830'
MERCADO_PAGO_URL = 'https://api.mercadopago.com/checkout/preferences'

@app.route('/create-preference', methods=['POST'])
def create_preference():
    try:
        data = request.json
        
        # Prepare the preference
        preference = {
            'items': [
                {
                    'title': data.get('title', 'Reserva de Cancha'),
                    'quantity': 1,
                    'unit_price': float(data.get('price', 0))
                }
            ],
            'payer': {
                'email': data.get('email', 'cliente@example.com'),
                'name': data.get('name', 'Cliente'),
                'phone': {
                    'number': data.get('phone', '')
                }
            },
            'back_urls': {
                'success': data.get('success_url', 'https://pumpkinhead94.github.io/padel-turnos/'),
                'failure': data.get('failure_url', 'https://pumpkinhead94.github.io/padel-turnos/'),
                'pending': data.get('pending_url', 'https://pumpkinhead94.github.io/padel-turnos/')
            },
            'auto_return': 'approved',
            'binary_mode': True
        }
        
        headers = {
            'Authorization': f'Bearer {MERCADO_PAGO_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Send request to Mercado Pago
        response = requests.post(MERCADO_PAGO_URL, json=preference, headers=headers)
        response.raise_for_status()
        
        preference_data = response.json()
        
        return jsonify({
            'init_point': preference_data.get('init_point'),
            'preference_id': preference_data.get('id')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
