from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import time
# from main import main

app = Flask(__name__)

# Generate sample graphs
def generate_graph1():
    df = pd.DataFrame({'Category': ['A', 'B', 'C', 'D'], 'Values': [10, 20, 30, 40]})
    fig = px.bar(df, x="Category", y="Values", title="Bar Chart")
    return 
    return fig.to_json()

def generate_graph2():
    df = pd.DataFrame({'X': range(10), 'Y': [x**2 for x in range(10)]})
    fig = px.line(df, x="X", y="Y", title="Line Chart")
    return fig.to_json()

def generate_graph3():
    df = pd.DataFrame({'X': range(10), 'Y': [x**1.5 for x in range(10)]})
    fig = px.scatter(df, x="X", y="Y", title="Scatter Plot")
    return fig.to_json()

# Chatbot API route
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "").strip().lower()
    
    # Simple rule-based chatbot logic
    responses = {
        "hello": "Hi there! How can I assist you?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "what is your name": "I'm a simple chatbot built into this dashboard.",
        "help": "I can answer basic questions. Try asking 'hello' or 'what is your name'."
    }
    
    response = responses.get(user_message, "I'm not sure how to respond to that. Try asking something else!")
    return jsonify({"response": response})

@app.route("/")
def index():
    # stock_plot_path, sentiment_plot_path, data_df = main()
    stock_plot_path, sentiment_plot_path, data_df = "/static", 0, 0
    df = pd.read_csv("static/data/dataframe.csv")
    table_html = df.to_html(classes='table table-striped', index=False)
    return render_template("index.html", #stock_plot_url=stock_plot_path, 
                        #    sentiment_plot_url=sentiment_plot_path, 
                        #    data=data_df.to_html(classes='data'))
                        # graph1=generate_graph1(),
                        plot_path="static/images/stock_plot.png", table=table_html, sentiment_path="static\images\market_sentiment.png")#,
                        # graph2=generate_graph2(), graph3=generate_graph3())


if __name__ == "__main__":
    app.run(debug=True)

 # // let graph1 = JSON.parse({{ graph1 | tojson | safe }});



# from flask import Flask, render_template, request, jsonify
# import pandas as pd
# import plotly.express as px
# import time

# app = Flask(__name__)

# # Generate sample graphs
# def generate_graph1():
#     df = pd.DataFrame({'Category': ['A', 'B', 'C', 'D'], 'Values': [10, 20, 30, 40]})
#     fig = px.bar(df, x="Category", y="Values", title="Bar Chart")
#     return fig.to_json()

# def generate_graph2():
#     df = pd.DataFrame({'X': range(10), 'Y': [x**2 for x in range(10)]})
#     fig = px.line(df, x="X", y="Y", title="Line Chart")
#     return fig.to_json()

# def generate_graph3():
#     df = pd.DataFrame({'X': range(10), 'Y': [x**1.5 for x in range(10)]})
#     fig = px.scatter(df, x="X", y="Y", title="Scatter Plot")
#     return fig.to_json()

# # Chatbot API route
# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     user_message = request.json.get("message", "").strip().lower()
    
#     # Simple rule-based chatbot logic
#     responses = {
#         "hello": "Hi there! How can I assist you?",
#         "how are you": "I'm just a bot, but I'm doing great! How about you?",
#         "what is your name": "I'm a simple chatbot built into this dashboard.",
#         "help": "I can answer basic questions. Try asking 'hello' or 'what is your name'."
#     }
    
#     response = responses.get(user_message, "I'm not sure how to respond to that. Try asking something else!")
#     return jsonify({"response": response})

# @app.route("/")
# def index():
#     return render_template("index.html", graph1=generate_graph1(), graph2=generate_graph2(), graph3=generate_graph3())

# if __name__ == "__main__":
#     app.run(debug=True)

