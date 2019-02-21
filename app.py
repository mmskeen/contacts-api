#!flask/bin/python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

contacts = [
    {
        'id': 1,
        'name': u'John Smith',
        'city': u'Provo',
        'state': u'UT'
    },
    {
        'id': 2,
        'name': u'Jane Doe',
        'city': u'Charlottesville',
        'state': u'VA'
    },
    {
        'id': 3,
        'name': u'Paul Smith',
        'city': u'Provo',
        'state': u'UT'
    },
    {
        'id': 4,
        'name': u'Jessica Doe',
        'city': u'Charlottesville',
        'state': u'VA'
    },
    {
        'id': 5,
        'name': u'Jennifer Doe',
        'city': u'Charlottesville',
        'state': u'VA'
    }
]

@app.route('/contact', methods=['GET'])
def get_contacts():
    pageSize = request.args.get('pageSize', default = 5, type = int)
    page = request.args.get('page', default = 1, type = int)
    query = "j"
    return jsonify({'contacts': get_contacts(pageSize, page, query)})

@app.route('/contact/<name>', methods=['GET'])
def get_contact(name):
    contact = get_singleContact(name)
    if len(contact) == 0:
        abort(404)
    return jsonify({'contact': contact[0]})

@app.route('/contact', methods=['POST'])
def create_contact():
    if not request.json or not 'name' in request.json:
        abort(400)
    name = request.json['name']
    city = request.json.get("city", "")
    state = request.json.get('state', "")
    contact = create_contact(name, city, state)
    if contact is None:
        abort(400)
    return jsonify({'contact': contact}), 201

@app.route('/contact/<name>', methods=['PUT'])
def update_contact(name):
    contact = get_singleContact(name)
    if len(contact) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'city' in request.json and type(request.json['city']) != str:
        abort(400)
    if 'state' in request.json and type(request.json['state']) is not str:
        abort(400)
    city = request.json.get('city', contact[0]['city'])
    state = request.json.get('state', contact[0]['state'])
    update_contact(contact[0], city, state)
    return jsonify({'contact': contact[0]})

@app.route('/contact/<name>', methods=['DELETE'])
def delete_contact(name):
    contact = get_singleContact(name)
    if len(contact) == 0:
        abort(404)
    delete_singleContact(contact[0])
    return jsonify({'result': True})

def delete_singleContact(contact):
    contacts.remove(contact)

def update_contact(contact, city, state):
    contact['city'] = city
    contact['state'] = state

def get_contacts(pageSize, page, query):
    start = (page - 1) * pageSize
    end = page * pageSize
    return contacts[start:end]

def get_singleContact(name):
    return [contact for contact in contacts if contact['name'] == name]

def create_contact(name, city, state):
    contact = {
        'id': contacts[-1]['id'] + 1,
        'name': name,
        'city': city,
        'state': state
    }
    contacts.append(contact)
    return contact

if __name__ == '__main__':
    app.run(debug=True)
