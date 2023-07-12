import json
import requests

import quart
import quart_cors
from quart import request

url = 'https://api.sheety.co/f5c895111f00b6e7890112005cf20758/movies/sheet1'

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.get("/search")
async def get_search():
    args = request.args
    genre = args.get('genre')
    year = args.get('year')

    if genre is not None and not genre.isdigit():
        response = requests.get(url+"?filter[genre]="+genre)
    elif genre is not None and genre.isdigit():
        response = requests.get(url+"?filter[year]="+genre)
    elif year is not None and year.isdigit():
        response = requests.get(url+"?filter[year]="+year)
    else:
        response = requests.get(url)
    data = response.json()
    return quart.Response(response=json.dumps(data), status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
