import os
import time
from notion_client import Client

# Notion setup
notion_token = 'your_notion_integration_token'
notion_client = Client(auth=notion_token)
database_id = 'your_notion_database_id'

# Local directory to monitor
watch_directory = 'path/to/your/local/folder'

def get_files_in_directory(directory):
    """
    Get a list of file paths in the given directory
    """
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def file_already_uploaded(file_name, notion_client, database_id):
    """
    Check if the file has already been uploaded to Notion by searching for its name in the database
    """
    query = notion_client.databases.query(
        **{
            'database_id': database_id,
            'filter': {
                'property': 'Name',
                'text': {
                    'equals': file_name
                }
            }
        }
    )
    return len(query['results']) > 0

def upload_file_to_notion(file_path, notion_client, database_id):
    """
    Upload a file to Notion by creating a new page with the file's name and content
    Note: This function currently only logs the action; you'll need to implement actual file uploading or linking.
    """
    file_name = os.path.basename(file_path)
    if not file_already_uploaded(file_name, notion_client, database_id):
        # For demonstration, this will only create a new page with the file's name.
        # Extend this to upload the file's content or a link to the file.
        notion_client.pages.create(
            **{
                'parent': {'database_id': database_id},
                'properties': {
                    'Name': {
                        'title': [
                            {
                                'text': {
                                    'content': file_name
                                }
                            }
                        ]
                    }
                }
            }
        )
        print(f'Uploaded {file_name} to Notion')

def monitor_directory_and_sync(directory, notion_client, database_id):
    """
    Monitor the specified directory and sync new files to Notion
    """
    known_files = set()
    while True:
        current_files = set(get_files_in_directory(directory))
        new_files = current_files - known_files
        if new_files:
            for file_path in new_files:
                upload_file_to_notion(file_path, notion_client, database_id)
        known_files = current_files
        time.sleep(10)  # Check every 10 seconds

if __name__ == '__main__':
    monitor_directory_and_sync(watch_directory, notion_client, database_id)
