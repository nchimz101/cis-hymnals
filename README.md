# Multilingual Hymnal API

## Overview
A FastAPI-powered service for accessing hymn collections across multiple languages.

## Features
- Multi-language hymnal support
- Flexible hymn retrieval
- Simple, intuitive REST API

## Supported Languages
- English
- Tswana
- Sotho
- Chichewa
- Tonga
- Shona
- Venda
- Swahili
- And more... (full list in `/languages` endpoint)

## Prerequisites
- Python 3.8+
- FastAPI
- Uvicorn

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/hymnal-api.git

# Navigate to project directory
cd hymnal-api

# Install dependencies
pip install -r requirements.txt
```

## Running the API
```bash
# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints
- `GET /languages`: List all available languages
- `GET /hymnals/{language_key}`: Get hymns for a language
- `GET /hymnals/{language_key}/{number}`: Get specific hymn

## Query Parameters
- `min_number`: Filter minimum hymn number
- `max_number`: Filter maximum hymn number

## Example Requests
```
# Get all English hymns
/hymnals/english

# Get English hymns between 10-20
/hymnals/english?min_number=10&max_number=20

# Get specific hymn
/hymnals/english/15
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit changes
4. Push to the branch
5. Create pull request
6. Make sure you check if the file content is valid and that the hymns render as expected here [Hymnal Previewer](https://previewer-psi.vercel.app/)


## License
## License

    Copyright 2025 Nchimunya Munyama
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
       http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and limitations under the License.



## Copyright info
The copyrights for each hymnal belong to the respective publishing houses.


  
