import requests

# # Replace 'xxxxxxxx-xxxxxxxx-xxxxxxxx-xxxxxxxx' with your actual Wiley-TDM-Client-Token
# # client_token = 'xxxxxxxx-xxxxxxxx-xxxxxxxx-xxxxxxxx'
# client_token = "1dc65049-57fa-41d5-bb12-39cbdf95bbb5"
# # Replace the DOI and download URL with the appropriate values
# doi = '10.1111/j.1365-2486.2005.00961.x'
# download_url = f'https://api.wiley.com/onlinelibrary/tdm/v1/articles/{doi}'

# # Prepare headers
# headers = {
#     'Wiley-TDM-Client-Token': client_token,
# }

# # Make a GET request to download the article
# response = requests.get(download_url, headers=headers, allow_redirects=True)

# if response.status_code == 200:
#     # If the request is successful, save the PDF to a file
#     with open(f'{doi.replace("/", "_")}.pdf', 'wb') as file:
#         file.write(response.content)
#     print(f"Article downloaded successfully as '{doi}.pdf'")
# else:
#     print(f"Failed to download the article. Status code: {response.status_code}")
import parser_pdf

print(parser_pdf.get_from_doi2bibapi("10.1111/j.1529-8817.2004.00726.x"))