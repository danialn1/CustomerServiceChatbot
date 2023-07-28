import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request, jsonify

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

knowledge_base = {
    "What are your business hours?": "Our business hours are Monday to Friday, 9:00 AM to 6:00 PM (GMT).",
    "How can I contact customer support?": "You can reach our customer support team through phone at +923125495373 or via email at xyz@info.com.",
    "What payment methods do you accept?": "We accept credit/debit cards (Visa, MasterCard, American Express), PayPal, and bank transfers.",
    "Is there a return policy?": "Yes, we have a 30-day return policy. Please refer to our Returns & Refunds page for more details.",
    "Can I track my order?": "Yes, you can track your order by logging into your account or using the tracking number provided in the shipping confirmation email.",
    "Do you offer international shipping?": "Yes, we offer international shipping to most countries. Shipping fees may vary based on the destination.",
    "How do I reset my password?": "To reset your password, go to the login page and click on the 'Forgot Password' link. Follow the instructions to reset it.",
    "Are your products covered by a warranty?": "Yes, most of our products come with a standard one-year warranty. Check the product description for specific warranty details.",
    "What is your shipping time frame?": "Our standard shipping time frame is 3-5 business days. International orders may take longer to arrive.",
    "Can I cancel my order?": "Yes, you can cancel your order within 24 hours of placing it. Contact our customer support team for assistance.",
    "What is your exchange policy?": "We offer exchanges for products of the same value within 14 days of purchase. Please review our Exchange Policy for more details.",
    "Do you have a loyalty program?": "Yes, we have a loyalty program where you can earn points for purchases and redeem them for discounts on future orders.",
    "How can I check the status of my order?": "You can check the status of your order by logging into your account and navigating to the 'Order History' section.",
    "What is your price matching policy?": "We offer price matching for identical items found at a lower price on eligible competitor websites. Please review our Price Match Policy for more details.",
    "Do you offer free shipping?": "Yes, we offer free standard shipping on orders over $50 within the contiguous United States.",
    "Can I return an item in-store that I purchased online?": "Yes, you can return an item purchased online in-store within 30 days of purchase. Please bring the packing slip or order confirmation email as proof of purchase.",
    "What is your response time for email inquiries?": "We aim to respond to email inquiries within 1-2 business days.",
    "Can I add items to an existing order?": "Unfortunately, we cannot add items to an existing order. You will need to place a new order for additional items.",
    "How can I leave a product review?": "You can leave a product review on the product page by clicking on the 'Write a Review' button and following the instructions.",
    "What is your in-store pickup process?": "When selecting in-store pickup during checkout, you will receive an email notification when your order is ready for pickup at the designated store location.",
    "Do you offer expedited shipping options?": "Yes, we offer expedited shipping options for faster delivery. You can choose your preferred shipping method during checkout.",
    "What is your policy on backordered items?": "If an item is on backorder, it means it is currently out of stock but will be available for purchase again soon. You can still place an order, and we will ship it once it's back in stock.",
    "How do I apply a discount code to my order?": "You can apply a discount code during the checkout process. Enter the code in the 'Discount Code' field and click 'Apply' to see the adjusted total.",
    "What is your process for handling damaged items during shipping?": "If you receive a damaged item, please contact our customer support team immediately, and we will assist you in resolving the issue.",
    "Do you offer gift cards?": "Yes, we offer gift cards that can be purchased online or in-store. Gift cards are a great way to gift someone the flexibility to choose their favorite products.",
    "Can I change my shipping address after placing an order?": "If your order hasn't been shipped yet, you may be able to change the shipping address. Please contact customer support as soon as possible.",
    "What is your process for handling product recalls?": "In the event of a product recall, we will communicate the details through our website and other communication channels, providing instructions on returning the affected products.",
    "Can I request a custom order for a product?": "We may consider custom orders for certain products. Please contact our sales team to discuss your requirements.",
    "What is your process for handling incorrect shipments?": "If you receive an incorrect item, please contact our customer support team, and we will arrange for the correct product to be sent to you.",
    "What is your email newsletter frequency?": "Our email newsletter is typically sent out once a week, and it includes information on promotions, new products, and updates.",
    "Do you offer installation services for your products?": "We provide installation services for select products. Please review the product details or contact our sales team for more information.",
    "What do I do if I receive a defective product?": "If you receive a defective product, please contact our customer support team within the warranty period for assistance.",
    "Can I return an item without the original packaging?": "We recommend returning products in their original packaging, but if it's not possible, please contact customer support for further instructions.",
    "What is your process for handling damaged-in-transit claims?": "If your order arrives damaged, please contact our customer support team to initiate a claim and provide photos of the damaged items and packaging.",
    "Can I change the shipping method for my order?": "If your order hasn't been shipped yet, you may be able to change the shipping method. Contact customer support for assistance.",
    "What is your process for resolving billing disputes?": "If you have a billing dispute, please contact our customer support team with detailed information, and we will investigate the matter.",
    "Do you offer a live chat option for technical support?": "Yes, we offer live chat support for technical issues related to our products and services.",
    "What are the benefits of creating an account on your website?": "Creating an account allows you to track orders, save billing information, and access exclusive promotions and offers.",
    "What do I do if I receive a defective digital product?": "If you encounter issues with a digital product, contact our customer support team, and we will assist you in resolving the problem.",
    "Can I return a personalized/customized item?": "Unfortunately, personalized or customized items are typically not eligible for return. Please review our Return Policy for more details.",
    "What is your process for handling shipping delays?": "In case of shipping delays, we will work closely with the shipping carrier to resolve the issue and keep you informed about the status of your order.",
    "Do you offer installation guides for your products?": "Yes, we provide installation guides for many of our products. You can find them on the product page or in the product's packaging.",
    "Can I return an item purchased during a promotional sale?": "Yes, items purchased during a promotional sale are eligible for return under our standard Return Policy.",
    "What is your process for handling incorrect pricing on your website?": "If you notice incorrect pricing on our website, please contact our customer support team, and we will investigate and correct the issue.",
    "Can I change the shipping address for an order that has already shipped?": "Unfortunately, the shipping address cannot be changed once an order has shipped. Please ensure the correct address is provided at the time of purchase.",
    "What is your process for handling product defects?": "If you encounter a product defect, please contact our customer support team, and we will work to resolve the issue as quickly as possible.",
    "Do you offer technical support for your software products?": "Yes, we provide technical support for our software products. Contact our support team with any technical issues you encounter.",
    "How can I provide feedback on your customer support service?": "We value your feedback on our customer support service. You can leave feedback by responding to the support follow-up email or contacting our team directly.",
    "What is your process for handling damaged digital downloads?": "If you encounter a defect in a digital download, contact our customer support team, and we will provide you with a new download link.",
    "Can I return a personalized/customized item?": "Unfortunately, personalized or customized items are typically not eligible for return. Please review our Return Policy for more details.",
    "What is your process for handling shipping delays?": "In case of shipping delays, we will work closely with the shipping carrier to resolve the issue and keep you informed about the status of your order.",
    "Do you offer installation guides for your products?": "Yes, we provide installation guides for many of our products. You can find them on the product page or in the product's packaging.",
    "Can I return an item purchased during a promotional sale?": "Yes, items purchased during a promotional sale are eligible for return under our standard Return Policy.",
    "What is your process for handling incorrect pricing on your website?": "If you notice incorrect pricing on our website, please contact our customer support team, and we will investigate and correct the issue.",
    "Can I change the shipping address for an order that has already shipped?": "Unfortunately, the shipping address cannot be changed once an order has shipped. Please ensure the correct address is provided at the time of purchase.",
    "What is your process for handling product defects?": "If you encounter a product defect, please contact our customer support team, and we will work to resolve the issue as quickly as possible.",
    "Do you offer technical support for your software products?": "Yes, we provide technical support for our software products. Contact our support team with any technical issues you encounter.",
    "How can I provide feedback on your customer support service?": "We value your feedback on our customer support service. You can leave feedback by responding to the support follow-up email or contacting our team directly.",
    "What is your process for handling damaged digital downloads?": "If you encounter a defect in a digital download, contact our customer support team, and we will provide you with a new download link.",
    "Can I return a personalized/customized item?": "Unfortunately, personalized or customized items are typically not eligible for return. Please review our Return Policy for more details.",
    "What is your process for handling shipping delays?": "In case of shipping delays, we will work closely with the shipping carrier to resolve the issue and keep you informed about the status of your order.",
    "Do you offer installation guides for your products?": "Yes, we provide installation guides for many of our products. You can find them on the product page or in the product's packaging.",
    "Can I return an item purchased during a promotional sale?": "Yes, items purchased during a promotional sale are eligible for return under our standard Return Policy.",
    "What is your process for handling incorrect pricing on your website?": "If you notice incorrect pricing on our website, please contact our customer support team, and we will investigate and correct the issue.",
    "Can I change the shipping address for an order that has already shipped?": "Unfortunately, the shipping address cannot be changed once an order has shipped. Please ensure the correct address is provided at the time of purchase.",
    "What is your process for handling product defects?": "If you encounter a product defect, please contact our customer support team, and we will work to resolve the issue as quickly as possible.",
    "Do you offer technical support for your software products?": "Yes, we provide technical support for our software products. Contact our support team with any technical issues you encounter.",
    "How can I provide feedback on your customer support service?": "We value your feedback on our customer support service. You can leave feedback by responding to the support follow-up email or contacting our team directly.",
    "What is your process for handling damaged digital downloads?": "If you encounter a defect in a digital download, contact our customer support team, and we will provide you with a new download link.",
    "Can I return a personalized/customized item?": "Unfortunately, personalized or customized items are typically not eligible for return. Please review our Return Policy for more details.",
    "What is your process for handling shipping delays?": "In case of shipping delays, we will work closely with the shipping carrier to resolve the issue and keep you informed about the status of your order.",
    "Do you offer installation guides for your products?": "Yes, we provide installation guides for many of our products. You can find them on the product page or in the product's packaging.",
    "Can I return an item purchased during a promotional sale?": "Yes, items purchased during a promotional sale are eligible for return under our standard Return Policy.",
    "What is your process for handling incorrect pricing on your website?": "If you notice incorrect pricing on our website, please contact our customer support team, and we will investigate and correct the issue.",
    "Can I change the shipping address for an order that has already shipped?": "Unfortunately, the shipping address cannot be changed once an order has shipped. Please ensure the correct address is provided at the time of purchase.",
    "What is your process for handling product defects?": "If you encounter a product defect, please contact our customer support team, and we will work to resolve the issue as quickly as possible.",
    "Do you offer technical support for your software products?": "Yes, we provide technical support for our software products. Contact our support team with any technical issues you encounter.",
    "How can I provide feedback on your customer support service?": "We value your feedback on our customer support service. You can leave feedback by responding to the support follow-up email or contacting our team directly.",
    "What is your process for handling damaged digital downloads?": "If you encounter a defect in a digital download, contact our customer support team, and we will provide you with a new download link.",
    "Can I return a personalized/customized item?": "Unfortunately, personalized or customized items are typically not eligible for return. Please review our Return Policy for more details.",
    "What is your process for handling shipping delays?": "In case of shipping delays, we will work closely with the shipping carrier to resolve the issue and keep you informed about the status of your order.",
    "Do you offer installation guides for your products?": "Yes, we provide installation guides for many of our products. You can find them on the product page or in the product's packaging.",
    "Can I return an item purchased during a promotional sale?": "Yes, items purchased during a promotional sale are eligible for return under our standard Return Policy.",
    "What is your process for handling incorrect pricing on your website?": "If you notice incorrect pricing on our website, please contact our customer support team, and we will investigate and correct the issue.",
    "Can I change the shipping address for an order that has already shipped?": "Unfortunately, the shipping address cannot be changed once an order has shipped. Please ensure the correct address is provided at the time of purchase.",
    "What is your process for handling product defects?": "If you encounter a product defect, please contact our customer support team, and we will work to resolve the issue as quickly as possible.",
    "Do you offer technical support for your software products?": "Yes, we provide technical support for our software products. Contact our support team with any technical issues you encounter.",
    "How can I provide feedback on your customer support service?": "We value your feedback on our customer support service. You can leave feedback by responding to the support follow-up email or contacting our team directly.",
    "What is your process for handling damaged digital downloads?": "If you encounter a defect in a digital download, contact our customer support team, and we will provide you with a new download link.",
    "Can I return a personalized/customized item?": "Unfortunately, personalized or customized items are typically not eligible for return. Please review our Return Policy for more details.",
    "What is your process for handling shipping delays?": "In case of shipping delays, we will work closely with the shipping carrier to resolve the issue and keep you informed about the status of your order.",
    "Do you offer installation guides for your products?": "Yes, we provide installation guides for many of our products. You can find them on the product page or in the product's packaging.",
    "Can I return an item purchased during a promotional sale?": "Yes, items purchased during a promotional sale are eligible for return under our standard Return Policy.",
    "What is your process for handling incorrect pricing on your website?": "If you notice incorrect pricing on our website, please contact our customer support team, and we will investigate and correct the issue.",
    "Can I change the shipping address for an order that has already shipped?": "Unfortunately, the shipping address cannot be changed once an order has shipped. Please ensure the correct address is provided at the time of purchase.",
    "What is your process for handling product defects?": "If you encounter a product defect, please contact our customer support team, and we will work to resolve the issue as quickly as possible.",
    "Do you offer technical support for your software products?": "Yes, we provide technical support for our software products. Contact our support team with any technical issues you encounter.",
    "How can I provide feedback on your customer support service?": "We value your feedback on our customer support service. You can leave feedback by responding to the support follow-up email or contacting our team directly.",
    "What is your process for handling damaged digital downloads?": "If you encounter a defect in a digital download, contact our customer support team, and we will provide you with a new download link.",
    "Can I return a personalized/customized item?": "Unfortunately, personalized or customized items are typically not eligible for return. Please review our Return Policy for more details.",
    "What is your process for handling shipping delays?": "In case of shipping delays, we will work closely with the shipping carrier to resolve the issue and keep you informed about the status of your order.",
    "Do you offer installation guides for your products?": "Yes, we provide installation guides for many of our products. You can find them on the product page or in the product's packaging.",
    "Can I return an item purchased during a promotional sale?": "Yes, items purchased during a promotional sale are eligible for return under our standard Return Policy.",
    "What is your process for handling incorrect pricing on your website?": "If you notice incorrect pricing on our website, please contact our customer support team, and we will investigate and correct the issue.",
    "Can I change the shipping address for an order that has already shipped?": "Unfortunately, the shipping address cannot be changed once an order has shipped. Please ensure the correct address is provided at the time of purchase.",
    "What is your process for handling product defects?": "If you encounter a product defect, please contact our customer support team, and we will work to resolve the issue as quickly as possible.",
    "Do you offer technical support for your software products?": "Yes, we provide technical support for our software products. Contact our support team with any technical issues you encounter.",
    "How can I provide feedback on your customer support service?": "We value your feedback on our customer support service. You can leave feedback by responding to the support follow-up email or contacting our team directly.",
    "What is your process for handling damaged digital downloads?": "If you encounter a defect in a digital download, contact our customer support team, and we will provide you with a new download link.",
    "Can I return a personalized/customized item?": "Unfortunately, personalized or customized items are typically not eligible for return. Please review our Return Policy for more details.",
    "What is your process for handling shipping delays?": "In case of shipping delays, we will work closely with the shipping carrier to resolve the issue and keep you informed about the status of your order.",
    "Do you offer installation guides for your products?": "Yes, we provide installation guides for many of our products. You can find them on the product page or in the product's packaging.",
    "Can I return an item purchased during a promotional sale?": "Yes, items purchased during a promotional sale are eligible for return under our standard Return Policy.",
    "What is your process for handling incorrect pricing on your website?": "If you notice incorrect pricing on our website, please contact our customer support team, and we will investigate and correct the issue.",
    "Can I change the shipping address for an order that has already shipped?": "Unfortunately, the shipping address cannot be changed once an order has shipped. Please ensure the correct address is provided at the time of purchase.",
    "What is your process for handling product defects?": "If you encounter a product defect, please contact our customer support team, and we will work to resolve the issue as quickly as possible.",
    "Do you offer technical support for your software products?": "Yes, we provide technical support for our software products. Contact our support team with any technical issues you encounter.",
    "How can I provide feedback on your customer support service?": "We value your feedback on our customer support service. You can leave feedback by responding to the support follow-up email or contacting our team directly."
}





def generate_response(prompt, chat_history_ids=None):
    if chat_history_ids is None:
        # If chat_history_ids is not provided, encode the prompt and create a new tensor
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
    else:
        # If chat_history_ids is provided, it means there is an existing conversation history
        # We need to concatenate the new input with the chat history
        new_user_input_ids = tokenizer.encode(prompt, return_tensors="pt")
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        input_ids = bot_input_ids

    attention_mask = torch.ones_like(input_ids)  # Explicitly set attention mask to 1 for all tokens

    # Generate the response while limiting the total chat history to 1000 tokens
    output = model.generate(input_ids, attention_mask=attention_mask, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Decode the output to get the response
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return response


def chatbot_interface(question):
    if question in knowledge_base:
        response_text = knowledge_base[question]
    else:
        prompt = f"{question}"
        response_text = generate_response(prompt)

        # Check if the response from generate_response is empty or similar to the input question
        if not response_text.strip() or response_text.strip().lower() == question.strip().lower():
            response_text = "I'm sorry, I don't have an answer to that question at the moment. Please try asking something else."

    return response_text


@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    question = data["question"]

    answer = chatbot_interface(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run()
