# Clustering-docs-and-modeling-topics
Clustering a list of documents and generating topics for each cluster.

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

Make sure you have Python 3 installed on your system.

### Installation

1. Clone this repository to your local machine:

```sh
git clone https://github.com/Sann-Htet/Clustering-docs-and-modeling-topics.git
```

2. Navigate into the project directory:

```sh
cd Clustering-docs-and-modeling-topics
```

3. Create a virtual environment:

```sh
python -m venv .venv
```

4. Activate the virtual environment:

   - On Windows:

     ```sh
     .venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```sh
     source .venv/bin/activate
     ```

5. Install the project dependencies:

```sh
pip install -r requirements.txt
```

### Usage

1. Run the FastAPI application:

```sh
uvicorn api:app --reload
```


2. Once the server is running, you can access the API at `http://127.0.0.1:8000` (by default). Visit this URL in your browser or use tools like Postman to interact with the APIs.

### Testing

You can test the APIs using tools like:

- [Postman](https://www.postman.com/)
- [curl](https://curl.se/)

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for any improvements or fixes.
