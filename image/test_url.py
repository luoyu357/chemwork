import requests


def is_valid_file_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    }

    try:
        # Using HEAD to check the existence of the file without downloading its content
        response = requests.head(url, headers=headers, allow_redirects=True)

        # Check if we got a successful response or a 403 Forbidden
        if response.status_code == 200 or response.status_code == 403:
            return True
    except requests.RequestException:
        pass

    return False


# Check the provided URL
url = "https://pubs.acs.org/na101/home/literatum/publisher/achs/journals/content/joceah/2019/joceah.2019.84.issue-5/acs.joc.8b02978/20190222/images/medium/jo-2018-02978q_0004.gif"
if is_valid_file_url(url):
    print(f"{url} points to a valid file/resource.")
else:
    print(f"{url} does NOT point to a valid file/resource.")


import requests

def download_file(url, save_path):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        with requests.get(url, headers=headers, stream=True) as response:
            response.raise_for_status()  # Raise an error for bad responses
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):  # 8KB chunks
                    file.write(chunk)
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        return False

    return True

# Provide the URL and the path where you want to save the file
url = "https://pubs.acs.org/na101/home/literatum/publisher/achs/journals/content/joceah/2019/joceah.2019.84.issue-5/acs.joc.8b02978/20190222/images/medium/jo-2018-02978q_0004.gif"
save_path = "path_where_you_want_to_save_the_file.gif"

if download_file(url, save_path):
    print(f"File downloaded successfully and saved to {save_path}.")
else:
    print("Failed to download the file.")
