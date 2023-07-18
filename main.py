import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Define the Crunchbase API endpoint
url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/searches/organizations"

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "1b2826a25dmsh9d86c195a8439afp1a1b81jsn1ff37b2ff8f0",
    "X-RapidAPI-Host": "crunchbase-crunchbase-v1.p.rapidapi.com"
}

@app.route('/organizations', methods=['GET'])
def get_organizations():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'No company name provided'}), 400

    payload = {
        "field_ids": ["identifier", "location_identifiers", "short_description", "rank_org"],
        "limit": 50,
        "order": [
            {
                "field_id": "rank_org",
                "sort": "asc"
            }
        ],
        "query": [
            {
                "field_id": "location_identifiers",
                "operator_id": "includes",
                "type": "predicate",
                "values": ["6106f5dc-823e-5da8-40d7-51612c0b2c4e"]
            },
            {
                "field_id": "facet_ids",
                "operator_id": "includes",
                "type": "predicate",
                "values": ["company"]
            },
            {
                "field_id": "identifier",
                "operator_id": "contains",
                "type": "predicate",
                "values": [name]
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    organizations = []
    for entity in data['entities']:
        org_data = {
            'uuid': entity['uuid'],
            'name': entity['properties']['identifier']['value'],
            'image': entity['properties']['identifier']['image_id'],
            'description': entity['properties']['short_description'],
            'rank': entity['properties']['rank_org'],
            'locations': [location['value'] for location in entity['properties']['location_identifiers']]
        }
        organizations.append(org_data)
    return render_template('organizations.html', organizations=organizations)

if __name__ == '__main__':
    app.run()
