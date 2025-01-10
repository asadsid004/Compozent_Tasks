import requests


def fetch_api_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("Post Details:")
            print(f"Title: {data.get('title')}")
            print(f"Body: {data.get('body')}")
            print("\nFetching Comments:")

            # Fetch comments associated with the post
            comments_url = url + "/comments"
            comments_response = requests.get(comments_url)
            if comments_response.status_code == 200:
                comments = comments_response.json()
                for idx, comment in enumerate(comments, 1):
                    print(f"Comment {idx}: {comment.get('body')}")
            else:
                print("Failed to fetch comments.")
        else:
            print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


api_url = "https://jsonplaceholder.typicode.com/posts/1"
fetch_api_data(api_url)
