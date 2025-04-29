import os
import logging
from flask import Flask, render_template, request

# Create and configure Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Set up logging
logger = logging.getLogger(__name__)

# Main route - Serve the index page
@app.route("/")
def index():
    logger.debug("Rendering index page")
    return render_template("index.html", message="Hello World!")

# HTMX endpoint - Updated greeting
@app.route("/greet", methods=["POST"])
def greet():
    logger.debug("HTMX greeting request received")
    # Return only the HTML fragment that will be swapped
    return "<h1 class='display-4 text-center mb-4'>Hello HTMX World!</h1>"

# HTMX endpoint - Counter functionality
@app.route("/count", methods=["POST"])
def count():
    # Get the current count from the request
    current_count = int(request.form.get("current", 0))
    new_count = current_count + 1
    logger.debug(f"Incrementing count from {current_count} to {new_count}")
    
    # Return HTML fragment with updated count
    return f"""
    <div id="counter-display" class="my-3">
        <h2 class="text-center">Count: {new_count}</h2>
        <div class="d-flex justify-content-center">
            <button class="btn btn-secondary" 
                    hx-post="/count" 
                    hx-trigger="click" 
                    hx-target="#counter-display"
                    hx-include="[name='current']">
                Increment
            </button>
        </div>
        <input type="hidden" name="current" value="{new_count}">
    </div>
    """
