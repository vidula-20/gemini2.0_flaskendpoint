from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize the Flask app
app = Flask(__name__)

# Configure the Gemini API key
genai.configure(api_key="")

# Function to get response from Gemini 2.0 Flash
def get_gemini_response(user_input):
    prompt = f"""
    You are an advanced AI assistant designed to process and categorize user queries related to e-commerce optimization. Your task is to understand the user's query and match it to predefined passages, metadata listed below. Each query corresponds to a specific tool or category, and you should identify which one applies.
    
    For each query, provide the most accurate response by identifying the corresponding tool. If the query doesn't match any predefined one, return 'no match found'.
    
    Rules:
    - Your response should include only the following fields: `agentname`, `agentid`, `metadata`, `endpoint`.
    - Do not include any extra sentences, formatting, or JSON. Just return the four fields each on a new line.
    - If a tool name is matched, respond with the corresponding fields only.
    - If no match is found, respond with 'no match found' and only include the required fields.
    
    Here are the example queries and their corresponding tools:
    
    query : "How can I optimize images for my e-commerce store?"
response : "store_id"
passages : "The Image Optimiser tool uses AI-driven compression techniques and requires the store ID to function effectively."
metadata : "Tool: Image Optimiser, Feature: AI Image compression, Input: store_id"
positivequery : "TRUE"
agentname : "Image Optimiser"
agentid : "1"
endpoint : "/imageoptimiser"

query : "I wanna optimize images in my store."
response : "store_id"
passages :  "The tool uses AI-driven compression techniques to reduce loading times and bandwidth usage."
metadata : "Tool: Image Optimiser, Feature: Website Performance optimization"
positivequery : "TRUE"
agentname : "Image Optimiser"
agentid : "1"
endpoint : "/imageoptimiser"

query : "How do I reduce image sizes for my e-commerce store?"
response : "store_id"
passages : "Optimizes product images for web performance with reduced loading times and bandwidth usage. Requires a store ID for operation"
metadata : "Tool: Image Optimiser, Feature: Reducing image size improves performance, Input: store_id"
positivequery : "TRUE"
agentname : "Image Optimiser"
agentid : "1"
endpoint : "/imageoptimiser"

query : "How do I optimize videos in my website?"
response : "none"
passages : "The Image Optimiser supports multiple image formats but does not process videos."
metadata : "Tool: none, Feature: none, Input: none"
positivequery : "FALSE"
agentname : "none"
agentid : "0"
endpoint : "none"

query : "How can I enhance images for my e-commerce website?"
response : "store_id"
passages : "Using Image Optimiser tool might give you increased performance of your store"
metadata : "Tool: Image Optimiser, Feature: Enhances and improves images from a website, Input: store_id"
positivequery : "TRUE"
agentname : "Image Optimiser"
agentid : "1"
endpoint : "/imageoptimiser"

query : "How do I enhance videos in my website?"
response : "none"
passages : "The closest available tool is Image Optimiser, which supports image optimization, optimizing the image sizes in your store, not videos."
metadata : "Tool: none, Feature: none, Input: none"
positivequery : "FALSE"
agentname : "none"
agentid : "0"
endpoint : "none"

query : "How can I optimize my category pages for better SEO?"
response : "store_id-category_ids-fields-user_instructions-llm"
passages : "The Category Data Optimiser enhances category pages by optimizing titles, descriptions, and keywords to improve SEO performance. Requires store ID, category IDs, and specific fields to update."
metadata : "Tool: Category Data Optimiser, Feature: SEO optimization specialized for Category data, Input: store_id, category_ids, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Category Data Optimiser"
agentid : "15"
endpoint : "/categorydataoptimiser"

query : "What do I need to enhance meta descriptions for categories?"
response : "store_id-category_ids-fields-user_instructions-llm"
passages : "Meta descriptions for category pages are optimized by analyzing high-performing keywords and maintaining ideal character lengths. Input requirements include store ID and category IDs."
metadata : "Tool: Category Data Optimiser, Feature: Optimising not only meta description of the category data of store, also optimises name, description, page title, meta_keywords, Input: store_id, category_ids, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Category Data Optimiser"
agentid : "15"
endpoint : "/categorydataoptimiser"

query : "Can you help me improve search visibility for my categories?"
response : "store_id-category_ids-fields-user_instructions-llm"
passages : "Category Data Optimiser uses strategic keyword optimization and content analysis to improve search visibility for e-commerce categories."
metadata : "Tool: Category Data Optimiser, Feature: Search visibility improvement specific for category data of a store, Input: store_id, category_ids, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Category Data Optimiser"
agentid : "15"
endpoint : "/categorydataoptimiser"

query : "How do I improve the taxonomy structure of my categories?"
response : "none"
passages : "Category Data Optimiser tool focuses on optimizing only name, description, page_title, meta_keywords but does not support taxonomy restructuring or anything else."
metadata : "Tool: none, Feature: none, Input: none"
positivequery : "FALSE"
agentname : "none"
agentid : "0"
endpoint : "none"

query : "How can I improve rankings for my e-commerce categories?"
response : "store_id-category_ids-fields-user_instructions-llm"
passages : "Rankings of categories in your store are improved by optimizing search terms, meta descriptions, and titles using high-performing keywords."
metadata : "Tool: Category Data Optimiser, Feature: Search rankings improvement specific for category data, Input: store_id, category_ids, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Category Data Optimiser"
agentid : "15"
endpoint : "/categorydataoptimiser"

query : "I wanna optimize name and description of a category in my store."
response : "store_id-category_ids-fields-user_instructions-llm"
passages : "The Category Data Optimiser enhances category pages by optimizing titles, descriptions, and keywords to improve SEO performance. Requires store ID, category IDs, and specific fields to update."
metadata : "Tool: Category Data Optimiser, Feature: SEO optimization specialized for Category data, Input: store_id, category_ids, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Category Data Optimiser"
agentid : "15"
endpoint : "/categorydataoptimiser"

query : "I want to optimise category data"
response : "store_id-category_ids-fields-user_instructions-llm"
passages : "Category data optimiser uses strategic keyword optimization and content analysis to improve search visibility for e-commerce categories."
metadata : "Tool: Category Data Optimiser, Feature: SEO optimization specialized for Category data, Input: store_id, category_ids, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Category Data Optimiser"
agentid : "15"
endpoint : "/categorydataoptimiser"

query : "How can I optimize product names for better SEO?"
response : "store_id-skus-fields-user_instructions-llm"
passages : "The Product Data Optimiser uses AI to enhance product names, descriptions, video title and video description, image title and image description, search keywords, meta keywords for SEO impact. These fields are specific for product data."
metadata : "Tool: Product Data Optimiser, Feature: Product data optimization, Input: store_id, skus, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Product Data Optimiser"
agentid : "16"
endpoint : "/productdataoptimiser"

query : "What do I need to improve product descriptions?"
response : "store_id-skus-fields-user_instructions-llm"
passages : "Product descriptions are optimized by analyzing customer engagement trends and SEO keywords."
metadata : "Tool: Product Data Optimiser, Feature: Product Description optimization, Input: store_id, skus, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Product Data Optimiser"
agentid : "16"
endpoint : "/productdataoptimiser"

query : "How do I optimize my product data for e-commerce?"
response : "store_id-skus-fields-user_instructions-llm"
passages : "Product Data Optimiser improves product naming and descriptions for e-commerce platforms using AI-powered techniques. Not only does it optimize product names and descriptions, but it also optimizes video title and video description, image title and image description, search keywords, and meta keywords for SEO impact."
metadata : "Tool: Product Data Optimiser, Feature: E-commerce Product Data optimization, Input: store_id, skus, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Product Data Optimiser"
agentid : "16"
endpoint : "/productdataoptimiser"

query : "How do I improve search rankings for my products?"
response : "store_id-skus-fields-user_instructions-llm"
passages : "Rankings are improved by optimizing product names and descriptions using high-performing keywords."
metadata : "Tool: Product Data Optimiser, Feature: Search rankings improvement specifically for product data, Input: store_id, skus, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Product Data Optimiser"
agentid : "16"
endpoint : "/productdataoptimiser"

query : "How can I make my product descriptions more engaging to customers"
response : "store_id-skus-fields-user_instructions-llm"
passages : "Engaging product descriptions are implemented by AI-driven enhancements. Product Data Optimiser can enhance product data and metadata like video title, video description, image title, image description, search keywords, meta keywords for SEO impact."
metadata : "Tool: Product Data Optimiser, Feature: Customer engagement improvement by optimizing specifically product data, Input: store_id, skus, fields, user_instructions, llm"
positivequery : "TRUE"
agentname : "Product Data Optimiser"
agentid : "16"
endpoint : "/productdataoptimiser"

query : "How do I optimise product images?"
response : "store_id"
passages : "The Image Optimiser tool uses AI-driven compression techniques and requires the store ID to function effectively."
metadata : "Tool: Image Optimiser, Feature: AI Image compression, Input: store_id"
positivequery : "TRUE"
agentname : "Image Optimiser"
agentid : "1"
endpoint : "/imageoptimiser"

query : "Can I optimise product videos?"
response : "none"
passages : "The Product Data Optimiser uses AI to enhance text fields like product names, descriptions, video title and video description, image title and image description, search keywords, and meta keywords for SEO impact. It can't optimise videos."
metadata : "Tool: none, Feature: none, Input: none"
positivequery : "FALSE"
agentname : "none"
agentid : "0"
endpoint : "none"

query : "I wanna optimize product images in my store."
response : "store_id"
passages : "The tool uses AI-driven compression techniques to reduce loading times and bandwidth usage."
metadata : "Tool: Image Optimiser, Feature: Website Performance optimization, Input: store_id"
positivequery : "TRUE"
agentname : "Image Optimiser"
agentid : "1"
endpoint : "/imageoptimiser"

query : "How can I enhance images of all products for my e-commerce website?"
response : "store_id"
passages : "Using the Image Optimiser tool might give you increased performance for your store."
metadata : "Tool: Image Optimiser, Feature: Reducing image size improves performance, Input: store_id"
positivequery : "TRUE"
agentname : "Image Optimiser"
agentid : "1"
endpoint : "/imageoptimiser"

query : "How can I check if my webpage follows brand guidelines?"
response : "store_id-base_url-selected_url-brand_story-color_palette-typography-brand_voice"
passages : "The Brand Guide Optimiser scans user-provided URLs to evaluate visual elements, content, and styling against brand guidelines."
metadata : "Tool: Brand Guide Optimiser, Feature: Brand compliance analysis by analyzing brand text content, CSS content, Input: store_id, base_url, selected_url, brand_story, color_palette, typography, brand_voice"
positivequery : "TRUE"
agentname : "Brand Guide Optimiser"
agentid : "14"
endpoint : "/brandguideoptimiser"

query : "What do I need to analyze my webpage for brand consistency?"
response : "store_id-base_url-selected_url-brand_story-color_palette-typography-brand_voice"
passages : "To analyze brand consistency, the tool requires inputs such as store ID, base URL, selected URL, and brand elements like color palette and typography."
metadata : "Tool: Brand Guide Optimiser, Feature: Brand consistency checker, Input: store_id, base_url, selected_url, brand_story, color_palette, typography, brand_voice"
positivequery : "TRUE"
agentname : "Brand Guide Optimiser"
agentid : "14"
endpoint : "/brandguideoptimiser"

query : "Can you help me validate my website against brand standards?"
response : "store_id-base_url-selected_url-brand_story-color_palette-typography-brand_voice"
passages : "Brand Guide Optimiser validates webpages by comparing them with brand standards. It assesses visual elements like color palette and typography for alignment with the brand story."
metadata : "Tool: Brand Guide Optimiser, Feature: Brand standards validation, Input: store_id, base_url, selected_url, brand_story, color_palette, typography, brand_voice"
positivequery : "TRUE"
agentname : "Brand Guide Optimiser"
agentid : "14"
endpoint : "/brandguideoptimiser"

query : "How do I ensure my website aligns with my brand identity?"
response : "store_id-base_url-selected_url-brand_story-color_palette-typography-brand_voice"
passages : "Brand Guide Optimiser evaluates webpages for alignment with brand identity by analyzing content styling, color palette, typography, and brand voice."
metadata : "Tool: Brand Guide Optimiser, Feature: Brand identity verification, Input: store_id, base_url, selected_url, brand_story, color_palette, typography, brand_voice"
positivequery : "TRUE"
agentname : "Brand Guide Optimiser"
agentid : "14"
endpoint : "/brandguideoptimiser"

query : "How do I improve the visual consistency of my website?"
response : "store_id-base_url-selected_url-brand_story-color_palette-typography-brand_voice"
passages : "Visual consistency is improved by ensuring alignment with the color palette and typography defined in the brand guide. Brand Guide Optimiser analyzes these elements based on user-provided URLs."
metadata : "Tool: Brand Guide Optimiser, Feature: Visual consistency improvement, Input: store_id, base_url, selected_url, brand_story, color_palette, typography, brand_voice"
positivequery : "TRUE"
agentname : "Brand Guide Optimiser"
agentid : "14"
endpoint : "/brandguideoptimiser"

query : "How can I verify if my website uses the correct typography?"
response : "store_id-base_url-selected_url-brand_story-color_palette-typography-brand_voice"
passages : "Typography is verified by comparing webpage text styles against the font specifications in the provided brand guide. Inputs include store ID and URLs of pages to analyze."
metadata : "Tool: Brand Guide Optimiser, Feature: Typography verification, Input: store_id, base_url, selected_url, brand_story, color_palette, typography, brand_voice"
positivequery : "TRUE"
agentname : "Brand Guide Optimiser"
agentid : "14"
endpoint : "/brandguideoptimiser"

query : "How can I check the SEO performance of my website?"
response : "store_id-urls"
passages : "The SEO Performance Reporter uses PageSpeed API to analyze performance of a website in terms of SEO performance metrics, and search visibility."
metadata : "Tool: SEO Performance Reporter, Feature: SEO performance analysis by using PageSpeed API, reports only SEO performance, not overall performance, Input: store_id, urls"
positivequery : "TRUE"
agentname : "SEO Performance Reporter"
agentid : "22"
endpoint : "/seoperformancereporter"

query : "Can you help me generate an SEO report for my website?"
response : "store_id-urls"
passages : "The tool generates comprehensive SEO reports by analyzing webpage optimization and search engine visibility. Inputs required are store ID and URLs of the pages to analyze."
metadata : "Tool: SEO Performance Reporter, Feature: SEO reporting by using PageSpeed API, Input: store_id, urls"
positivequery : "TRUE"
agentname : "SEO Performance Reporter"
agentid : "22"
endpoint : "/seoperformancereporter"

query : "How do I evaluate my website's search engine visibility?"
response : "store_id-urls"
passages : "Search engine visibility is tracked by analyzing key metrics provided by the SEO Performance Tracker. It evaluates how well pages are optimized for search engines using inputs store ID and URLs."
metadata : "Tool: SEO Performance Reporter, Feature: SEO performance analysis by using PageSpeed API, Input: store_id, urls"
positivequery : "TRUE"
agentname : "SEO Performance Reporter"
agentid : "22"
endpoint : "/seoperformancereporter"

query : "Can this tool help me monitor my website's performance over time?"
response : "none"
passages : "The SEO Performance Reporter uses PageSpeed API to analyze performance of a website in terms of SEO performance metrics, and search visibility. SEO Performance Reporter cannot monitor the performance."
metadata : "Tool: none, Feature: none, Input: none"
positivequery : "FALSE"
agentname : "none"
agentid : "0"
endpoint : "none"

query : "I want to evaluate SEO performance of my website"
response : "store_id-urls"
passages : "The SEO Performance Reporter uses PageSpeed API to analyze performance of a website in terms of SEO performance metrics, and search visibility."
metadata : "Tool: SEO Performance Reporter, Feature: SEO performance analysis by using PageSpeed API, reports only SEO performance, not overall performance, Input: store_id, urls"
positivequery : "TRUE"
agentname : "SEO Performance Reporter"
agentid : "22"
endpoint : "/seoperformancereporter"

query : "I want to see how my site performs in terms of SEO"
response : "store_id-urls"
passages : "The tool generates comprehensive SEO reports by analyzing webpage optimization and search engine visibility. Inputs required are store ID and URLs of the pages to analyze."
metadata : "Tool: SEO Performance Reporter, Feature: SEO reporting by using PageSpeed API, Input: store_id, urls"
positivequery : "TRUE"
agentname : "SEO Performance Reporter"
agentid : "22"
endpoint : "/seoperformancereporter"

query : "How can I check if my product data is complete?"
response : "store_id"
passages : "The Schema Validator analyzes product data completeness by validating essential fields such as names, descriptions, specifications, pricing, and metadata. It identifies missing or empty fields and provides a detailed report. Inputs required include store ID."
metadata : "Tool: Schema Validator, Feature: Data completeness analysis, specific for product data, Input: store_id"
positivequery : "TRUE"
agentname : "Schema Validator"
agentid : "20"
endpoint : "/schemavalidator"

query : "What do I need to validate my product data schema?"
response : "store_id"
passages : "To validate product data schema, the tool requires inputs such as store ID. It checks for missing or incomplete fields in product entries like specifications and pricing. Only validation, not optimization."
metadata : "Tool: Schema Validator, Feature: Schema validation of product data, Input: store_id"
positivequery : "TRUE"
agentname : "Schema Validator"
agentid : "20"
endpoint : "/schemavalidator"

query : "Can you help me verify the attributes of my product data?"
response : "store_id"
passages : "Schema Validator performs attribute verification by analyzing product entries for missing or incomplete fields like descriptions and metadata. Inputs include store ID. Only validation, not optimization."
metadata : "Tool: Schema Validator, Feature: Attribute checking of product data, Input: store_id"
positivequery : "TRUE"
agentname : "Schema Validator"
agentid : "20"
endpoint : "/schemavalidator"

query : "How do I check if all fields in my product data are filled?"
response : "store_id"
passages : "Schema Validator checks for missing or empty fields in essential attributes like names and metadata of a product data in an ecommerce store. It provides a detailed report on field completeness using inputs like store ID. Only validation, not optimization."
metadata : "Tool: Schema Validator, Feature: Field validation of product data. Only validation, not optimization. Input: store_id"
positivequery : "TRUE"
agentname : "Schema Validator"
agentid : "20"
endpoint : "/schemavalidator"

query : "I have a lot of products in my store, can you help me filter products with incomplete data?"
response : "store_id"
passages : "The Schema Validator analyzes product data completeness by validating essential fields such as names, descriptions, specifications, pricing, and metadata. It identifies missing or empty fields and provides a detailed report. Inputs required include store ID."
metadata : "Tool: Schema Validator, Feature: Data completeness analysis, specific for product data, Input: store_id"
positivequery : "TRUE"
agentname : "Schema Validator"
agentid : "20"
endpoint : "/schemavalidator"

query : "Can you check completeness of data of all products in my store?"
response : "store_id"
passages : "To validate product data schema, the tool requires inputs such as store ID. It checks for missing or incomplete fields in product entries like specifications and pricing. Only validation, not optimization."
metadata : "Tool: Schema Validator, Feature: Schema validation of product data, Input: store_id"
positivequery : "TRUE"
agentname : "Schema Validator"
agentid : "20"
endpoint : "/schemavalidator"

query : "How can I generate high-performing keywords for my pages in my store?"
response : "store_id-urls-llm"
passages : "The Keyword Analyser uses AI to analyze multiple URLs and generate high-performing keyword suggestions. It extracts and recommends strategic keywords to improve search visibility. Inputs required include store ID and URLs."
metadata : "Tool: Keyword Analyser, Feature: Keyword generation of a particular page, Input: store_id, urls, llm"
positivequery : "TRUE"
agentname : "Keyword Analyser"
agentid : "22"
endpoint : "/keywordanalyser"

query : "I need to analyze keywords for my website"
response : "store_id-urls-llm"
passages : "To analyze keywords for a website, the Keyword Analyser requires inputs such as store ID and URLs. It leverages LLM technology to extract and recommend optimized keywords based on content analysis."
metadata : "Tool: Keyword Analyser, Feature: Keyword analysis, Input: store_id, urls, llm"
positivequery : "TRUE"
agentname : "Keyword Analyser"
agentid : "22"
endpoint : "/keywordanalyser"

query : "Can you help me improve search visibility with better keywords?"
response : "store_id-urls-llm"
passages : "Keyword Analyser improves search visibility by analyzing content from multiple URLs and suggesting AI-enhanced strategic keywords. Inputs required include store ID and URLs."
metadata : "Tool: Keyword Analyser, Feature: Search visibility improvement, Input: store_id, urls"
positivequery : "TRUE"
agentname : "Keyword Analyser"
agentid : "22"
endpoint : "/keywordanalyser"

query : "How do I optimize my content with AI-driven keyword suggestions?"
response : "store_id-urls-llm"
passages : "Content optimization is achieved by using AI-driven keyword recommendations generated by analyzing URL content. Inputs include store ID and URLs of the pages to analyze."
metadata : "Tool: Keyword Analyser, Feature: AI-enhanced keyword optimization, Input: store_id, urls"
positivequery : "TRUE"
agentname : "Keyword Analyser"
agentid : "22"
endpoint : "/keywordanalyser"

query : "How can I get a list of strategic keywords for my blog posts?"
response : "store_id-urls-llm"
passages : "Strategic keywords are generated by analyzing blog post content using LLM technology. The tool extracts high-performing terms based on URL content analysis. Inputs include store ID and URLs of the posts to analyze."
metadata : "Tool: Keyword Analyser, Feature: Blog keyword strategy"
positivequery : "TRUE"
agentname : "Keyword Analyser"
agentid : "22"
endpoint : "/keywordanalyser"

    Now, based on the user's input, identify the appropriate tool by matching it to one of the queries. If the query doesn't match any of the examples above, respond with 'no match found' and include only the required fields.

    User Query: "{user_input}"
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Define a route to handle user queries
@app.route('/ask', methods=['GET'])
def ask():
    user_query = request.args.get('query')
    if not user_query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    response_text = get_gemini_response(user_query)
    return response_text, 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
