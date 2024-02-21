# 2 16

from flask import Flask, render_template, abort 
from data import tours, departures


app = Flask(__name__) 


@app.route("/")
def render_main(): 
	return render_template("index.html", hotels=tours)


@app.route("/departures/<departure>/")
def render_departures(departure): 
	data = {key: value for key, value in tours.items() if value["departure"] == departure }
	count = len(data) 
	min_price = min([value["price"] for key, value in data.items()])
	max_price = max([value["price"] for key, value in data.items()])
	min_night = min([value["nights"] for key, value in data.items()])
	max_night = max([value["nights"] for key, value in data.items()])

	return render_template(
		"departure.html", 
		hotels=tours, 
		departure=departure,
		count=count, 
		min_price=min_price, 
		max_price=max_price, 
		min_night=min_night,
		max_night=max_night
	)


@app.route("/tours/<int:id>/")
def render_tours(id): 
	if id > len(tours) or type(id) == str:
		abort(404)

	return render_template(
		"tour.html", 
		title=tours[id]["title"], 
		stars=int(tours[id]["stars"]),
		country=tours[id]["country"],
		departure=departures[tours[id]["departure"]], 
		description=tours[id]["description"], 
		price=tours[id]["price"]
	)


@app.route("/data/")
def render_data(): 
	html = "<h1>Все туры</h1>"
	for i, j in tours.items(): 
		html += f"""<p>{j['country']}: <a href='/data/tours/{i}'>{j['title']} {j['price']} {j['stars']}*</a></p>"""
	return html


@app.route("/data/departures/<departure>/")
def render_data_departures(departure):
	html = f"<h1>Туры по направлению {departures[departure].split()[1]}</h1>" 
	for i, j in tours.items(): 
		if j["departure"] == departure: 
			html += f"""<p>{j['country']}: <a href='/data/tours/{i}'>{j['title']} {j['price']} {j['stars']}*</a></p>"""
	return html


@app.route("/data/tours/<int:id>/")
def render_data_tours(id): 
	data = tours[id]
	html = f"""
		<h1>{data['country']}: {data['title']} {data['price']}:</h1>
		<p>{data['nights']} ночей</p>
		<p>Стоимость: {data['price']}</p>
		<p>{data['description']}</p>
	"""
	return html


@app.errorhandler(404)
def render_error(error): 
	return render_template("error.html")



if __name__ == "__main__": 
	app.run()

