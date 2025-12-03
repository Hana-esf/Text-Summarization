from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flasgger import Swagger, swag_from
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows all origins. You can customize it if needed.
# Configuring the SQLite database path
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)
db = SQLAlchemy(app)
swagger = Swagger(app)

# Define the Model
class SummaryModel(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    original_text = db.Column(db.Text, nullable=False)
    is_file = db.Column(db.Boolean, nullable=False, default=False)
    file_path = db.Column(db.String(255))
    summarized = db.Column(db.Text)
    score = db.Column(db.Float)
    created_date:datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    minsize = db.Column(db.Integer, nullable=False)
    maxsize = db.Column(db.Integer, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Helper function to validate input data
def validate_input(data, fields):
    missing_fields = [field for field in fields if field not in data]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"
    return True, None

# Helper function to validate file type
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process_text', methods=['POST'])
@swag_from({
    'summary': 'Process the provided text and return the ID of the created summary.',
    'parameters': [
        {
            'name': 'original_text',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'original_text': {'type': 'string'},
                    'minsize': {'type': 'integer'},
                    'maxsize': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Summary created successfully'}
    }
})
def process_text():
    data = request.json
    is_valid, error_message = validate_input(data, ['text','minsize','maxsize'])
    
    if not is_valid:
        return jsonify({'error': error_message}), 400

    original_text = data['text']
    minsize = data['minsize']
    maxsize = data['maxsize']
    # Simulate summarization (replace with actual logic)
    summarized = original_text[:maxsize] + "..." if len(original_text) > 50 else original_text

    summary = SummaryModel(
        original_text=original_text,
        minsize=minsize,
        maxsize=maxsize,
        is_file=False,
        summarized=summarized
    )
    
    db.session.add(summary)
    db.session.commit()

    return jsonify({'id': summary.id})

@app.route('/process_file', methods=['POST'])
@swag_from({
    'tags': ['Summary'],
    'description': 'Process file to create a summary',
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'PDF or text file to be summarized'
        }
    ],
    'responses': {
        200: {
            'description': 'Summary created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'example': 'd290f1ee-6c54-4b01-90e6-d701748f0851'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input or file not allowed',
        }
    }
})
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    minsize = request.json['minsize']
    maxsize = request.json['maxsize']
    is_valid, error_message = validate_input(request.json, ['text','minsize','maxsize'])
    
    if not is_valid:
        return jsonify({'error': error_message}), 400
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Only PDF and text files are permitted.'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Save the file locally
    file.save(file_path)

    # Simulate summarization from file content (replace with actual logic)
    with open(file_path, 'r') as f:
        original_text = f.read()

    summarized = original_text[:50] + "..." if len(original_text) > 50 else original_text
    
    summary = SummaryModel(
        original_text=original_text,
        minsize=minsize,
        maxsize=maxsize,
        is_file=False,
        summarized=summarized
    )
    
    db.session.add(summary)
    db.session.commit()

    return jsonify({'id': summary.id})

@app.route('/rate_summary/<string:id>', methods=['PUT'])
@swag_from({
    'tags': ['Summary'],
    'description': 'Rate the summarized text',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the summary to rate'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'score': {
                        'type': 'number',
                        'format': 'float',
                        'example': 8.5
                    }
                },
                'required': ['score']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Summary rated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'example': 'd290f1ee-6c54-4b01-90e6-d701748f0851'
                    },
                    'score': {
                        'type': 'float',
                        'example': 8.5
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input or score already assigned',
        },
        404: {
            'description': 'Summary not found',
        }
    }
})
def rate_summary(id):
    data = request.json
    is_valid, error_message = validate_input(data, ['score'])
    if not is_valid:
        return jsonify({'error': error_message}), 400

    score = data['score']

    if not isinstance(score, (int, float)) or not (0 <= score <= 10):
        return jsonify({'error': 'Score must be a number between 0 and 10'}), 400

    summary = SummaryModel.query.get(id)
    
    if not summary:
        return jsonify({'error': 'Summary not found'}), 404

    if summary.score is not None:
        return jsonify({'error': 'Score has already been assigned and cannot be reassigned'}), 400

    summary.score = score
    db.session.commit()

    return jsonify({'id': summary.id, 'score': summary.score})

@app.route('/get_summary/<string:id>', methods=['GET'])
@swag_from({
    'tags': ['Summary'],
    'description': 'Get the summary data by ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the summary to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Summary retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'example': 'd290f1ee-6c54-4b01-90e6-d701748f0851'
                    },
                    'original_text': {
                        'type': 'string',
                        'example': 'This is the original text that was summarized.'
                    },
                    'is_file': {
                        'type': 'boolean',
                        'example': False
                    },
                    'file_path': {
                        'type': 'string',
                        'example': 'uploads/file.txt'
                    },
                    'summarized': {
                        'type': 'string',
                        'example': 'This is the summarized text...'
                    },
                    'score': {
                        'type': 'float',
                        'example': 8.5
                    },
                    'created_date': {
                        'type': 'string',
                        'example': '2024-08-04T12:34:56'
                    }
                }
            }
        },
        404: {
            'description': 'Summary not found',
        }
    }
})
def get_summary(id):
    summary:SummaryModel = SummaryModel.query.get(id)
    
    if not summary:
        return jsonify({'error': 'Summary not found'}), 404

    return jsonify({
        'id': summary.id,
        'original_text': summary.original_text,
        'is_file': summary.is_file,
        'file_path': summary.file_path,
        'summarized': summary.summarized,
        'score': summary.score,
        'minsize': summary.minsize,
        'maxsize': summary.maxsize,
        'created_date': summary.created_date.isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
