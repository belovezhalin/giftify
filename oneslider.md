---
marp: true
theme: default
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

<style>
section {
  font-size: 12px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.column {
  flex: 33%;
  padding: 5px;
  box-sizing: border-box;
  justify-content: center;
}
.column:first-child {
    margin-right: 5%;
}
h1, h2, h3 {
  margin-top: 5px;
  margin-bottom: 5px;
}
ul {
  padding-left: 15px;
}
</style>

# 🎁 Giftify - Project Summary

Giftify is a platform for discovering and managing gift certificates across various categories. Built with a scalable architecture and design patterns, it ensures flexibility and ease of use.

<div class="column">

## 🛠️ Key Features
- Intuitive gift management
- Scalable and flexible design
- Cart persistence (Cookies)

## 🏗️ Applied Design Patterns
- **Factory Method**
- **Strategy**
- **Observer**
- **Decorator**
- **Template Method**
- **Registry**

</div><div class="column">

## ✅ Test Results
- **Unit Tests**: 16 tests covering various components
- **Integration Tests**: Ensure correct interaction between classes
- **Coverage**: 78% (Measured using Coverage.py, accessible via `start htmlcov/index.html`)
- **Interface testing:** Found minor UX issues to be improved
- **Payment Testing**: Successfully tested with PayPal sandbox account  

## 📞 Repository Link
[Giftify Project Repository](https://github.com/belovezhalin/giftify)

</div><div class="column">

## 📊 Key Components
- **User** - Represents a user
- **Customer** - Linked to User, represents a customer
- **Category** - Represents a product category
- **Product** - Contains details like name, price, category, place, image, discount, and special mark
- **Order** - Linked to Customer, contains order date, completion status, and transaction ID
- **OrderItem** - Linked to Product and Order, contains quantity and date added
- **ProductAdmin** - Admin class for products, includes display, filter, and search fields
- **ProductDecorator** - Allows adding extra features to products
- **SaleDecorator** - Adds discount and sale price
- **SpecialOccasionDecorator** - Adds special occasion mark
- **Observer** - Interface for observers, includes `update` method
- **Subject** - Manages observer list and notifies them of changes
- **UserObserver** - Implements `update` method for users
- **Views** - Handles various views like registration, product list, product detail, cart, checkout, update item, and process order

</div>

