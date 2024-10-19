from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the saved deep learning model
model = load_model('my_model.h5')

# Serve the home page
@app.route('/')
def home():
    return render_template('index.html')  # This will render your index.html from the templates folder


@app.route('/recommend', methods=['GET'])
def recommend():
    city = request.args.get('city')  # Get city from the URL query string
    print(f"City received: {city}")  # Log the city to the terminal
    
    if not city:
        return jsonify({"error": "City not specified"}), 400

    # Generate recommendations using the deep learning model
    try:
        recommendations = get_recommendations(city)
        print(f"Recommendations: {recommendations}")  # Log recommendations
    except Exception as e:
        print(f"Error during recommendation generation: {e}")  # Log any errors
        return jsonify({"error": "Recommendation error"}), 500

    # Return the recommendations as JSON
    return jsonify(recommendations)

import pandas as pd

def get_recommendations(city):
    if city == 'newyork':
        all_restaurants = [
            {
                "name": "Double Chicken Please", 
                "description": "A contemporary take on traditional American dishes, featuring expertly crafted chicken-centric meals.", 
                "image": "double_chicken_please.jpeg", 
                "price": "$35.00 per meal", 
                "rating": "★★★★★",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            },
            {
                "name": "Juliana’s Pizza", 
                "description": "Famous for its coal-fired pizzas, Juliana’s offers an authentic New York pizza experience.", 
                "image": "julianas_pizza.jpeg", 
                "price": "$25.00 per pizza", 
                "rating": "★★★★☆",
                "url": "https://julianaspizza.com/"
            },
            {
                "name": "Roberta's", 
                "description": "A well-known Brooklyn staple, Roberta’s delivers delightful wood-fired pizzas and modern cuisine.", 
                "image": "robertas.jpeg", 
                "price": "$30.00 per pizza", 
                "rating": "★★★★☆",
                "url": "https://www.robertaspizza.com/"
            },
            {
                "name": "Red Hook Tavern", 
                "description": "A rustic gastropub with a welcoming ambiance, offering a diverse range of craft beers and hearty meals.", 
                "image": "red_hook_tavern.jpeg", 
                "price": "$40.00 per meal", 
                "rating": "★★★★☆",
                "url": "https://www.redhooktavern.com/"
            },
            {
                "name": "The House", 
                "description": "A charming historic carriage house turned restaurant serving New American cuisine in an intimate setting.", 
                "image": "the_house.jpeg", 
                "price": "$45.00 per meal", 
                "rating": "★★★★★",
                "url": "https://wearethehouse.com/"
            }
        ]
    elif city == 'mumbai':
        all_restaurants = [
            {
                "name": "Leopold Cafe", 
                "description": "A historical and iconic cafe in Mumbai known for its lively atmosphere.", 
                "image": "leopold_cafe.jpeg", 
                "price": "₹500 per meal", 
                "rating": "★★★★★",
                "url": "https://www.instagram.com/leopoldcafemumbai/?hl=en"
            },
            {
                "name": "Bademiya", 
                "description": "Famous street food joint known for its kebabs and rolls.", 
                "image": "bademiya.jpeg", 
                "price": "₹200 per roll", 
                "rating": "★★★★☆",
                "url": "https://bademiya.com/"
            },
            {
                "name": "Bombay Canteen", 
                "description": "A chic eatery serving modern Indian cuisine.", 
                "image": "bombay_canteen.jpeg", 
                "price": "₹1,200 per meal", 
                "rating": "★★★★★",
                "url": "https://thebombaycanteen.com/"
            },
            {
                "name": "Britannia & Co.", 
                "description": "A legendary Parsi restaurant serving some of the best Berry Pulao in town.", 
                "image": "britannia_co.jpeg", 
                "price": "₹800 per meal", 
                "rating": "★★★★☆",
                "url": "https://www.instagram.com/britannia_co/?hl=en"
            },
            {
                "name": "Cafe Mondegar", 
                "description": "A vibrant cafe known for its eclectic murals and jukebox.", 
                "image": "cafe_mondegar.jpeg", 
                "price": "₹600 per meal", 
                "rating": "★★★★☆",
                "url": "https://www.instagram.com/cafemondegar/"
            }
        ]
    elif city == 'london':
        all_restaurants = [
            {
                "name": "Dishoom", 
                "description": "A Bombay-inspired restaurant serving flavorful Indian dishes.", 
                "image": "dishoom.jpeg", 
                "price": "£20 per meal", 
                "rating": "★★★★★",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            },
            {
                "name": "Honest Burgers", 
                "description": "A cozy spot for handcrafted burgers made with fresh ingredients.", 
                "image": "honest_burgers.jpeg", 
                "price": "£15 per burger", 
                "rating": "★★★★☆",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            },
            {
                "name": "Duck & Waffle", 
                "description": "Offering a unique experience with British and European cuisine at a high-rise location.", 
                "image": "duck_waffle.jpeg", 
                "price": "£40 per meal", 
                "rating": "★★★★★",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            },
            {
                "name": "Sketch", 
                "description": "An elegant restaurant known for its afternoon tea and Michelin-star dining.", 
                "image": "sketch.jpeg", 
                "price": "£60 per meal", 
                "rating": "★★★★★",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            },
            {
                "name": "Flat Iron", 
                "description": "A favorite for steak lovers, serving delicious cuts at affordable prices.", 
                "image": "flat_iron.jpeg", 
                "price": "£12 per steak", 
                "rating": "★★★★☆",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            }
        ]
    elif city == 'paris':
        all_restaurants = [
            {
                "name": "Le Jules Verne", 
                "description": "A Michelin-starred restaurant located inside the Eiffel Tower, offering a fine dining experience with a view.", 
                "image": "le_jules_verne.jpeg", 
                "price": "€250 per meal", 
                "rating": "★★★★★",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            },
            {
                "name": "Cafe de Flore", 
                "description": "A classic Parisian cafe known for its rich history and lively ambiance.", 
                "image": "cafe_de_flore.jpeg", 
                "price": "€30 per meal", 
                "rating": "★★★★☆",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            },
            {
                "name": "Epicure", 
                "description": "A luxurious 3-Michelin-star restaurant offering gourmet French cuisine.", 
                "image": "epicure.jpeg", 
                "price": "€350 per meal", 
                "rating": "★★★★★",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            },
            {
                "name": "Angelina", 
                "description": "Famous for its hot chocolate and traditional pastries.", 
                "image": "angelina.jpeg", 
                "price": "€15 per pastry", 
                "rating": "★★★★☆",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            },
            {
                "name": "Guy Savoy", 
                "description": "An acclaimed Michelin-star restaurant known for its refined French dishes.", 
                "image": "guy_savoy.jpeg", 
                "price": "€280 per meal", 
                "rating": "★★★★★",
                "url": "https://doublechickenplease.com/?srsltid=AfmBOophI_Zg5rUxSP7D9y6BJnNFCRd0kFZwnf0Yx4BQjiC2XOTstVGY"
            }
        ]
    else:
        all_restaurants = [{"error": "No recommendations available for this city"}]

    return all_restaurants



if __name__ == "__main__":
    app.run(debug=True)
