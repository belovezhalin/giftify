# Giftify

Giftify is a platform for discovering and managing gift certificates across various categories. Built with scalable architecture and design patterns, it ensures flexibility and ease of use for personalized gifting solutions.

## Applied Design Patterns and Their Justification

The project utilizes a variety of design patterns that enhance code readability, modularity, and facilitate application development:

1. **Strategy** – Enables flexible management of different algorithms, e.g., in `cart.js` for handling logged-in and guest users. This pattern simplifies extending and modifying functionality without altering the client code.
2. **Template Method** – Used in Django's template system, allowing for the creation of base templates (e.g., `store/main.html`) that can be extended by other templates (e.g., `cart.html`). This ensures interface consistency and promotes efficient code reuse.
3. **Registry** – Applied in `admin.py`, it facilitates central registration of models in Django's admin panel, simplifying data structure management and their visibility within the system.
4. **Decorator** – Allows for dynamically adding new functionalities to existing code elements. In `decorators.py`, it enables extending function behaviors without altering their original implementation.
5. **Factory** – The `cookieCart` function in `utils.py` acts as a simple factory pattern, enabling the creation of shopping cart objects based on data stored in cookies. This separates object creation logic and makes it more maintainable.
6. **Observer** – Implemented in the notification system for new offers to users. This mechanism automatically informs registered users (observers) about updates, increasing interactivity and usability of the application.
7. **Model-View-Template (MVT)** – The architecture used in Django ensures a clear separation of responsibilities between the model layer, business logic, and presentation. This facilitates code organization and application development.

## Running Unit Tests

To run the unit tests for the project, follow these steps:

1. Make sure you have `pytest` installed:
   ```bash
   pip install pytest
   ```
2. Navigate to the root directory of the project, where the tests/ folder is located.

3. Run all tests with the following command:
   ```bash
   pytest
   ```
4. To see more detailed test results, use the -v flag:
   ```bash
   pytest -v
   The tests are located in the tests/ folder. Each test file begins with test_ .
   ```
