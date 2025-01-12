# Giftify

Giftify is a platform for discovering and managing gift certificates across various categories. Built with scalable architecture and design patterns, it ensures flexibility and ease of use for personalized gifting solutions.

## Applied Design Patterns and Their Justification

The project uses several design patterns aimed at improving code organization and making development easier:

- **Factory Method** – Allows for flexible and easy creation of certificate objects, making the system extensible.
- **Singleton** – Ensures that only one instance of the shopping cart exists in the application, which allows for centralized state management.
- **Strategy** – Enables the use of different filtering methods for certificates, making it easy to extend with new filters.
- **Observer** – Implements notifications to users about new offers.
- **Decorator** – Allows for dynamically adding new features to certificates (e.g., promotional or premium tags).
- **Facade** – Simplifies access to various system functions, such as searching and filtering certificates.

## Implementation of SOLID Principles in the Project

The SOLID principles are applied in the following ways:

- **S (Single Responsibility Principle)**: Each class and interface in the project has one well-defined responsibility. For example, `User` manages user data, and `CertificateFactory` is responsible for creating certificates.
- **O (Open/Closed Principle)**: The code is open for extensions (e.g., new types of certificates) but closed for modifications. New certificates can be added by extending classes without changing existing code.
- **L (Liskov Substitution Principle)**: Derived classes (e.g., `SpaCertificate`, `CulinaryCertificate`, `SportsCertificate`) can be used in place of the base class `BaseCertificate` without introducing errors.
- **I (Interface Segregation Principle)**: Small, dedicated interfaces such as `ICertificate` are used to implement only the required methods.
- **D (Dependency Inversion Principle)**: High-level classes (e.g., `ShoppingCart`, `CatalogFacade`) do not depend on certificate implementation details but on abstractions (e.g., `ICertificate`).

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
