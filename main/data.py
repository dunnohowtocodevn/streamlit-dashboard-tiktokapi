import requests
import csv
import os

      

#Get the number of tabs in the main shopping page
def get_tab_list(user_id):
    base_url = "https://tiktok-shop2.p.rapidapi.com/api/v1/shop/products/"
    url = base_url + str(user_id) + "/tab_list"

    querystring = {"region":"VN"}

    #API host info
    headers = {
	"X-RapidAPI-Key": "API KEY",
	"X-RapidAPI-Host": "tiktok-shop2.p.rapidapi.com"
    }

    #get the data in the format of json
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return len(data["data"]["tab_list"])

#Collect user data
def get_user_data(user_id, num):
    
    base_url = "https://tiktok-shop2.p.rapidapi.com/api/v1/shop/products/"
    url = base_url + str(user_id) + "/detail_page"
   

    
    querystring = {"tab_id":num,"region":"VN","count":"10","offset":"0"}

    headers = { "X-RapidAPI-Key": "API KEY",
	                "X-RapidAPI-Host": "tiktok-shop2.p.rapidapi.com"}


    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
            data = response.json()
            
            return data.get("data", {}).get("product_list", {})
    else:
            return None, None, None, None

#Write user data to a csv file
def write_to_csv(filename, data):
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Product_ID", "Product Name", "Sold Count", "Price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if csvfile.tell() == 0:
            writer.writeheader()
        for product in data:
            writer.writerow({"Product_ID": product.get("product_id", ""), "Product Name": product.get("product_name", ""), "Sold Count": product.get("product_sold_count", ""), "Price": product.get("format_available_price", "")})

#Obtain the product id from the first file    
def read_product_ids_from_csv(file_path):
    product_ids = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            # Assuming the product ID is in the first column of each row
            product_ids.append(row[0])
    return product_ids

#Get data about each product
def get_product_details(product_id):
    
    base_url = "https://tiktok-shop2.p.rapidapi.com/api/v1/shop/product/"
    url = base_url + str(product_id)

    querystring = {"region":"VN"}
    #API host info
    headers = {
	    "X-RapidAPI-Key": "API KEY",
	    "X-RapidAPI-Host": "tiktok-shop2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
            data = response.json()

            return data["data"]["products"]
    else:
          return None

#Write the data about the products to a csv file  
def write_to_file(data):
    
    csv_filename = "products.csv"
    file_exists = os.path.exists(csv_filename)

    # Wrte data to CSV
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Product_ID", "Stock","SKU","Price_After_Discount", "Rating", "Review_Count"])  # Write header
            file_exists = True
        for product in data:
            row_data = [
                product["product_id"],
                product["skus"][0]["stock"],  
                product["skus"][0]["sku_id"],
                product["skus"][0]["price"]["real_price"]["price_val"],
                
                product["product_detail_review"]["product_rating"],
                product["product_detail_review"]["review_count"]
                ]
            writer.writerow(row_data)


#main function
def collect_data(user_id):
    #Get the number of shop pages
    num = get_tab_list(user_id)

    if user_id:
        #Iterate over the pages to get basic data about the user
        for x in range(1,num+1,1):
            user_data = get_user_data(user_id, x)
            if user_data:
                write_to_csv("tiktok_user_data.csv", user_data)
                print("Data has been successfully written to 'tiktok_user_data.csv'")
            else:
                print(f"Failed to retrieve data for user with ID: {user_id}")
        #Get data about the products        
        product_ids = read_product_ids_from_csv("tiktok_user_data.csv")
        for product_id in product_ids:
            data = get_product_details(product_id)
            if product_id:
                write_to_file(data)
                print("Data retrieved")
            else:
                 print("no data")
    else:
        print("No user ID entered.")


