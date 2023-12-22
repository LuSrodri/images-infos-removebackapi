# images-infos-removebackapi
API to remove background from images using AI.

## How to use
In a computer with Python, execute follow commands:
- Create a .env file with `X_RAPIDAPI_PROXY_SECRET` value;
- Install venv package `python -m venv venv`;
- In Windows initialize venv `.\venv\Scripts\activate`;
- In Linux initialize venv `source venv/bin/activate`;
- Install dependencies `pip install -r requirements.txt`;
- Run `python app.py` and;
- Enjoy it!

## How it work
We use a pre-trained AI called rembg where the user give a image and is returned a URL hosted in Google Cloud with image without background.
